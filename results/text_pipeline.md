# `text` vs `pipeline` (segmentation) vs `pipeline_text`

## Locae: C
Data: `data/3200_180000.txt`

| On filters | text mean | text 99% CI | pipeline mean | pipeline 99% CI | pipeline_text mean | pipeline_text 99% CI |
|----------------------------|-----------|-------------|---------------|-----------------|--------------------|----------------------|
| **lower, stem, edge, stopwords** | 1.688s    | 1.685s..1.691s | 362.092ms     | 361.121ms..363.265ms | 1.664s             | 1.659s..1.669s      |
| **lower, stem, stopwords**       | 1.615s    | 1.611s..1.620s | 326.149ms     | 324.657ms..328.035ms | 1.620s             | 1.615s..1.625s      |
| **lower, edge, stopwords**       | 1.684s    | 1.678s..1.690s | 353.982ms     | 353.341ms..354.696ms | 1.650s             | 1.646s..1.654s      |
| **stem, edge, stopwords**        | 503.066ms | 501.212ms..504.958ms | 349.873ms     | 348.553ms..351.304ms | 523.422ms          | 522.207ms..525.134ms |
| **lower, stopwords**             | 1.625s    | 1.619s..1.631s | 337.901ms     | 336.043ms..342.078ms | 1.605s             | 1.599s..1.613s      |
| **stem, stopwords**              | 434.786ms | 433.343ms..436.427ms | 306.038ms     | 304.948ms..308.445ms | 483.623ms          | 481.548ms..485.378ms |
| **edge, stopwords**              | 499.738ms | 498.073ms..502.538ms | 331.109ms     | 330.560ms..331.838ms | 510.852ms          | 508.761ms..513.077ms |
| **stopwords**                    | 435.406ms | 433.104ms..438.176ms | 287.434ms     | 286.950ms..287.926ms | 466.423ms          | 462.383ms..474.711ms |

## Locale: en
Data: `data/3200_180000.txt`

| On filters | text mean | text 99% CI | pipeline mean | pipeline 99% CI | pipeline_text mean | pipeline_text 99% CI |
|----------------------------|-----------|-------------|---------------|-----------------|--------------------|----------------------|
| **lower, stem, edge, stopwords**  | 2.336s    | 2.324s..2.347s | 890.762ms     | 885.283ms..896.951ms | 2.299s             | 2.296s..2.302s      |
| **lower, stem, stopwords**        | 2.260s    | 2.252s..2.270s | 859.984ms     | 852.811ms..872.869ms | 2.270s             | 2.264s..2.277s      |
| **lower, edge, stopwords**        | 1.685s    | 1.675s..1.698s | 377.591ms     | 372.469ms..386.265ms | 1.660s             | 1.653s..1.666s      |
| **stem, edge, stopwords**         | 1.080s    | 1.074s..1.086s | 886.486ms     | 879.034ms..894.477ms | 1.133s             | 1.116s..1.156s      |
| **lower, stopwords**              | 1.616s    | 1.610s..1.623s | 314.433ms     | 307.250ms..325.540ms | 1.604s             | 1.595s..1.615s      |
| **stem, stopwords**               | 1.008s    | 1.006s..1.012s | 844.323ms     | 838.777ms..849.661ms | 1.084s             | 1.070s..1.100s      |
| **edge, stopwords**               | 512.636ms | 505.681ms..520.604ms | 339.453ms     | 335.096ms..345.407ms | 517.860ms          | 509.333ms..533.279ms |
| **stopwords**                     | 447.892ms | 442.421ms..453.703ms | 286.917ms     | 285.509ms..289.558ms | 466.329ms          | 465.022ms..467.639ms |


<details>
<summary>Full log (locale C)</summary>

