"""
bench.py -- tokenizer benchmark runner

Usage:
  python bench.py [--bench REGEXP] [--systems LIST] [--count N] [--warmup N]
                  [--data FILE] [-o FILE] [--compare FILE]
  python bench.py compare OLD NEW

Examples:
  # Run all benchmarks
  python bench.py

  # Run only pattern benchmarks, 20 runs, save results
  python bench.py --bench pattern --count 20 --data data/wiki_lines.txt -o results/run1.txt

  # Run and compare against a previous run
  python bench.py --count 20 --data data/wiki_lines.txt -o results/run2.txt --compare results/run1.txt

  # Compare two saved files
  python bench.py compare results/run1.txt results/run2.txt
"""

import argparse
import os
import random
import re
import struct
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).parent.resolve()

@dataclass
class BenchResult:
    name: str
    runs: int
    lines: int
    mean_ns: float
    ci_lo_ns: float   # 95% bootstrap CI for mean run time
    ci_hi_ns: float
    ci99_lo_ns: float
    ci99_hi_ns: float
    p50_ns: float
    p95_ns: float
    p99_ns: float
    p100_ns: float
    tokens: Optional[int] = None
    checksum: Optional[int] = None

    def to_line(self) -> str:
        """Serialise to go-bench-inspired one-liner for result files."""
        return (
            f"{self.name}\t{self.runs}\t{self.mean_ns:.0f} ns/op"
            f"\t{self.ci_lo_ns:.0f} ci95-lo-ns"
            f"\t{self.ci_hi_ns:.0f} ci95-hi-ns"
            f"\t{self.ci99_lo_ns:.0f} ci99-lo-ns"
            f"\t{self.ci99_hi_ns:.0f} ci99-hi-ns"
            f"\t{self.p50_ns:.0f} p50-ns"
            f"\t{self.p95_ns:.0f} p95-ns"
            f"\t{self.p99_ns:.0f} p99-ns"
            f"\t{self.p100_ns:.0f} p100-ns"
        )

_HEADER_RE   = re.compile(r"tokenizer=\S+\s+runs=(\d+)\s+lines=(\d+)(?:\s+tokens=(\d+))?")
_RUNS_NS_RE  = re.compile(r"^runs_ns=([\d,]+)\s*$", re.MULTILINE)

_NS_RE       = re.compile(
    r"time_ns\s+p50=(\d+(?:\.\d+)?)\s+p95=(\d+(?:\.\d+)?)"
    r"\s+p99=(\d+(?:\.\d+)?)\s+p100=(\d+(?:\.\d+)?)\s+mean=(\d+(?:\.\d+)?)"
)
_CHECKSUM_RE = re.compile(r"^checksum=(-?\d+)", re.MULTILINE)
# New format: mean + bootstrap 95% / 99% CI + latency percentiles.
_LINE_RE_FULL = re.compile(
    r"(Benchmark\S+)\s+(\d+)\s+(\d+(?:\.\d+)?)\s+ns/op"
    r"\s+(\d+(?:\.\d+)?)\s+ci95-lo-ns"
    r"\s+(\d+(?:\.\d+)?)\s+ci95-hi-ns"
    r"\s+(\d+(?:\.\d+)?)\s+ci99-lo-ns"
    r"\s+(\d+(?:\.\d+)?)\s+ci99-hi-ns"
    r"\s+(\d+(?:\.\d+)?)\s+p50-ns"
    r"\s+(\d+(?:\.\d+)?)\s+p95-ns"
    r"\s+(\d+(?:\.\d+)?)\s+p99-ns"
    r"\s+(\d+(?:\.\d+)?)\s+p100-ns"
)
# Saved `-o` lines from before ci99 columns (ci95 + percentiles only).
_LINE_RE_FULL_V1 = re.compile(
    r"(Benchmark\S+)\s+(\d+)\s+(\d+(?:\.\d+)?)\s+ns/op"
    r"\s+(\d+(?:\.\d+)?)\s+ci95-lo-ns"
    r"\s+(\d+(?:\.\d+)?)\s+ci95-hi-ns"
    r"\s+(\d+(?:\.\d+)?)\s+p50-ns"
    r"\s+(\d+(?:\.\d+)?)\s+p95-ns"
    r"\s+(\d+(?:\.\d+)?)\s+p99-ns"
    r"\s+(\d+(?:\.\d+)?)\s+p100-ns"
)
# Saved file: mean + CI only (no percentiles) - older `-o` output.
_LINE_RE_CI = re.compile(
    r"(Benchmark\S+)\s+(\d+)\s+(\d+(?:\.\d+)?)\s+ns/op"
    r"\s+(\d+(?:\.\d+)?)\s+ci95-lo-ns"
    r"\s+(\d+(?:\.\d+)?)\s+ci95-hi-ns"
)
# Legacy saved lines (percentiles).
_LINE_RE_PCT = re.compile(
    r"(Benchmark\S+)\s+(\d+)\s+(\d+(?:\.\d+)?)\s+ns/op"
    r"\s+(\d+(?:\.\d+)?)\s+p50-ns"
    r"\s+(\d+(?:\.\d+)?)\s+p95-ns"
    r"\s+(\d+(?:\.\d+)?)\s+p99-ns"
    r"\s+(\d+(?:\.\d+)?)\s+p100-ns"
)

