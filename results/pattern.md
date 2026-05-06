# Unicode words 

```
 make bench-pattern DATA=sample.txt PATTERN_REGEX='[\p{L}\p{M}\p{Nd}]+'
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench pattern --systems all --count 10 --warmup 2 --data sample.txt     --regex-pattern "[\p{L}\p{M}\p{Nd}]+"
tokenizers: pattern
systems:    lucene, tantivy, serenedb
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/sample.txt

--- pattern ---
  BenchmarkLucene/Pattern ...  3.863s mean  p50=3.860s  95% CI [3.836s, 3.892s]  99% CI [3.828s, 3.903s]  (10 runs, 10,000 lines)
  BenchmarkTantivy/Pattern ...  2.408s mean  p50=2.408s  95% CI [2.405s, 2.412s]  99% CI [2.404s, 2.413s]  (10 runs, 10,000 lines)
  BenchmarkSerenedb/Pattern ...  3.503s mean  p50=3.500s  95% CI [3.497s, 3.510s]  99% CI [3.495s, 3.512s]  (10 runs, 10,000 lines)

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                           mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkLucene/Pattern      3.863s    3.860s    3.957s    3.957s    3.957s     3.836s..3.892s         3.828s..3.903s        8.04M
BenchmarkTantivy/Pattern     2.408s    2.408s    2.421s    2.421s    2.421s     2.405s..2.412s         2.404s..2.413s       12.89M
BenchmarkSerenedb/Pattern    3.503s    3.500s    3.525s    3.525s    3.525s     3.497s..3.510s         3.495s..3.512s        8.86M
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pattern  OK  lucene=1145527231713813367  serenedb=1145527231713813367  tantivy=1145527231713813367
```

# ASCII words

```
❯ make bench-pattern DATA=sample.txt PATTERN_REGEX='[A-Za-z]+'
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench pattern --systems all --count 10 --warmup 2 --data sample.txt     --regex-pattern "[A-Za-z]+"
tokenizers: pattern
systems:    lucene, tantivy, serenedb
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/sample.txt

--- pattern ---
  BenchmarkLucene/Pattern ...  2.127s mean  p50=2.131s  95% CI [2.110s, 2.144s]  99% CI [2.105s, 2.149s]  (10 runs, 10,000 lines)
  BenchmarkTantivy/Pattern ...  2.334s mean  p50=2.335s  95% CI [2.329s, 2.339s]  99% CI [2.327s, 2.340s]  (10 runs, 10,000 lines)
  BenchmarkSerenedb/Pattern ...  3.255s mean  p50=3.250s  95% CI [3.248s, 3.263s]  99% CI [3.246s, 3.266s]  (10 runs, 10,000 lines)

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                           mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkLucene/Pattern      2.127s    2.131s    2.180s    2.180s    2.180s     2.110s..2.144s         2.105s..2.149s       14.14M
BenchmarkTantivy/Pattern     2.334s    2.335s    2.346s    2.346s    2.346s     2.329s..2.339s         2.327s..2.340s       12.89M
BenchmarkSerenedb/Pattern    3.255s    3.250s    3.286s    3.286s    3.286s     3.248s..3.263s         3.246s..3.266s        9.24M
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pattern  OK  lucene=6213023852931653588  serenedb=6213023852931653588  tantivy=6213023852931653588
```

# URL extraction

```

```

# Alternation

```
❯ make bench-pattern DATA=sample.txt PATTERN_REGEX='(cat|dog|mouse|elephant|tiger|lion)'
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench pattern --systems all --count 10 --warmup 2 --data sample.txt     --regex-pattern "(cat|dog|mouse|elephant|tiger|lion)"
tokenizers: pattern
systems:    lucene, tantivy, serenedb
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/sample.txt

--- pattern ---
  BenchmarkLucene/Pattern ...  7.508s mean  p50=7.506s  95% CI [7.493s, 7.527s]  99% CI [7.489s, 7.533s]  (10 runs, 10,000 lines)
  BenchmarkTantivy/Pattern ...  44.435ms mean  p50=44.416ms  95% CI [43.282ms, 45.616ms]  99% CI [42.939ms, 45.855ms]  (10 runs, 10,000 lines)
  BenchmarkSerenedb/Pattern ...  279.879ms mean  p50=262.191ms  95% CI [260.957ms, 303.810ms]  99% CI [259.231ms, 311.555ms]  (10 runs, 10,000 lines)

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                           mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkLucene/Pattern      7.508s    7.506s    7.565s    7.565s    7.565s     7.493s..7.527s         7.489s..7.533s       14.79K
BenchmarkTantivy/Pattern   44.435ms  44.416ms  47.569ms  47.569ms  47.569ms   43.282ms..45.616ms     42.939ms..45.855ms      2.50M
BenchmarkSerenedb/Pattern 279.879ms 262.191ms 360.468ms 360.468ms 360.468ms  260.957ms..303.810ms   259.231ms..311.555ms   396.79K
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pattern  OK  lucene=960112847218191264  serenedb=960112847218191264  tantivy=960112847218191264
```

