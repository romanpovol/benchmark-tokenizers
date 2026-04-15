#include <benchmark/benchmark.h>

#include <string>
#include <vector>
#include <fstream>
#include <iostream>
#include <utility>

// ============================================================
// Подключение библиотек
// ============================================================
#include "double_metaphone.h"  // pixelglow
#include "mtfn.h"              // fizzup/mtfn

// ============================================================
// Тестовые данные
// ============================================================

static const std::vector<std::string> kShortWords = {
    "cat", "dog", "fish", "bird", "tree", "book", "lamp",
    "stone", "river", "cloud", "smoke", "blade", "frame",
    "ghost", "knack", "psalm", "wrist", "gnome", "phone",
    "knight", "write", "wrong", "knows", "plumb", "eight"
};

static const std::vector<std::string> kMediumWords = {
    "Schmidt", "Angier", "Carlson", "Ashcraft", "Tymczak",
    "algorithm", "metaphone", "phonetic", "symphony", "telephone",
    "psychiatry", "pneumonia", "mnemonic", "pterodactyl", "chrysalis",
    "lieutenant", "bourgeois", "rendezvous", "entrepreneur", "silhouette",
    "catalogue", "technique", "mystique", "grotesque", "arabesque"
};

static const std::vector<std::string> kLongWords = {
    "Schwarzenegger", "Constantinople", "psychotherapist",
    "electrophoresis", "diphtheria", "onomatopoeia",
    "autobiography", "philanthropist", "archaeological",
    "telecommunications", "internationalization", "misunderstanding",
    "acknowledgement", "characteristically", "enthusiastically",
    "incomprehensible", "disproportionate", "unconstitutional",
    "extraterrestrial", "antidisestablishmentarianism"
};

static const std::vector<std::string> kTrickyWords = {
    "Czar", "Czerny", "Gnocchi", "Ghiradelli", "Phoebe",
    "Tchaikovsky", "Thatcher", "Wraith", "Pneumatic", "Mnemosyne",
    "Ptolemy", "Pseudo", "Xylophone", "Zhivago", "Schaefer",
    "Ochoa", "Bacchus", "Bacher", "Caesar", "Chianti",
    "Chutzpah", "Dzhokhar", "Filipowicz", "Geiger", "Jankelowicz",
    "Mclaughlin", "Mcintyre", "Phlegm", "Wright", "Knightsbridge"
};

// ============================================================
// Загрузка слов из файла
// ============================================================

static std::vector<std::string> LoadWordsFromFile(const std::string& path,
                                                   size_t max_words = 100000) {
    std::vector<std::string> words;
    std::ifstream file(path);
    if (!file.is_open()) return words;
    std::string line;
    while (std::getline(file, line) && words.size() < max_words) {
        auto start = line.find_first_not_of(" \t\r\n");
        auto end = line.find_last_not_of(" \t\r\n");
        if (start != std::string::npos) {
            words.push_back(line.substr(start, end - start + 1));
        }
    }
    return words;
}

static std::vector<std::string> gFileWords;

static void LoadFileWordsOnce() {
    static bool loaded = false;
    if (!loaded) {
        gFileWords = LoadWordsFromFile("data/words.txt", 100000);
        if (!gFileWords.empty()) {
            std::cout << "[INFO] Loaded " << gFileWords.size()
                      << " words from data/words.txt\n";
        } else {
            std::cout << "[INFO] data/words.txt not found, "
                         "skipping file-based benchmarks\n";
        }
        loaded = true;
    }
}

// ============================================================
// Утилита: смешанный список слов
// ============================================================

static std::vector<std::string> BuildMixedWordList(size_t n) {
    std::vector<std::string> all;
    all.insert(all.end(), kShortWords.begin(), kShortWords.end());
    all.insert(all.end(), kMediumWords.begin(), kMediumWords.end());
    all.insert(all.end(), kLongWords.begin(), kLongWords.end());
    all.insert(all.end(), kTrickyWords.begin(), kTrickyWords.end());

    std::vector<std::string> result;
    result.reserve(n);
    for (size_t i = 0; i < n; ++i) {
        result.push_back(all[i % all.size()]);
    }
    return result;
}

