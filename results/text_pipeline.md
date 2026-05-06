# SereneDB: `text` vs `pipeline`

Пары с одинаковой сеткой stem x lower x edge

| Вариант (одинаковые флаги) | text mean | text 99% CI | pipeline mean | pipeline 99% CI |
|----------------------------|-----------|-------------|---------------|-----------------|
| полный | 4.409s | 4.371s..4.451s | 4.065s | 4.051s..4.084s |
| no-edge | 4.262s | 4.230s..4.289s | 3.995s | 3.980s..4.009s |
| no-lower | 2.008s | 1.980s..2.065s | 1.308s | 1.293s..1.337s |
| no-lower-no-edge | 1.872s | 1.862s..1.885s | 1.223s | 1.208s..1.235s |
| no-stem | 3.189s | 3.179s..3.201s | 3.727s | 3.699s..3.751s |
| no-stem-no-edge | 3.042s | 3.030s..3.052s | 3.599s | 3.589s..3.609s |
| no-stem-no-lower | 894.366ms | 890.780ms..898.140ms | 890.511ms | 888.659ms..892.514ms |
| no-stem-no-lower-no-edge | 768.522ms | 766.711ms..770.853ms | 811.099ms | 808.457ms..813.608ms |

<details>
<summary>Полный лог</summary>

```
❯ make bench-text-pipeline SYSTEMS=serenedb DATA=sample_small.txt
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench '^(text|pipeline)' --systems serenedb --count 10 --warmup 2 --data sample_small.txt      --regex-pattern '(\w+)\s+([^"]+)\s+HTTP/[0-9.]+"\s+status:\s*(404)'
tokenizers: text, text-no-edge, text-no-lower, text-no-lower-no-edge, text-no-stem, text-no-stem-no-edge, text-no-stem-no-lower, text-no-stem-no-lower-no-edge, pipeline, pipeline-no-edge, pipeline-no-lower, pipeline-no-lower-no-edge, pipeline-no-stem, pipeline-no-stem-no-edge, pipeline-no-stem-no-lower, pipeline-no-stem-no-lower-no-edge
systems:    serenedb
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/sample_small.txt

--- text ---
  BenchmarkSerenedb/Text ...  4.409s mean  p50=4.390s  95% CI [4.379s, 4.441s]  99% CI [4.371s, 4.451s]  (10 runs, 1,000 lines)

--- text-no-edge ---
  BenchmarkSerenedb/Text-no-edge ...  4.262s mean  p50=4.284s  95% CI [4.237s, 4.283s]  99% CI [4.230s, 4.289s]  (10 runs, 1,000 lines)

--- text-no-lower ---
  BenchmarkSerenedb/Text-no-lower ...  2.008s mean  p50=1.989s  95% CI [1.983s, 2.048s]  99% CI [1.980s, 2.065s]  (10 runs, 1,000 lines)

--- text-no-lower-no-edge ---
  BenchmarkSerenedb/Text-no-lower-no-edge ...  1.872s mean  p50=1.870s  95% CI [1.864s, 1.881s]  99% CI [1.862s, 1.885s]  (10 runs, 1,000 lines)

--- text-no-stem ---
  BenchmarkSerenedb/Text-no-stem ...  3.189s mean  p50=3.186s  95% CI [3.181s, 3.197s]  99% CI [3.179s, 3.201s]  (10 runs, 1,000 lines)

--- text-no-stem-no-edge ---
  BenchmarkSerenedb/Text-no-stem-no-edge ...  3.042s mean  p50=3.047s  95% CI [3.033s, 3.050s]  99% CI [3.030s, 3.052s]  (10 runs, 1,000 lines)

--- text-no-stem-no-lower ---
  BenchmarkSerenedb/Text-no-stem-no-lower ...  894.366ms mean  p50=894.271ms  95% CI [891.644ms, 897.275ms]  99% CI [890.780ms, 898.140ms]  (10 runs, 1,000 lines)

--- text-no-stem-no-lower-no-edge ---
  BenchmarkSerenedb/Text-no-stem-no-lower-no-edge ...  768.522ms mean  p50=768.974ms  95% CI [767.039ms, 770.245ms]  99% CI [766.711ms, 770.853ms]  (10 runs, 1,000 lines)

--- pipeline ---
  BenchmarkSerenedb/Pipeline ...  4.065s mean  p50=4.061s  95% CI [4.054s, 4.079s]  99% CI [4.051s, 4.084s]  (10 runs, 1,000 lines)

--- pipeline-no-edge ---
  BenchmarkSerenedb/Pipeline-no-edge ...  3.995s mean  p50=4.001s  95% CI [3.984s, 4.005s]  99% CI [3.980s, 4.009s]  (10 runs, 1,000 lines)

--- pipeline-no-lower ---
  BenchmarkSerenedb/Pipeline-no-lower ...  1.308s mean  p50=1.300s  95% CI [1.295s, 1.328s]  99% CI [1.293s, 1.337s]  (10 runs, 1,000 lines)

--- pipeline-no-lower-no-edge ---
  BenchmarkSerenedb/Pipeline-no-lower-no-edge ...  1.223s mean  p50=1.225s  95% CI [1.212s, 1.232s]  99% CI [1.208s, 1.235s]  (10 runs, 1,000 lines)

--- pipeline-no-stem ---
  BenchmarkSerenedb/Pipeline-no-stem ...  3.727s mean  p50=3.738s  95% CI [3.706s, 3.746s]  99% CI [3.699s, 3.751s]  (10 runs, 1,000 lines)

--- pipeline-no-stem-no-edge ---
  BenchmarkSerenedb/Pipeline-no-stem-no-edge ...  3.599s mean  p50=3.599s  95% CI [3.591s, 3.607s]  99% CI [3.589s, 3.609s]  (10 runs, 1,000 lines)

--- pipeline-no-stem-no-lower ---
  BenchmarkSerenedb/Pipeline-no-stem-no-lower ...  890.511ms mean  p50=890.399ms  95% CI [889.040ms, 892.045ms]  99% CI [888.659ms, 892.514ms]  (10 runs, 1,000 lines)

--- pipeline-no-stem-no-lower-no-edge ---
  BenchmarkSerenedb/Pipeline-no-stem-no-lower-no-edge ...  811.099ms mean  p50=812.613ms  95% CI [809.042ms, 813.074ms]  99% CI [808.457ms, 813.608ms]  (10 runs, 1,000 lines)

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                                                     mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkSerenedb/Text                                 4.409s    4.390s    4.474s    4.474s    4.474s     4.379s..4.441s         4.371s..4.451s        1.46M
BenchmarkSerenedb/Text-no-edge                         4.262s    4.284s    4.301s    4.301s    4.301s     4.237s..4.283s         4.230s..4.289s      511.88K
BenchmarkSerenedb/Text-no-lower                        2.008s    1.989s    2.170s    2.170s    2.170s     1.983s..2.048s         1.980s..2.065s        3.26M
BenchmarkSerenedb/Text-no-lower-no-edge                1.872s    1.870s    1.902s    1.902s    1.902s     1.864s..1.881s         1.862s..1.885s        1.19M
BenchmarkSerenedb/Text-no-stem                         3.189s    3.186s    3.211s    3.211s    3.211s     3.181s..3.197s         3.179s..3.201s        2.02M
BenchmarkSerenedb/Text-no-stem-no-edge                 3.042s    3.047s    3.060s    3.060s    3.060s     3.033s..3.050s         3.030s..3.052s      717.21K
BenchmarkSerenedb/Text-no-stem-no-lower             894.366ms 894.271ms 901.666ms 901.666ms 901.666ms  891.644ms..897.275ms   890.780ms..898.140ms     7.33M
BenchmarkSerenedb/Text-no-stem-no-lower-no-edge     768.522ms 768.974ms 774.289ms 774.289ms 774.289ms  767.039ms..770.245ms   766.711ms..770.853ms     2.90M
BenchmarkSerenedb/Pipeline                             4.065s    4.061s    4.110s    4.110s    4.110s     4.054s..4.079s         4.051s..4.084s        1.58M
BenchmarkSerenedb/Pipeline-no-edge                     3.995s    4.001s    4.024s    4.024s    4.024s     3.984s..4.005s         3.980s..4.009s      546.09K
BenchmarkSerenedb/Pipeline-no-lower                    1.308s    1.300s    1.387s    1.387s    1.387s     1.295s..1.328s         1.293s..1.337s        5.01M
BenchmarkSerenedb/Pipeline-no-lower-no-edge            1.223s    1.225s    1.250s    1.250s    1.250s     1.212s..1.232s         1.208s..1.235s        1.83M
BenchmarkSerenedb/Pipeline-no-stem                     3.727s    3.738s    3.767s    3.767s    3.767s     3.706s..3.746s         3.699s..3.751s        1.73M
BenchmarkSerenedb/Pipeline-no-stem-no-edge             3.599s    3.599s    3.621s    3.621s    3.621s     3.591s..3.607s         3.589s..3.609s      606.22K
BenchmarkSerenedb/Pipeline-no-stem-no-lower         890.511ms 890.399ms 894.471ms 894.471ms 894.471ms  889.040ms..892.045ms   888.659ms..892.514ms     7.37M
BenchmarkSerenedb/Pipeline-no-stem-no-lower-no-edge 811.099ms 812.613ms 815.606ms 815.606ms 815.606ms  809.042ms..813.074ms   808.457ms..813.608ms     2.75M
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pipeline  SINGLE  serenedb=-274087441542650178
  checksum/Pipeline-no-edge  SINGLE  serenedb=-1417360207602844945
  checksum/Pipeline-no-lower  SINGLE  serenedb=9222712700660269680
  checksum/Pipeline-no-lower-no-edge  SINGLE  serenedb=858996794035370824
  checksum/Pipeline-no-stem  SINGLE  serenedb=8586809143420619973
  checksum/Pipeline-no-stem-no-edge  SINGLE  serenedb=1554050099052931300
  checksum/Pipeline-no-stem-no-lower  SINGLE  serenedb=1313773056324225708
  checksum/Pipeline-no-stem-no-lower-no-edge  SINGLE  serenedb=6569443083707496824
  checksum/Text  SINGLE  serenedb=-274087441542650178
  checksum/Text-no-edge  SINGLE  serenedb=-1417360207602844945
  checksum/Text-no-lower  SINGLE  serenedb=9222712700660269680
  checksum/Text-no-lower-no-edge  SINGLE  serenedb=858996794035370824
  checksum/Text-no-stem  SINGLE  serenedb=8586809143420619973
  checksum/Text-no-stem-no-edge  SINGLE  serenedb=1554050099052931300
  checksum/Text-no-stem-no-lower  SINGLE  serenedb=1313773056324225708
  checksum/Text-no-stem-no-lower-no-edge  SINGLE  serenedb=6569443083707496824
```
</details>