```
❯ make bench-text-pipeline SYSTEMS=serenedb DATA=data/3200_180000.txt EXTRA_ARGS="--locale C"
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench '^(text|pipeline)' --systems serenedb --count 10 --warmup 2 --data /home/romanp/benchmark-tokenizers/data/3200_180000.txt --locale C
tokenizers: text, text-no-edge, text-no-lower, text-no-lower-no-edge, text-no-stem, text-no-stem-no-edge, text-no-stem-no-lower, text-no-stem-no-lower-no-edge, pipeline, pipeline-no-edge, pipeline-no-lower, pipeline-no-lower-no-edge, pipeline-no-stem, pipeline-no-stem-no-edge, pipeline-no-stem-no-lower, pipeline-no-stem-no-lower-no-edge, pipeline_text, pipeline_text-no-edge, pipeline_text-no-lower, pipeline_text-no-lower-no-edge, pipeline_text-no-stem, pipeline_text-no-stem-no-edge, pipeline_text-no-stem-no-lower, pipeline_text-no-stem-no-lower-no-edge
systems:    serenedb
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/data/3200_180000.txt

--- text ---
  BenchmarkSerenedb/Text ...  1.688s mean  p50=1.690s  95% CI [1.685s, 1.690s]  99% CI [1.685s, 1.691s]  (10 runs, 149,175 lines)

--- text-no-edge ---
  BenchmarkSerenedb/Text-no-edge ...  1.615s mean  p50=1.616s  95% CI [1.612s, 1.619s]  99% CI [1.611s, 1.620s]  (10 runs, 149,175 lines)

--- text-no-lower ---
  BenchmarkSerenedb/Text-no-lower ...  503.066ms mean  p50=503.110ms  95% CI [501.634ms, 504.486ms]  99% CI [501.212ms, 504.958ms]  (10 runs, 149,175 lines)

--- text-no-lower-no-edge ---
  BenchmarkSerenedb/Text-no-lower-no-edge ...  434.786ms mean  p50=434.354ms  95% CI [433.657ms, 436.052ms]  99% CI [433.343ms, 436.427ms]  (10 runs, 149,175 lines)

--- text-no-stem ---
  BenchmarkSerenedb/Text-no-stem ...  1.684s mean  p50=1.687s  95% CI [1.680s, 1.688s]  99% CI [1.678s, 1.690s]  (10 runs, 149,175 lines)

--- text-no-stem-no-edge ---
  BenchmarkSerenedb/Text-no-stem-no-edge ...  1.625s mean  p50=1.629s  95% CI [1.621s, 1.630s]  99% CI [1.619s, 1.631s]  (10 runs, 149,175 lines)

--- text-no-stem-no-lower ---
  BenchmarkSerenedb/Text-no-stem-no-lower ...  499.738ms mean  p50=499.331ms  95% CI [498.324ms, 501.754ms]  99% CI [498.073ms, 502.538ms]  (10 runs, 149,175 lines)

--- text-no-stem-no-lower-no-edge ---
  BenchmarkSerenedb/Text-no-stem-no-lower-no-edge ...  435.406ms mean  p50=435.087ms  95% CI [433.493ms, 437.591ms]  99% CI [433.104ms, 438.176ms]  (10 runs, 149,175 lines)

--- pipeline ---
  BenchmarkSerenedb/Pipeline ...  362.092ms mean  p50=361.581ms  95% CI [361.289ms, 362.976ms]  99% CI [361.121ms, 363.265ms]  (10 runs, 149,175 lines)

--- pipeline-no-edge ---
  BenchmarkSerenedb/Pipeline-no-edge ...  326.149ms mean  p50=325.828ms  95% CI [324.942ms, 327.546ms]  99% CI [324.657ms, 328.035ms]  (10 runs, 149,175 lines)

--- pipeline-no-lower ---
  BenchmarkSerenedb/Pipeline-no-lower ...  349.873ms mean  p50=349.144ms  95% CI [348.818ms, 350.991ms]  99% CI [348.553ms, 351.304ms]  (10 runs, 149,175 lines)

--- pipeline-no-lower-no-edge ---
  BenchmarkSerenedb/Pipeline-no-lower-no-edge ...  306.038ms mean  p50=305.358ms  95% CI [305.040ms, 307.736ms]  99% CI [304.948ms, 308.445ms]  (10 runs, 149,175 lines)

--- pipeline-no-stem ---
  BenchmarkSerenedb/Pipeline-no-stem ...  353.982ms mean  p50=353.985ms  95% CI [353.470ms, 354.527ms]  99% CI [353.341ms, 354.696ms]  (10 runs, 149,175 lines)

--- pipeline-no-stem-no-edge ---
  BenchmarkSerenedb/Pipeline-no-stem-no-edge ...  337.901ms mean  p50=336.307ms  95% CI [336.180ms, 340.728ms]  99% CI [336.043ms, 342.078ms]  (10 runs, 149,175 lines)

--- pipeline-no-stem-no-lower ---
  BenchmarkSerenedb/Pipeline-no-stem-no-lower ...  331.109ms mean  p50=330.879ms  95% CI [330.665ms, 331.640ms]  99% CI [330.560ms, 331.838ms]  (10 runs, 149,175 lines)

--- pipeline-no-stem-no-lower-no-edge ---
  BenchmarkSerenedb/Pipeline-no-stem-no-lower-no-edge ...  287.434ms mean  p50=287.697ms  95% CI [287.046ms, 287.808ms]  99% CI [286.950ms, 287.926ms]  (10 runs, 149,175 lines)

--- pipeline_text ---
  BenchmarkSerenedb/PipelineText ...  1.664s mean  p50=1.666s  95% CI [1.660s, 1.668s]  99% CI [1.659s, 1.669s]  (10 runs, 149,175 lines)

--- pipeline_text-no-edge ---
  BenchmarkSerenedb/PipelineText-no-edge ...  1.620s mean  p50=1.619s  95% CI [1.616s, 1.624s]  99% CI [1.615s, 1.625s]  (10 runs, 149,175 lines)

--- pipeline_text-no-lower ---
  BenchmarkSerenedb/PipelineText-no-lower ...  523.422ms mean  p50=522.614ms  95% CI [522.405ms, 524.688ms]  99% CI [522.207ms, 525.134ms]  (10 runs, 149,175 lines)

--- pipeline_text-no-lower-no-edge ---
  BenchmarkSerenedb/PipelineText-no-lower-no-edge ...  483.623ms mean  p50=484.135ms  95% CI [482.083ms, 485.026ms]  99% CI [481.548ms, 485.378ms]  (10 runs, 149,175 lines)

--- pipeline_text-no-stem ---
  BenchmarkSerenedb/PipelineText-no-stem ...  1.650s mean  p50=1.651s  95% CI [1.647s, 1.653s]  99% CI [1.646s, 1.654s]  (10 runs, 149,175 lines)

--- pipeline_text-no-stem-no-edge ---
  BenchmarkSerenedb/PipelineText-no-stem-no-edge ...  1.605s mean  p50=1.603s  95% CI [1.600s, 1.611s]  99% CI [1.599s, 1.613s]  (10 runs, 149,175 lines)

--- pipeline_text-no-stem-no-lower ---
  BenchmarkSerenedb/PipelineText-no-stem-no-lower ...  510.852ms mean  p50=510.884ms  95% CI [509.206ms, 512.579ms]  99% CI [508.761ms, 513.077ms]  (10 runs, 149,175 lines)

--- pipeline_text-no-stem-no-lower-no-edge ---
  BenchmarkSerenedb/PipelineText-no-stem-no-lower-no-edge ...  466.423ms mean  p50=464.241ms  95% CI [462.823ms, 472.317ms]  99% CI [462.383ms, 474.711ms]  (10 runs, 149,175 lines)

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                                                         mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkSerenedb/Text                                     1.688s    1.690s    1.692s    1.692s    1.692s     1.685s..1.690s         1.685s..1.691s        2.12M
BenchmarkSerenedb/Text-no-edge                             1.615s    1.616s    1.625s    1.625s    1.625s     1.612s..1.619s         1.611s..1.620s      765.48K
BenchmarkSerenedb/Text-no-lower                         503.066ms 503.110ms 507.668ms 507.668ms 507.668ms  501.634ms..504.486ms   501.212ms..504.958ms     7.27M
BenchmarkSerenedb/Text-no-lower-no-edge                 434.786ms 434.354ms 438.377ms 438.377ms 438.377ms  433.657ms..436.052ms   433.343ms..436.427ms     2.91M
BenchmarkSerenedb/Text-no-stem                             1.684s    1.687s    1.693s    1.693s    1.693s     1.680s..1.688s         1.678s..1.690s        2.13M
BenchmarkSerenedb/Text-no-stem-no-edge                     1.625s    1.629s    1.636s    1.636s    1.636s     1.621s..1.630s         1.619s..1.631s      760.82K
BenchmarkSerenedb/Text-no-stem-no-lower                 499.738ms 499.331ms 507.469ms 507.469ms 507.469ms  498.324ms..501.754ms   498.073ms..502.538ms     7.31M
BenchmarkSerenedb/Text-no-stem-no-lower-no-edge         435.406ms 435.087ms 441.637ms 441.637ms 441.637ms  433.493ms..437.591ms   433.104ms..438.176ms     2.91M
BenchmarkSerenedb/Pipeline                              362.092ms 361.581ms 364.725ms 364.725ms 364.725ms  361.289ms..362.976ms   361.121ms..363.265ms     9.90M
BenchmarkSerenedb/Pipeline-no-edge                      326.149ms 325.828ms 331.088ms 331.088ms 331.088ms  324.942ms..327.546ms   324.657ms..328.035ms     3.79M
BenchmarkSerenedb/Pipeline-no-lower                     349.873ms 349.144ms 352.280ms 352.280ms 352.280ms  348.818ms..350.991ms   348.553ms..351.304ms    10.45M
BenchmarkSerenedb/Pipeline-no-lower-no-edge             306.038ms 305.358ms 313.026ms 313.026ms 313.026ms  305.040ms..307.736ms   304.948ms..308.445ms     4.14M
BenchmarkSerenedb/Pipeline-no-stem                      353.982ms 353.985ms 355.412ms 355.412ms 355.412ms  353.470ms..354.527ms   353.341ms..354.696ms    10.13M
BenchmarkSerenedb/Pipeline-no-stem-no-edge              337.901ms 336.307ms 349.779ms 349.779ms 349.779ms  336.180ms..340.728ms   336.043ms..342.078ms     3.66M
BenchmarkSerenedb/Pipeline-no-stem-no-lower             331.109ms 330.879ms 332.794ms 332.794ms 332.794ms  330.665ms..331.640ms   330.560ms..331.838ms    11.04M
BenchmarkSerenedb/Pipeline-no-stem-no-lower-no-edge     287.434ms 287.697ms 288.448ms 288.448ms 288.448ms  287.046ms..287.808ms   286.950ms..287.926ms     4.40M
BenchmarkSerenedb/PipelineText                             1.664s    1.666s    1.672s    1.672s    1.672s     1.660s..1.668s         1.659s..1.669s        2.15M
BenchmarkSerenedb/PipelineText-no-edge                     1.620s    1.619s    1.632s    1.632s    1.632s     1.616s..1.624s         1.615s..1.625s      763.39K
BenchmarkSerenedb/PipelineText-no-lower                 523.422ms 522.614ms 528.215ms 528.215ms 528.215ms  522.405ms..524.688ms   522.207ms..525.134ms     6.98M
BenchmarkSerenedb/PipelineText-no-lower-no-edge         483.623ms 484.135ms 486.479ms 486.479ms 486.479ms  482.083ms..485.026ms   481.548ms..485.378ms     2.62M
BenchmarkSerenedb/PipelineText-no-stem                     1.650s    1.651s    1.660s    1.660s    1.660s     1.647s..1.653s         1.646s..1.654s        2.17M
BenchmarkSerenedb/PipelineText-no-stem-no-edge             1.605s    1.603s    1.626s    1.626s    1.626s     1.600s..1.611s         1.599s..1.613s      770.60K
BenchmarkSerenedb/PipelineText-no-stem-no-lower         510.852ms 510.884ms 516.482ms 516.482ms 516.482ms  509.206ms..512.579ms   508.761ms..513.077ms     7.16M
BenchmarkSerenedb/PipelineText-no-stem-no-lower-no-edge 466.423ms 464.241ms 490.059ms 490.059ms 490.059ms  462.823ms..472.317ms   462.383ms..474.711ms     2.71M
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pipeline  SINGLE  serenedb=-2185265358433199132
  checksum/Pipeline-no-edge  SINGLE  serenedb=-4039542650979156371
  checksum/Pipeline-no-lower  SINGLE  serenedb=-8860989700246166785
  checksum/Pipeline-no-lower-no-edge  SINGLE  serenedb=-8113956017355530404
  checksum/Pipeline-no-stem  SINGLE  serenedb=-2185265358433199132
  checksum/Pipeline-no-stem-no-edge  SINGLE  serenedb=-4039542650979156371
  checksum/Pipeline-no-stem-no-lower  SINGLE  serenedb=-8860989700246166785
  checksum/Pipeline-no-stem-no-lower-no-edge  SINGLE  serenedb=-8113956017355530404
  checksum/Pipelinetext  SINGLE  serenedb=-2185265358433199132
  checksum/Pipelinetext-no-edge  SINGLE  serenedb=-4039542650979156371
  checksum/Pipelinetext-no-lower  SINGLE  serenedb=-8860989700246166785
  checksum/Pipelinetext-no-lower-no-edge  SINGLE  serenedb=-8113956017355530404
  checksum/Pipelinetext-no-stem  SINGLE  serenedb=-2185265358433199132
  checksum/Pipelinetext-no-stem-no-edge  SINGLE  serenedb=-4039542650979156371
  checksum/Pipelinetext-no-stem-no-lower  SINGLE  serenedb=-8860989700246166785
  checksum/Pipelinetext-no-stem-no-lower-no-edge  SINGLE  serenedb=-8113956017355530404
  checksum/Text  SINGLE  serenedb=-2185265358433199132
  checksum/Text-no-edge  SINGLE  serenedb=-4039542650979156371
  checksum/Text-no-lower  SINGLE  serenedb=-8860989700246166785
  checksum/Text-no-lower-no-edge  SINGLE  serenedb=-8113956017355530404
  checksum/Text-no-stem  SINGLE  serenedb=-2185265358433199132
  checksum/Text-no-stem-no-edge  SINGLE  serenedb=-4039542650979156371
  checksum/Text-no-stem-no-lower  SINGLE  serenedb=-8860989700246166785
  checksum/Text-no-stem-no-lower-no-edge  SINGLE  serenedb=-8113956017355530404
```
</details>