# Logs

```
❯ make bench-pattern DATA=data/openstack_normal1.log PATTERN_REGEX='\"(\w+)\s+([^\"]+)\s+HTTP/[0-9.]+\"\s+status:\s*(404)'
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench pattern --systems all --count 10 --warmup 2 --data data/openstack_normal1.log      --regex-pattern '\"(\w+)\s+([^\"]+)\s+HTTP/[0-9.]+\"\s+status:\s*(404)'
tokenizers: pattern
systems:    lucene, tantivy, serenedb
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/data/openstack_normal1.log

--- pattern ---
  BenchmarkLucene/Pattern ...  202.391ms mean  p50=206.741ms  95% CI [195.986ms, 208.823ms]  99% CI [194.081ms, 210.453ms]  (10 runs, 52,312 lines)
  BenchmarkTantivy/Pattern ...  7.802ms mean  p50=7.793ms  95% CI [7.699ms, 7.924ms]  99% CI [7.671ms, 7.962ms]  (10 runs, 52,312 lines)
  BenchmarkSerenedb/Pattern ...  9.208ms mean  p50=8.939ms  95% CI [8.493ms, 10.066ms]  99% CI [8.332ms, 10.356ms]  (10 runs, 52,312 lines)

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                           mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkLucene/Pattern   202.391ms 206.741ms 216.265ms 216.265ms 216.265ms  195.986ms..208.823ms   194.081ms..210.453ms     5.30K
BenchmarkTantivy/Pattern    7.802ms   7.793ms   8.238ms   8.238ms   8.238ms    7.699ms..7.924ms       7.671ms..7.962ms     137.39K
BenchmarkSerenedb/Pattern   9.208ms   8.939ms  12.156ms  12.156ms  12.156ms   8.493ms..10.066ms      8.332ms..10.356ms     116.43K
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pattern  OK  lucene=-2759798521077754872  serenedb=-2759798521077754872  tantivy=-2759798521077754872
```

```
❯ make bench-pattern DATA=data/openstack_normal2.log PATTERN_REGEX='\"(\w+)\s+([^\"]+)\s+HTTP/[0-9.]+\"\s+status:\s*(404)'
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench pattern --systems all --count 10 --warmup 2 --data data/openstack_normal2.log      --regex-pattern '\"(\w+)\s+([^\"]+)\s+HTTP/[0-9.]+\"\s+status:\s*(404)'
tokenizers: pattern
systems:    lucene, tantivy, serenedb
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/data/openstack_normal2.log

--- pattern ---
  BenchmarkLucene/Pattern ...  409.210ms mean  p50=455.574ms  95% CI [345.932ms, 474.140ms]  99% CI [328.498ms, 493.956ms]  (10 runs, 137,074 lines)
  BenchmarkTantivy/Pattern ...  14.232ms mean  p50=14.246ms  95% CI [14.189ms, 14.274ms]  99% CI [14.178ms, 14.287ms]  (10 runs, 137,074 lines)
  BenchmarkSerenedb/Pattern ...  17.027ms mean  p50=16.951ms  95% CI [16.873ms, 17.181ms]  99% CI [16.839ms, 17.232ms]  (10 runs, 137,074 lines)

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                           mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkLucene/Pattern   409.210ms 455.574ms 529.939ms 529.939ms 529.939ms  345.932ms..474.140ms   328.498ms..493.956ms     6.18K
BenchmarkTantivy/Pattern   14.232ms  14.246ms  14.351ms  14.351ms  14.351ms   14.189ms..14.274ms     14.178ms..14.287ms    177.63K
BenchmarkSerenedb/Pattern  17.027ms  16.951ms  17.352ms  17.352ms  17.352ms   16.873ms..17.181ms     16.839ms..17.232ms    148.47K
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pattern  OK  lucene=-6529721797986903200  serenedb=-6529721797986903200  tantivy=-6529721797986903200
```