// ============================================================
// PIXELGLOW бенчмарки
// ============================================================

static void BM_Pixelglow_ShortWords(benchmark::State& state) {
    for (auto _ : state) {
        for (const auto& word : kShortWords) {
            auto result = dm::double_metaphone(word);
            benchmark::DoNotOptimize(result);
        }
    }
    state.SetItemsProcessed(state.iterations() *
                            static_cast<int64_t>(kShortWords.size()));
}
BENCHMARK(BM_Pixelglow_ShortWords);

static void BM_Pixelglow_MediumWords(benchmark::State& state) {
    for (auto _ : state) {
        for (const auto& word : kMediumWords) {
            auto result = dm::double_metaphone(word);
            benchmark::DoNotOptimize(result);
        }
    }
    state.SetItemsProcessed(state.iterations() *
                            static_cast<int64_t>(kMediumWords.size()));
}
BENCHMARK(BM_Pixelglow_MediumWords);

static void BM_Pixelglow_LongWords(benchmark::State& state) {
    for (auto _ : state) {
        for (const auto& word : kLongWords) {
            auto result = dm::double_metaphone(word);
            benchmark::DoNotOptimize(result);
        }
    }
    state.SetItemsProcessed(state.iterations() *
                            static_cast<int64_t>(kLongWords.size()));
}
BENCHMARK(BM_Pixelglow_LongWords);

static void BM_Pixelglow_TrickyWords(benchmark::State& state) {
    for (auto _ : state) {
        for (const auto& word : kTrickyWords) {
            auto result = dm::double_metaphone(word);
            benchmark::DoNotOptimize(result);
        }
    }
    state.SetItemsProcessed(state.iterations() *
                            static_cast<int64_t>(kTrickyWords.size()));
}
BENCHMARK(BM_Pixelglow_TrickyWords);

static void BM_Pixelglow_SingleWord(benchmark::State& state) {
    const std::string word = "Schwarzenegger";
    for (auto _ : state) {
        auto result = dm::double_metaphone(word);
        benchmark::DoNotOptimize(result);
    }
    state.SetItemsProcessed(state.iterations());
}
BENCHMARK(BM_Pixelglow_SingleWord);

static void BM_Pixelglow_FileWords(benchmark::State& state) {
    LoadFileWordsOnce();
    if (gFileWords.empty()) {
        state.SkipWithMessage("data/words.txt not available");
        return;
    }
    for (auto _ : state) {
        for (const auto& word : gFileWords) {
            auto result = dm::double_metaphone(word);
            benchmark::DoNotOptimize(result);
        }
    }
    state.SetItemsProcessed(state.iterations() *
                            static_cast<int64_t>(gFileWords.size()));
}
BENCHMARK(BM_Pixelglow_FileWords);

static void BM_Pixelglow_Batch(benchmark::State& state) {
    auto words = BuildMixedWordList(static_cast<size_t>(state.range(0)));
    for (auto _ : state) {
        for (const auto& word : words) {
            auto result = dm::double_metaphone(word);
            benchmark::DoNotOptimize(result);
        }
    }
    state.SetItemsProcessed(state.iterations() *
                            static_cast<int64_t>(words.size()));
}
BENCHMARK(BM_Pixelglow_Batch)
    ->Arg(100)
    ->Arg(1000)
    ->Arg(10000)
    ->Arg(100000);

// ============================================================
// MTFN бенчмарки
// ============================================================

static void BM_Mtfn_ShortWords(benchmark::State& state) {
    for (auto _ : state) {
        for (const auto& word : kShortWords) {
            mtfn::sound s(word);
            benchmark::DoNotOptimize(s.primary());
            benchmark::DoNotOptimize(s.alternate());
        }
    }
    state.SetItemsProcessed(state.iterations() *
                            static_cast<int64_t>(kShortWords.size()));
}
BENCHMARK(BM_Mtfn_ShortWords);

