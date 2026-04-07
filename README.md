# Tokenizer Benchmark

Cross-system tokenizer benchmark: **Lucene**, **Tantivy**, **SereneDB**.

Measures tokenization throughput and verifies that all systems produce identical tokens via a canonical checksum.

Supported tokenizers:
- `pattern` -- regex-based word tokenizer (`\w+`)
- `path` -- path hierarchy tokenizer (emits cumulative prefixes: `/a`, `/a/b`, `/a/b/c`)

---

## Adding your own tokenizer

### Step 1

- Pick a stable tokenizer id, e.g. `my_tokenizer`
- Decide which options are part of the benchmark surface
- Add the tokenizer to the “Supported tokenizers” list at the top of this README

### Step 2 - wire it into `bench.py`

Edit `bench.py` so the new tokenizer can be selected and executed:

- Tokenizer list / CLI validation: add the new id to the supported tokenizers
- Per-system command mapping:
  - Pass `--tokenizer <name>` (or map to the system-specific name, if it differs)
  - Thread any tokenizer options you want to benchmark (example: `--reverse` for `path`)
- Parsing requirements
  - Each system must print total tokens processed and a canonical checksum
  - `bench.py` compares checksums and fails the run on mismatch

### Common pitfalls

- Split vs prefix semantics: different libraries have similarly named tokenizers with different
  output (e.g. “path” vs “path hierarchy”). Always validate by checksum and (when debugging) token
  dumps
- Unicode / regex differences: `\w` and Unicode character classes differ across engines/versions
- Wrapping arithmetic: checksum must use wrapping 64-bit arithmetic consistently

---

## Prerequisites

| Tool | Min version | Notes |
|------|-------------|-------|
| Python | 3.8+ | runs `bench.py` and helper scripts |
| JDK | 21 | Lucene; auto-detected by Gradle |
| Gradle | -- | bundled via `./gradlew`, no install needed |
| Rust + Cargo | stable | `rustup.rs` |
| CMake | 3.16+ | only for SereneDB |
| Ninja | any | only for SereneDB |
| clang++ | 21 | only for SereneDB |

---

## Quick start (Lucene + Tantivy)

```bash
# 1. Build Tantivy benchmark
cd tantivy-bench && cargo build --release && cd ..

# 2. Run (Lucene builds automatically via Gradle on first run)
make bench DATA=tantivy-bench/test_words.txt
```

---

## Adding SereneDB

iresearch-bench is compiled inside the SereneDB CMake tree.
It requires a cloned SereneDB repository with a Release build.

### Step 1 -- configure and build SereneDB (once)

```bash
cd ../serenedb

cmake --preset bench \
  -DCMAKE_C_COMPILER=clang-21 \
  -DCMAKE_CXX_COMPILER=clang++-21 \
  -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON

ninja -C build_bench iresearch-static
```

### Step 2 -- build iresearch-bench

```bash
cd ../benchmark-tokenizers

make iresearch-build IRESEARCH_SRC=../serenedb
```

This will:
1. Copy `iresearch-bench/` sources into SereneDB's build tree temporarily
2. Compile the binary via `cmake --build`
3. Remove all added files -- SereneDB is left unmodified

Binary lands at: `../serenedb/build_bench/bin/iresearch-bench`

### Step 3 -- run with iresearch

```bash
export IRESEARCH_SRC=../serenedb

make bench DATA=tantivy-bench/test_words.txt
```

---

## Make targets

```
make bench                           run all tokenizers × all systems
make bench-pattern                   pattern/regex tokenizer only
make bench-path                      path hierarchy tokenizer only
make bench-lucene                    Lucene only
make bench-tantivy                   Tantivy only
make bench-iresearch                 iresearch only
make iresearch-build IRESEARCH_SRC=  build iresearch-bench binary (Release)
make iresearch-build-prof            rebuild SereneDB+RE2 with frame pointers for profiling
make profile-iresearch               profile iresearch-bench (perf flamegraph / callgrind)
make compare OLD=a.txt NEW=b.txt     compare two saved result files
make help                            show all targets and variables
```

## Variables

| Variable          | Description                                           | Default                        |
|-------------------|-------------------------------------------------------|--------------------------------|
| `DATA`            | Input file -- one document per line                   | `tantivy-bench/test_words.txt` |
| `COUNT`           | Number of timed runs                                  | `10`                           |
| `WARMUP`          | Number of warmup runs (not measured)                  | `2`                            |
| `SYSTEMS`         | `lucene`, `tantivy`, `iresearch`, or `all`            | `all`                          |
| `REVERSE`         | `1` -- reverse path hierarchy (path only, no Tantivy) | --                              |
| `OUTPUT`          | Save results to file                                  | --                              |
| `COMPARE`         | Compare against a previously saved result file        | --                              |
| `IRESEARCH_SRC`   | Path to cloned SereneDB repository                    | --                              |
| `IRESEARCH_BUILD` | Path to SereneDB build directory                      | `$IRESEARCH_SRC/build_bench`   |