_BOOTSTRAP_B = 4000
_BOOTSTRAP_SEED = 1


def _mk_runs_dump_path() -> Path:
    fd, name = tempfile.mkstemp(prefix="tokbench_", suffix=".runs")
    os.close(fd)
    return Path(name)


def _read_run_times_le(path: Path) -> list[float]:
    """Read per-run wall times written as uint64 little-endian (one per 8 bytes)."""
    data = path.read_bytes()
    if not data:
        return []
    if len(data) % 8 != 0:
        raise ValueError(f"runs dump size {len(data)} is not a multiple of 8")
    n = len(data) // 8
    return [float(x) for x in struct.unpack(f"<{n}Q", data)]


def _latency_percentiles_ns(run_ns: list[float]) -> tuple[float, float, float, float]:
    """p50 / p95 / p99 / p100 over per-run wall times (same indexing as Rust/Java/C++ benches)."""
    if not run_ns:
        return (0.0, 0.0, 0.0, 0.0)
    s = sorted(run_ns)
    n = len(s)
    p50 = s[int(n * 0.50)]
    p95 = s[int(n * 0.95)]
    p99 = s[min(int(n * 0.99), n - 1)]
    p100 = s[n - 1]
    return (p50, p95, p99, p100)


def _bootstrap_cis_mean_ns(
    runs_ns: list[float], *, b: int = _BOOTSTRAP_B, seed: int = _BOOTSTRAP_SEED
) -> tuple[float, float, float, float, float]:
    """Bootstrap distribution of mean(run); return (mean_ns, ci95_lo, ci95_hi, ci99_lo, ci99_hi)."""
    n = len(runs_ns)
    if n == 0:
        return (0.0, 0.0, 0.0, 0.0, 0.0)
    mean_ns = sum(runs_ns) / n
    if n < 2:
        return (mean_ns, mean_ns, mean_ns, mean_ns, mean_ns)
    rng = random.Random(seed)
    boots: list[float] = []
    for _ in range(b):
        s = 0.0
        for _ in range(n):
            s += runs_ns[rng.randrange(n)]
        boots.append(s / n)
    boots.sort()

    def interval(alpha: float) -> tuple[float, float]:
        lo_i = max(0, int((alpha / 2) * b))
        hi_i = min(b - 1, int((1 - alpha / 2) * b))
        return (boots[lo_i], boots[hi_i])

    lo95, hi95 = interval(0.05)
    lo99, hi99 = interval(0.01)
    return (mean_ns, lo95, hi95, lo99, hi99)


