# Unicode words 

```
❯ make bench-pattern DATA=sample.txt PATTERN_REGEX='[\p{L}\p{M}\p{Nd}]+'
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench pattern --systems all --count 10 --warmup 2 --data /home/romanp/benchmark-tokenizers/sample.txt  --regex-pattern '[\p{L}\p{M}\p{Nd}]+'
tokenizers: pattern
systems:    lucene, tantivy, serenedb
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/sample.txt

--- pattern ---
  BenchmarkLucene/Pattern ...  3.811s mean  p50=3.822s  95% CI [3.769s, 3.853s]  99% CI [3.760s, 3.871s]  (10 runs, 10,000 lines)
  BenchmarkTantivy/Pattern ...  2.392s mean  p50=2.393s  95% CI [2.390s, 2.393s]  99% CI [2.389s, 2.394s]  (10 runs, 10,000 lines)
  BenchmarkSerenedb/Pattern ...  2.135s mean  p50=2.135s  95% CI [2.133s, 2.136s]  99% CI [2.133s, 2.137s]  (10 runs, 10,000 lines)

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                           mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkLucene/Pattern      3.811s    3.822s    3.956s    3.956s    3.956s     3.769s..3.853s         3.760s..3.871s        8.15M
BenchmarkTantivy/Pattern     2.392s    2.393s    2.396s    2.396s    2.396s     2.390s..2.393s         2.389s..2.394s       12.98M
BenchmarkSerenedb/Pattern    2.135s    2.135s    2.139s    2.139s    2.139s     2.133s..2.136s         2.133s..2.137s       14.54M
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pattern  OK  lucene=1145527231713813367  serenedb=1145527231713813367  tantivy=1145527231713813367
```

# ASCII words

```
❯ make bench-pattern DATA=sample.txt PATTERN_REGEX='[A-Za-z]+'
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench pattern --systems all --count 10 --warmup 2 --data /home/romanp/benchmark-tokenizers/sample.txt  --regex-pattern '[A-Za-z]+'
tokenizers: pattern
systems:    lucene, tantivy, serenedb
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/sample.txt

--- pattern ---
  BenchmarkLucene/Pattern ...  2.198s mean  p50=2.191s  95% CI [2.184s, 2.213s]  99% CI [2.180s, 2.217s]  (10 runs, 10,000 lines)
  BenchmarkTantivy/Pattern ...  2.341s mean  p50=2.336s  95% CI [2.334s, 2.349s]  99% CI [2.332s, 2.351s]  (10 runs, 10,000 lines)
  BenchmarkSerenedb/Pattern ...  2.053s mean  p50=2.053s  95% CI [2.051s, 2.056s]  99% CI [2.051s, 2.057s]  (10 runs, 10,000 lines)

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                           mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkLucene/Pattern      2.198s    2.191s    2.240s    2.240s    2.240s     2.184s..2.213s         2.180s..2.217s       13.69M
BenchmarkTantivy/Pattern     2.341s    2.336s    2.363s    2.363s    2.363s     2.334s..2.349s         2.332s..2.351s       12.85M
BenchmarkSerenedb/Pattern    2.053s    2.053s    2.060s    2.060s    2.060s     2.051s..2.056s         2.051s..2.057s       14.65M
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pattern  OK  lucene=6213023852931653588  serenedb=6213023852931653588  tantivy=6213023852931653588
```

# Alternation

