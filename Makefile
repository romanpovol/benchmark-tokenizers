DATA    ?= tantivy-bench/test_words.txt
COUNT   ?= 10
WARMUP  ?= 2
SYSTEMS ?= all
# OUTPUT  -- set to save results, e.g.  make bench OUTPUT=results/run1.txt
# COMPARE -- set to compare against a previous run, e.g. COMPARE=results/run1.txt
# REVERSE -- set to 1 to use reverse path hierarchy, e.g. make bench-path REVERSE=1

_OUTPUT_ARG  = $(if $(OUTPUT),-o $(OUTPUT))
_COMPARE_ARG = $(if $(COMPARE),--compare $(COMPARE))
_REVERSE_ARG = $(if $(filter 1 true yes,$(REVERSE)),--reverse)
_BASE        = --systems $(SYSTEMS) --count $(COUNT) --warmup $(WARMUP) \
               --data $(DATA) $(_OUTPUT_ARG) $(_COMPARE_ARG) $(_REVERSE_ARG)

# Path to cloned iresearch/serenedb repo
# export IRESEARCH_SRC=/path/to/serenedb
# make bench-iresearch IRESEARCH_SRC=/path/to/serenedb
#
# By default uses serenedb/build (whatever preset was last configured).
# For benchmarking, use a Release build:
#   cd /path/to/serenedb && cmake --preset bench -DCMAKE_C_COMPILER=clang-21 -DCMAKE_CXX_COMPILER=clang++-21 && ninja iresearch-bench
# Or point to an existing Release build dir:
#   make iresearch-build IRESEARCH_SRC=../serenedb IRESEARCH_BUILD=../serenedb/build-release
# Auto-detect Release build dir: prefer build_bench (bench preset), fall back to build
_SDB_ABS     = $(if $(IRESEARCH_SRC),$(abspath $(IRESEARCH_SRC)),)
_SDB_BENCH   = $(_SDB_ABS)/build_bench
_SDB_DEFAULT = $(if $(wildcard $(_SDB_BENCH)/bin/iresearch-bench),$(_SDB_BENCH),$(_SDB_ABS)/build)
IRESEARCH_BUILD ?= $(_SDB_DEFAULT)

.PHONY: help bench bench-pattern bench-path bench-lucene bench-tantivy bench-iresearch iresearch-build compare

help:
	@echo "Tokenizer benchmark runner"
	@echo ""
	@echo "Targets:"
	@printf "  %-20s %s\n" bench           "run all benchmarks"
	@printf "  %-20s %s\n" bench-pattern   "run pattern/regex benchmarks only"
	@printf "  %-20s %s\n" bench-path      "run path/facet benchmarks only"
	@printf "  %-20s %s\n" bench-lucene    "run Lucene benchmarks only"
	@printf "  %-20s %s\n" bench-tantivy   "run Tantivy benchmarks only"
	@printf "  %-20s %s\n" bench-iresearch "run iresearch benchmarks only"
	@printf "  %-20s %s\n" iresearch-build "build iresearch-bench (needs IRESEARCH_SRC=)"
	@printf "  %-20s %s\n" compare         "compare OLD= and NEW= result files"
	@echo ""
	@echo "Variables:"
	@printf "  %-18s %s\n" "DATA=<file>"    "input data file (default: $(DATA))"
	@printf "  %-18s %s\n" "COUNT=<n>"      "count runs      (default: $(COUNT))"
	@printf "  %-18s %s\n" "WARMUP=<n>"     "warmup runs     (default: $(WARMUP))"
	@printf "  %-18s %s\n" "SYSTEMS=<list>" "lucene, tantivy, iresearch, or all (default: $(SYSTEMS))"
	@printf "  %-18s %s\n" "OUTPUT=<file>"  "save results to file"
	@printf "  %-18s %s\n" "COMPARE=<file>" "compare against a previous OUTPUT file"
	@printf "  %-18s %s\n" "REVERSE=1"      "reverse path hierarchy mode (path tokenizer only, no Tantivy)"

bench:
	python3 bench.py --bench . $(_BASE)

bench-pattern:
	python3 bench.py --bench pattern $(_BASE)

bench-path:
	python3 bench.py --bench path $(_BASE)

bench-lucene:
	python3 bench.py --bench . --systems lucene \
	  --count $(COUNT) --warmup $(WARMUP) --data $(DATA) $(_OUTPUT_ARG) $(_COMPARE_ARG)

bench-tantivy:
	python3 bench.py --bench . --systems tantivy \
	  --count $(COUNT) --warmup $(WARMUP) --data $(DATA) $(_OUTPUT_ARG) $(_COMPARE_ARG)

bench-iresearch:
	python3 bench.py --bench . --systems iresearch \
	  --count $(COUNT) --warmup $(WARMUP) --data $(DATA) $(_OUTPUT_ARG) $(_COMPARE_ARG)

iresearch-build:
	@test -n "$(IRESEARCH_SRC)" || { \
	  echo "Usage: make iresearch-build IRESEARCH_SRC=/path/to/serenedb"; \
	  echo "       For Release benchmarks, also set IRESEARCH_BUILD=../serenedb/build-bench"; \
	  exit 1; }
	@# Inject sources into serenedb's bench dir, build, then clean up
	mkdir -p $(abspath $(IRESEARCH_SRC))/tests/bench/iresearch-bench
	cp iresearch-bench/main.cpp iresearch-bench/CMakeLists.txt \
	  $(abspath $(IRESEARCH_SRC))/tests/bench/iresearch-bench/
	@grep -qF 'iresearch-bench' \
	  $(abspath $(IRESEARCH_SRC))/tests/bench/CMakeLists.txt || \
	  echo 'add_subdirectory(iresearch-bench)' \
	  >> $(abspath $(IRESEARCH_SRC))/tests/bench/CMakeLists.txt
	@# Build using serenedb's ninja build tree
	cmake --build $(abspath $(IRESEARCH_BUILD)) \
	  --target iresearch-bench -j$(shell nproc)
	@# Clean up: restore serenedb to its original state
	cd $(abspath $(IRESEARCH_SRC)) && git restore tests/bench/CMakeLists.txt
	rm -rf $(abspath $(IRESEARCH_SRC))/tests/bench/iresearch-bench

compare:
	@test -n "$(OLD)" || { echo "Usage: make compare OLD=<file> NEW=<file>"; exit 1; }
	@test -n "$(NEW)" || { echo "Usage: make compare OLD=<file> NEW=<file>"; exit 1; }
	python3 bench.py compare $(OLD) $(NEW)
