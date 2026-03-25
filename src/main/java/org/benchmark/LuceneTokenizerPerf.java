package org.benchmark;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.StringReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Locale;
import java.util.regex.Pattern;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.Tokenizer;
import org.apache.lucene.analysis.path.PathHierarchyTokenizer;
import org.apache.lucene.analysis.pattern.PatternTokenizer;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.apache.lucene.analysis.tokenattributes.OffsetAttribute;
import org.apache.lucene.analysis.tokenattributes.PositionIncrementAttribute;
import org.apache.lucene.util.ArrayUtil;

/**
 * Benchmark Lucene pattern and path-hierarchy tokenizers, following the style of
 * <a href="https://github.com/mikemccand/luceneutil/blob/14054579ee857cb89603027bccef5101d337bb7d/src/extra/perf/TestAnalyzerPerf.java">TestAnalyzerPerf</a>:
 * read lines from a file, for each line run {@code tokenStream} / {@code reset} / {@code incrementToken()}.
 */
public final class LuceneTokenizerPerf {

    private static final int DEFAULT_WARMUP = 2;
    private static final int DEFAULT_RUNS = 20;
    private static final String DEFAULT_PATTERN = "\\w+";

    private LuceneTokenizerPerf() {}

    public static void main(String[] args) throws Exception {
        if (args.length < 2) {
            System.err.println(
                    "Usage: LuceneTokenizerPerf <data-file> <pattern|path> [--regex-pattern REGEX] [--runs N] [--warmup N]");
            System.err.println("pattern  — PatternTokenizer (default regex: " + DEFAULT_PATTERN + ")");
            System.err.println("path     — PathHierarchyTokenizer");
            System.exit(1);
        }

        Path dataFile = Path.of(args[0]);
        String mode = args[1].toLowerCase(Locale.ROOT);
        String regexPattern = DEFAULT_PATTERN;
        int runs = DEFAULT_RUNS;
        int warmup = DEFAULT_WARMUP;

        for (int i = 2; i < args.length; i++) {
            switch (args[i]) {
                case "--regex-pattern" -> {
                    if (i + 1 >= args.length) {
                        throw new IllegalArgumentException("--regex-pattern needs a value");
                    }
                    regexPattern = args[++i];
                }
                case "--runs" -> {
                    if (i + 1 >= args.length) {
                        throw new IllegalArgumentException("--runs needs a value");
                    }
                    runs = Integer.parseInt(args[++i]);
                }
                case "--warmup" -> {
                    if (i + 1 >= args.length) {
                        throw new IllegalArgumentException("--warmup needs a value");
                    }
                    warmup = Integer.parseInt(args[++i]);
                }
                default -> throw new IllegalArgumentException("Unknown option: " + args[i]);
            }
        }

        List<String> lines = loadLines(dataFile);
        if (lines.isEmpty()) {
            System.err.println("No non-empty lines in " + dataFile);
            System.exit(1);
        }

        Pattern compiled = Pattern.compile(regexPattern);
        Analyzer analyzer =
                switch (mode) {
                    case "pattern" -> new PatternAnalyzer(compiled, -1);
                    case "path" -> new PathHierarchyAnalyzer();
                    default ->
                            throw new IllegalArgumentException(
                                    "Second arg must be 'pattern' or 'path', got: " + args[1]);
                };

        for (int w = 0; w < warmup; w++) {
            processAllLinesOnce(analyzer, lines);
        }

        List<Long> runNanos = new ArrayList<>(runs);
        for (int r = 0; r < runs; r++) {
            long t0 = System.nanoTime();
            long hash = processAllLinesOnce(analyzer, lines);
            long elapsed = System.nanoTime() - t0;
            runNanos.add(elapsed);
            // keep hash observable across runs
            if (r == 0) {
                System.err.println("checksum(first run)=" + hash);
            }
        }

        Collections.sort(runNanos);
        int n = runNanos.size();
        long p50 = runNanos.get((int) (n * 0.50));
        long p95 = runNanos.get((int) (n * 0.95));
        long p99 = runNanos.get(Math.min((int) (n * 0.99), n - 1));
        long p100 = runNanos.get(n - 1);
        long mean = runNanos.stream().mapToLong(Long::longValue).sum() / n;

        System.out.printf(
                Locale.ROOT,
                "tokenizer=%s runs=%d lines=%d%n",
                mode,
                runs,
                lines.size());
        System.out.printf(
                Locale.ROOT,
                "time_ms p50=%.2f p95=%.2f p99=%.2f p100=%.2f mean=%.2f%n",
                p50 / 1_000_000.0,
                p95 / 1_000_000.0,
                p99 / 1_000_000.0,
                p100 / 1_000_000.0,
                mean / 1_000_000.0);
        System.out.printf(
                Locale.ROOT,
                "time_ns p50=%d p95=%d p99=%d p100=%d mean=%d%n",
                p50,
                p95,
                p99,
                p100,
                mean);
    }

    private static List<String> loadLines(Path path) throws IOException {
        List<String> out = new ArrayList<>();
        try (BufferedReader reader = Files.newBufferedReader(path, StandardCharsets.UTF_8)) {
            String line;
            while ((line = reader.readLine()) != null) {
                String t = line.trim();
                if (!t.isEmpty()) {
                    out.add(t);
                }
            }
        }
        return out;
    }

    /**
     * One full pass over all lines; per line: same token consumption as TestAnalyzerPerf (hash terms and attributes).
     */
    private static long processAllLinesOnce(Analyzer analyzer, List<String> lines) throws IOException {
        long hash = 0;
        for (String s : lines) {
            try (TokenStream ts = analyzer.tokenStream("field", new StringReader(s))) {
                ts.reset();

                CharTermAttribute termAtt = ts.getAttribute(CharTermAttribute.class);
                PositionIncrementAttribute posIncAtt =
                        ts.hasAttribute(PositionIncrementAttribute.class)
                                ? ts.getAttribute(PositionIncrementAttribute.class)
                                : null;
                OffsetAttribute offsetAtt =
                        ts.hasAttribute(OffsetAttribute.class)
                                ? ts.getAttribute(OffsetAttribute.class)
                                : null;

                while (ts.incrementToken()) {
                    hash += 31L * ArrayUtil.hashCode(termAtt.buffer(), 0, termAtt.length());
                    if (posIncAtt != null) {
                        hash += 31L * posIncAtt.getPositionIncrement();
                    }
                    if (offsetAtt != null) {
                        hash += 31L * offsetAtt.startOffset();
                        hash += 31L * offsetAtt.endOffset();
                    }
                }
                ts.end();
            }
        }
        return hash;
    }

    /** PatternTokenizer with split-style group ({@code group = -1}). */
    private static final class PatternAnalyzer extends Analyzer {
        private final Pattern pattern;
        private final int group;

        PatternAnalyzer(Pattern pattern, int group) {
            this.pattern = pattern;
            this.group = group;
        }

        @Override
        protected TokenStreamComponents createComponents(String fieldName) {
            Tokenizer src = new PatternTokenizer(pattern, group);
            return new TokenStreamComponents(src);
        }
    }

    private static final class PathHierarchyAnalyzer extends Analyzer {
        @Override
        protected TokenStreamComponents createComponents(String fieldName) {
            Tokenizer src = new PathHierarchyTokenizer();
            return new TokenStreamComponents(src);
        }
    }
}