def _parse_run_output(
    text: str,
    name: str,
    *,
    runs_path: Optional[Path] = None,
) -> Optional[BenchResult]:
    h = _HEADER_RE.search(text)
    if not h:
        return None
    cs_m = _CHECKSUM_RE.search(text)

    run_vals: Optional[list[float]] = None
    if runs_path is not None and runs_path.is_file() and runs_path.stat().st_size > 0:
        try:
            run_vals = _read_run_times_le(runs_path)
        except (OSError, ValueError):
            run_vals = None

    if run_vals:
        mean_ns, ci95_lo, ci95_hi, ci99_lo, ci99_hi = _bootstrap_cis_mean_ns(run_vals)
        p50, p95, p99, p100 = _latency_percentiles_ns(run_vals)
    else:
        runs_m = _RUNS_NS_RE.search(text)
        if runs_m:
            parts = [p for p in runs_m.group(1).split(",") if p.strip()]
            if not parts:
                return None
            run_vals = [float(x) for x in parts]
            mean_ns, ci95_lo, ci95_hi, ci99_lo, ci99_hi = _bootstrap_cis_mean_ns(run_vals)
            p50, p95, p99, p100 = _latency_percentiles_ns(run_vals)
        else:
            n = _NS_RE.search(text)
            if not n:
                return None
            mean_ns = float(n.group(5))
            ci95_lo = ci95_hi = mean_ns
            ci99_lo = ci99_hi = mean_ns
            p50 = float(n.group(1))
            p95 = float(n.group(2))
            p99 = float(n.group(3))
            p100 = float(n.group(4))

    return BenchResult(
        name=name,
        runs=int(h.group(1)),
        lines=int(h.group(2)),
        tokens=int(h.group(3)) if h.group(3) else None,
        mean_ns=mean_ns,
        ci_lo_ns=ci95_lo,
        ci_hi_ns=ci95_hi,
        ci99_lo_ns=ci99_lo,
        ci99_hi_ns=ci99_hi,
        p50_ns=p50,
        p95_ns=p95,
        p99_ns=p99,
        p100_ns=p100,
        checksum=int(cs_m.group(1)) if cs_m else None,
    )


def _parse_result_file(path: str) -> dict[str, BenchResult]:
    results: dict[str, BenchResult] = {}
    with open(path) as f:
        for raw in f:
            m = _LINE_RE_FULL.search(raw)
            if m:
                name = m.group(1)
                mean_ns = float(m.group(3))
                results[name] = BenchResult(
                    name=name,
                    runs=int(m.group(2)),
                    lines=0,
                    mean_ns=mean_ns,
                    ci_lo_ns=float(m.group(4)),
                    ci_hi_ns=float(m.group(5)),
                    ci99_lo_ns=float(m.group(6)),
                    ci99_hi_ns=float(m.group(7)),
                    p50_ns=float(m.group(8)),
                    p95_ns=float(m.group(9)),
                    p99_ns=float(m.group(10)),
                    p100_ns=float(m.group(11)),
                )
                continue
            m = _LINE_RE_FULL_V1.search(raw)
            if m:
                name = m.group(1)
                mean_ns = float(m.group(3))
                results[name] = BenchResult(
                    name=name,
                    runs=int(m.group(2)),
                    lines=0,
                    mean_ns=mean_ns,
                    ci_lo_ns=float(m.group(4)),
                    ci_hi_ns=float(m.group(5)),
                    ci99_lo_ns=mean_ns,
                    ci99_hi_ns=mean_ns,
                    p50_ns=float(m.group(6)),
                    p95_ns=float(m.group(7)),
                    p99_ns=float(m.group(8)),
                    p100_ns=float(m.group(9)),
                )
                continue
            m = _LINE_RE_CI.search(raw)
            if m:
                name = m.group(1)
                mean_ns = float(m.group(3))
                results[name] = BenchResult(
                    name=name,
                    runs=int(m.group(2)),
                    lines=0,
                    mean_ns=mean_ns,
                    ci_lo_ns=float(m.group(4)),
                    ci_hi_ns=float(m.group(5)),
                    ci99_lo_ns=mean_ns,
                    ci99_hi_ns=mean_ns,
                    p50_ns=mean_ns,
                    p95_ns=mean_ns,
                    p99_ns=mean_ns,
                    p100_ns=mean_ns,
                )
                continue
            m2 = _LINE_RE_PCT.search(raw)
            if m2:
                name = m2.group(1)
                mean_ns = float(m2.group(3))
                results[name] = BenchResult(
                    name=name,
                    runs=int(m2.group(2)),
                    lines=0,
                    mean_ns=mean_ns,
                    ci_lo_ns=mean_ns,
                    ci_hi_ns=mean_ns,
                    ci99_lo_ns=mean_ns,
                    ci99_hi_ns=mean_ns,
                    p50_ns=float(m2.group(4)),
                    p95_ns=float(m2.group(5)),
                    p99_ns=float(m2.group(6)),
                    p100_ns=float(m2.group(7)),
                )
    return results