---

# `text` vs `pipeline with segmentation` (en_US locale) `data/3200_small.txt` (8 687 строк)

| Вариант (одинаковые флаги) | text mean | text 99% CI | pipeline mean | pipeline 99% CI |
|----------------------------|-----------|-------------|---------------|-----------------|
| полный | 134.021ms | 133.726ms..134.346ms | 108.657ms | 107.102ms..111.385ms |
| no-edge | 131.139ms | 130.718ms..131.596ms | 104.144ms | 103.509ms..104.818ms |
| no-lower | 64.695ms | 63.897ms..66.195ms | 23.284ms | 22.726ms..23.876ms |
| no-lower-no-edge | 60.956ms | 60.396ms..61.593ms | 19.840ms | 19.735ms..19.973ms |
| no-stem | 98.431ms | 97.846ms..98.990ms | 102.679ms | 102.384ms..103.185ms |
| no-stem-no-edge | 94.864ms | 94.233ms..95.592ms | 100.845ms | 99.966ms..102.160ms |
| no-stem-no-lower | 29.380ms | 29.182ms..29.604ms | 19.904ms | 19.801ms..20.008ms |
| no-stem-no-lower-no-edge | 25.562ms | 25.496ms..25.618ms | 17.254ms | 17.169ms..17.359ms |

<details>
<summary>Полный лог</summary>

