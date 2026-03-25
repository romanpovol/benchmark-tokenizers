#!/usr/bin/env python3
"""
Read WikipediaExtractor output (Tanl <doc>…</doc> blocks) and write one UTF-8 line per document
for Lucene/Tantivy line-based benchmarks.
"""
from __future__ import annotations

import argparse
import os
import re
import sys

DOC_BLOCK = re.compile(
    r'<doc id="[^"]*" url="[^"]*" title="[^"]*">\n(.*?)\n</doc>\n',
    re.DOTALL,
)

PARAGRAPH_SEP = "\u2029"


def normalize_body(text: str) -> str:
    t = text.replace(PARAGRAPH_SEP, " ").replace("\n", " ").replace("\r", " ")
    return " ".join(t.split())


def iter_wiki_files(root: str):
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            if name.startswith("wiki_") and not name.endswith(".bz2"):
                yield os.path.join(dirpath, name)


def main() -> None:
    ap = argparse.ArgumentParser(description="Tanl wiki extract → one line per document")
    ap.add_argument("extracted_dir", help="Directory passed to WikipediaExtractor -o")
    ap.add_argument(
        "out_txt",
        nargs="?",
        default="-",
        help="Output .txt (default: stdout)",
    )
    ap.add_argument(
        "--max-docs",
        type=int,
        default=0,
        help="Stop after N documents (0 = no limit)",
    )
    args = ap.parse_args()

    out = open(args.out_txt, "w", encoding="utf-8") if args.out_txt != "-" else sys.stdout
    try:
        n = 0
        for path in sorted(iter_wiki_files(args.extracted_dir)):
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                raw = f.read()
            for m in DOC_BLOCK.finditer(raw):
                line = normalize_body(m.group(1))
                if line:
                    out.write(line + "\n")
                    n += 1
                    if args.max_docs and n >= args.max_docs:
                        return
    finally:
        if out is not sys.stdout:
            out.close()


if __name__ == "__main__":
    main()
