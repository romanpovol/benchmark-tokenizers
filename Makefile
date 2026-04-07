DATA    ?= tantivy-bench/test_words.txt
COUNT   ?= 10
WARMUP  ?= 2
SYSTEMS ?= all
# OUTPUT  -- set to save results, e.g.  make bench OUTPUT=results/run1.txt
# COMPARE -- set to compare against a previous run, e.g. COMPARE=results/run1.txt
# REVERSE -- set to 1 to use reverse path hierarchy, e.g. make bench-path REVERSE=1

# Profiling options (used by profile-iresearch)
#   PROF_TOKENIZER -- tokenizer to profile: pattern or path (default: pattern)
#   PROF_COUNT     -- number of runs inside the profiled process (default: 100)
#   PROF_MODE      -- perf | perf-stat | callgrind (default: perf)
#   PROF_OUT       -- output file/directory (default: profile/)
PROF_TOKENIZER ?= pattern
PROF_COUNT     ?= 100
PROF_MODE      ?= perf
PROF_OUT       ?= profile

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

_IRESEARCH_BIN = $(IRESEARCH_BUILD)/bin/iresearch-bench
_PROF_TOKENIZER = $(if $(filter path,$(PROF_TOKENIZER)),path_hierarchy,$(PROF_TOKENIZER))
_PROF_ARGS = --data $(DATA) --tokenizer $(_PROF_TOKENIZER) --runs $(PROF_COUNT) --warmup $(WARMUP) \
             $(if $(filter 1 true yes,$(REVERSE)),--reverse)

.PHONY: help bench bench-pattern bench-path bench-lucene bench-tantivy bench-iresearch \
        iresearch-build iresearch-build-prof profile-iresearch compare

help:
	@echo "Tokenizer benchmark runner"
	@echo ""
	@echo "Targets:"
	@printf "  %-20s %s\n" bench              "run all benchmarks"
	@printf "  %-20s %s\n" bench-pattern      "run pattern/regex benchmarks only"
	@printf "  %-20s %s\n" bench-path         "run path/facet benchmarks only"
	@printf "  %-20s %s\n" bench-lucene       "run Lucene benchmarks only"
	@printf "  %-20s %s\n" bench-tantivy      "run Tantivy benchmarks only"
	@printf "  %-20s %s\n" bench-iresearch 	  "run SereneDB benchmarks only"
	@printf "  %-20s %s\n" iresearch-build      "build iresearch-bench (needs IRESEARCH_SRC=)"
	@printf "  %-20s %s\n" iresearch-build-prof "rebuild serenedb+RE2 with frame pointers for profiling"
	@printf "  %-20s %s\n" profile-iresearch    "profile iresearch-bench (perf flamegraph / callgrind)"
	@printf "  %-20s %s\n" compare            "compare OLD= and NEW= result files"
	@echo ""
	@echo "Variables:"
	@printf "  %-18s %s\n" "DATA=<file>"    "input data file (default: $(DATA))"
	@printf "  %-18s %s\n" "COUNT=<n>"      "count runs      (default: $(COUNT))"
	@printf "  %-18s %s\n" "WARMUP=<n>"     "warmup runs     (default: $(WARMUP))"
	@printf "  %-18s %s\n" "SYSTEMS=<list>" "lucene, tantivy, SereneDB, or all (default: $(SYSTEMS))"
	@printf "  %-18s %s\n" "OUTPUT=<file>"  "save results to file"
	@printf "  %-18s %s\n" "COMPARE=<file>" "compare against a previous OUTPUT file"
	@printf "  %-18s %s\n" "REVERSE=1"         "reverse path hierarchy mode (path tokenizer only, no Tantivy)"
	@echo ""
	@echo "Profiling variables (profile-SereneDB):"
	@printf "  %-18s %s\n" "PROF_TOKENIZER="  "pattern or path (default: $(PROF_TOKENIZER))"
	@printf "  %-18s %s\n" "PROF_COUNT=<n>"   "runs inside profiled process (default: $(PROF_COUNT))"
	@printf "  %-18s %s\n" "PROF_MODE="       "perf | perf-stat | callgrind (default: $(PROF_MODE))"
	@printf "  %-18s %s\n" "PROF_OUT=<dir>"   "output directory (default: $(PROF_OUT))"

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

