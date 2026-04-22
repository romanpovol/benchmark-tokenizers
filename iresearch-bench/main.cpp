#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <string>
#include <string_view>
#include <vector>

#include <absl/strings/str_cat.h>

#include "iresearch/analysis/analyzers.hpp"
#include "iresearch/analysis/path_hierarchy_tokenizer.hpp"
#include "iresearch/analysis/pattern_tokenizer.hpp"

std::vector<std::string> load_lines(const std::string& path) {
  std::ifstream f(path);
  if (!f) {
    std::cerr << "Cannot open: " << path << "\n";
    std::exit(1);
  }
  std::vector<std::string> lines;
  std::string line;
  while (std::getline(f, line)) {
    if (!line.empty() && line.back() == '\r') {
      line.pop_back();
    }
    if (!line.empty()) {
      lines.push_back(std::move(line));
    }
  }
  return lines;
}

__attribute__((noinline))
uint64_t hash_term(uint64_t h, std::string_view term) {
  for (unsigned char b : term) {
    h = h * 31u + static_cast<uint64_t>(b);
  }
  return h;
}

__attribute__((noinline))
std::pair<int64_t, uint64_t> process_lines(
  irs::analysis::Analyzer& tokenizer, const std::vector<std::string>& lines) {
  auto* term_attr = irs::get<irs::TermAttr>(tokenizer);

  uint64_t h = 0;
  uint64_t count = 0;

  for (auto& line : lines) {
    tokenizer.reset(line);
    while (tokenizer.next()) {
      std::string_view text = irs::ViewCast<char>(term_attr->value);
      h = hash_term(h, text);
      ++count;
    }
  }
  return {static_cast<int64_t>(h), count};
}

struct Percentiles {
  uint64_t p50, p95, p99, p100;
};

Percentiles calc_percentiles(std::vector<uint64_t>& v) {
  std::sort(v.begin(), v.end());
  size_t n = v.size();
  return {
    v[static_cast<size_t>(n * 0.50)],
    v[static_cast<size_t>(n * 0.95)],
    v[std::min(static_cast<size_t>(n * 0.99), n - 1)],
    v[n - 1],
  };
}

std::string BuildPipelineConfig(bool pipe_no_stopwords, bool pipe_no_stem,
                                bool pipe_no_edge) {
  std::vector<std::string_view> steps;
  steps.emplace_back(R"({
    "type": "text",
    "properties": {
      "locale": "en_US.UTF-8",
      "case": "none",
      "accent": true,
      "stemming": false,
      "stopwords": []
    }
  })");
  steps.emplace_back(R"({
    "type": "norm",
    "properties": {
      "locale": "en_US.UTF-8",
      "case": "lower",
      "accent": false
    }
  })");
  if (!pipe_no_stopwords) {
    steps.emplace_back(R"({
      "type": "stopwords",
      "properties": {
        "stopwords": [
          "the","and","or","but","in","on","at","to","of","for",
          "a","an","is","it","as","be","by","if","we"
        ],
        "hex": false
      }
    })");
  }
  if (!pipe_no_stem) {
    steps.emplace_back(R"({
      "type": "stem",
      "properties": {
        "locale": "en_US.UTF-8"
      }
    })");
  }
  if (!pipe_no_edge) {
    steps.emplace_back(R"({
      "type": "edge_ngram",
      "properties": {
        "min": 1,
        "max": 3,
        "preserveOriginal": false
      }
    })");
  }

  std::string config = R"({"pipeline":[)";
  for (size_t i = 0; i < steps.size(); ++i) {
    if (i != 0) {
      config += ",";
    }
    config += steps[i];
  }
  config += "]}";
  return config;
}