```
❯ make bench-text-pipeline SYSTEMS=serenedb DATA=data/3200_small.txt
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench '^(text|pipeline)' --systems serenedb --count 10 --warmup 2 --data data/3200_small.txt      --regex-pattern '(\w+)\s+([^"]+)\s+HTTP/[0-9.]+"\s+status:\s*(404)'
tokenizers: text, text-no-edge, text-no-lower, text-no-lower-no-edge, text-no-stem, text-no-stem-no-edge, text-no-stem-no-lower, text-no-stem-no-lower-no-edge, pipeline, pipeline-no-edge, pipeline-no-lower, pipeline-no-lower-no-edge, pipeline-no-stem, pipeline-no-stem-no-edge, pipeline-no-stem-no-lower, pipeline-no-stem-no-lower-no-edge
systems:    serenedb
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/data/3200_small.txt

--- text ---
  BenchmarkSerenedb/Text ...  134.021ms mean  p50=133.966ms  95% CI [133.786ms, 134.279ms]  99% CI [133.726ms, 134.346ms]  (10 runs, 8,687 lines)

--- text-no-edge ---
  BenchmarkSerenedb/Text-no-edge ...  131.139ms mean  p50=130.880ms  95% CI [130.800ms, 131.494ms]  99% CI [130.718ms, 131.596ms]  (10 runs, 8,687 lines)

--- text-no-lower ---
  BenchmarkSerenedb/Text-no-lower ...  64.695ms mean  p50=63.947ms  95% CI [63.920ms, 65.866ms]  99% CI [63.897ms, 66.195ms]  (10 runs, 8,687 lines)

--- text-no-lower-no-edge ---
  BenchmarkSerenedb/Text-no-lower-no-edge ...  60.956ms mean  p50=61.046ms  95% CI [60.500ms, 61.439ms]  99% CI [60.396ms, 61.593ms]  (10 runs, 8,687 lines)

--- text-no-stem ---
  BenchmarkSerenedb/Text-no-stem ...  98.431ms mean  p50=98.447ms  95% CI [97.992ms, 98.858ms]  99% CI [97.846ms, 98.990ms]  (10 runs, 8,687 lines)

--- text-no-stem-no-edge ---
  BenchmarkSerenedb/Text-no-stem-no-edge ...  94.864ms mean  p50=94.886ms  95% CI [94.353ms, 95.406ms]  99% CI [94.233ms, 95.592ms]  (10 runs, 8,687 lines)

--- text-no-stem-no-lower ---
  BenchmarkSerenedb/Text-no-stem-no-lower ...  29.380ms mean  p50=29.360ms  95% CI [29.222ms, 29.544ms]  99% CI [29.182ms, 29.604ms]  (10 runs, 8,687 lines)

--- text-no-stem-no-lower-no-edge ---
  BenchmarkSerenedb/Text-no-stem-no-lower-no-edge ...  25.562ms mean  p50=25.573ms  95% CI [25.513ms, 25.607ms]  99% CI [25.496ms, 25.618ms]  (10 runs, 8,687 lines)

--- pipeline ---
  BenchmarkSerenedb/Pipeline ...  108.657ms mean  p50=107.702ms  95% CI [107.252ms, 110.654ms]  99% CI [107.102ms, 111.385ms]  (10 runs, 8,687 lines)

--- pipeline-no-edge ---
  BenchmarkSerenedb/Pipeline-no-edge ...  104.144ms mean  p50=103.898ms  95% CI [103.654ms, 104.686ms]  99% CI [103.509ms, 104.818ms]  (10 runs, 8,687 lines)

--- pipeline-no-lower ---
  BenchmarkSerenedb/Pipeline-no-lower ...  23.284ms mean  p50=23.320ms  95% CI [22.845ms, 23.750ms]  99% CI [22.726ms, 23.876ms]  (10 runs, 8,687 lines)

--- pipeline-no-lower-no-edge ---
  BenchmarkSerenedb/Pipeline-no-lower-no-edge ...  19.840ms mean  p50=19.793ms  95% CI [19.753ms, 19.942ms]  99% CI [19.735ms, 19.973ms]  (10 runs, 8,687 lines)

--- pipeline-no-stem ---
  BenchmarkSerenedb/Pipeline-no-stem ...  102.679ms mean  p50=102.480ms  95% CI [102.418ms, 103.053ms]  99% CI [102.384ms, 103.185ms]  (10 runs, 8,687 lines)

--- pipeline-no-stem-no-edge ---
  BenchmarkSerenedb/Pipeline-no-stem-no-edge ...  100.845ms mean  p50=100.791ms  95% CI [100.118ms, 101.764ms]  99% CI [99.966ms, 102.160ms]  (10 runs, 8,687 lines)

--- pipeline-no-stem-no-lower ---
  BenchmarkSerenedb/Pipeline-no-stem-no-lower ...  19.904ms mean  p50=19.935ms  95% CI [19.824ms, 19.985ms]  99% CI [19.801ms, 20.008ms]  (10 runs, 8,687 lines)

--- pipeline-no-stem-no-lower-no-edge ---
  BenchmarkSerenedb/Pipeline-no-stem-no-lower-no-edge ...  17.254ms mean  p50=17.233ms  95% CI [17.185ms, 17.332ms]  99% CI [17.169ms, 17.359ms]  (10 runs, 8,687 lines)

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                                                     mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkSerenedb/Text                              134.021ms 133.966ms 134.724ms 134.724ms 134.724ms  133.786ms..134.279ms   133.726ms..134.346ms     1.53M
BenchmarkSerenedb/Text-no-edge                      131.139ms 130.880ms 132.132ms 132.132ms 132.132ms  130.800ms..131.494ms   130.718ms..131.596ms   534.84K
BenchmarkSerenedb/Text-no-lower                      64.695ms  63.947ms  68.822ms  68.822ms  68.822ms   63.920ms..65.866ms     63.897ms..66.195ms      3.26M
BenchmarkSerenedb/Text-no-lower-no-edge              60.956ms  61.046ms  62.435ms  62.435ms  62.435ms   60.500ms..61.439ms     60.396ms..61.593ms      1.19M
BenchmarkSerenedb/Text-no-stem                       98.431ms  98.447ms  99.348ms  99.348ms  99.348ms   97.992ms..98.858ms     97.846ms..98.990ms      2.09M
BenchmarkSerenedb/Text-no-stem-no-edge               94.864ms  94.886ms  96.527ms  96.527ms  96.527ms   94.353ms..95.406ms     94.233ms..95.592ms    739.35K
BenchmarkSerenedb/Text-no-stem-no-lower              29.380ms  29.360ms  29.816ms  29.816ms  29.816ms   29.222ms..29.544ms     29.182ms..29.604ms      7.18M
BenchmarkSerenedb/Text-no-stem-no-lower-no-edge      25.562ms  25.573ms  25.671ms  25.671ms  25.671ms   25.513ms..25.607ms     25.496ms..25.618ms      2.84M
BenchmarkSerenedb/Pipeline                          108.657ms 107.702ms 116.612ms 116.612ms 116.612ms  107.252ms..110.654ms   107.102ms..111.385ms     1.89M
BenchmarkSerenedb/Pipeline-no-edge                  104.144ms 103.898ms 105.584ms 105.584ms 105.584ms  103.654ms..104.686ms   103.509ms..104.818ms   673.47K
BenchmarkSerenedb/Pipeline-no-lower                  23.284ms  23.320ms  24.684ms  24.684ms  24.684ms   22.845ms..23.750ms     22.726ms..23.876ms      9.04M
BenchmarkSerenedb/Pipeline-no-lower-no-edge          19.840ms  19.793ms  20.170ms  20.170ms  20.170ms   19.753ms..19.942ms     19.735ms..19.973ms      3.66M
BenchmarkSerenedb/Pipeline-no-stem                  102.679ms 102.480ms 104.211ms 104.211ms 104.211ms  102.418ms..103.053ms   102.384ms..103.185ms     2.00M
BenchmarkSerenedb/Pipeline-no-stem-no-edge          100.845ms 100.791ms 104.031ms 104.031ms 104.031ms  100.118ms..101.764ms   99.966ms..102.160ms    695.50K
BenchmarkSerenedb/Pipeline-no-stem-no-lower          19.904ms  19.935ms  20.117ms  20.117ms  20.117ms   19.824ms..19.985ms     19.801ms..20.008ms     10.60M
BenchmarkSerenedb/Pipeline-no-stem-no-lower-no-edge  17.254ms  17.233ms  17.510ms  17.510ms  17.510ms   17.185ms..17.332ms     17.169ms..17.359ms      4.20M
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pipeline  SINGLE  serenedb=-4373233049016623111
  checksum/Pipeline-no-edge  SINGLE  serenedb=-718050764594079629
  checksum/Pipeline-no-lower  SINGLE  serenedb=5381102110575537924
  checksum/Pipeline-no-lower-no-edge  SINGLE  serenedb=-7493770933881443262
  checksum/Pipeline-no-stem  SINGLE  serenedb=-8244147419173801149
  checksum/Pipeline-no-stem-no-edge  SINGLE  serenedb=6150305461528611725
  checksum/Pipeline-no-stem-no-lower  SINGLE  serenedb=6607809168995586917
  checksum/Pipeline-no-stem-no-lower-no-edge  SINGLE  serenedb=-126306427893353410
  checksum/Text  SINGLE  serenedb=-4373233049016623111
  checksum/Text-no-edge  SINGLE  serenedb=-718050764594079629
  checksum/Text-no-lower  SINGLE  serenedb=5381102110575537924
  checksum/Text-no-lower-no-edge  SINGLE  serenedb=-7493770933881443262
  checksum/Text-no-stem  SINGLE  serenedb=-8244147419173801149
  checksum/Text-no-stem-no-edge  SINGLE  serenedb=6150305461528611725
  checksum/Text-no-stem-no-lower  SINGLE  serenedb=6607809168995586917
  checksum/Text-no-stem-no-lower-no-edge  SINGLE  serenedb=-126306427893353410
```
</details>