```
❯ make bench-pattern DATA=sample.txt PATTERN_REGEX='(cat|dog|mouse|elephant|tiger|lion)'
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench pattern --systems all --count 10 --warmup 2 --data /home/romanp/benchmark-tokenizers/sample.txt  --regex-pattern '(cat|dog|mouse|elephant|tiger|lion)'
tokenizers: pattern
systems:    lucene, tantivy, serenedb
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/sample.txt

--- pattern ---
  BenchmarkLucene/Pattern ...  7.590s mean  p50=7.584s  95% CI [7.518s, 7.665s]  99% CI [7.497s, 7.692s]  (10 runs, 10,000 lines)
  BenchmarkTantivy/Pattern ...  32.610ms mean  p50=32.623ms  95% CI [32.586ms, 32.641ms]  99% CI [32.581ms, 32.651ms]  (10 runs, 10,000 lines)
  BenchmarkSerenedb/Pattern ...  24.829ms mean  p50=24.738ms  95% CI [24.667ms, 25.102ms]  99% CI [24.653ms, 25.227ms]  (10 runs, 10,000 lines)

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                           mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkLucene/Pattern      7.590s    7.584s    7.771s    7.771s    7.771s     7.518s..7.665s         7.497s..7.692s       14.63K
BenchmarkTantivy/Pattern   32.610ms  32.623ms  32.715ms  32.715ms  32.715ms   32.586ms..32.641ms     32.581ms..32.651ms      3.41M
BenchmarkSerenedb/Pattern  24.829ms  24.738ms  25.974ms  25.974ms  25.974ms   24.667ms..25.102ms     24.653ms..25.227ms      4.47M
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pattern  OK  lucene=960112847218191264  serenedb=960112847218191264  tantivy=960112847218191264
```

```
❯ make bench-pattern DATA=sample.txt PATTERN_REGEX='(philosophical|alongside|stretches|acknowledging|turn|moral|become|style|santa|freedom|properties|syria|replicate|road|sentiments|generate|pursue|returned|communist|that|remains|important|orientation|turned|latest|assailants|repressed|particularly|grew|creative|enlightened|china|collectivised|schools|bring|militancy|relationships|likely|eurocentric|creativity|methods|small|bombs|been|potential|women|technology|planning|works|founders|government|fascists|fascist|belief|evolving|enlightenment|eliminate|science|world|syndicates|europe|haven|figure|diverse|minarchy|consumption|replacing|open|general|social|industrialisation|syndicate|tenets|usages|william|elite|defined|coercion|distinct|goldman|mean|consciousness|jura|friendly|relationship|dominating|responsible|plays|could|constitutes|humans|differ|east|relations|international|engaged|heterosexism|carry|available|historical)' SYSTEMS=tantivy,serenedb
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench pattern --systems tantivy,serenedb --count 10 --warmup 2 --data /home/romanp/benchmark-tokenizers/sample.txt  --regex-pattern '(philosophical|alongside|stretches|acknowledging|turn|moral|become|style|santa|freedom|properties|syria|replicate|road|sentiments|generate|pursue|returned|communist|that|remains|important|orientation|turned|latest|assailants|repressed|particularly|grew|creative|enlightened|china|collectivised|schools|bring|militancy|relationships|likely|eurocentric|creativity|methods|small|bombs|been|potential|women|technology|planning|works|founders|government|fascists|fascist|belief|evolving|enlightenment|eliminate|science|world|syndicates|europe|haven|figure|diverse|minarchy|consumption|replacing|open|general|social|industrialisation|syndicate|tenets|usages|william|elite|defined|coercion|distinct|goldman|mean|consciousness|jura|friendly|relationship|dominating|responsible|plays|could|constitutes|humans|differ|east|relations|international|engaged|heterosexism|carry|available|historical)'
tokenizers: pattern
systems:    tantivy, serenedb
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/sample.txt

--- pattern ---
  BenchmarkTantivy/Pattern ...  419.530ms mean  p50=424.842ms  95% CI [413.509ms, 425.725ms]  99% CI [412.065ms, 427.882ms]  (10 runs, 10,000 lines)
  BenchmarkSerenedb/Pattern ...  317.147ms mean  p50=317.321ms  95% CI [316.591ms, 317.738ms]  99% CI [316.442ms, 317.926ms]  (10 runs, 10,000 lines)

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                           mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkTantivy/Pattern  419.530ms 424.842ms 437.707ms 437.707ms 437.707ms  413.509ms..425.725ms   412.065ms..427.882ms     1.58M
BenchmarkSerenedb/Pattern 317.147ms 317.321ms 318.744ms 318.744ms 318.744ms  316.591ms..317.738ms   316.442ms..317.926ms     2.09M
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pattern  OK  serenedb=-7689585518870136302  tantivy=-7689585518870136302
```

