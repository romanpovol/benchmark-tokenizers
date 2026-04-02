**not clean runs**

# Path hierarchy

```
❯ make bench-path DATA=data/paths.txt SYSTEMS=all
python3 bench.py --bench path --systems all --count 10 --warmup 2 --data data/paths.txt   
tokenizers: path
systems:    lucene, tantivy, iresearch
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/data/paths.txt

--- path ---
  BenchmarkLucene/Path ...  121.276ms mean  (10 runs, 100,000 lines)
  BenchmarkTantivy/Path ...  59.429ms mean  (10 runs, 100,000 lines)
  BenchmarkIresearch/Path ...  25.650ms mean  (10 runs, 100,000 lines)

───────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
───────────────────────────────────────────────────────────────────────────────────────────────
name                           mean         p50         p95         p99        p100       tok/s
───────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkLucene/Path      121.276ms   111.099ms   153.032ms   153.032ms   153.032ms       5.29M
BenchmarkTantivy/Path      59.429ms    59.607ms    61.303ms    61.303ms    61.303ms      10.80M
BenchmarkIresearch/Path    25.650ms    25.709ms    26.521ms    26.521ms    26.521ms      25.02M
───────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Path  OK  iresearch=-8411998038007610440  lucene=-8411998038007610440  tantivy=-8411998038007610440
```

# Reverse path hierarchy (tantivy not support)

```
❯ make bench-path REVERSE=1 DATA=data/paths.txt SYSTEMS=lucene,iresearch
python3 bench.py --bench path --systems lucene,iresearch --count 10 --warmup 2 --data data/paths.txt   --reverse
tokenizers: path
systems:    lucene, iresearch
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/data/paths.txt

--- path ---
  BenchmarkLucene/Path ...  135.802ms mean  (10 runs, 100,000 lines)
  BenchmarkIresearch/Path ...  27.694ms mean  (10 runs, 100,000 lines)

───────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
───────────────────────────────────────────────────────────────────────────────────────────────
name                           mean         p50         p95         p99        p100       tok/s
───────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkLucene/Path      135.802ms   132.049ms   175.462ms   175.462ms   175.462ms       5.46M
BenchmarkIresearch/Path    27.694ms    27.676ms    28.562ms    28.562ms    28.562ms      26.78M
───────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Path  OK  iresearch=-1515999624014964263  lucene=-1515999624014964263
```

# Pattern

```
❯ make bench-pattern DATA=sample.txt SYSTEMS=all
python3 bench.py --bench pattern --systems all --count 10 --warmup 2 --data sample.txt   
tokenizers: pattern
systems:    lucene, tantivy, iresearch
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/sample.txt

--- pattern ---
  BenchmarkLucene/Pattern ...  4.408s mean  (10 runs, 10,000 lines)
  BenchmarkTantivy/Pattern ...  2.714s mean  (10 runs, 10,000 lines)
  BenchmarkIresearch/Pattern ...  3.157s mean  (10 runs, 10,000 lines)

──────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
──────────────────────────────────────────────────────────────────────────────────────────────────
name                              mean         p50         p95         p99        p100       tok/s
──────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkLucene/Pattern         4.408s      4.091s      6.582s      6.582s      6.582s       7.04M
BenchmarkTantivy/Pattern        2.714s      2.698s      2.966s      2.966s      2.966s      11.43M
BenchmarkIresearch/Pattern      3.157s      3.174s      3.285s      3.285s      3.285s       9.82M
──────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pattern  OK  iresearch=4066605535946015185  lucene=4066605535946015185  tantivy=4066605535946015185
```