def _run_lucene(tokenizer: str, data: Path, count: int, warmup: int,
                reverse: bool = False, debug: bool = False) -> Optional[BenchResult]:
    name = f"BenchmarkLucene/{tokenizer.capitalize()}"
    rev_flag = " --reverse" if reverse else ""
    runs_path = _mk_runs_dump_path()
    parsed: Optional[BenchResult] = None
    combined = ""
    try:
        args_str = (
            f"{data} {tokenizer} --runs {count} --warmup {warmup}{rev_flag} "
            f"--bench-runs-file {runs_path.resolve()}"
        )
        cmd = ["./gradlew", "run", "-q", f"--args={args_str}"]

        print(f"  {name} ...", end="", flush=True)
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=ROOT, stdin=subprocess.DEVNULL
        )
        combined = result.stdout + result.stderr

        if result.returncode != 0:
            print(" FAILED")
            _print_subprocess_err(combined)
            return None

        if debug:
            _echo_captured_stdout(result)
        parsed = _parse_run_output(combined, name, runs_path=runs_path)
    finally:
        runs_path.unlink(missing_ok=True)

    if parsed:
        print(
            f"  {_fmt_ns(parsed.mean_ns)} mean  p50={_fmt_ns(parsed.p50_ns)}  "
            f"95% CI [{_fmt_ns(parsed.ci_lo_ns)}, {_fmt_ns(parsed.ci_hi_ns)}]  "
            f"99% CI [{_fmt_ns(parsed.ci99_lo_ns)}, {_fmt_ns(parsed.ci99_hi_ns)}]  "
            f"({parsed.runs} runs, {parsed.lines:,} lines)"
        )
    else:
        print(" PARSE ERROR")
        _print_subprocess_err(combined[:500])
    return parsed


def _run_tantivy(tokenizer: str, data: Path, count: int, warmup: int,
                 reverse: bool = False, debug: bool = False) -> Optional[BenchResult]:
    if reverse and tokenizer == "path":
        # Tantivy FacetTokenizer has no reverse mode
        return None
    name = f"BenchmarkTantivy/{tokenizer.capitalize()}"
    tantivy_type = {"pattern": "regex", "path": "facet"}[tokenizer]
    runs_path = _mk_runs_dump_path()
    parsed: Optional[BenchResult] = None
    combined = ""
    try:
        cmd = [
            "cargo", "run", "--release", "-q", "--",
            "--data", str(data),
            "--tokenizer", tantivy_type,
            "--runs", str(count),
            "--warmup", str(warmup),
            "--bench-runs-file", str(runs_path.resolve()),
        ]

        print(f"  {name} ...", end="", flush=True)
        result = subprocess.run(
            cmd, capture_output=True, text=True,
            cwd=ROOT / "tantivy-bench", stdin=subprocess.DEVNULL,
        )
        combined = result.stdout + result.stderr

        if result.returncode != 0:
            print(" FAILED")
            _print_subprocess_err(combined)
            return None

        if debug:
            _echo_captured_stdout(result)
        parsed = _parse_run_output(combined, name, runs_path=runs_path)
    finally:
        runs_path.unlink(missing_ok=True)

    if parsed:
        print(
            f"  {_fmt_ns(parsed.mean_ns)} mean  p50={_fmt_ns(parsed.p50_ns)}  "
            f"95% CI [{_fmt_ns(parsed.ci_lo_ns)}, {_fmt_ns(parsed.ci_hi_ns)}]  "
            f"99% CI [{_fmt_ns(parsed.ci99_lo_ns)}, {_fmt_ns(parsed.ci99_hi_ns)}]  "
            f"({parsed.runs} runs, {parsed.lines:,} lines)"
        )
    else:
        print(" PARSE ERROR")
        _print_subprocess_err(combined[:500])
    return parsed