```
❯ make bench-pattern DATA=sample.txt PATTERN_REGEX='(cat|carrot)'
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench pattern --systems all --count 10 --warmup 2 --data /home/romanp/benchmark-tokenizers/sample.txt  --regex-pattern '(cat|carrot)'
tokenizers: pattern
systems:    lucene, tantivy, serenedb
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/sample.txt

--- pattern ---
  BenchmarkLucene/Pattern ...  2.706s mean  p50=2.710s  95% CI [2.694s, 2.718s]  99% CI [2.691s, 2.721s]  (10 runs, 10,000 lines)
  BenchmarkTantivy/Pattern ...  27.379ms mean  p50=27.070ms  95% CI [26.864ms, 28.023ms]  99% CI [26.789ms, 28.151ms]  (10 runs, 10,000 lines)
  BenchmarkSerenedb/Pattern ...  25.888ms mean  p50=26.089ms  95% CI [25.596ms, 26.141ms]  99% CI [25.535ms, 26.194ms]  (10 runs, 10,000 lines)

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                           mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkLucene/Pattern      2.706s    2.710s    2.736s    2.736s    2.736s     2.694s..2.718s         2.691s..2.721s       31.02K
BenchmarkTantivy/Pattern   27.379ms  27.070ms  29.348ms  29.348ms  29.348ms   26.864ms..28.023ms     26.789ms..28.151ms      3.07M
BenchmarkSerenedb/Pattern  25.888ms  26.089ms  26.431ms  26.431ms  26.431ms   25.596ms..26.141ms     25.535ms..26.194ms      3.24M
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pattern  OK  lucene=5020413419399913304  serenedb=5020413419399913304  tantivy=5020413419399913304
```

# Logs

```
❯ make bench-pattern DATA=data/openstack.log PATTERN_REGEX='\"(\w+)\s+([^\"]+)\s+HTTP/[0-9.]+\"\s+status:\s*(404)'
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench pattern --systems all --count 10 --warmup 2 --data /home/romanp/benchmark-tokenizers/data/openstack.log  --regex-pattern '\"(\w+)\s+([^\"]+)\s+HTTP/[0-9.]+\"\s+status:\s*(404)'
tokenizers: pattern
systems:    lucene, tantivy, serenedb
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/data/openstack.log

--- pattern ---
  BenchmarkLucene/Pattern ...  415.444ms mean  p50=408.586ms  95% CI [407.477ms, 425.575ms]  99% CI [406.042ms, 428.984ms]  (10 runs, 189,386 lines)
  BenchmarkTantivy/Pattern ...  19.637ms mean  p50=19.622ms  95% CI [19.610ms, 19.664ms]  99% CI [19.603ms, 19.671ms]  (10 runs, 189,386 lines)
  BenchmarkSerenedb/Pattern ...  22.228ms mean  p50=23.906ms  95% CI [20.410ms, 23.901ms]  99% CI [19.937ms, 23.917ms]  (10 runs, 189,386 lines)

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                           mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkLucene/Pattern   415.444ms 408.586ms 454.184ms 454.184ms 454.184ms  407.477ms..425.575ms   406.042ms..428.984ms     8.67K
BenchmarkTantivy/Pattern   19.637ms  19.622ms  19.712ms  19.712ms  19.712ms   19.610ms..19.664ms     19.603ms..19.671ms    183.33K
BenchmarkSerenedb/Pattern  22.228ms  23.906ms  23.945ms  23.945ms  23.945ms   20.410ms..23.901ms     19.937ms..23.917ms    161.96K
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pattern  OK  lucene=-1098032139727540376  serenedb=-1098032139727540376  tantivy=-1098032139727540376
```