## lower через segmentation + С locale

| Вариант (одинаковые флаги) | text mean | text 99% CI | pipeline mean | pipeline 99% CI |
|----------------------------|-----------|-------------|---------------|-----------------|
| полный | 99.389ms | 98.796ms..100.003ms | 63.361ms | 62.417ms..64.769ms |
| no-edge | 96.110ms | 95.358ms..96.863ms | 63.461ms | 61.170ms..69.530ms |
| no-lower | 29.882ms | 29.448ms..30.340ms | 63.933ms | 63.272ms..64.785ms |
| no-lower-no-edge | 25.985ms | 25.837ms..26.143ms | 61.041ms | 60.538ms..61.627ms |
| no-stem | 98.885ms | 98.387ms..99.564ms | 21.084ms | 20.390ms..22.007ms |
| no-stem-no-edge | 95.580ms | 94.845ms..96.459ms | 19.534ms | 18.343ms..21.315ms |
| no-stem-no-lower | 29.785ms | 29.550ms..30.053ms | 19.596ms | 19.516ms..19.687ms |
| no-stem-no-lower-no-edge | 26.505ms | 26.243ms..26.920ms | 16.466ms | 16.360ms..16.637ms |

<details>
<summary>Полный лог</summary>

```
❯ make bench-text-pipeline SYSTEMS=serenedb DATA=data/3200_small.txt
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench '^(text|pipeline)' --systems serenedb --count 10 --warmup 2 --data data/3200_small.txt      --regex-pattern '(\w+)\s+([^"]+)\s+HTTP/[0-9.]+"\s+status:\s*(404)'
tokenizers: text, text-no-edge, text-no-lower, text-no-lower-no-edge, text-no-stem, text-no-stem-no-edge, text-no-stem-no-lower, text-no-stem-no-lower-no-edge, pipeline, pipeline-no-edge, pipeline-no-lower, pipeline-no-lower-no-edge, pipeline-no-stem, pipeline-no-stem-no-edge, pipeline-no-stem-no-lower, pipeline-no-stem-no-lower-no-edge
systems:    serenedb
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/data/3200_small.txt

--- text ---
  BenchmarkSerenedb/Text ...  99.389ms mean  p50=99.578ms  95% CI [98.947ms, 99.842ms]  99% CI [98.796ms, 100.003ms]  (10 runs, 8,687 lines)

--- text-no-edge ---
  BenchmarkSerenedb/Text-no-edge ...  96.110ms mean  p50=96.434ms  95% CI [95.506ms, 96.706ms]  99% CI [95.358ms, 96.863ms]  (10 runs, 8,687 lines)

--- text-no-lower ---
  BenchmarkSerenedb/Text-no-lower ...  29.882ms mean  p50=30.123ms  95% CI [29.530ms, 30.236ms]  99% CI [29.448ms, 30.340ms]  (10 runs, 8,687 lines)

--- text-no-lower-no-edge ---
  BenchmarkSerenedb/Text-no-lower-no-edge ...  25.985ms mean  p50=25.966ms  95% CI [25.869ms, 26.104ms]  99% CI [25.837ms, 26.143ms]  (10 runs, 8,687 lines)

--- text-no-stem ---
  BenchmarkSerenedb/Text-no-stem ...  98.885ms mean  p50=98.669ms  95% CI [98.476ms, 99.394ms]  99% CI [98.387ms, 99.564ms]  (10 runs, 8,687 lines)

--- text-no-stem-no-edge ---
  BenchmarkSerenedb/Text-no-stem-no-edge ...  95.580ms mean  p50=95.312ms  95% CI [95.007ms, 96.213ms]  99% CI [94.845ms, 96.459ms]  (10 runs, 8,687 lines)

--- text-no-stem-no-lower ---
  BenchmarkSerenedb/Text-no-stem-no-lower ...  29.785ms mean  p50=29.826ms  95% CI [29.592ms, 29.993ms]  99% CI [29.550ms, 30.053ms]  (10 runs, 8,687 lines)

--- text-no-stem-no-lower-no-edge ---
  BenchmarkSerenedb/Text-no-stem-no-lower-no-edge ...  26.505ms mean  p50=26.422ms  95% CI [26.283ms, 26.801ms]  99% CI [26.243ms, 26.920ms]  (10 runs, 8,687 lines)

--- pipeline ---
  BenchmarkSerenedb/Pipeline ...  63.361ms mean  p50=63.212ms  95% CI [62.554ms, 64.379ms]  99% CI [62.417ms, 64.769ms]  (10 runs, 8,687 lines)

--- pipeline-no-edge ---
  BenchmarkSerenedb/Pipeline-no-edge ...  63.461ms mean  p50=61.444ms  95% CI [61.246ms, 67.593ms]  99% CI [61.170ms, 69.530ms]  (10 runs, 8,687 lines)

--- pipeline-no-lower ---
  BenchmarkSerenedb/Pipeline-no-lower ...  63.933ms mean  p50=63.985ms  95% CI [63.411ms, 64.562ms]  99% CI [63.272ms, 64.785ms]  (10 runs, 8,687 lines)

--- pipeline-no-lower-no-edge ---
  BenchmarkSerenedb/Pipeline-no-lower-no-edge ...  61.041ms mean  p50=61.115ms  95% CI [60.645ms, 61.480ms]  99% CI [60.538ms, 61.627ms]  (10 runs, 8,687 lines)

--- pipeline-no-stem ---
  BenchmarkSerenedb/Pipeline-no-stem ...  21.084ms mean  p50=20.562ms  95% CI [20.490ms, 21.795ms]  99% CI [20.390ms, 22.007ms]  (10 runs, 8,687 lines)

--- pipeline-no-stem-no-edge ---
  BenchmarkSerenedb/Pipeline-no-stem-no-edge ...  19.534ms mean  p50=18.452ms  95% CI [18.501ms, 20.873ms]  99% CI [18.343ms, 21.315ms]  (10 runs, 8,687 lines)

--- pipeline-no-stem-no-lower ---
  BenchmarkSerenedb/Pipeline-no-stem-no-lower ...  19.596ms mean  p50=19.559ms  95% CI [19.535ms, 19.665ms]  99% CI [19.516ms, 19.687ms]  (10 runs, 8,687 lines)

--- pipeline-no-stem-no-lower-no-edge ---
  BenchmarkSerenedb/Pipeline-no-stem-no-lower-no-edge ...  16.466ms mean  p50=16.380ms  95% CI [16.372ms, 16.590ms]  99% CI [16.360ms, 16.637ms]  (10 runs, 8,687 lines)

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                                                     mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkSerenedb/Text                               99.389ms  99.578ms 100.507ms 100.507ms 100.507ms   98.947ms..99.842ms    98.796ms..100.003ms      2.06M
BenchmarkSerenedb/Text-no-edge                       96.110ms  96.434ms  97.462ms  97.462ms  97.462ms   95.506ms..96.706ms     95.358ms..96.863ms    729.77K
BenchmarkSerenedb/Text-no-lower                      29.882ms  30.123ms  30.819ms  30.819ms  30.819ms   29.530ms..30.236ms     29.448ms..30.340ms      7.06M
BenchmarkSerenedb/Text-no-lower-no-edge              25.985ms  25.966ms  26.337ms  26.337ms  26.337ms   25.869ms..26.104ms     25.837ms..26.143ms      2.79M
BenchmarkSerenedb/Text-no-stem                       98.885ms  98.669ms 100.580ms 100.580ms 100.580ms   98.476ms..99.394ms     98.387ms..99.564ms      2.08M
BenchmarkSerenedb/Text-no-stem-no-edge               95.580ms  95.312ms  97.168ms  97.168ms  97.168ms   95.007ms..96.213ms     94.845ms..96.459ms    733.82K
BenchmarkSerenedb/Text-no-stem-no-lower              29.785ms  29.826ms  30.346ms  30.346ms  30.346ms   29.592ms..29.993ms     29.550ms..30.053ms      7.08M
BenchmarkSerenedb/Text-no-stem-no-lower-no-edge      26.505ms  26.422ms  27.645ms  27.645ms  27.645ms   26.283ms..26.801ms     26.243ms..26.920ms      2.74M
BenchmarkSerenedb/Pipeline                           63.361ms  63.212ms  67.408ms  67.408ms  67.408ms   62.554ms..64.379ms     62.417ms..64.769ms      3.24M
BenchmarkSerenedb/Pipeline-no-edge                   63.461ms  61.444ms  81.561ms  81.561ms  81.561ms   61.246ms..67.593ms     61.170ms..69.530ms      1.11M
BenchmarkSerenedb/Pipeline-no-lower                  63.933ms  63.985ms  66.316ms  66.316ms  66.316ms   63.411ms..64.562ms     63.272ms..64.785ms      3.30M
BenchmarkSerenedb/Pipeline-no-lower-no-edge          61.041ms  61.115ms  62.504ms  62.504ms  62.504ms   60.645ms..61.480ms     60.538ms..61.627ms      1.19M
BenchmarkSerenedb/Pipeline-no-stem                   21.084ms  20.562ms  23.253ms  23.253ms  23.253ms   20.490ms..21.795ms     20.390ms..22.007ms      9.73M
BenchmarkSerenedb/Pipeline-no-stem-no-edge           19.534ms  18.452ms  24.503ms  24.503ms  24.503ms   18.501ms..20.873ms     18.343ms..21.315ms      3.59M
BenchmarkSerenedb/Pipeline-no-stem-no-lower          19.596ms  19.559ms  19.798ms  19.798ms  19.798ms   19.535ms..19.665ms     19.516ms..19.687ms     10.77M
BenchmarkSerenedb/Pipeline-no-stem-no-lower-no-edge  16.466ms  16.380ms  16.955ms  16.955ms  16.955ms   16.372ms..16.590ms     16.360ms..16.637ms      4.41M
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pipeline  SINGLE  serenedb=-8244147419173801149
  checksum/Pipeline-no-edge  SINGLE  serenedb=6150305461528611725
  checksum/Pipeline-no-lower  SINGLE  serenedb=6607809168995586917
  checksum/Pipeline-no-lower-no-edge  SINGLE  serenedb=-126306427893353410
  checksum/Pipeline-no-stem  SINGLE  serenedb=-8244147419173801149
  checksum/Pipeline-no-stem-no-edge  SINGLE  serenedb=6150305461528611725
  checksum/Pipeline-no-stem-no-lower  SINGLE  serenedb=6607809168995586917
  checksum/Pipeline-no-stem-no-lower-no-edge  SINGLE  serenedb=-126306427893353410
  checksum/Text  SINGLE  serenedb=-8244147419173801149
  checksum/Text-no-edge  SINGLE  serenedb=6150305461528611725
  checksum/Text-no-lower  SINGLE  serenedb=6607809168995586917
  checksum/Text-no-lower-no-edge  SINGLE  serenedb=-126306427893353410
  checksum/Text-no-stem  SINGLE  serenedb=-8244147419173801149
  checksum/Text-no-stem-no-edge  SINGLE  serenedb=6150305461528611725
  checksum/Text-no-stem-no-lower  SINGLE  serenedb=6607809168995586917
  checksum/Text-no-stem-no-lower-no-edge  SINGLE  serenedb=-126306427893353410
```
</details>