<details>
<summary>Full log (locale en)</summary>

```
❯ make bench-text-pipeline SYSTEMS=serenedb DATA=data/3200_180000.txt EXTRA_ARGS="--locale en"
SERENEDB_BENCH=/home/romanp/serenedb/build_bench_no_lto/bin/iresearch-bench python3 bench.py --bench '^(text|pipeline)' --systems serenedb --count 10 --warmup 2 --data /home/romanp/benchmark-tokenizers/data/3200_180000.txt --locale en
tokenizers: text, text-no-edge, text-no-lower, text-no-lower-no-edge, text-no-stem, text-no-stem-no-edge, text-no-stem-no-lower, text-no-stem-no-lower-no-edge, pipeline, pipeline-no-edge, pipeline-no-lower, pipeline-no-lower-no-edge, pipeline-no-stem, pipeline-no-stem-no-edge, pipeline-no-stem-no-lower, pipeline-no-stem-no-lower-no-edge, pipeline_text, pipeline_text-no-edge, pipeline_text-no-lower, pipeline_text-no-lower-no-edge, pipeline_text-no-stem, pipeline_text-no-stem-no-edge, pipeline_text-no-stem-no-lower, pipeline_text-no-stem-no-lower-no-edge
systems:    serenedb
count:      10  warmup: 2
data:       /home/romanp/benchmark-tokenizers/data/3200_180000.txt

--- text ---
  BenchmarkSerenedb/Text ...  2.336s mean  p50=2.341s  95% CI [2.327s, 2.344s]  99% CI [2.324s, 2.347s]  (10 runs, 149,175 lines)

--- text-no-edge ---
  BenchmarkSerenedb/Text-no-edge ...  2.260s mean  p50=2.259s  95% CI [2.254s, 2.268s]  99% CI [2.252s, 2.270s]  (10 runs, 149,175 lines)

--- text-no-lower ---
  BenchmarkSerenedb/Text-no-lower ...  1.080s mean  p50=1.080s  95% CI [1.075s, 1.085s]  99% CI [1.074s, 1.086s]  (10 runs, 149,175 lines)

--- text-no-lower-no-edge ---
  BenchmarkSerenedb/Text-no-lower-no-edge ...  1.008s mean  p50=1.008s  95% CI [1.006s, 1.011s]  99% CI [1.006s, 1.012s]  (10 runs, 149,175 lines)

--- text-no-stem ---
  BenchmarkSerenedb/Text-no-stem ...  1.685s mean  p50=1.685s  95% CI [1.677s, 1.695s]  99% CI [1.675s, 1.698s]  (10 runs, 149,175 lines)

--- text-no-stem-no-edge ---
  BenchmarkSerenedb/Text-no-stem-no-edge ...  1.616s mean  p50=1.618s  95% CI [1.611s, 1.621s]  99% CI [1.610s, 1.623s]  (10 runs, 149,175 lines)

--- text-no-stem-no-lower ---
  BenchmarkSerenedb/Text-no-stem-no-lower ...  512.636ms mean  p50=513.705ms  95% CI [507.253ms, 518.342ms]  99% CI [505.681ms, 520.604ms]  (10 runs, 149,175 lines)

--- text-no-stem-no-lower-no-edge ---
  BenchmarkSerenedb/Text-no-stem-no-lower-no-edge ...  447.892ms mean  p50=448.627ms  95% CI [443.662ms, 452.260ms]  99% CI [442.421ms, 453.703ms]  (10 runs, 149,175 lines)

--- pipeline ---
  BenchmarkSerenedb/Pipeline ...  890.762ms mean  p50=892.149ms  95% CI [886.323ms, 895.510ms]  99% CI [885.283ms, 896.951ms]  (10 runs, 149,175 lines)

--- pipeline-no-edge ---
  BenchmarkSerenedb/Pipeline-no-edge ...  859.984ms mean  p50=857.450ms  95% CI [853.775ms, 868.978ms]  99% CI [852.811ms, 872.869ms]  (10 runs, 149,175 lines)

--- pipeline-no-lower ---
  BenchmarkSerenedb/Pipeline-no-lower ...  886.486ms mean  p50=886.439ms  95% CI [880.478ms, 892.608ms]  99% CI [879.034ms, 894.477ms]  (10 runs, 149,175 lines)

--- pipeline-no-lower-no-edge ---
  BenchmarkSerenedb/Pipeline-no-lower-no-edge ...  844.323ms mean  p50=847.686ms  95% CI [840.144ms, 848.338ms]  99% CI [838.777ms, 849.661ms]  (10 runs, 149,175 lines)

--- pipeline-no-stem ---
  BenchmarkSerenedb/Pipeline-no-stem ...  377.591ms mean  p50=375.564ms  95% CI [373.075ms, 383.935ms]  99% CI [372.469ms, 386.265ms]  (10 runs, 149,175 lines)

--- pipeline-no-stem-no-edge ---
  BenchmarkSerenedb/Pipeline-no-stem-no-edge ...  314.433ms mean  p50=312.665ms  95% CI [308.304ms, 322.597ms]  99% CI [307.250ms, 325.540ms]  (10 runs, 149,175 lines)

--- pipeline-no-stem-no-lower ---
  BenchmarkSerenedb/Pipeline-no-stem-no-lower ...  339.453ms mean  p50=339.493ms  95% CI [335.964ms, 344.178ms]  99% CI [335.096ms, 345.407ms]  (10 runs, 149,175 lines)

--- pipeline-no-stem-no-lower-no-edge ---
  BenchmarkSerenedb/Pipeline-no-stem-no-lower-no-edge ...  286.917ms mean  p50=286.078ms  95% CI [285.684ms, 288.856ms]  99% CI [285.509ms, 289.558ms]  (10 runs, 149,175 lines)

--- pipeline_text ---
  BenchmarkSerenedb/PipelineText ...  2.299s mean  p50=2.298s  95% CI [2.296s, 2.301s]  99% CI [2.296s, 2.302s]  (10 runs, 149,175 lines)

--- pipeline_text-no-edge ---
  BenchmarkSerenedb/PipelineText-no-edge ...  2.270s mean  p50=2.268s  95% CI [2.265s, 2.276s]  99% CI [2.264s, 2.277s]  (10 runs, 149,175 lines)

--- pipeline_text-no-lower ---
  BenchmarkSerenedb/PipelineText-no-lower ...  1.133s mean  p50=1.124s  95% CI [1.119s, 1.150s]  99% CI [1.116s, 1.156s]  (10 runs, 149,175 lines)

--- pipeline_text-no-lower-no-edge ---
  BenchmarkSerenedb/PipelineText-no-lower-no-edge ...  1.084s mean  p50=1.086s  95% CI [1.073s, 1.096s]  99% CI [1.070s, 1.100s]  (10 runs, 149,175 lines)

--- pipeline_text-no-stem ---
  BenchmarkSerenedb/PipelineText-no-stem ...  1.660s mean  p50=1.658s  95% CI [1.654s, 1.665s]  99% CI [1.653s, 1.666s]  (10 runs, 149,175 lines)

--- pipeline_text-no-stem-no-edge ---
  BenchmarkSerenedb/PipelineText-no-stem-no-edge ...  1.604s mean  p50=1.603s  95% CI [1.597s, 1.612s]  99% CI [1.595s, 1.615s]  (10 runs, 149,175 lines)

--- pipeline_text-no-stem-no-lower ---
  BenchmarkSerenedb/PipelineText-no-stem-no-lower ...  517.860ms mean  p50=512.524ms  95% CI [510.393ms, 528.872ms]  99% CI [509.333ms, 533.279ms]  (10 runs, 149,175 lines)

--- pipeline_text-no-stem-no-lower-no-edge ---
  BenchmarkSerenedb/PipelineText-no-stem-no-lower-no-edge ...  466.329ms mean  p50=467.060ms  95% CI [465.324ms, 467.301ms]  99% CI [465.022ms, 467.639ms]  (10 runs, 149,175 lines)

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
RESULTS
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
name                                                         mean       p50       p95       p99      p100         95%CI                  99%CI             tok/s
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
BenchmarkSerenedb/Text                                     2.336s    2.341s    2.362s    2.362s    2.362s     2.327s..2.344s         2.324s..2.347s        1.53M
BenchmarkSerenedb/Text-no-edge                             2.260s    2.259s    2.284s    2.284s    2.284s     2.254s..2.268s         2.252s..2.270s      547.09K
BenchmarkSerenedb/Text-no-lower                            1.080s    1.080s    1.092s    1.092s    1.092s     1.075s..1.085s         1.074s..1.086s        3.38M
BenchmarkSerenedb/Text-no-lower-no-edge                    1.008s    1.008s    1.016s    1.016s    1.016s     1.006s..1.011s         1.006s..1.012s        1.26M
BenchmarkSerenedb/Text-no-stem                             1.685s    1.685s    1.720s    1.720s    1.720s     1.677s..1.695s         1.675s..1.698s        2.13M
BenchmarkSerenedb/Text-no-stem-no-edge                     1.616s    1.618s    1.634s    1.634s    1.634s     1.611s..1.621s         1.610s..1.623s      765.37K
BenchmarkSerenedb/Text-no-stem-no-lower                 512.636ms 513.705ms 530.795ms 530.795ms 530.795ms  507.253ms..518.342ms   505.681ms..520.604ms     7.13M
BenchmarkSerenedb/Text-no-stem-no-lower-no-edge         447.892ms 448.627ms 460.341ms 460.341ms 460.341ms  443.662ms..452.260ms   442.421ms..453.703ms     2.83M
BenchmarkSerenedb/Pipeline                              890.762ms 892.149ms 904.616ms 904.616ms 904.616ms  886.323ms..895.510ms   885.283ms..896.951ms     4.02M
BenchmarkSerenedb/Pipeline-no-edge                      859.984ms 857.450ms 894.480ms 894.480ms 894.480ms  853.775ms..868.978ms   852.811ms..872.869ms     1.44M
BenchmarkSerenedb/Pipeline-no-lower                     886.486ms 886.439ms 902.004ms 902.004ms 902.004ms  880.478ms..892.608ms   879.034ms..894.477ms     4.11M
BenchmarkSerenedb/Pipeline-no-lower-no-edge             844.323ms 847.686ms 854.046ms 854.046ms 854.046ms  840.144ms..848.338ms   838.777ms..849.661ms     1.50M
BenchmarkSerenedb/Pipeline-no-stem                      377.591ms 375.564ms 401.745ms 401.745ms 401.745ms  373.075ms..383.935ms   372.469ms..386.265ms     9.49M
BenchmarkSerenedb/Pipeline-no-stem-no-edge              314.433ms 312.665ms 346.748ms 346.748ms 346.748ms  308.304ms..322.597ms   307.250ms..325.540ms     3.93M
BenchmarkSerenedb/Pipeline-no-stem-no-lower             339.453ms 339.493ms 356.288ms 356.288ms 356.288ms  335.964ms..344.178ms   335.096ms..345.407ms    10.77M
BenchmarkSerenedb/Pipeline-no-stem-no-lower-no-edge     286.917ms 286.078ms 294.566ms 294.566ms 294.566ms  285.684ms..288.856ms   285.509ms..289.558ms     4.41M
BenchmarkSerenedb/PipelineText                             2.299s    2.298s    2.305s    2.305s    2.305s     2.296s..2.301s         2.296s..2.302s        1.56M
BenchmarkSerenedb/PipelineText-no-edge                     2.270s    2.268s    2.288s    2.288s    2.288s     2.265s..2.276s         2.264s..2.277s      544.81K
BenchmarkSerenedb/PipelineText-no-lower                    1.133s    1.124s    1.194s    1.194s    1.194s     1.119s..1.150s         1.116s..1.156s        3.22M
BenchmarkSerenedb/PipelineText-no-lower-no-edge            1.084s    1.086s    1.124s    1.124s    1.124s     1.073s..1.096s         1.070s..1.100s        1.17M
BenchmarkSerenedb/PipelineText-no-stem                     1.660s    1.658s    1.678s    1.678s    1.678s     1.654s..1.665s         1.653s..1.666s        2.16M
BenchmarkSerenedb/PipelineText-no-stem-no-edge             1.604s    1.603s    1.628s    1.628s    1.628s     1.597s..1.612s         1.595s..1.615s      770.85K
BenchmarkSerenedb/PipelineText-no-stem-no-lower         517.860ms 512.524ms 560.893ms 560.893ms 560.893ms  510.393ms..528.872ms   509.333ms..533.279ms     7.06M
BenchmarkSerenedb/PipelineText-no-stem-no-lower-no-edge 466.329ms 467.060ms 468.714ms 468.714ms 468.714ms  465.324ms..467.301ms   465.022ms..467.639ms     2.71M
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

  checksum/Pipeline  SINGLE  serenedb=-7976158020131564385
  checksum/Pipeline-no-edge  SINGLE  serenedb=-2714671596248611555
  checksum/Pipeline-no-lower  SINGLE  serenedb=-3135569776225635040
  checksum/Pipeline-no-lower-no-edge  SINGLE  serenedb=-3995590251925273354
  checksum/Pipeline-no-stem  SINGLE  serenedb=-2185265358433199132
  checksum/Pipeline-no-stem-no-edge  SINGLE  serenedb=-4039542650979156371
  checksum/Pipeline-no-stem-no-lower  SINGLE  serenedb=-8860989700246166785
  checksum/Pipeline-no-stem-no-lower-no-edge  SINGLE  serenedb=-8113956017355530404
  checksum/Pipelinetext  SINGLE  serenedb=-7976158020131564385
  checksum/Pipelinetext-no-edge  SINGLE  serenedb=-2714671596248611555
  checksum/Pipelinetext-no-lower  SINGLE  serenedb=-3135569776225635040
  checksum/Pipelinetext-no-lower-no-edge  SINGLE  serenedb=-3995590251925273354
  checksum/Pipelinetext-no-stem  SINGLE  serenedb=-2185265358433199132
  checksum/Pipelinetext-no-stem-no-edge  SINGLE  serenedb=-4039542650979156371
  checksum/Pipelinetext-no-stem-no-lower  SINGLE  serenedb=-8860989700246166785
  checksum/Pipelinetext-no-stem-no-lower-no-edge  SINGLE  serenedb=-8113956017355530404
  checksum/Text  SINGLE  serenedb=-7976158020131564385
  checksum/Text-no-edge  SINGLE  serenedb=-2714671596248611555
  checksum/Text-no-lower  SINGLE  serenedb=-3135569776225635040
  checksum/Text-no-lower-no-edge  SINGLE  serenedb=-3995590251925273354
  checksum/Text-no-stem  SINGLE  serenedb=-2185265358433199132
  checksum/Text-no-stem-no-edge  SINGLE  serenedb=-4039542650979156371
  checksum/Text-no-stem-no-lower  SINGLE  serenedb=-8860989700246166785
  checksum/Text-no-stem-no-lower-no-edge  SINGLE  serenedb=-8113956017355530404
```
</details>