```
❯ make bench-pattern DATA=data/emails-slim.ndjson PATTERN_REGEX='\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z'
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench pattern --systems all --count 10 --warmup 2 --data /home/romanp/benchmark-tokenizers/data/emails-slim.ndjson  --regex-pattern '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z'
tokenizers: pattern
systems:    lucene, tantivy, serenedb
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/data/emails-slim.ndjson

--- pattern ---
  BenchmarkLucene/Pattern ...  7.255s mean  p50=7.239s  95% CI [7.210s, 7.311s]  99% CI [7.199s, 7.333s]  (10 runs, 1,783,792 lines)
  BenchmarkTantivy/Pattern ...  310.094ms mean  p50=310.011ms  95% CI [309.937ms, 310.280ms]  99% CI [309.898ms, 310.346ms]  (10 runs, 1,783,792 lines)
  BenchmarkSerenedb/Pattern ...  1.318s mean  p50=1.319s  95% CI [1.316s, 1.319s]  99% CI [1.315s, 1.320s]  (10 runs, 1,783,792 lines)

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                           mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkLucene/Pattern      7.255s    7.239s    7.465s    7.465s    7.465s     7.210s..7.311s         7.199s..7.333s      245.19K
BenchmarkTantivy/Pattern  310.094ms 310.011ms 310.638ms 310.638ms 310.638ms  309.937ms..310.280ms   309.898ms..310.346ms     5.74M
BenchmarkSerenedb/Pattern    1.318s    1.319s    1.323s    1.323s    1.323s     1.316s..1.319s         1.315s..1.320s        1.35M
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pattern  OK  lucene=-2398094469988587416  serenedb=-2398094469988587416  tantivy=-2398094469988587416
```

```
❯ make bench-pattern DATA=data/emails-slim.ndjson PATTERN_REGEX='1\d{3}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z'
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench pattern --systems all --count 10 --warmup 2 --data /home/romanp/benchmark-tokenizers/data/emails-slim.ndjson  --regex-pattern '1\d{3}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z'
tokenizers: pattern
systems:    lucene, tantivy, serenedb
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/data/emails-slim.ndjson

--- pattern ---
  BenchmarkLucene/Pattern ...  5.471s mean  p50=5.465s  95% CI [5.442s, 5.511s]  99% CI [5.437s, 5.527s]  (10 runs, 1,783,792 lines)
  BenchmarkTantivy/Pattern ...  261.777ms mean  p50=261.545ms  95% CI [261.027ms, 262.590ms]  99% CI [260.829ms, 262.845ms]  (10 runs, 1,783,792 lines)
  BenchmarkSerenedb/Pattern ...  243.690ms mean  p50=244.436ms  95% CI [242.008ms, 245.314ms]  99% CI [241.464ms, 245.812ms]  (10 runs, 1,783,792 lines)

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                           mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkLucene/Pattern      5.471s    5.465s    5.622s    5.622s    5.622s     5.442s..5.511s         5.437s..5.527s          400
BenchmarkTantivy/Pattern  261.777ms 261.545ms 263.894ms 263.894ms 263.894ms  261.027ms..262.590ms   260.829ms..262.845ms     8.36K
BenchmarkSerenedb/Pattern 243.690ms 244.436ms 248.422ms 248.422ms 248.422ms  242.008ms..245.314ms   241.464ms..245.812ms     8.98K
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pattern  OK  lucene=6346580772906205022  serenedb=6346580772906205022  tantivy=6346580772906205022
```