# iresearch-build-prof: rebuilds ALL of SereneDB (including RE2/abseil) with
# -fno-omit-frame-pointer so perf can unwind through library calls.
# Use the result with: make profile-iresearch IRESEARCH_BUILD=../serenedb/build_prof ...
iresearch-build-prof:
	@test -n "$(IRESEARCH_SRC)" || { \
	  echo "Usage: make iresearch-build-prof IRESEARCH_SRC=/path/to/serenedb"; \
	  exit 1; }
	@echo "Configuring serenedb with frame pointers (build_prof) ..."
	cmake -S $(abspath $(IRESEARCH_SRC)) \
	  -B $(abspath $(IRESEARCH_SRC))/build_prof \
	  --preset bench \
	  -DCMAKE_C_COMPILER=clang-21 \
	  -DCMAKE_CXX_COMPILER=clang++-21 \
	  -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON \
	  -DCMAKE_C_FLAGS="-fno-omit-frame-pointer" \
	  -DCMAKE_CXX_FLAGS="-fno-omit-frame-pointer"
	@echo "Building iresearch-static ..."
	cmake --build $(abspath $(IRESEARCH_SRC))/build_prof \
	  --target iresearch-static -j$(shell nproc)
	@# Inject and build iresearch-bench
	mkdir -p $(abspath $(IRESEARCH_SRC))/tests/bench/iresearch-bench
	cp iresearch-bench/main.cpp iresearch-bench/CMakeLists.txt \
	  $(abspath $(IRESEARCH_SRC))/tests/bench/iresearch-bench/
	@grep -qF 'iresearch-bench' \
	  $(abspath $(IRESEARCH_SRC))/tests/bench/CMakeLists.txt || \
	  echo 'add_subdirectory(iresearch-bench)' \
	  >> $(abspath $(IRESEARCH_SRC))/tests/bench/CMakeLists.txt
	cmake --build $(abspath $(IRESEARCH_SRC))/build_prof \
	  --target iresearch-bench -j$(shell nproc)
	@# Clean up serenedb
	cd $(abspath $(IRESEARCH_SRC)) && git restore tests/bench/CMakeLists.txt
	rm -rf $(abspath $(IRESEARCH_SRC))/tests/bench/iresearch-bench
	@echo ""
	@echo "Profile binary: $(abspath $(IRESEARCH_SRC))/build_prof/bin/iresearch-bench"
	@echo "Run with: make profile-iresearch IRESEARCH_BUILD=$(abspath $(IRESEARCH_SRC))/build_prof DATA=... PROF_TOKENIZER=pattern"

_FLAMEGRAPH_DIR ?= /tmp/FlameGraph
_KERNEL_VER     = $(shell uname -r)
_PERF_PKG       = linux-tools-$(_KERNEL_VER) linux-tools-generic

# Install perf if missing (requires sudo)
_ensure_perf:
	@if ! command -v perf > /dev/null 2>&1; then \
	  echo "perf not found -- installing $(_PERF_PKG) ..."; \
	  sudo apt-get install -y $(_PERF_PKG); \
	fi

# Install valgrind if missing (requires sudo)
_ensure_valgrind:
	@if ! command -v valgrind > /dev/null 2>&1; then \
	  echo "valgrind not found -- installing ..."; \
	  sudo apt-get install -y valgrind; \
	fi

# Clone FlameGraph scripts if missing (no root needed)
_ensure_flamegraph:
	@if [ ! -f "$(_FLAMEGRAPH_DIR)/flamegraph.pl" ]; then \
	  echo "FlameGraph not found -- cloning to $(_FLAMEGRAPH_DIR) ..."; \
	  git clone --depth=1 https://github.com/brendangregg/FlameGraph $(_FLAMEGRAPH_DIR); \
	fi

.PHONY: _ensure_perf _ensure_valgrind _ensure_flamegraph

profile-iresearch:
	@test -f "$(_IRESEARCH_BIN)" || { \
	  echo "iresearch-bench not found at $(_IRESEARCH_BIN)"; \
	  echo "Run: make iresearch-build IRESEARCH_SRC=/path/to/serenedb"; \
	  exit 1; }
	@mkdir -p $(PROF_OUT)
	@echo "Profiling: $(_IRESEARCH_BIN)"
	@echo "  tokenizer=$(PROF_TOKENIZER)  runs=$(PROF_COUNT)  mode=$(PROF_MODE)"
	@echo "  data=$(DATA)  output=$(PROF_OUT)/"
	@echo ""
ifeq ($(PROF_MODE),perf)
	$(MAKE) _ensure_perf _ensure_flamegraph
	perf record -g -F 999 -o $(PROF_OUT)/perf.data -- \
	  $(_IRESEARCH_BIN) $(_PROF_ARGS)
	perf script -i $(PROF_OUT)/perf.data \
	  | $(_FLAMEGRAPH_DIR)/stackcollapse-perf.pl \
	  | $(_FLAMEGRAPH_DIR)/flamegraph.pl > $(PROF_OUT)/flamegraph.svg
	@echo ""
	@echo "Flamegraph: $(PROF_OUT)/flamegraph.svg"
	@echo "Raw data:   $(PROF_OUT)/perf.data  (perf report -i $(PROF_OUT)/perf.data)"
else ifeq ($(PROF_MODE),perf-stat)
	$(MAKE) _ensure_perf
	perf stat -d -d -d -- $(_IRESEARCH_BIN) $(_PROF_ARGS)
else ifeq ($(PROF_MODE),callgrind)
	$(MAKE) _ensure_valgrind
	valgrind --tool=callgrind \
	  --callgrind-out-file=$(PROF_OUT)/callgrind.out \
	  --cache-sim=yes --branch-sim=yes \
	  $(_IRESEARCH_BIN) $(_PROF_ARGS)
	@echo ""
	@echo "Callgrind output: $(PROF_OUT)/callgrind.out"
	@echo "Open with: kcachegrind $(PROF_OUT)/callgrind.out"
else
	@echo "Unknown PROF_MODE=$(PROF_MODE). Use: perf | perf-stat | callgrind"; exit 1
endif

compare:
	@test -n "$(OLD)" || { echo "Usage: make compare OLD=<file> NEW=<file>"; exit 1; }
	@test -n "$(NEW)" || { echo "Usage: make compare OLD=<file> NEW=<file>"; exit 1; }
	python3 bench.py compare $(OLD) $(NEW)