## `text` × `pipeline` with `text` (locale C), `data/3200_small.txt` (8 687 строк)

| Вариант (одинаковые флаги) | text mean | text 99% CI | pipeline mean | pipeline 99% CI |
|----------------------------|-----------|-------------|---------------|-----------------|
| полный | 99.859ms | 99.529ms..100.331ms | 162.478ms | 161.115ms..164.058ms |
| no-edge | 96.017ms | 95.184ms..97.761ms | 159.496ms | 158.463ms..160.823ms |
| no-lower | 29.889ms | 29.770ms..30.020ms | 77.251ms | 76.277ms..78.501ms |
| no-lower-no-edge | 26.717ms | 26.607ms..26.840ms | 75.045ms | 74.759ms..75.366ms |
| no-stem | 101.467ms | 99.257ms..106.330ms | 116.470ms | 116.111ms..116.865ms |
| no-stem-no-edge | 96.313ms | 95.792ms..96.821ms | 112.812ms | 112.258ms..113.398ms |
| no-stem-no-lower | 30.016ms | 29.923ms..30.173ms | 31.494ms | 31.166ms..32.216ms |
| no-stem-no-lower-no-edge | 27.545ms | 27.073ms..28.157ms | 28.575ms | 28.482ms..28.689ms |

<details>
<summary>Полный лог</summary>