void usage() {
  std::cerr <<
    "Usage: iresearch-bench --data FILE [--tokenizer pattern|path|path_hierarchy|text|pipeline]\n"
    "                       [--runs N] [--warmup N] [--dump]\n"
    "\n"
    "PatternTokenizer options (pattern / path):\n"
    "  --regex-pattern REGEX\n"
    "\n"
    "PathHierarchyTokenizer options (path_hierarchy):\n"
    "  --delimiter STRING    path separator (default: /)\n"
    "  --replacement STRING  replacement for delimiter in token (default: /)\n"
    "  --reverse             reverse mode for domain-like hierarchies\n"
    "  --skip N              skip first N tokens (default: 0)\n"
    "\n"
    "Pipeline A/B options (only with --tokenizer pipeline):\n"
    "  --pipe-no-stopwords   remove stopwords stage\n"
    "  --pipe-no-stem        remove stem stage\n"
    "  --pipe-no-edge        remove edge_ngram stage\n"
    "\n"
    "Text options (only with --tokenizer text):\n"
    "  --text-no-stem        disable stemming in text tokenizer\n"
    "\n"
    "Tokenizer modes:\n"
    "  pattern        group=0,  default regex \\w+  (match mode -- emits matches)\n"
    "  path           group=-1, default regex [/]+  (split mode -- emits segments)\n"
    "  path_hierarchy PathHierarchyTokenizer, emits cumulative path prefixes\n"
    "  text           SereneDB full text_tokenizer (lower+stop+stem+edge_ngram)\n"
    "  pipeline       PipelineTokenizer: text -> norm(lower) -> stopwords -> stem -> edge_ngram\n";
}

