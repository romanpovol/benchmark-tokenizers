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

# Text vs Pipeline (`sample_small.txt`)

Dataset: `sample_small.txt` (1,000 lines)

```
❯ make bench-pipeline SYSTEMS=iresearch IRESEARCH_SRC=../serenedb DATA=sample_small.txt
python3 bench.py --bench pipeline --systems iresearch --count 10 --warmup 2 --data sample_small.txt   
tokenizers: pipeline
systems:    iresearch
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/sample_small.txt

--- pipeline ---
  BenchmarkIresearch/Pipeline ...  4.511s mean  (10 runs, 1,000 lines)

───────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
───────────────────────────────────────────────────────────────────────────────────────────────────
name                               mean         p50         p95         p99        p100       tok/s
───────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkIresearch/Pipeline      4.511s      4.505s      4.535s      4.535s      4.535s       1.42M
───────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pipeline  SINGLE  iresearch=-274087441542650178
```

```
❯ make bench-text SYSTEMS=iresearch IRESEARCH_SRC=../serenedb DATA=sample_small.txt
python3 bench.py --bench text --systems iresearch --count 10 --warmup 2 --data sample_small.txt   
tokenizers: text
systems:    iresearch
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/sample_small.txt

--- text ---
  BenchmarkIresearch/Text ...  4.019s mean  (10 runs, 1,000 lines)

───────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
───────────────────────────────────────────────────────────────────────────────────────────────
name                           mean         p50         p95         p99        p100       tok/s
───────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkIresearch/Text      4.019s      4.016s      4.037s      4.037s      4.037s       1.60M
───────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Text  SINGLE  iresearch=-274087441542650178
```

| Variant | mean | tokens | checksum | relative to full pipeline |
|---|---|---|---|---|
| `text` (full monolith) | 4373.20 ms | 6,424,113 | -274087441542650178 | -7.29% |
| `pipeline` (full) | 4717.21 ms | 6,424,113 | -274087441542650178 | baseline |
| `pipeline --pipe-no-edge` | 4660.13 ms | 2,181,558 | -1417360207602844945 | -1.21% |
| `pipeline --pipe-no-stem` | 3387.68 ms | 6,435,401 | 8586809143420619973 | -28.18% |
| `pipeline --pipe-no-stopwords` | 4850.42 ms | 8,220,076 | 6465231610464383666 | +2.82% |
| `pipeline --pipe-no-stopwords --pipe-no-stem` | 3374.15 ms | 8,231,364 | 811169010777660283 | -28.47% |

Besides the pipeline overhead, the biggest contribution comes from the stemmer

# Stem cache optimization

Added in-memory cache in `StemmingTokenizer` (`token -> stem`, 16384 entries with clear-on-full policy).

```
❯ make bench-pipeline SYSTEMS=iresearch IRESEARCH_SRC=../serenedb DATA=sample_small.txt
python3 bench.py --bench pipeline --systems iresearch --count 10 --warmup 2 --data sample_small.txt   
tokenizers: pipeline
systems:    iresearch
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/sample_small.txt

--- pipeline ---
  BenchmarkIresearch/Pipeline ...  3.667s mean  (10 runs, 1,000 lines)

───────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
───────────────────────────────────────────────────────────────────────────────────────────────────
name                               mean         p50         p95         p99        p100       tok/s
───────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkIresearch/Pipeline      3.667s      3.667s      3.683s      3.683s      3.683s       1.75M
───────────────────────────────────────────────────────────────────────────────────────────────────
  checksum/Pipeline  SINGLE  iresearch=-274087441542650178
```

```
❯ make bench-text SYSTEMS=iresearch IRESEARCH_SRC=../serenedb DATA=sample_small.txt
python3 bench.py --bench text --systems iresearch --count 10 --warmup 2 --data sample_small.txt   
tokenizers: text
systems:    iresearch
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/sample_small.txt

--- text ---
  BenchmarkIresearch/Text ...  4.033s mean  (10 runs, 1,000 lines)

───────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
───────────────────────────────────────────────────────────────────────────────────────────────
name                           mean         p50         p95         p99        p100       tok/s
───────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkIresearch/Text      4.033s      4.032s      4.080s      4.080s      4.080s       1.59M
───────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Text  SINGLE  iresearch=-274087441542650178
```