```
❯ make bench-text-pipeline SYSTEMS=serenedb DATA=data/3200_small.txt
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench '^(text|pipeline)' --systems serenedb --count 10 --warmup 2 --data data/3200_small.txt      --regex-pattern '(\w+)\s+([^"]+)\s+HTTP/[0-9.]+"\s+status:\s*(404)'
tokenizers: text, text-no-edge, text-no-lower, text-no-lower-no-edge, text-no-stem, text-no-stem-no-edge, text-no-stem-no-lower, text-no-stem-no-lower-no-edge, pipeline, pipeline-no-edge, pipeline-no-lower, pipeline-no-lower-no-edge, pipeline-no-stem, pipeline-no-stem-no-edge, pipeline-no-stem-no-lower, pipeline-no-stem-no-lower-no-edge
systems:    serenedb
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/data/3200_small.txt

--- text ---
  BenchmarkSerenedb/Text ...  99.859ms mean  p50=99.701ms  95% CI [99.578ms, 100.199ms]  99% CI [99.529ms, 100.331ms]  (10 runs, 8,687 lines)

--- text-no-edge ---
  BenchmarkSerenedb/Text-no-edge ...  96.017ms mean  p50=95.434ms  95% CI [95.267ms, 97.256ms]  99% CI [95.184ms, 97.761ms]  (10 runs, 8,687 lines)

--- text-no-lower ---
  BenchmarkSerenedb/Text-no-lower ...  29.889ms mean  p50=29.920ms  95% CI [29.796ms, 29.988ms]  99% CI [29.770ms, 30.020ms]  (10 runs, 8,687 lines)

--- text-no-lower-no-edge ---
  BenchmarkSerenedb/Text-no-lower-no-edge ...  26.717ms mean  p50=26.709ms  95% CI [26.631ms, 26.811ms]  99% CI [26.607ms, 26.840ms]  (10 runs, 8,687 lines)

--- text-no-stem ---
  BenchmarkSerenedb/Text-no-stem ...  101.467ms mean  p50=99.634ms  95% CI [99.427ms, 104.853ms]  99% CI [99.257ms, 106.330ms]  (10 runs, 8,687 lines)

--- text-no-stem-no-edge ---
  BenchmarkSerenedb/Text-no-stem-no-edge ...  96.313ms mean  p50=96.402ms  95% CI [95.899ms, 96.700ms]  99% CI [95.792ms, 96.821ms]  (10 runs, 8,687 lines)

--- text-no-stem-no-lower ---
  BenchmarkSerenedb/Text-no-stem-no-lower ...  30.016ms mean  p50=29.976ms  95% CI [29.938ms, 30.125ms]  99% CI [29.923ms, 30.173ms]  (10 runs, 8,687 lines)

--- text-no-stem-no-lower-no-edge ---
  BenchmarkSerenedb/Text-no-stem-no-lower-no-edge ...  27.545ms mean  p50=27.290ms  95% CI [27.160ms, 28.003ms]  99% CI [27.073ms, 28.157ms]  (10 runs, 8,687 lines)

--- pipeline ---
  BenchmarkSerenedb/Pipeline ...  162.478ms mean  p50=161.444ms  95% CI [161.381ms, 163.696ms]  99% CI [161.115ms, 164.058ms]  (10 runs, 8,687 lines)

--- pipeline-no-edge ---
  BenchmarkSerenedb/Pipeline-no-edge ...  159.496ms mean  p50=159.559ms  95% CI [158.673ms, 160.476ms]  99% CI [158.463ms, 160.823ms]  (10 runs, 8,687 lines)

--- pipeline-no-lower ---
  BenchmarkSerenedb/Pipeline-no-lower ...  77.251ms mean  p50=76.636ms  95% CI [76.456ms, 78.170ms]  99% CI [76.277ms, 78.501ms]  (10 runs, 8,687 lines)

--- pipeline-no-lower-no-edge ---
  BenchmarkSerenedb/Pipeline-no-lower-no-edge ...  75.045ms mean  p50=75.184ms  95% CI [74.815ms, 75.280ms]  99% CI [74.759ms, 75.366ms]  (10 runs, 8,687 lines)

--- pipeline-no-stem ---
  BenchmarkSerenedb/Pipeline-no-stem ...  116.470ms mean  p50=116.640ms  95% CI [116.193ms, 116.765ms]  99% CI [116.111ms, 116.865ms]  (10 runs, 8,687 lines)

--- pipeline-no-stem-no-edge ---
  BenchmarkSerenedb/Pipeline-no-stem-no-edge ...  112.812ms mean  p50=112.693ms  95% CI [112.374ms, 113.263ms]  99% CI [112.258ms, 113.398ms]  (10 runs, 8,687 lines)

--- pipeline-no-stem-no-lower ---
  BenchmarkSerenedb/Pipeline-no-stem-no-lower ...  31.494ms mean  p50=31.277ms  95% CI [31.192ms, 31.996ms]  99% CI [31.166ms, 32.216ms]  (10 runs, 8,687 lines)

--- pipeline-no-stem-no-lower-no-edge ---
  BenchmarkSerenedb/Pipeline-no-stem-no-lower-no-edge ...  28.575ms mean  p50=28.557ms  95% CI [28.500ms, 28.662ms]  99% CI [28.482ms, 28.689ms]  (10 runs, 8,687 lines)

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                                                     mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkSerenedb/Text                               99.859ms  99.701ms 101.057ms 101.057ms 101.057ms  99.578ms..100.199ms    99.529ms..100.331ms      2.06M
BenchmarkSerenedb/Text-no-edge                       96.017ms  95.434ms 101.023ms 101.023ms 101.023ms   95.267ms..97.256ms     95.184ms..97.761ms    730.47K
BenchmarkSerenedb/Text-no-lower                      29.889ms  29.920ms  30.209ms  30.209ms  30.209ms   29.796ms..29.988ms     29.770ms..30.020ms      7.06M
BenchmarkSerenedb/Text-no-lower-no-edge              26.717ms  26.709ms  26.966ms  26.966ms  26.966ms   26.631ms..26.811ms     26.607ms..26.840ms      2.72M
BenchmarkSerenedb/Text-no-stem                      101.467ms  99.634ms 116.008ms 116.008ms 116.008ms  99.427ms..104.853ms    99.257ms..106.330ms      2.02M
BenchmarkSerenedb/Text-no-stem-no-edge               96.313ms  96.402ms  97.396ms  97.396ms  97.396ms   95.899ms..96.700ms     95.792ms..96.821ms    728.23K
BenchmarkSerenedb/Text-no-stem-no-lower              30.016ms  29.976ms  30.444ms  30.444ms  30.444ms   29.938ms..30.125ms     29.923ms..30.173ms      7.03M
BenchmarkSerenedb/Text-no-stem-no-lower-no-edge      27.545ms  27.290ms  28.885ms  28.885ms  28.885ms   27.160ms..28.003ms     27.073ms..28.157ms      2.63M
BenchmarkSerenedb/Pipeline                          162.478ms 161.444ms 165.738ms 165.738ms 165.738ms  161.381ms..163.696ms   161.115ms..164.058ms     1.26M
BenchmarkSerenedb/Pipeline-no-edge                  159.496ms 159.559ms 163.208ms 163.208ms 163.208ms  158.673ms..160.476ms   158.463ms..160.823ms   439.75K
BenchmarkSerenedb/Pipeline-no-lower                  77.251ms  76.636ms  80.273ms  80.273ms  80.273ms   76.456ms..78.170ms     76.277ms..78.501ms      2.73M
BenchmarkSerenedb/Pipeline-no-lower-no-edge          75.045ms  75.184ms  75.731ms  75.731ms  75.731ms   74.815ms..75.280ms     74.759ms..75.366ms    966.66K
BenchmarkSerenedb/Pipeline-no-stem                  116.470ms 116.640ms 117.494ms 117.494ms 117.494ms  116.193ms..116.765ms   116.111ms..116.865ms     1.76M
BenchmarkSerenedb/Pipeline-no-stem-no-edge          112.812ms 112.693ms 114.061ms 114.061ms 114.061ms  112.374ms..113.263ms   112.258ms..113.398ms   621.72K
BenchmarkSerenedb/Pipeline-no-stem-no-lower          31.494ms  31.277ms  33.663ms  33.663ms  33.663ms   31.192ms..31.996ms     31.166ms..32.216ms      6.70M
BenchmarkSerenedb/Pipeline-no-stem-no-lower-no-edge  28.575ms  28.557ms  28.827ms  28.827ms  28.827ms   28.500ms..28.662ms     28.482ms..28.689ms      2.54M
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pipeline  SINGLE  serenedb=-8244147419173801149
  checksum/Pipeline-no-edge  SINGLE  serenedb=6150305461528611725
  checksum/Pipeline-no-lower  SINGLE  serenedb=6607809168995586917
  checksum/Pipeline-no-lower-no-edge  SINGLE  serenedb=-126306427893353410
  checksum/Pipeline-no-stem  SINGLE  serenedb=-8244147419173801149
  checksum/Pipeline-no-stem-no-edge  SINGLE  serenedb=6150305461528611725
  checksum/Pipeline-no-stem-no-lower  SINGLE  serenedb=6607809168995586917
  checksum/Pipeline-no-stem-no-lower-no-edge  SINGLE  serenedb=-126306427893353410
  checksum/Text  SINGLE  serenedb=-8244147419173801149
  checksum/Text-no-edge  SINGLE  serenedb=6150305461528611725
  checksum/Text-no-lower  SINGLE  serenedb=6607809168995586917
  checksum/Text-no-lower-no-edge  SINGLE  serenedb=-126306427893353410
  checksum/Text-no-stem  SINGLE  serenedb=-8244147419173801149
  checksum/Text-no-stem-no-edge  SINGLE  serenedb=6150305461528611725
  checksum/Text-no-stem-no-lower  SINGLE  serenedb=6607809168995586917
  checksum/Text-no-stem-no-lower-no-edge  SINGLE  serenedb=-126306427893353410
```
</details>

