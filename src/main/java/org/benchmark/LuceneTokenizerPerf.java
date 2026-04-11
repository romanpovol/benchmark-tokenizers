package org.benchmark;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.StringReader;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
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
import org.apache.lucene.analysis.path.ReversePathHierarchyTokenizer;
import org.apache.lucene.analysis.pattern.PatternTokenizer;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;

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
                    "Usage: LuceneTokenizerPerf <data-file> <pattern|path> [--regex-pattern REGEX] [--runs N] [--warmup N] [--reverse] [--bench-runs-file PATH]");
            System.err.println("pattern - PatternTokenizer (default regex: " + DEFAULT_PATTERN + ")");
            System.err.println("path    - PathHierarchyTokenizer (forward); add --reverse for ReversePathHierarchyTokenizer");
            System.exit(1);
        }

        Path dataFile = Path.of(args[0]);
        String mode = args[1].toLowerCase(Locale.ROOT);
        String regexPattern = DEFAULT_PATTERN;
        int runs = DEFAULT_RUNS;
        int warmup = DEFAULT_WARMUP;
        boolean reverse = false;
        Path benchRunsFile = null;
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
                case "--reverse" -> reverse = true;
                case "--bench-runs-file" -> {
                    if (i + 1 >= args.length) {
                        throw new IllegalArgumentException("--bench-runs-file needs a value");
                    }
                    benchRunsFile = Path.of(args[++i]);
                }
                default -> throw new IllegalArgumentException("Unknown option: " + args[i]);
            }
        }

        List<String> lines = loadLines(dataFile);
        if (lines.isEmpty()) {
            System.err.println("No non-empty lines in " + dataFile);
            System.exit(1);
        }

        Pattern compiled = Pattern.compile(regexPattern, Pattern.UNICODE_CHARACTER_CLASS);
        Analyzer analyzer =
                switch (mode) {
                    case "pattern" -> new PatternAnalyzer(compiled, 0);
                    case "path" -> reverse ? new ReversePathHierarchyAnalyzer() : new PathHierarchyAnalyzer();
                    default ->
                            throw new IllegalArgumentException(
                                    "Second arg must be 'pattern' or 'path', got: " + args[1]);
                };

        for (int w = 0; w < warmup; w++) {
            processAllLinesOnce(analyzer, lines);
        }

        long checksum = 0;
        long tokenCount = 0;
        List<Long> runNanos = new ArrayList<>(runs);
        for (int r = 0; r < runs; r++) {
            long t0 = System.nanoTime();
            long[] result = processAllLinesOnce(analyzer, lines);
            long elapsed = System.nanoTime() - t0;
            runNanos.add(elapsed);
            if (r == 0) {
                checksum   = result[0];
                tokenCount = result[1];
            }
        }

        int n = runNanos.size();
        long mean = runNanos.stream().mapToLong(Long::longValue).sum() / n;

        List<Long> sorted = new ArrayList<>(runNanos);
        Collections.sort(sorted);
        long p50 = sorted.get((int) (n * 0.50));
        long p95 = sorted.get((int) (n * 0.95));
        long p99 = sorted.get(Math.min((int) (n * 0.99), n - 1));
        long p100 = sorted.get(n - 1);

        System.out.printf(
                Locale.ROOT,
                "tokenizer=%s runs=%d lines=%d tokens=%d%n",
                mode,
                runs,
                lines.size(),
                tokenCount);
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
        if (benchRunsFile != null) {
            ByteBuffer buf = ByteBuffer.allocate(n * 8).order(ByteOrder.LITTLE_ENDIAN);
            for (long v : runNanos) {
                buf.putLong(v);
            }
            Files.write(benchRunsFile, buf.array());
        }
        System.out.printf(Locale.ROOT, "checksum=%d%n", checksum);
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

    private static long[] processAllLinesOnce(Analyzer analyzer, List<String> lines) throws IOException {
        long h = 0;
        long count = 0;
        for (String s : lines) {
            try (TokenStream ts = analyzer.tokenStream("field", new StringReader(s))) {
                ts.reset();
                CharTermAttribute termAtt = ts.getAttribute(CharTermAttribute.class);
                while (ts.incrementToken()) {
                    count++;
                    for (byte b : termAtt.toString().getBytes(StandardCharsets.UTF_8)) {
                        h = h * 31 + (b & 0xFF);
                    }
                }
                ts.end();
            }
        }
        return new long[]{h, count};
    }

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

    private static final class ReversePathHierarchyAnalyzer extends Analyzer {
        @Override
        protected TokenStreamComponents createComponents(String fieldName) {
            Tokenizer src = new ReversePathHierarchyTokenizer();
            return new TokenStreamComponents(src);
        }
    }
}
