use clap::{Parser, ValueEnum};
use regex::Regex;
use std::fs::File;
use std::io::{BufRead, BufReader, Write};
use std::path::PathBuf;
use std::time::Instant;

use tantivy::schema::Facet;
use tantivy::tokenizer::{FacetTokenizer, RegexTokenizer, TokenStream, Tokenizer};

const DEFAULT_REGEX_PATTERN: &str = r"\w+";
const DEFAULT_WARMUP: u32 = 2;
const DEFAULT_RUNS: u32 = 20;

#[derive(Clone, Debug, ValueEnum)]
enum TokenizerKind {
    #[value(alias = "pattern")]
    Regex,

    #[value(alias = "path")]
    Facet,
}

#[derive(Parser)]
#[command(about = "Benchmark Tantivy regex and facet tokenizers (token stream only, Lucene-style)")]
struct Args {
    #[arg(short, long)]
    data: PathBuf,

    #[arg(value_enum, short, long, default_value = "regex")]
    tokenizer: TokenizerKind,

    #[arg(long, default_value = DEFAULT_REGEX_PATTERN)]
    regex_pattern: String,

    #[arg(short, long, default_value_t = DEFAULT_RUNS)]
    runs: u32,

    #[arg(long, default_value_t = DEFAULT_WARMUP)]
    warmup: u32,

    // Measure `RegexTokenizer::token_stream` as Tantivy calls it (clones `Regex` per line internally its very slow; use only for profiling)
    #[arg(long, default_value_t = false)]
    per_line_regex_clone: bool,

    // Print every token to stdout and exit, skipping benchmark
    #[arg(long, default_value_t = false)]
    dump: bool,

    /// Write per-run wall times (ns) as uint64
    #[arg(long, value_name = "PATH")]
    bench_runs_file: Option<PathBuf>,
}

fn load_lines(path: &PathBuf) -> Vec<String> {
    let f = File::open(path).expect("open data file");
    let mut lines = Vec::new();
    for line in BufReader::new(f).lines() {
        if let Ok(s) = line {
            let s = s.trim().to_string();
            if !s.is_empty() {
                lines.push(s);
            }
        }
    }
    lines
}

fn canonical_hash_token(h: &mut i64, text: &str) {
    for b in text.bytes() {
        *h = h.wrapping_mul(31).wrapping_add(b as i64);
    }
}

// Hash a FacetTokenizer token without allocating:
// prepend '/' and replace '\x00' separators with '/' on the fly
fn canonical_hash_facet_token(h: &mut i64, raw: &str) {
    *h = h.wrapping_mul(31).wrapping_add(b'/' as i64);
    for b in raw.bytes() {
        let mapped = if b == b'\x00' { b'/' } else { b };
        *h = h.wrapping_mul(31).wrapping_add(mapped as i64);
    }
}

// One compiled `Regex` per run, comparable to Lucene (single PatternTokenizer instance)
fn process_lines_regex_shared(re: &Regex, lines: &[String]) -> (i64, u64) {
    let mut h: i64 = 0;
    let mut count: u64 = 0;
    for line in lines {
        for m in re.find_iter(line) {
            if m.start() == m.end() {
                continue;
            }
            canonical_hash_token(&mut h, m.as_str());
            count += 1;
        }
    }
    (h, count)
}

// https://github.com/quickwit-oss/tantivy/pull/1759#discussion_r1061400442
fn process_lines_regex(tokenizer: &mut RegexTokenizer, lines: &[String]) -> (i64, u64) {
    let mut h: i64 = 0;
    let mut count: u64 = 0;
    for line in lines {
        let mut stream = tokenizer.token_stream(line.as_str());
        while stream.advance() {
            canonical_hash_token(&mut h, &stream.token().text);
            count += 1;
        }
    }
    (h, count)
}

fn process_lines_facet(tokenizer: &mut FacetTokenizer, lines: &[String]) -> (i64, u64) {
    let mut h: i64 = 0;
    let mut count: u64 = 0;
    for line in lines {
        let facet = Facet::from_text(line).expect("valid facet path");
        let encoded = facet.encoded_str();
        let mut stream = tokenizer.token_stream(encoded);
        while stream.advance() {
            // FacetTokenizer encodes '/' as '\x00' and strips the leading '/'.
            // It also emits an empty root token ("") - skip it, Lucene/iresearch don't emit "/".
            // Token "a\x00b\x00c" represents "/a/b/c" - restore it to match
            // Lucene PathHierarchyTokenizer and iresearch PathHierarchyTokenizer.
            let raw = &stream.token().text;
            if raw.is_empty() {
                continue;
            }
            canonical_hash_facet_token(&mut h, raw);
            count += 1;
        }
    }
    (h, count)
}