---

# `text` vs `pipeline with segmentation` (en_US locale) `data/3200_mid.txt` (84 314 строк)

| Вариант (одинаковые флаги) | text mean | text 99% CI | pipeline mean | pipeline 99% CI |
|----------------------------|-----------|-------------|---------------|-----------------|
| полный | 1.292s | 1.276s..1.312s | 1.076s | 1.071s..1.080s |
| no-edge | 1.241s | 1.233s..1.251s | 1.051s | 1.045s..1.057s |
| no-lower | 604.808ms | 602.585ms..607.666ms | 263.753ms | 262.241ms..265.390ms |
| no-lower-no-edge | 568.188ms | 566.600ms..571.311ms | 238.704ms | 237.101ms..240.484ms |
| no-stem | 929.610ms | 925.656ms..934.009ms | 978.948ms | 975.899ms..982.250ms |
| no-stem-no-edge | 889.565ms | 885.812ms..894.157ms | 949.993ms | 948.541ms..951.837ms |
| no-stem-no-lower | 279.173ms | 278.087ms..280.685ms | 188.729ms | 188.138ms..189.425ms |
| no-stem-no-lower-no-edge | 244.249ms | 242.674ms..246.550ms | 164.881ms | 163.135ms..167.406ms |

<details>
<summary>Полный лог</summary>