```
❯ make bench-pattern DATA=data/emails-slim.ndjson PATTERN_REGEX='\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z'
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench pattern --systems all --count 10 --warmup 2 --data data/emails-slim.ndjson      --regex-pattern '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z'
tokenizers: pattern
systems:    lucene, tantivy, serenedb
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/data/emails-slim.ndjson

--- pattern ---
  BenchmarkLucene/Pattern ...  7.412s mean  p50=7.333s  95% CI [7.319s, 7.518s]  99% CI [7.296s, 7.552s]  (10 runs, 1,783,792 lines)
  BenchmarkTantivy/Pattern ...  327.151ms mean  p50=321.443ms  95% CI [317.735ms, 340.570ms]  99% CI [315.974ms, 346.376ms]  (10 runs, 1,783,792 lines)
  BenchmarkSerenedb/Pattern ...  1.484s mean  p50=1.487s  95% CI [1.477s, 1.491s]  99% CI [1.474s, 1.494s]  (10 runs, 1,783,792 lines)

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                           mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkLucene/Pattern      7.412s    7.333s    7.702s    7.702s    7.702s     7.319s..7.518s         7.296s..7.552s      239.98K
BenchmarkTantivy/Pattern  327.151ms 321.443ms 383.726ms 383.726ms 383.726ms  317.735ms..340.570ms   315.974ms..346.376ms     5.44M
BenchmarkSerenedb/Pattern    1.484s    1.487s    1.505s    1.505s    1.505s     1.477s..1.491s         1.474s..1.494s        1.20M
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pattern  OK  lucene=-2398094469988587416  serenedb=-2398094469988587416  tantivy=-2398094469988587416
```

```
❯ make bench-pattern DATA=data/emails-slim100000.ndjson PATTERN_REGEX='[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' SYSTEMS=tantivy,serenedb,lucene
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench pattern --systems tantivy,serenedb,lucene --count 10 --warmup 2 --data data/emails-slim100000.ndjson      --regex-pattern '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
tokenizers: pattern
systems:    tantivy, serenedb, lucene
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/data/emails-slim100000.ndjson

--- pattern ---
  BenchmarkTantivy/Pattern ...  5.280ms mean  p50=5.296ms  95% CI [5.244ms, 5.317ms]  99% CI [5.231ms, 5.326ms]  (10 runs, 10,000 lines)
  BenchmarkSerenedb/Pattern ...  16.130ms mean  p50=15.108ms  95% CI [14.711ms, 17.554ms]  99% CI [14.425ms, 18.011ms]  (10 runs, 10,000 lines)
  BenchmarkLucene/Pattern ...  398.648ms mean  p50=398.788ms  95% CI [394.577ms, 402.794ms]  99% CI [393.571ms, 404.308ms]  (10 runs, 10,000 lines)

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                           mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkTantivy/Pattern    5.280ms   5.296ms   5.367ms   5.367ms   5.367ms    5.244ms..5.317ms       5.231ms..5.326ms       7.63M
BenchmarkSerenedb/Pattern  16.130ms  15.108ms  18.944ms  18.944ms  18.944ms   14.711ms..17.554ms     14.425ms..18.011ms      2.50M
BenchmarkLucene/Pattern   398.648ms 398.788ms 408.528ms 408.528ms 408.528ms  394.577ms..402.794ms   393.571ms..404.308ms   101.12K
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pattern  OK  lucene=-3827470838621939998  serenedb=-3827470838621939998  tantivy=-3827470838621939998
```

```
❯ make bench-pattern DATA=data/emails-slim100000.ndjson PATTERN_REGEX='"([^"\\]|\\.)*"' SYSTEMS=tantivy,serenedb,lucene
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench pattern --systems tantivy,serenedb,lucene --count 10 --warmup 2 --data data/emails-slim100000.ndjson      --regex-pattern '"([^"\\]|\\.)*"'
tokenizers: pattern
systems:    tantivy, serenedb, lucene
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/data/emails-slim100000.ndjson

--- pattern ---
  BenchmarkTantivy/Pattern ...  38.014ms mean  p50=37.765ms  95% CI [37.404ms, 38.746ms]  99% CI [37.240ms, 38.945ms]  (10 runs, 10,000 lines)
  BenchmarkSerenedb/Pattern ...  52.855ms mean  p50=53.494ms  95% CI [51.584ms, 54.075ms]  99% CI [51.221ms, 54.446ms]  (10 runs, 10,000 lines)
  BenchmarkLucene/Pattern ...  139.514ms mean  p50=139.838ms  95% CI [134.366ms, 144.755ms]  99% CI [133.076ms, 146.279ms]  (10 runs, 10,000 lines)

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                           mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkTantivy/Pattern   38.014ms  37.765ms  40.322ms  40.322ms  40.322ms   37.404ms..38.746ms     37.240ms..38.945ms      7.49M
BenchmarkSerenedb/Pattern  52.855ms  53.494ms  56.202ms  56.202ms  56.202ms   51.584ms..54.075ms     51.221ms..54.446ms      5.39M
BenchmarkLucene/Pattern   139.514ms 139.838ms 153.481ms 153.481ms 153.481ms  134.366ms..144.755ms   133.076ms..146.279ms     2.04M
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pattern  OK  lucene=-6314459940781782201  serenedb=-6314459940781782201  tantivy=-6314459940781782201
```