fn main() {
    let args = Args::parse();
    let lines = load_lines(&args.data);
    if lines.is_empty() {
        eprintln!("No non-empty lines in {}", args.data.display());
        return;
    }

    let mode_label = match args.tokenizer {
        TokenizerKind::Regex => "regex",
        TokenizerKind::Facet => "facet",
    };

    match args.tokenizer {
        TokenizerKind::Regex => {
            let re = Regex::new(&args.regex_pattern).expect("valid regex");
            let mut tokenizer = RegexTokenizer::new(&args.regex_pattern).expect("valid regex");

            if args.dump {
                for line in &lines {
                    for m in re.find_iter(line) {
                        if m.start() != m.end() {
                            println!("{}", m.as_str());
                        }
                    }
                }
                return;
            }

            if args.per_line_regex_clone {
                for _ in 0..args.warmup {
                    process_lines_regex(&mut tokenizer, &lines);
                }
            } else {
                for _ in 0..args.warmup {
                    process_lines_regex_shared(&re, &lines);
                }
            }

            let mut checksum = 0i64;
            let mut token_count = 0u64;
            let mut latencies = Vec::with_capacity(args.runs as usize);
            for r in 0..args.runs {
                let start = Instant::now();
                let (hash, count) = if args.per_line_regex_clone {
                    process_lines_regex(&mut tokenizer, &lines)
                } else {
                    process_lines_regex_shared(&re, &lines)
                };
                let elapsed = start.elapsed().as_nanos() as u64;
                latencies.push(elapsed);
                if r == 0 {
                    checksum = hash;
                    token_count = count;
                }
            }
            print_results(
                mode_label,
                args.runs,
                lines.len(),
                token_count,
                &latencies,
                checksum,
            );
            if let Some(ref p) = args.bench_runs_file {
                write_bench_runs_file(p, &latencies);
            }
        }
        TokenizerKind::Facet => {
            let mut tokenizer = FacetTokenizer::default();

            if args.dump {
                for line in &lines {
                    let facet = Facet::from_text(line).expect("valid facet path");
                    let encoded = facet.encoded_str();
                    let mut stream = tokenizer.token_stream(encoded);
                    while stream.advance() {
                        let raw = &stream.token().text;
                        if !raw.is_empty() {
                            println!("/{}", raw.replace('\x00', "/"));
                        }
                    }
                }
                return;
            }

            for _ in 0..args.warmup {
                process_lines_facet(&mut tokenizer, &lines);
            }
            let mut checksum = 0i64;
            let mut token_count = 0u64;
            let mut latencies = Vec::with_capacity(args.runs as usize);
            for r in 0..args.runs {
                let start = Instant::now();
                let (hash, count) = process_lines_facet(&mut tokenizer, &lines);
                let elapsed = start.elapsed().as_nanos() as u64;
                latencies.push(elapsed);
                if r == 0 {
                    checksum = hash;
                    token_count = count;
                }
            }
            print_results(
                mode_label,
                args.runs,
                lines.len(),
                token_count,
                &latencies,
                checksum,
            );
            if let Some(ref p) = args.bench_runs_file {
                write_bench_runs_file(p, &latencies);
            }
        }
    }
}

fn print_results(
    tokenizer: &str,
    runs: u32,
    line_count: usize,
    token_count: u64,
    latencies: &[u64],
    checksum: i64,
) {
    let mut sorted = latencies.to_vec();
    sorted.sort_unstable();
    let n = sorted.len();
    let p50 = sorted[(n as f64 * 0.50) as usize];
    let p95 = sorted[(n as f64 * 0.95) as usize];
    let p99 = sorted[(n as f64 * 0.99).min((n - 1) as f64) as usize];
    let p100 = sorted[n - 1];
    let mean_ns: u64 = latencies.iter().sum::<u64>() / latencies.len() as u64;

    println!("tokenizer={tokenizer} runs={runs} lines={line_count} tokens={token_count}");
    println!(
        "time_ms p50={:.2} p95={:.2} p99={:.2} p100={:.2} mean={:.2}",
        p50 as f64 / 1e6,
        p95 as f64 / 1e6,
        p99 as f64 / 1e6,
        p100 as f64 / 1e6,
        mean_ns as f64 / 1e6
    );
    println!("time_ns p50={p50} p95={p95} p99={p99} p100={p100} mean={mean_ns}");
    println!("checksum={checksum}");
}

fn write_bench_runs_file(path: &PathBuf, latencies: &[u64]) {
    let mut f = File::create(path).expect("create --bench-runs-file");
    for &v in latencies {
        f.write_all(&v.to_le_bytes())
            .expect("write per-run time to --bench-runs-file");
    }
}
