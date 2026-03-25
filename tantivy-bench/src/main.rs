//! Бенчмарк Tantivy в том же духе, что и Lucene `LuceneTokenizerPerf` / `TestAnalyzerPerf`:
//! строки из файла, на каждой строке только потребление токен-потока (`advance()` + атрибуты токена),
//! без построения индекса. Перцентили по времени полного прохода; память — снаружи (`/usr/bin/time -v`).

use clap::{Parser, ValueEnum};
use regex::Regex;
use std::fs::File;
use std::io::{BufRead, BufReader};
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

    /// Измерять `RegexTokenizer::token_stream` как в Tantivy (на каждую строку клонируется `Regex` внутри API — очень медленно; только для профилирования накладных расходов)
    #[arg(long, default_value_t = false)]
    per_line_regex_clone: bool,
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

fn term_hash_bytes(text: &str) -> i64 {
    let mut h: i64 = 0;
    for b in text.bytes() {
        h = h.wrapping_mul(31).wrapping_add(b as i64);
    }
    h
}

fn hash_token(t: &tantivy::tokenizer::Token) -> i64 {
    hash_token_parts(
        t.text.as_str(),
        t.position,
        t.position_length,
        t.offset_from,
        t.offset_to,
    )
}

fn hash_token_parts(
    text: &str,
    position: usize,
    position_length: usize,
    offset_from: usize,
    offset_to: usize,
) -> i64 {
    let mut h: i64 = 0;
    h += term_hash_bytes(text);
    h += 31 * position as i64;
    h += 31 * position_length as i64;
    h += 31 * offset_from as i64;
    h += 31 * offset_to as i64;
    h
}

/// Один скомпилированный `Regex` на весь прогон — сопоставимо с Lucene (один `PatternTokenizer`).
/// Семантика как у `RegexTokenizer`: последовательные непересекающиеся совпадения, позиции 0,1,… после reset (как `usize::MAX` + 1, + 2, …).
fn process_lines_regex_shared(re: &Regex, lines: &[String]) -> i64 {
    let mut hash: i64 = 0;
    for line in lines {
        let mut pos = usize::MAX;
        for m in re.find_iter(line) {
            if m.start() == m.end() {
                continue;
            }
            pos = pos.wrapping_add(1);
            let h = hash_token_parts(m.as_str(), pos, 1, m.start(), m.end());
            hash = hash.wrapping_add(31 * h);
        }
    }
    hash
}

fn process_lines_regex(tokenizer: &mut RegexTokenizer, lines: &[String]) -> i64 {
    let mut hash: i64 = 0;
    for line in lines {
        let mut stream = tokenizer.token_stream(line.as_str());
        while stream.advance() {
            hash = hash.wrapping_add(31 * hash_token(stream.token()));
        }
    }
    hash
}

fn process_lines_facet(tokenizer: &mut FacetTokenizer, lines: &[String]) -> i64 {
    let mut hash: i64 = 0;
    for line in lines {
        let facet = Facet::from_text(line).expect("valid facet path");
        let encoded = facet.encoded_str();
        let mut stream = tokenizer.token_stream(encoded);
        while stream.advance() {
            hash = hash.wrapping_add(31 * hash_token(stream.token()));
        }
    }
    hash
}

fn percentiles(latencies_ns: &mut [u64]) -> (u64, u64, u64, u64) {
    latencies_ns.sort_unstable();
    let n = latencies_ns.len();
    if n == 0 {
        return (0, 0, 0, 0);
    }
    let p50 = latencies_ns[(n as f64 * 0.50) as usize];
    let p95 = latencies_ns[(n as f64 * 0.95) as usize];
    let p99 = latencies_ns[(n as f64 * 0.99).min((n - 1) as f64) as usize];
    let p100 = latencies_ns[n - 1];
    (p50, p95, p99, p100)
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

            if args.per_line_regex_clone {
                for _ in 0..args.warmup {
                    process_lines_regex(&mut tokenizer, &lines);
                }
            } else {
                for _ in 0..args.warmup {
                    process_lines_regex_shared(&re, &lines);
                }
            }

            let mut latencies = Vec::with_capacity(args.runs as usize);
            for r in 0..args.runs {
                let start = Instant::now();
                let checksum = if args.per_line_regex_clone {
                    process_lines_regex(&mut tokenizer, &lines)
                } else {
                    process_lines_regex_shared(&re, &lines)
                };
                let elapsed = start.elapsed().as_nanos() as u64;
                latencies.push(elapsed);
                if r == 0 {
                    eprintln!("checksum(first run)={checksum}");
                }
            }
            print_results(mode_label, args.runs, lines.len(), &mut latencies);
        }
        TokenizerKind::Facet => {
            let mut tokenizer = FacetTokenizer::default();
            for _ in 0..args.warmup {
                process_lines_facet(&mut tokenizer, &lines);
            }
            let mut latencies = Vec::with_capacity(args.runs as usize);
            for r in 0..args.runs {
                let start = Instant::now();
                let checksum = process_lines_facet(&mut tokenizer, &lines);
                let elapsed = start.elapsed().as_nanos() as u64;
                latencies.push(elapsed);
                if r == 0 {
                    eprintln!("checksum(first run)={checksum}");
                }
            }
            print_results(mode_label, args.runs, lines.len(), &mut latencies);
        }
    }
}

fn print_results(tokenizer: &str, runs: u32, line_count: usize, latencies: &mut [u64]) {
    let (p50, p95, p99, p100) = percentiles(latencies);
    let mean_ns: u64 = latencies.iter().sum::<u64>() / latencies.len() as u64;

    println!("tokenizer={tokenizer} runs={runs} lines={line_count}");
    println!(
        "time_ms p50={:.2} p95={:.2} p99={:.2} p100={:.2} mean={:.2}",
        p50 as f64 / 1e6,
        p95 as f64 / 1e6,
        p99 as f64 / 1e6,
        p100 as f64 / 1e6,
        mean_ns as f64 / 1e6
    );
    println!(
        "time_ns p50={p50} p95={p95} p99={p99} p100={p100} mean={mean_ns}"
    );
}