static void BM_Mtfn_MediumWords(benchmark::State& state) {
    for (auto _ : state) {
        for (const auto& word : kMediumWords) {
            mtfn::sound s(word);
            benchmark::DoNotOptimize(s.primary());
            benchmark::DoNotOptimize(s.alternate());
        }
    }
    state.SetItemsProcessed(state.iterations() *
                            static_cast<int64_t>(kMediumWords.size()));
}
BENCHMARK(BM_Mtfn_MediumWords);

static void BM_Mtfn_LongWords(benchmark::State& state) {
    for (auto _ : state) {
        for (const auto& word : kLongWords) {
            mtfn::sound s(word);
            benchmark::DoNotOptimize(s.primary());
            benchmark::DoNotOptimize(s.alternate());
        }
    }
    state.SetItemsProcessed(state.iterations() *
                            static_cast<int64_t>(kLongWords.size()));
}
BENCHMARK(BM_Mtfn_LongWords);

static void BM_Mtfn_TrickyWords(benchmark::State& state) {
    for (auto _ : state) {
        for (const auto& word : kTrickyWords) {
            mtfn::sound s(word);
            benchmark::DoNotOptimize(s.primary());
            benchmark::DoNotOptimize(s.alternate());
        }
    }
    state.SetItemsProcessed(state.iterations() *
                            static_cast<int64_t>(kTrickyWords.size()));
}
BENCHMARK(BM_Mtfn_TrickyWords);

static void BM_Mtfn_SingleWord(benchmark::State& state) {
    const std::string word = "Schwarzenegger";
    for (auto _ : state) {
        mtfn::sound s(word);
        benchmark::DoNotOptimize(s.primary());
        benchmark::DoNotOptimize(s.alternate());
    }
    state.SetItemsProcessed(state.iterations());
}
BENCHMARK(BM_Mtfn_SingleWord);

// Бенчмарк сравнения (уникальная фича mtfn — operator==)
static void BM_Mtfn_Compare(benchmark::State& state) {
    for (auto _ : state) {
        for (size_t i = 0; i + 1 < kMediumWords.size(); i += 2) {
            bool eq = mtfn::sounds_like(kMediumWords[i], kMediumWords[i + 1]);
            benchmark::DoNotOptimize(eq);
        }
    }
    state.SetItemsProcessed(state.iterations() *
                            static_cast<int64_t>(kMediumWords.size() / 2));
}
BENCHMARK(BM_Mtfn_Compare);

// Бенчмарк без ограничения длины (limit_length = false)
static void BM_Mtfn_MediumWords_Unlimited(benchmark::State& state) {
    for (auto _ : state) {
        for (const auto& word : kMediumWords) {
            mtfn::sound s(word, false);  // limit_length = false
            benchmark::DoNotOptimize(s.primary());
            benchmark::DoNotOptimize(s.alternate());
        }
    }
    state.SetItemsProcessed(state.iterations() *
                            static_cast<int64_t>(kMediumWords.size()));
}
BENCHMARK(BM_Mtfn_MediumWords_Unlimited);

static void BM_Mtfn_FileWords(benchmark::State& state) {
    LoadFileWordsOnce();
    if (gFileWords.empty()) {
        state.SkipWithMessage("data/words.txt not available");
        return;
    }
    for (auto _ : state) {
        for (const auto& word : gFileWords) {
            mtfn::sound s(word);
            benchmark::DoNotOptimize(s.primary());
            benchmark::DoNotOptimize(s.alternate());
        }
    }
    state.SetItemsProcessed(state.iterations() *
                            static_cast<int64_t>(gFileWords.size()));
}
BENCHMARK(BM_Mtfn_FileWords);

static void BM_Mtfn_Batch(benchmark::State& state) {
    auto words = BuildMixedWordList(static_cast<size_t>(state.range(0)));
    for (auto _ : state) {
        for (const auto& word : words) {
            mtfn::sound s(word);
            benchmark::DoNotOptimize(s.primary());
            benchmark::DoNotOptimize(s.alternate());
        }
    }
    state.SetItemsProcessed(state.iterations() *
                            static_cast<int64_t>(words.size()));
}
BENCHMARK(BM_Mtfn_Batch)
    ->Arg(100)
    ->Arg(1000)
    ->Arg(10000)
    ->Arg(100000);