int main(int argc, char** argv) {
  std::string data_path;
  std::string tokenizer_kind = "pattern";
  bool dump = false;
  int runs = 20;
  int warmup = 2;

  std::string regex_pattern;

  std::string ph_delimiter = "/";
  std::string ph_replacement = "/";
  bool ph_reverse = false;
  int ph_skip = 0;
  bool pipe_no_stopwords = false;
  bool pipe_no_stem = false;
  bool pipe_no_edge = false;
  bool text_no_stem = false;

  for (int i = 1; i < argc; ++i) {
    std::string_view arg = argv[i];
    auto next_arg = [&]() -> std::string_view {
      if (i + 1 >= argc) {
        std::cerr << arg << " requires a value\n";
        std::exit(1);
      }
      return argv[++i];
    };
    if (arg == "--data") {
      data_path = std::string(next_arg());
    } else if (arg == "--tokenizer") {
      tokenizer_kind = std::string(next_arg());
    } else if (arg == "--runs") {
      runs = std::stoi(std::string(next_arg()));
    } else if (arg == "--warmup") {
      warmup = std::stoi(std::string(next_arg()));
    } else if (arg == "--dump") {
      dump = true;
    } else if (arg == "--regex-pattern") {
      regex_pattern = std::string(next_arg());
    } else if (arg == "--delimiter") {
      ph_delimiter = std::string(next_arg());
    } else if (arg == "--replacement") {
      ph_replacement = std::string(next_arg());
    } else if (arg == "--reverse") {
      ph_reverse = true;
    } else if (arg == "--skip") {
      ph_skip = std::stoi(std::string(next_arg()));
    } else if (arg == "--pipe-no-stopwords") {
      pipe_no_stopwords = true;
    } else if (arg == "--pipe-no-stem") {
      pipe_no_stem = true;
    } else if (arg == "--pipe-no-edge") {
      pipe_no_edge = true;
    } else if (arg == "--text-no-stem") {
      text_no_stem = true;
    } else {
      std::cerr << "Unknown option: " << argv[i] << "\n";
      usage();
      return 1;
    }
  }

  if (data_path.empty()) {
    usage();
    return 1;
  }

  auto lines = load_lines(data_path);
  if (lines.empty()) {
    std::cerr << "No non-empty lines in " << data_path << "\n";
    return 1;
  }

  std::unique_ptr<irs::analysis::Analyzer> tokenizer_owner;
  irs::analysis::Analyzer* tokenizer = nullptr;

  if (tokenizer_kind == "text") {
    irs::analysis::analyzers::Init();
    static constexpr auto kJson = irs::Type<irs::text_format::Json>::get();
    const std::string text_config = absl::StrCat(
      R"({
      "locale": "en_US.UTF-8",
      "case": "lower",
      "accent": false,
      "stemming": )",
      text_no_stem ? "false" : "true",
      R"(,
      "stopwords": [
        "the","and","or","but","in","on","at","to","of","for",
        "a","an","is","it","as","be","by","if","we"
      ],
      "edgeNGram": {
        "min": 1,
        "max": 3,
        "preserveOriginal": false
      }
    })");
    tokenizer_owner = irs::analysis::analyzers::Get("text", kJson, text_config);
    if (!tokenizer_owner) {
      std::cerr << "Failed to create text tokenizer\n";
      return 1;
    }
    tokenizer = tokenizer_owner.get();
  } else if (tokenizer_kind == "pipeline") {
    irs::analysis::analyzers::Init();
    static constexpr auto kJson = irs::Type<irs::text_format::Json>::get();
    const std::string pipeline_config =
      BuildPipelineConfig(pipe_no_stopwords, pipe_no_stem, pipe_no_edge);
    tokenizer_owner =
      irs::analysis::analyzers::Get("pipeline", kJson, pipeline_config);
    if (!tokenizer_owner) {
      std::cerr << "Failed to create pipeline tokenizer\n";
      return 1;
    }
    tokenizer = tokenizer_owner.get();
  } else if (tokenizer_kind == "path_hierarchy") {
    irs::analysis::PathHierarchyTokenizer::Options opts;
    opts.delimiter = ph_delimiter;
    opts.replacement = ph_replacement;
    opts.reverse = ph_reverse;
    opts.skip = static_cast<size_t>(ph_skip);
    tokenizer_owner = irs::analysis::PathHierarchyTokenizer::make(std::move(opts));
    if (!tokenizer_owner) {
      std::cerr << "Failed to create PathHierarchyTokenizer\n";
      return 1;
    }
    tokenizer = tokenizer_owner.get();
  } else {
    int group = 0;
    if (tokenizer_kind == "path") {
      group = -1;
      if (regex_pattern.empty()) {
        regex_pattern = "[/]+";
      }
    } else {
      group = 0;
      // RE2 approximation of Java UNICODE_CHARACTER_CLASS \w / Rust regex \w:
      //   Rust \w = [\p{Alphabetic}\p{Nd}\p{Pc}\p{Join_Control}]
      //   RE2 mapping:
      //     \p{L}            = letters (all scripts)
      //     \p{Nl}           = letter-numbers (Roman numerals, part of
      //     \p{Alphabetic})
      //     \p{M}            = combining marks (covers Other_Alphabetic vowel
      //     signs)
      //     \p{Nd}           = decimal digits only (\p{No} superscripts
      //     excluded)
      //     \p{Pc}           = connector punctuation (_, ‿, ⁀ etc.)
      //     \x{200C}\x{200D} = ZWNJ/ZWJ (the two Join_Control chars)
      if (regex_pattern.empty()) {
        regex_pattern =
          "[\\p{L}\\p{M}\\p{Nl}\\p{Nd}\\p{Pc}\\x{200C}\\x{200D}]+";
      }
    }
    tokenizer_owner =
      std::make_unique<irs::analysis::PatternTokenizer>(regex_pattern, group);
    tokenizer = tokenizer_owner.get();
  }

  if (dump) {
    auto* term_attr = irs::get<irs::TermAttr>(*tokenizer);
    for (auto& line : lines) {
      tokenizer->reset(line);
      while (tokenizer->next()) {
        std::string_view text = irs::ViewCast<char>(term_attr->value);
        std::printf("%.*s\n", static_cast<int>(text.size()), text.data());
      }
    }
    return 0;
  }

  for (int w = 0; w < warmup; ++w) {
    process_lines(*tokenizer, lines);
  }

  int64_t checksum = 0LL;
  uint64_t token_count = 0;
  std::vector<uint64_t> latencies;
  latencies.reserve(runs);

  for (int r = 0; r < runs; ++r) {
    auto t0 = std::chrono::high_resolution_clock::now();
    auto [hash, count] = process_lines(*tokenizer, lines);
    auto t1 = std::chrono::high_resolution_clock::now();

    uint64_t ns = static_cast<uint64_t>(
      std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count());
    latencies.push_back(ns);

    if (r == 0) {
      checksum = hash;
      token_count = count;
    }
  }

  auto p = calc_percentiles(latencies);
  uint64_t mean_ns =
    std::accumulate(latencies.begin(), latencies.end(), uint64_t{0}) /
    latencies.size();

  std::printf("tokenizer=%s runs=%d lines=%zu tokens=%llu\n",
              tokenizer_kind.c_str(), runs, lines.size(),
              static_cast<unsigned long long>(token_count));
  std::printf("time_ms p50=%.2f p95=%.2f p99=%.2f p100=%.2f mean=%.2f\n",
              p.p50 / 1e6, p.p95 / 1e6, p.p99 / 1e6, p.p100 / 1e6,
              mean_ns / 1e6);
  std::printf("time_ns p50=%llu p95=%llu p99=%llu p100=%llu mean=%llu\n",
              static_cast<unsigned long long>(p.p50),
              static_cast<unsigned long long>(p.p95),
              static_cast<unsigned long long>(p.p99),
              static_cast<unsigned long long>(p.p100),
              static_cast<unsigned long long>(mean_ns));
  std::printf("checksum=%lld\n", static_cast<long long>(checksum));

  return 0;
}
