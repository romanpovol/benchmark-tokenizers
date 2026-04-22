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
  BenchmarkLucene/Path ...  111.197ms mean  p50=105.982ms  95% CI [104.933ms, 119.518ms]  99% CI [104.399ms, 122.428ms]  (10 runs, 100,000 lines)
  BenchmarkTantivy/Path ...  57.670ms mean  p50=57.639ms  95% CI [57.464ms, 57.910ms]  99% CI [57.420ms, 57.988ms]  (10 runs, 100,000 lines)
  BenchmarkIresearch/Path ...  22.224ms mean  p50=22.229ms  95% CI [22.184ms, 22.265ms]  99% CI [22.174ms, 22.275ms]  (10 runs, 100,000 lines)

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                         mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkLucene/Path    111.197ms 105.982ms 139.957ms 139.957ms 139.957ms  104.933ms..119.518ms   104.399ms..122.428ms     5.77M
BenchmarkTantivy/Path    57.670ms  57.639ms  58.501ms  58.501ms  58.501ms   57.464ms..57.910ms     57.420ms..57.988ms     11.13M
BenchmarkIresearch/Path  22.224ms  22.229ms  22.315ms  22.315ms  22.315ms   22.184ms..22.265ms     22.174ms..22.275ms     28.87M
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

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
  BenchmarkLucene/Path ...  118.222ms mean  p50=111.889ms  95% CI [111.827ms, 126.702ms]  99% CI [110.417ms, 129.688ms]  (10 runs, 100,000 lines)
  BenchmarkIresearch/Path ...  24.799ms mean  p50=24.786ms  95% CI [24.677ms, 24.929ms]  99% CI [24.643ms, 24.968ms]  (10 runs, 100,000 lines)

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                         mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkLucene/Path    118.222ms 111.889ms 146.696ms 146.696ms 146.696ms  111.827ms..126.702ms   110.417ms..129.688ms     6.27M
BenchmarkIresearch/Path  24.799ms  24.786ms  25.189ms  25.189ms  25.189ms   24.677ms..24.929ms     24.643ms..24.968ms     29.91M
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

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
  BenchmarkIresearch/Pipeline ...  4.601s mean  p50=4.588s  95% CI [4.579s, 4.635s]  99% CI [4.576s, 4.650s]  (10 runs, 1,000 lines)

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                             mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkIresearch/Pipeline    4.601s    4.588s    4.738s    4.738s    4.738s     4.579s..4.635s         4.576s..4.650s        1.40M
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

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
  BenchmarkIresearch/Text ...  4.103s mean  p50=4.084s  95% CI [4.073s, 4.138s]  99% CI [4.066s, 4.150s]  (10 runs, 1,000 lines)

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                         mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkIresearch/Text    4.103s    4.084s    4.211s    4.211s    4.211s     4.073s..4.138s         4.066s..4.150s        1.57M
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

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
  BenchmarkIresearch/Pipeline ...  3.673s mean  p50=3.672s  95% CI [3.667s, 3.679s]  99% CI [3.666s, 3.681s]  (10 runs, 1,000 lines)

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                             mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkIresearch/Pipeline    3.673s    3.672s    3.692s    3.692s    3.692s     3.667s..3.679s         3.666s..3.681s        1.75M
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pipeline  SINGLE  iresearch=-274087441542650178
```
