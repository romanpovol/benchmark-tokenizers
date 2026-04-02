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
import re
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
            f"\t{self.p50_ns:.0f} p50-ns"
            f"\t{self.p95_ns:.0f} p95-ns"
            f"\t{self.p99_ns:.0f} p99-ns"
            f"\t{self.p100_ns:.0f} p100-ns"
        )

_HEADER_RE   = re.compile(r"tokenizer=\S+\s+runs=(\d+)\s+lines=(\d+)(?:\s+tokens=(\d+))?")
_NS_RE       = re.compile(
    r"time_ns\s+p50=(\d+(?:\.\d+)?)\s+p95=(\d+(?:\.\d+)?)"
    r"\s+p99=(\d+(?:\.\d+)?)\s+p100=(\d+(?:\.\d+)?)\s+mean=(\d+(?:\.\d+)?)"
)
_CHECKSUM_RE = re.compile(r"^checksum=(-?\d+)", re.MULTILINE)
_LINE_RE     = re.compile(
    r"(Benchmark\S+)\s+(\d+)\s+(\d+(?:\.\d+)?)\s+ns/op"
    r"\s+(\d+(?:\.\d+)?)\s+p50-ns"
    r"\s+(\d+(?:\.\d+)?)\s+p95-ns"
    r"\s+(\d+(?:\.\d+)?)\s+p99-ns"
    r"\s+(\d+(?:\.\d+)?)\s+p100-ns"
)


def _parse_run_output(text: str, name: str) -> Optional[BenchResult]:
    h = _HEADER_RE.search(text)
    n = _NS_RE.search(text)
    if not h or not n:
        return None
    cs_m = _CHECKSUM_RE.search(text)
    return BenchResult(
        name=name,
        runs=int(h.group(1)),
        lines=int(h.group(2)),
        tokens=int(h.group(3)) if h.group(3) else None,
        p50_ns=float(n.group(1)),
        p95_ns=float(n.group(2)),
        p99_ns=float(n.group(3)),
        p100_ns=float(n.group(4)),
        mean_ns=float(n.group(5)),
        checksum=int(cs_m.group(1)) if cs_m else None,
    )


def _parse_result_file(path: str) -> dict[str, BenchResult]:
    results: dict[str, BenchResult] = {}
    with open(path) as f:
        for raw in f:
            m = _LINE_RE.search(raw)
            if m:
                name = m.group(1)
                results[name] = BenchResult(
                    name=name,
                    runs=int(m.group(2)),
                    lines=0,
                    mean_ns=float(m.group(3)),
                    p50_ns=float(m.group(4)),
                    p95_ns=float(m.group(5)),
                    p99_ns=float(m.group(6)),
                    p100_ns=float(m.group(7)),
                )
    return results

def _run_lucene(tokenizer: str, data: Path, count: int, warmup: int,
                reverse: bool = False) -> Optional[BenchResult]:
    name = f"BenchmarkLucene/{tokenizer.capitalize()}"
    rev_flag = " --reverse" if reverse else ""
    args_str = f"{data} {tokenizer} --runs {count} --warmup {warmup}{rev_flag}"
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

    parsed = _parse_run_output(combined, name)
    if parsed:
        print(f"  {_fmt_ns(parsed.mean_ns)} mean  ({parsed.runs} runs, {parsed.lines:,} lines)")
    else:
        print(" PARSE ERROR")
        _print_subprocess_err(combined[:500])
    return parsed


def _run_tantivy(tokenizer: str, data: Path, count: int, warmup: int,
                 reverse: bool = False) -> Optional[BenchResult]:
    if reverse and tokenizer == "path":
        # Tantivy FacetTokenizer has no reverse mode
        return None
    name = f"BenchmarkTantivy/{tokenizer.capitalize()}"
    tantivy_type = {"pattern": "regex", "path": "facet"}[tokenizer]
    cmd = [
        "cargo", "run", "--release", "-q", "--",
        "--data", str(data),
        "--tokenizer", tantivy_type,
        "--runs", str(count),
        "--warmup", str(warmup),
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

    parsed = _parse_run_output(combined, name)
    if parsed:
        print(f"  {_fmt_ns(parsed.mean_ns)} mean  ({parsed.runs} runs, {parsed.lines:,} lines)")
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
                   reverse: bool = False) -> Optional[BenchResult]:
    name = f"BenchmarkIresearch/{tokenizer.capitalize()}"

    binary = _iresearch_binary()
    if binary is None:
        print(f" NOT BUILT (run: cmake -S iresearch-bench -B iresearch-bench/build "
              f"-DIRESEARCH_SRC=... && cmake --build iresearch-bench/build)")
        return None

    irs_tokenizer = "path_hierarchy" if tokenizer == "path" else tokenizer
    cmd = [
        str(binary),
        "--data", str(data),
        "--tokenizer", irs_tokenizer,
        "--runs", str(count),
        "--warmup", str(warmup),
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

    parsed = _parse_run_output(combined, name)
    if parsed:
        print(f"  {_fmt_ns(parsed.mean_ns)} mean  ({parsed.runs} runs, {parsed.lines:,} lines)")
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
    tok_hdr = f"  {'tok/s':>10}" if has_tokens else ""
    hdr = f"{'name':<{col}}  {'mean':>10}  {'p50':>10}  {'p95':>10}  {'p99':>10}  {'p100':>10}{tok_hdr}"
    sep = "─" * len(hdr)
    print(f"\n{sep}")
    print("RESULTS")
    print(sep)
    print(hdr)
    print(sep)
    for r in results:
        tok_col = ""
        if has_tokens:
            tok_col = f"  {_fmt_tok_per_sec(r.tokens, r.mean_ns):>10}" if r.tokens else f"  {'--':>10}"
        print(
            f"{r.name:<{col}}"
            f"  {_fmt_ns(r.mean_ns):>10}"
            f"  {_fmt_ns(r.p50_ns):>10}"
            f"  {_fmt_ns(r.p95_ns):>10}"
            f"  {_fmt_ns(r.p99_ns):>10}"
            f"  {_fmt_ns(r.p100_ns):>10}"
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
    print(f"COMPARISON  {Path(old_path).name}  →  {Path(new_path).name}")
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
        "--data", metavar="FILE", default="tantivy-bench/test_words.txt",
        help="Path to input data file. (default: tantivy-bench/test_words.txt)",
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

    results: list[BenchResult] = []
    for tok in tokenizers:
        print(f"\n--- {tok} ---")
        for sys_name in systems:
            r = _RUNNERS[sys_name](tok, data, args.count, args.warmup, reverse)
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
        print(f"\nResults saved → {args.o}")

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
