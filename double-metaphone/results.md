```
2026-04-15T17:38:40+03:00
Running ./dm_bench
Run on (12 X 2541.77 MHz CPU s)
CPU Caches:
  L1 Data 32 KiB (x6)
  L1 Instruction 32 KiB (x6)
  L2 Unified 512 KiB (x6)
  L3 Unified 4096 KiB (x2)
Load Average: 2.94, 2.43, 2.29
----------------------------------------------------------------------------------------
Benchmark                              Time             CPU   Iterations UserCounters...
----------------------------------------------------------------------------------------
BM_Pixelglow_ShortWords             2009 ns         2008 ns       322775 items_per_second=12.4475M/s
BM_Pixelglow_MediumWords            3433 ns         3427 ns       202713 items_per_second=7.29598M/s
BM_Pixelglow_LongWords              5701 ns         5688 ns       118596 items_per_second=3.51589M/s
BM_Pixelglow_TrickyWords            3669 ns         3666 ns       186705 items_per_second=8.18425M/s
BM_Pixelglow_SingleWord              201 ns          201 ns      3335139 items_per_second=4.98094M/s
[INFO] Loaded 100000 words from data/words.txt
BM_Pixelglow_FileWords          15703558 ns     15697848 ns           42 items_per_second=6.3703M/s
BM_Pixelglow_Batch/100             16239 ns        16218 ns        41340 items_per_second=6.16582M/s
BM_Pixelglow_Batch/1000           162519 ns       162509 ns         4121 items_per_second=6.15351M/s
BM_Pixelglow_Batch/10000         1618704 ns      1618688 ns          408 items_per_second=6.17784M/s
BM_Pixelglow_Batch/100000       16212583 ns     16212029 ns           41 items_per_second=6.16826M/s
BM_Mtfn_ShortWords                  5923 ns         5923 ns       108089 items_per_second=4.22077M/s
BM_Mtfn_MediumWords                 9639 ns         9639 ns        67876 items_per_second=2.5937M/s
BM_Mtfn_LongWords                   8490 ns         8490 ns        76165 items_per_second=2.35579M/s
BM_Mtfn_TrickyWords                10648 ns        10647 ns        57186 items_per_second=2.81766M/s
BM_Mtfn_SingleWord                   502 ns          502 ns      1224565 items_per_second=1.99114M/s
BM_Mtfn_Compare                     9355 ns         9354 ns        69665 items_per_second=1.28283M/s
BM_Mtfn_MediumWords_Unlimited      11243 ns        11242 ns        58575 items_per_second=2.22373M/s
BM_Mtfn_FileWords               35569340 ns     35568228 ns           20 items_per_second=2.8115M/s
BM_Mtfn_Batch/100                  36244 ns        36243 ns        19311 items_per_second=2.75918M/s
BM_Mtfn_Batch/1000                362412 ns       362401 ns         1937 items_per_second=2.75938M/s
BM_Mtfn_Batch/10000              3574879 ns      3570202 ns          196 items_per_second=2.80096M/s
BM_Mtfn_Batch/100000            37797248 ns     37796684 ns           18 items_per_second=2.64573M/s
```