def _iresearch_binary() -> Optional[Path]:
    """Find the iresearch-bench binary.

    Resolution order:
      1. IRESEARCH_BENCH env var (explicit path)
      2. ${IRESEARCH_SRC}/build/tests/bench/iresearch-bench/iresearch-bench
         (built via `make iresearch-build` inside serenedb cmake tree)
      3. iresearch-bench/build/iresearch-bench
    """
    env = os.environ.get("IRESEARCH_BENCH")
    if env:
        return Path(env)

    iresearch_src = os.environ.get("IRESEARCH_SRC", "")
    iresearch_build = os.environ.get("IRESEARCH_BUILD", "")
    if not iresearch_build and iresearch_src:
        sdb = Path(iresearch_src)
        bench_bin = sdb / "build_bench" / "bin" / "iresearch-bench"
        debug_bin = sdb / "build" / "bin" / "iresearch-bench"
        if bench_bin.exists():
            iresearch_build = str(sdb / "build_bench")
        elif debug_bin.exists():
            iresearch_build = str(sdb / "build")
    if iresearch_build:
        sdb_bin = Path(iresearch_build) / "bin" / "iresearch-bench"
        if sdb_bin.exists():
            return sdb_bin

    return None


def _build_iresearch() -> bool:
    iresearch_src = os.environ.get("IRESEARCH_SRC", "")
    if not iresearch_src:
        print("  IRESEARCH_SRC not set -- cannot build iresearch-bench")
        return False

    sdb = Path(iresearch_src).resolve()
    bench_dir = sdb / "tests" / "bench" / "iresearch-bench"
    bench_dir.mkdir(parents=True, exist_ok=True)

    # Sync sources into serenedb bench directory
    import shutil
    for f in ("main.cpp", "CMakeLists.txt"):
        shutil.copy(ROOT / "iresearch-bench" / f, bench_dir / f)

    # Register subdirectory if not already present
    bench_cmake = sdb / "tests" / "bench" / "CMakeLists.txt"
    content = bench_cmake.read_text()
    if "iresearch-bench" not in content:
        bench_cmake.write_text(content + "\nadd_subdirectory(iresearch-bench)\n")

    import multiprocessing
    r = subprocess.run(
        ["cmake", "--build", str(sdb / "build"),
         "--target", "iresearch-bench",
         "-j", str(multiprocessing.cpu_count())],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        _print_subprocess_err(r.stdout + r.stderr)
        return False
    return True


def _run_iresearch(tokenizer: str, data: Path, count: int, warmup: int,
                   reverse: bool = False, debug: bool = False) -> Optional[BenchResult]:
    name = f"BenchmarkIresearch/{tokenizer.capitalize()}"

    binary = _iresearch_binary()
    if binary is None:
        print(f" NOT BUILT (run: cmake -S iresearch-bench -B iresearch-bench/build "
              f"-DIRESEARCH_SRC=... && cmake --build iresearch-bench/build)")
        return None

    irs_tokenizer = "path_hierarchy" if tokenizer == "path" else tokenizer
    runs_path = _mk_runs_dump_path()
    parsed: Optional[BenchResult] = None
    combined = ""
    try:
        cmd = [
            str(binary),
            "--data", str(data),
            "--tokenizer", irs_tokenizer,
            "--runs", str(count),
            "--warmup", str(warmup),
            "--bench-runs-file", str(runs_path.resolve()),
        ]
        if reverse and tokenizer == "path":
            cmd.append("--reverse")

        print(f"  {name} ...", end="", flush=True)
        result = subprocess.run(
            cmd, capture_output=True, text=True, stdin=subprocess.DEVNULL
        )
        combined = result.stdout + result.stderr

        if result.returncode != 0:
            print(" FAILED")
            _print_subprocess_err(combined)
            return None

        if debug:
            _echo_captured_stdout(result)
        parsed = _parse_run_output(combined, name, runs_path=runs_path)
    finally:
        runs_path.unlink(missing_ok=True)

    if parsed:
        print(
            f"  {_fmt_ns(parsed.mean_ns)} mean  p50={_fmt_ns(parsed.p50_ns)}  "
            f"95% CI [{_fmt_ns(parsed.ci_lo_ns)}, {_fmt_ns(parsed.ci_hi_ns)}]  "
            f"99% CI [{_fmt_ns(parsed.ci99_lo_ns)}, {_fmt_ns(parsed.ci99_hi_ns)}]  "
            f"({parsed.runs} runs, {parsed.lines:,} lines)"
        )
    else:
        print(" PARSE ERROR")
        _print_subprocess_err(combined[:500])
    return parsed


_RUNNERS = {"lucene": _run_lucene, "tantivy": _run_tantivy, "iresearch": _run_iresearch}


def _check_checksums(results: list[BenchResult]) -> None:
    """Compare checksums across all systems for each tokenizer type."""
    by_tok: dict[str, dict[str, int]] = {}
    for r in results:
        parts = r.name.split("/")  # "BenchmarkLucene/Pattern"
        if len(parts) != 2 or r.checksum is None:
            continue
        tok = parts[1].lower()
        sys_name = parts[0].replace("Benchmark", "").lower()  # "lucene", "tantivy", "iresearch"
        by_tok.setdefault(tok, {})[sys_name] = r.checksum

    print()
    all_ok = True
    for tok, checksums in sorted(by_tok.items()):
        if len(checksums) < 2:
            continue  # only one system ran, nothing to compare
        label = f"checksum/{tok.capitalize()}"
        values = list(checksums.values())
        all_match = all(v == values[0] for v in values)
        detail = "  ".join(f"{s}={c}" for s, c in sorted(checksums.items()))
        if all_match:
            print(f"  {label}  {_color('OK', _GREEN)}  {detail}")
        else:
            print(f"  {label}  {_color('MISMATCH', _RED)}  {detail}")
            all_ok = False

    if not all_ok:
        sys.exit(1)

def _fmt_tok_per_sec(tokens: int, mean_ns: float) -> str:
    tps = tokens / mean_ns * 1e9
    if tps >= 1e9:
        return f"{tps / 1e9:.2f}G"
    if tps >= 1e6:
        return f"{tps / 1e6:.2f}M"
    if tps >= 1e3:
        return f"{tps / 1e3:.2f}K"
    return f"{tps:.0f}"


def _fmt_ns(ns: float) -> str:
    if ns >= 1e9:
        return f"{ns / 1e9:.3f}s"
    if ns >= 1e6:
        return f"{ns / 1e6:.3f}ms"
    if ns >= 1e3:
        return f"{ns / 1e3:.3f}µs"
    return f"{ns:.0f}ns"


def _print_subprocess_err(text: str) -> None:
    for line in text.strip().splitlines():
        print(f"    {line}", file=sys.stderr)


def _echo_captured_stdout(result: subprocess.CompletedProcess) -> None:
    out = result.stdout
    if not isinstance(out, str) or not out.strip():
        return
    print()
    for line in out.splitlines():
        print(f"    {line}")


_GREEN = "\033[32m"
_RED   = "\033[31m"
_RESET = "\033[0m"


def _color(text: str, code: str) -> str:
    return f"{code}{text}{_RESET}" if sys.stdout.isatty() else text

def _build_file_content(results: list[BenchResult], meta: str) -> str:
    lines = [
        "goos: linux",
        "pkg: benchmark-tokenizers",
        f"# {meta}",
        "",
    ]
    lines += [r.to_line() for r in results]
    lines += ["", "ok  benchmark-tokenizers"]
    return "\n".join(lines) + "\n"


def _print_results_table(results: list[BenchResult]) -> None:
    col = max(len(r.name) for r in results)
    has_tokens = any(r.tokens is not None for r in results)
    tok_hdr = f" {'tok/s':>8}" if has_tokens else ""
    w = 9
    ci95_w = 22
    ci99_w = 22
    hdr = (
        f"{'name':<{col}} {'mean':>{w}} {'p50':>{w}} {'p95':>{w}} {'p99':>{w}} {'p100':>{w}}"
        f" {'95%CI':^{ci95_w}} {'99%CI':^{ci99_w}}{tok_hdr}"
    )
    sep = "─" * len(hdr)
    print(f"\n{sep}")
    print("RESULTS")
    print(sep)
    print(hdr)
    print(sep)
    for r in results:
        tok_col = ""
        if has_tokens:
            tok_col = f" {_fmt_tok_per_sec(r.tokens, r.mean_ns):>8}" if r.tokens else f" {'--':>8}"
        ci95_txt = f"{_fmt_ns(r.ci_lo_ns)}..{_fmt_ns(r.ci_hi_ns)}"
        ci99_txt = f"{_fmt_ns(r.ci99_lo_ns)}..{_fmt_ns(r.ci99_hi_ns)}"
        print(
            f"{r.name:<{col}}"
            f" {_fmt_ns(r.mean_ns):>{w}}"
            f" {_fmt_ns(r.p50_ns):>{w}}"
            f" {_fmt_ns(r.p95_ns):>{w}}"
            f" {_fmt_ns(r.p99_ns):>{w}}"
            f" {_fmt_ns(r.p100_ns):>{w}}"
            f" {ci95_txt:^{ci95_w}}"
            f" {ci99_txt:^{ci99_w}}"
            f"{tok_col}"
        )
    print(sep)


def _do_compare(old_path: str, new_path: str) -> None:
    old = _parse_result_file(old_path)
    new = _parse_result_file(new_path)
    all_names = sorted(set(old) | set(new))

    if not all_names:
        print("No benchmark results found in the files.", file=sys.stderr)
        return

    col = max(len(n) for n in all_names) + 2
    hdr = f"{'name':<{col}}  {'old':>10}  {'new':>10}  {'delta':>9}"
    sep = "─" * len(hdr)
    print(f"\n{sep}")
    print(f"COMPARISON  {Path(old_path).name}  ->  {Path(new_path).name}")
    print(sep)
    print(hdr)
    print(sep)

    def _row(label: str, old_ns: float, new_ns: float) -> None:
        pct = (new_ns - old_ns) / old_ns * 100
        sign = "+" if pct > 0 else ""
        delta_str = f"{sign}{pct:.2f}%"
        if pct < -3:
            delta_str = _color(delta_str, _GREEN)
        elif pct > 3:
            delta_str = _color(delta_str, _RED)
        print(
            f"{label:<{col}}"
            f"  {_fmt_ns(old_ns):>10}"
            f"  {_fmt_ns(new_ns):>10}"
            f"  {delta_str:>9}"
        )

    for name in all_names:
        o = old.get(name)
        n = new.get(name)
        if o and n:
            _row(name, o.mean_ns, n.mean_ns)
            _row(f"  p50", o.p50_ns, n.p50_ns)
            _row(f"  p95", o.p95_ns, n.p95_ns)
            _row(f"  p99", o.p99_ns, n.p99_ns)
            _row(f"  p100", o.p100_ns, n.p100_ns)
            _row(f"  ci95_lo", o.ci_lo_ns, n.ci_lo_ns)
            _row(f"  ci95_hi", o.ci_hi_ns, n.ci_hi_ns)
            _row(f"  ci99_lo", o.ci99_lo_ns, n.ci99_lo_ns)
            _row(f"  ci99_hi", o.ci99_hi_ns, n.ci99_hi_ns)
        elif o:
            print(f"{name:<{col}}  {'--':>10}  {'(missing)':>10}")
        else:
            print(f"{name:<{col}}  {'(missing)':>10}  {'--':>10}")

    print(sep)

_ALL_TOKENIZERS = ["pattern", "path"]
_ALL_SYSTEMS    = ["lucene", "tantivy", "iresearch"]


def _add_run_args(p: argparse.ArgumentParser) -> None:
    p.add_argument(
        "--bench", metavar="REGEXP", default=".",
        help=(
            "Run benchmarks whose name matches REGEXP. "
            "Use 'pattern', 'path', or '.' for all. (default: .)"
        ),
    )
    p.add_argument(
        "--systems", metavar="LIST", default="all",
        help=(
            "Comma-separated systems to include: lucene, tantivy, or 'all'. "
            "(default: all)"
        ),
    )
    p.add_argument(
        "--count", "-n", type=int, metavar="N", default=10,
        help="Number of timed runs per benchmark. (default: 10)",
    )
    p.add_argument(
        "--warmup", type=int, metavar="N", default=2,
        help="Number of warmup runs (excluded from results). (default: 2)",
    )
    p.add_argument(
        "--data", metavar="FILE", default="test_words.txt",
        help="Path to input data file. (default: test_words.txt in repo root)",
    )
    p.add_argument(
        "-o", metavar="FILE",
        help="Save results to FILE in go-bench format.",
    )
    p.add_argument(
        "--compare", metavar="FILE",
        help="After running, compare new results against FILE (a previous -o output).",
    )
    p.add_argument(
        "--reverse", action="store_true",
        help="Run path tokenizer in reverse mode (ReversePathHierarchyTokenizer). Tantivy is excluded.",
    )
    p.add_argument(
        "--debug", action="store_true",
        help="Echo native benchmark stdout after capture (tokenizer=…, time_ms/time_ns, checksum). "
        "Default: stdout is only parsed, not printed.",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="bench.py",
        description="Tokenizer benchmark runner -- go-bench style interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  python bench.py
  python bench.py --bench pattern --systems lucene,tantivy --count 20 --data data/wiki.txt
  python bench.py --count 20 --data data/wiki.txt -o results/run1.txt
  python bench.py --count 20 --data data/wiki.txt -o results/run2.txt --compare results/run1.txt
  python bench.py compare results/run1.txt results/run2.txt
        """,
    )
    sub = parser.add_subparsers(dest="cmd")
    _add_run_args(parser)

    cmp_p = sub.add_parser("compare", help="Compare two saved result files")
    cmp_p.add_argument("old", help="Previous results file")
    cmp_p.add_argument("new", help="New results file")

    args = parser.parse_args()

    if args.cmd == "compare":
        for f in (args.old, args.new):
            if not Path(f).exists():
                parser.error(f"file not found: {f}")
        _do_compare(args.old, args.new)
        return

    bench_re = args.bench.lower()
    tokenizers = (
        _ALL_TOKENIZERS
        if bench_re == "."
        else [t for t in _ALL_TOKENIZERS if re.search(bench_re, t)]
    )
    if not tokenizers:
        parser.error(
            f"--bench {args.bench!r} matched nothing; "
            f"available: {', '.join(_ALL_TOKENIZERS)}"
        )

    if args.systems.lower() == "all":
        systems = _ALL_SYSTEMS
    else:
        systems = [s.strip() for s in args.systems.split(",")]
        unknown = [s for s in systems if s not in _ALL_SYSTEMS]
        if unknown:
            parser.error(
                f"unknown system(s): {unknown}; "
                f"available: {', '.join(_ALL_SYSTEMS)}"
            )

    data = Path(args.data).resolve()
    if not data.exists():
        parser.error(f"data file not found: {args.data}")

    print(f"tokenizers: {', '.join(tokenizers)}")
    print(f"systems:    {', '.join(systems)}")
    print(f"count:      {args.count}  warmup: {args.warmup}")
    print(f"data:       {data}")

    reverse = getattr(args, "reverse", False)
    debug = getattr(args, "debug", False)

    results: list[BenchResult] = []
    for tok in tokenizers:
        print(f"\n--- {tok} ---")
        for sys_name in systems:
            r = _RUNNERS[sys_name](tok, data, args.count, args.warmup, reverse, debug)
            if r:
                results.append(r)

    if not results:
        print("\nNo results collected.", file=sys.stderr)
        sys.exit(1)

    _print_results_table(results)
    _check_checksums(results)

    meta = (
        f"date={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        f"  data={args.data}  count={args.count}  warmup={args.warmup}"
    )
    output_text = _build_file_content(results, meta)

    saved_path: Optional[str] = None
    if args.o:
        Path(args.o).parent.mkdir(parents=True, exist_ok=True)
        Path(args.o).write_text(output_text)
        saved_path = args.o
        print(f"\nResults saved -> {args.o}")

    if args.compare:
        if not Path(args.compare).exists():
            print(f"Warning: --compare file not found: {args.compare}", file=sys.stderr)
        else:
            cleanup_tmp = False
            if not saved_path:
                tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False)
                tmp.write(output_text)
                tmp.close()
                saved_path = tmp.name
                cleanup_tmp = True
            _do_compare(args.compare, saved_path)
            if cleanup_tmp:
                os.unlink(saved_path)


if __name__ == "__main__":
    main()
