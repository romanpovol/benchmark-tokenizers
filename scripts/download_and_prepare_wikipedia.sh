#!/usr/bin/env bash
# Download a Wikipedia XML dump (bzip2), run luceneutil WikipediaExtractor on stdin, build wiki_lines.txt.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="${1:-${ROOT}/data/wiki_work}"
mkdir -p "${WORK}"

# Default: Simple English Wikipedia — much smaller than enwiki (~100–300 MB bz2 vs many GB).
# Override: WIKI_DUMP_URL='https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles-multistream1.xml-p1p41242.bz2'
: "${WIKI_DUMP_URL:=https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-pages-articles.xml.bz2}"

DUMP_BZ2="${WORK}/dump.xml.bz2"
EXTRACTED="${WORK}/extracted"
LINES="${WORK}/wiki_lines.txt"

echo "Dump URL: ${WIKI_DUMP_URL}"
echo "Work dir: ${WORK}"

if [[ ! -f "${DUMP_BZ2}" ]]; then
  echo "Downloading (can take a while)…"
  curl -fL --progress-bar -o "${DUMP_BZ2}.part" "${WIKI_DUMP_URL}"
  mv "${DUMP_BZ2}.part" "${DUMP_BZ2}"
else
  echo "Reusing existing ${DUMP_BZ2}"
fi

rm -rf "${EXTRACTED}"
mkdir -p "${EXTRACTED}"

echo "Running WikipediaExtractor (reads XML from bzcat | python3)…"
# -B: English Wikipedia base URL for <doc> metadata (text language still follows dump)
bzcat "${DUMP_BZ2}" | python3 "${ROOT}/scripts/WikipediaExtractor.py" \
  -b50m \
  -o "${EXTRACTED}" \
  -B "https://simple.wikipedia.org/wiki/"

echo "Building one-line-per-doc file…"
python3 "${ROOT}/scripts/extract_wiki_lines.py" "${EXTRACTED}" "${LINES}"

echo "Done: ${LINES}"
wc -l "${LINES}"