```
❯ make bench-text-pipeline SYSTEMS=serenedb DATA=data/3200_mid.txt
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench '^(text|pipeline)' --systems serenedb --count 10 --warmup 2 --data data/3200_mid.txt      --regex-pattern '(\w+)\s+([^"]+)\s+HTTP/[0-9.]+"\s+status:\s*(404)'
tokenizers: text, text-no-edge, text-no-lower, text-no-lower-no-edge, text-no-stem, text-no-stem-no-edge, text-no-stem-no-lower, text-no-stem-no-lower-no-edge, pipeline, pipeline-no-edge, pipeline-no-lower, pipeline-no-lower-no-edge, pipeline-no-stem, pipeline-no-stem-no-edge, pipeline-no-stem-no-lower, pipeline-no-stem-no-lower-no-edge
systems:    serenedb
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/data/3200_mid.txt

--- text ---
  BenchmarkSerenedb/Text ...  1.292s mean  p50=1.287s  95% CI [1.279s, 1.307s]  99% CI [1.276s, 1.312s]  (10 runs, 84,314 lines)

--- text-no-edge ---
  BenchmarkSerenedb/Text-no-edge ...  1.241s mean  p50=1.239s  95% CI [1.235s, 1.248s]  99% CI [1.233s, 1.251s]  (10 runs, 84,314 lines)

--- text-no-lower ---
  BenchmarkSerenedb/Text-no-lower ...  604.808ms mean  p50=605.285ms  95% CI [603.026ms, 606.831ms]  99% CI [602.585ms, 607.666ms]  (10 runs, 84,314 lines)

--- text-no-lower-no-edge ---
  BenchmarkSerenedb/Text-no-lower-no-edge ...  568.188ms mean  p50=567.305ms  95% CI [566.776ms, 570.365ms]  99% CI [566.600ms, 571.311ms]  (10 runs, 84,314 lines)

--- text-no-stem ---
  BenchmarkSerenedb/Text-no-stem ...  929.610ms mean  p50=929.722ms  95% CI [926.587ms, 932.878ms]  99% CI [925.656ms, 934.009ms]  (10 runs, 84,314 lines)

--- text-no-stem-no-edge ---
  BenchmarkSerenedb/Text-no-stem-no-edge ...  889.565ms mean  p50=888.595ms  95% CI [886.482ms, 893.048ms]  99% CI [885.812ms, 894.157ms]  (10 runs, 84,314 lines)

--- text-no-stem-no-lower ---
  BenchmarkSerenedb/Text-no-stem-no-lower ...  279.173ms mean  p50=278.899ms  95% CI [278.292ms, 280.298ms]  99% CI [278.087ms, 280.685ms]  (10 runs, 84,314 lines)

--- text-no-stem-no-lower-no-edge ---
  BenchmarkSerenedb/Text-no-stem-no-lower-no-edge ...  244.249ms mean  p50=243.369ms  95% CI [242.895ms, 245.987ms]  99% CI [242.674ms, 246.550ms]  (10 runs, 84,314 lines)

--- pipeline ---
  BenchmarkSerenedb/Pipeline ...  1.076s mean  p50=1.078s  95% CI [1.072s, 1.079s]  99% CI [1.071s, 1.080s]  (10 runs, 84,314 lines)

--- pipeline-no-edge ---
  BenchmarkSerenedb/Pipeline-no-edge ...  1.051s mean  p50=1.052s  95% CI [1.046s, 1.055s]  99% CI [1.045s, 1.057s]  (10 runs, 84,314 lines)

--- pipeline-no-lower ---
  BenchmarkSerenedb/Pipeline-no-lower ...  263.753ms mean  p50=263.924ms  95% CI [262.542ms, 265.042ms]  99% CI [262.241ms, 265.390ms]  (10 runs, 84,314 lines)

--- pipeline-no-lower-no-edge ---
  BenchmarkSerenedb/Pipeline-no-lower-no-edge ...  238.704ms mean  p50=238.705ms  95% CI [237.410ms, 240.078ms]  99% CI [237.101ms, 240.484ms]  (10 runs, 84,314 lines)

--- pipeline-no-stem ---
  BenchmarkSerenedb/Pipeline-no-stem ...  978.948ms mean  p50=979.555ms  95% CI [976.527ms, 981.520ms]  99% CI [975.899ms, 982.250ms]  (10 runs, 84,314 lines)

--- pipeline-no-stem-no-edge ---
  BenchmarkSerenedb/Pipeline-no-stem-no-edge ...  949.993ms mean  p50=949.590ms  95% CI [948.807ms, 951.398ms]  99% CI [948.541ms, 951.837ms]  (10 runs, 84,314 lines)

--- pipeline-no-stem-no-lower ---
  BenchmarkSerenedb/Pipeline-no-stem-no-lower ...  188.729ms mean  p50=188.597ms  95% CI [188.252ms, 189.280ms]  99% CI [188.138ms, 189.425ms]  (10 runs, 84,314 lines)

--- pipeline-no-stem-no-lower-no-edge ---
  BenchmarkSerenedb/Pipeline-no-stem-no-lower-no-edge ...  164.881ms mean  p50=164.607ms  95% CI [163.451ms, 166.759ms]  99% CI [163.135ms, 167.406ms]  (10 runs, 84,314 lines)

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                                                     mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkSerenedb/Text                                 1.292s    1.287s    1.338s    1.338s    1.338s     1.279s..1.307s         1.276s..1.312s        1.54M
BenchmarkSerenedb/Text-no-edge                         1.241s    1.239s    1.266s    1.266s    1.266s     1.235s..1.248s         1.233s..1.251s      551.52K
BenchmarkSerenedb/Text-no-lower                     604.808ms 605.285ms 612.107ms 612.107ms 612.107ms  603.026ms..606.831ms   602.585ms..607.666ms     3.35M
BenchmarkSerenedb/Text-no-lower-no-edge             568.188ms 567.305ms 576.615ms 576.615ms 576.615ms  566.776ms..570.365ms   566.600ms..571.311ms     1.23M
BenchmarkSerenedb/Text-no-stem                      929.610ms 929.722ms 939.056ms 939.056ms 939.056ms  926.587ms..932.878ms   925.656ms..934.009ms     2.14M
BenchmarkSerenedb/Text-no-stem-no-edge              889.565ms 888.595ms 902.551ms 902.551ms 902.551ms  886.482ms..893.048ms   885.812ms..894.157ms   769.34K
BenchmarkSerenedb/Text-no-stem-no-lower             279.173ms 278.899ms 282.939ms 282.939ms 282.939ms  278.292ms..280.298ms   278.087ms..280.685ms     7.28M
BenchmarkSerenedb/Text-no-stem-no-lower-no-edge     244.249ms 243.369ms 250.521ms 250.521ms 250.521ms  242.895ms..245.987ms   242.674ms..246.550ms     2.87M
BenchmarkSerenedb/Pipeline                             1.076s    1.078s    1.082s    1.082s    1.082s     1.072s..1.079s         1.071s..1.080s        1.85M
BenchmarkSerenedb/Pipeline-no-edge                     1.051s    1.052s    1.068s    1.068s    1.068s     1.046s..1.055s         1.045s..1.057s      651.44K
BenchmarkSerenedb/Pipeline-no-lower                 263.753ms 263.924ms 268.079ms 268.079ms 268.079ms  262.542ms..265.042ms   262.241ms..265.390ms     7.69M
BenchmarkSerenedb/Pipeline-no-lower-no-edge         238.704ms 238.705ms 242.390ms 242.390ms 242.390ms  237.410ms..240.078ms   237.101ms..240.484ms     2.94M
BenchmarkSerenedb/Pipeline-no-stem                  978.948ms 979.555ms 985.376ms 985.376ms 985.376ms  976.527ms..981.520ms   975.899ms..982.250ms     2.03M
BenchmarkSerenedb/Pipeline-no-stem-no-edge          949.993ms 949.590ms 954.158ms 954.158ms 954.158ms  948.807ms..951.398ms   948.541ms..951.837ms   720.40K
BenchmarkSerenedb/Pipeline-no-stem-no-lower         188.729ms 188.597ms 190.446ms 190.446ms 190.446ms  188.252ms..189.280ms   188.138ms..189.425ms    10.77M
BenchmarkSerenedb/Pipeline-no-stem-no-lower-no-edge 164.881ms 164.607ms 172.196ms 172.196ms 172.196ms  163.451ms..166.759ms   163.135ms..167.406ms     4.25M
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pipeline  SINGLE  serenedb=-6034335288063621306
  checksum/Pipeline-no-edge  SINGLE  serenedb=-5664440728914327306
  checksum/Pipeline-no-lower  SINGLE  serenedb=440086519885603818
  checksum/Pipeline-no-lower-no-edge  SINGLE  serenedb=-1041011869549050374
  checksum/Pipeline-no-stem  SINGLE  serenedb=-2784654529716357797
  checksum/Pipeline-no-stem-no-edge  SINGLE  serenedb=2302591325320108174
  checksum/Pipeline-no-stem-no-lower  SINGLE  serenedb=2802796628737376424
  checksum/Pipeline-no-stem-no-lower-no-edge  SINGLE  serenedb=7282322631482786906
  checksum/Text  SINGLE  serenedb=-6034335288063621306
  checksum/Text-no-edge  SINGLE  serenedb=-5664440728914327306
  checksum/Text-no-lower  SINGLE  serenedb=440086519885603818
  checksum/Text-no-lower-no-edge  SINGLE  serenedb=-1041011869549050374
  checksum/Text-no-stem  SINGLE  serenedb=-2784654529716357797
  checksum/Text-no-stem-no-edge  SINGLE  serenedb=2302591325320108174
  checksum/Text-no-stem-no-lower  SINGLE  serenedb=2802796628737376424
  checksum/Text-no-stem-no-lower-no-edge  SINGLE  serenedb=7282322631482786906
```
</details>