```
❯ make bench-pattern DATA=data/emails-slim100000.ndjson PATTERN_REGEX='[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench pattern --systems all --count 10 --warmup 2 --data /home/romanp/benchmark-tokenizers/data/emails-slim100000.ndjson  --regex-pattern '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
tokenizers: pattern
systems:    lucene, tantivy, serenedb
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/data/emails-slim100000.ndjson

--- pattern ---
  BenchmarkLucene/Pattern ...  397.077ms mean  p50=400.116ms  95% CI [394.002ms, 400.079ms]  99% CI [393.156ms, 401.080ms]  (10 runs, 10,000 lines)
  BenchmarkTantivy/Pattern ...  5.209ms mean  p50=5.212ms  95% CI [5.201ms, 5.216ms]  99% CI [5.199ms, 5.219ms]  (10 runs, 10,000 lines)
  BenchmarkSerenedb/Pattern ...  12.061ms mean  p50=12.036ms  95% CI [12.018ms, 12.113ms]  99% CI [12.006ms, 12.130ms]  (10 runs, 10,000 lines)

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                           mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkLucene/Pattern   397.077ms 400.116ms 404.122ms 404.122ms 404.122ms  394.002ms..400.079ms   393.156ms..401.080ms   101.52K
BenchmarkTantivy/Pattern    5.209ms   5.212ms   5.227ms   5.227ms   5.227ms    5.201ms..5.216ms       5.199ms..5.219ms       7.74M
BenchmarkSerenedb/Pattern  12.061ms  12.036ms  12.194ms  12.194ms  12.194ms   12.018ms..12.113ms     12.006ms..12.130ms      3.34M
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pattern  OK  lucene=-3827470838621939998  serenedb=-3827470838621939998  tantivy=-3827470838621939998
```

```
❯  make bench-pattern DATA=data/emails-slim100000.ndjson PATTERN_REGEX='"([^"\\]|\\.)*"'
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench pattern --systems all --count 10 --warmup 2 --data /home/romanp/benchmark-tokenizers/data/emails-slim100000.ndjson  --regex-pattern '"([^"\\]|\\.)*"'
tokenizers: pattern
systems:    lucene, tantivy, serenedb
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/data/emails-slim100000.ndjson

--- pattern ---
  BenchmarkLucene/Pattern ...  139.807ms mean  p50=134.919ms  95% CI [134.446ms, 145.865ms]  99% CI [133.274ms, 147.617ms]  (10 runs, 10,000 lines)
  BenchmarkTantivy/Pattern ...  36.945ms mean  p50=36.889ms  95% CI [36.870ms, 37.053ms]  99% CI [36.859ms, 37.095ms]  (10 runs, 10,000 lines)
  BenchmarkSerenedb/Pattern ...  37.844ms mean  p50=37.832ms  95% CI [37.818ms, 37.880ms]  99% CI [37.813ms, 37.893ms]  (10 runs, 10,000 lines)

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                           mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkLucene/Pattern   139.807ms 134.919ms 153.668ms 153.668ms 153.668ms  134.446ms..145.865ms   133.274ms..147.617ms     2.04M
BenchmarkTantivy/Pattern   36.945ms  36.889ms  37.386ms  37.386ms  37.386ms   36.870ms..37.053ms     36.859ms..37.095ms      7.71M
BenchmarkSerenedb/Pattern  37.844ms  37.832ms  37.973ms  37.973ms  37.973ms   37.818ms..37.880ms     37.813ms..37.893ms      7.53M
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pattern  OK  lucene=-6314459940781782201  serenedb=-6314459940781782201  tantivy=-6314459940781782201
```

# Groups 

```
❯ make bench-pattern DATA=data/emails-slim100000.ndjson PATTERN_REGEX='([A-Za-z0-9._%+-]+)@([A-Za-z0-9.-]+\.[A-Za-z]{2,})' SYSTEMS=lucene,serenedb GROUP=-1
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench pattern --systems lucene,serenedb --count 10 --warmup 2 --data /home/romanp/benchmark-tokenizers/data/emails-slim100000.ndjson  --regex-pattern '([A-Za-z0-9._%+-]+)@([A-Za-z0-9.-]+\.[A-Za-z]{2,})' --group -1
tokenizers: pattern
systems:    lucene, serenedb
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/data/emails-slim100000.ndjson

--- pattern ---
  BenchmarkLucene/Pattern ...  534.457ms mean  p50=534.139ms  95% CI [529.466ms, 539.710ms]  99% CI [528.145ms, 541.635ms]  (10 runs, 10,000 lines)
  BenchmarkSerenedb/Pattern ...  37.241ms mean  p50=37.250ms  95% CI [37.094ms, 37.387ms]  99% CI [37.041ms, 37.428ms]  (10 runs, 10,000 lines)

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                           mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkLucene/Pattern   534.457ms 534.139ms 549.743ms 549.743ms 549.743ms  529.466ms..539.710ms   528.145ms..541.635ms    94.13K
BenchmarkSerenedb/Pattern  37.241ms  37.250ms  37.590ms  37.590ms  37.590ms   37.094ms..37.387ms     37.041ms..37.428ms      1.35M
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pattern  OK  lucene=-8158773321456728999  serenedb=-8158773321456728999
```