---

## Examples

```bash
# Pattern benchmark, all systems, 20 runs
make bench-pattern COUNT=20 DATA=data/wiki.txt

# Path hierarchy, iresearch only
make bench-path SYSTEMS=iresearch DATA=data/paths.txt IRESEARCH_SRC=../serenedb

# Reverse path hierarchy (domain hierarchies), Lucene + iresearch
make bench-path REVERSE=1 SYSTEMS=lucene,iresearch DATA=data/paths.txt

# Save baseline, then compare after a change
make bench DATA=data/wiki.txt COUNT=10 OUTPUT=results/baseline.txt
make bench DATA=data/wiki.txt COUNT=10 OUTPUT=results/new.txt COMPARE=results/baseline.txt
```

---

## Datasets

### Built-in test file

`tantivy-bench/test_words.txt` -- small sample for quick smoke-testing.

### Path hierarchy dataset

```bash
python3 scripts/gen_paths.py -n 100000 -o data/paths.txt
```

Generates 100k Unix/URL/category paths starting with `/`, compatible with all three systems.

### Wikipedia

```bash
./scripts/download_and_prepare_wikipedia.sh # Simple English Wikipedia (~500 MB)
# result: data/wiki_work/wiki_lines.txt

# Limit to N lines for quick tests
python3 scripts/extract_wiki_lines.py data/wiki_work/extracted - --max-docs 10000 > sample.txt
```

See `scripts/README.md` for full options (custom dump URL, enwiki, etc).

---

## Profiling iresearch

```bash
# Flamegraph via perf -- saves profile/flamegraph.svg
make profile-iresearch IRESEARCH_BUILD=../serenedb/build_bench DATA=data/paths.txt PROF_TOKENIZER=path PROF_COUNT=200

# Quick hardware counters -- no root needed
make profile-iresearch PROF_MODE=perf-stat IRESEARCH_BUILD=../serenedb/build_bench DATA=data/paths.txt

# Callgrind -- open result with kcachegrind
make profile-iresearch PROF_MODE=callgrind PROF_COUNT=5 IRESEARCH_BUILD=../serenedb/build_bench DATA=data/paths.txt
```

> **Note:** `perf` modes require `perf_event_paranoid <= 1`.
> Check with `cat /proc/sys/kernel/perf_event_paranoid`.
> To set temporarily: `echo 1 | sudo tee /proc/sys/kernel/perf_event_paranoid`

### Seeing library internals in the flamegraph

By default SereneDB is built without frame pointers, so `perf` cannot unwind through RE2 and
other dependencies -- their calls are hidden under `[unknown]`

To get full call stacks through RE2, abseil, and all other libs, rebuild SereneDB with
`-fno-omit-frame-pointer` globally:

```bash
# One-time build into build_prof/ (takes same time as a normal full rebuild)
make iresearch-build-prof IRESEARCH_SRC=../serenedb

# Then profile using that build
make profile-iresearch \
  IRESEARCH_BUILD=../serenedb/build_prof \
  DATA=tantivy-bench/test_words.txt \
  PROF_TOKENIZER=pattern \
  PROF_COUNT=200
# -> profile/flamegraph.svg  with full RE2 stacks
```

`build_bench` (normal Release) and `build_prof` coexist -- regular benchmarks are unaffected.

| Variable        | Description                                      | Default     |
|-----------------|--------------------------------------------------|-------------|
| `PROF_TOKENIZER`| `pattern` or `path`                              | `pattern`   |
| `PROF_COUNT`    | Runs inside the profiled process                 | `100`       |
| `PROF_MODE`     | `perf` (flamegraph), `perf-stat`, `callgrind`    | `perf`      |
| `PROF_OUT`      | Output directory                                 | `profile/`  |

### Dependencies -- installed automatically if missing

| Mode         | Requires | How |
|--------------|----------|-----|
| `perf`       | `perf`, FlameGraph scripts | `perf` -- `sudo apt-get install linux-tools-$(uname -r) linux-tools-generic`; FlameGraph -- cloned from GitHub to `/tmp/FlameGraph` |
| `perf-stat`  | `perf` | same as above |
| `callgrind`  | `valgrind` | `sudo apt-get install valgrind` |

The Makefile checks for each tool before running and installs/clones what is missing.
`sudo` is only needed for `perf` and `valgrind`; FlameGraph requires no privileges

---

## Checksum verification

Every run computes a canonical hash over the UTF-8 bytes of all tokens and compares across systems.
A mismatch means the tokenizers produce different output -- the run exits with a non-zero code.

```
checksum/Pattern  OK       iresearch=4066605535946015185  lucene=4066605535946015185  tantivy=4066605535946015185
checksum/Pattern  MISMATCH iresearch=123...  lucene=456...  tantivy=789...
```