```
❯ make bench-pattern DATA=data/emails-slim100000.ndjson PATTERN_REGEX='([A-Za-z0-9._%+-]+)@([A-Za-z0-9.-]+\.[A-Za-z]{2,})' SYSTEMS=lucene,serenedb GROUP=1
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench pattern --systems lucene,serenedb --count 10 --warmup 2 --data /home/romanp/benchmark-tokenizers/data/emails-slim100000.ndjson  --regex-pattern '([A-Za-z0-9._%+-]+)@([A-Za-z0-9.-]+\.[A-Za-z]{2,})' --group 1
tokenizers: pattern
systems:    lucene, serenedb
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/data/emails-slim100000.ndjson

--- pattern ---
  BenchmarkLucene/Pattern ...  524.673ms mean  p50=526.651ms  95% CI [522.136ms, 527.309ms]  99% CI [521.403ms, 527.908ms]  (10 runs, 10,000 lines)
  BenchmarkSerenedb/Pattern ...  33.689ms mean  p50=33.748ms  95% CI [33.601ms, 33.777ms]  99% CI [33.581ms, 33.806ms]  (10 runs, 10,000 lines)

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                           mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkLucene/Pattern   524.673ms 526.651ms 529.922ms 529.922ms 529.922ms  522.136ms..527.309ms   521.403ms..527.908ms    76.83K
BenchmarkSerenedb/Pattern  33.689ms  33.748ms  33.879ms  33.879ms  33.879ms   33.601ms..33.777ms     33.581ms..33.806ms      1.20M
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pattern  OK  lucene=863121639432609151  serenedb=863121639432609151
```

```
❯ make bench-pattern DATA=data/emails-slim100000.ndjson PATTERN_REGEX='([A-Za-z0-9._%+-]+)@([A-Za-z0-9.-]+\.[A-Za-z]{2,})' SYSTEMS=lucene,serenedb GROUP=2
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench pattern --systems lucene,serenedb --count 10 --warmup 2 --data /home/romanp/benchmark-tokenizers/data/emails-slim100000.ndjson  --regex-pattern '([A-Za-z0-9._%+-]+)@([A-Za-z0-9.-]+\.[A-Za-z]{2,})' --group 2
tokenizers: pattern
systems:    lucene, serenedb
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/data/emails-slim100000.ndjson

--- pattern ---
  BenchmarkLucene/Pattern ...  516.239ms mean  p50=516.361ms  95% CI [513.165ms, 519.931ms]  99% CI [512.277ms, 521.153ms]  (10 runs, 10,000 lines)
  BenchmarkSerenedb/Pattern ...  33.602ms mean  p50=33.507ms  95% CI [33.467ms, 33.747ms]  99% CI [33.434ms, 33.797ms]  (10 runs, 10,000 lines)

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                           mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkLucene/Pattern   516.239ms 516.361ms 529.207ms 529.207ms 529.207ms  513.165ms..519.931ms   512.277ms..521.153ms    78.09K
BenchmarkSerenedb/Pattern  33.602ms  33.507ms  34.005ms  34.005ms  34.005ms   33.467ms..33.747ms     33.434ms..33.797ms      1.20M
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pattern  OK  lucene=-7670440117002695631  serenedb=-7670440117002695631
```