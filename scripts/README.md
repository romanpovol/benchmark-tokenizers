# Wikipedia dataset (luceneutil WikipediaExtractor)

Из корня проекта:

```bash
chmod +x scripts/download_and_prepare_wikipedia.sh
./scripts/download_and_prepare_wikipedia.sh
```

По умолчанию качается **Simple English Wikipedia** (`simplewiki-latest-pages-articles.xml.bz2`) — заметно меньше, чем полный enwiki. Результат: `data/wiki_work/wiki_lines.txt` (одна строка — один документ, как для `LuceneTokenizerPerf` / `tantivy-bench`).

Другой дамп (пример — первый кусок multistream enwiki; имя файла на зеркале может меняться):

```bash
export WIKI_DUMP_URL='https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles-multistream1.xml-p1p41242.bz2'
./scripts/download_and_prepare_wikipedia.sh /path/to/workdir
```

Для enwiki задайте подходящий `-B` в скрипте (base URL) или отредактируйте вызов `WikipediaExtractor.py`.

## Ограничить число строк (быстрый тест)

```bash
python3 scripts/extract_wiki_lines.py data/wiki_work/extracted - --max-docs 10000 > sample.txt
```

## Ручной конвейер

```bash
bzcat dump.xml.bz2 | python3 scripts/WikipediaExtractor.py -b50m -o ./extracted -B 'https://en.wikipedia.org/wiki/'
python3 scripts/extract_wiki_lines.py ./extracted ./wiki_lines.txt
```

Список дампов: [dumps.wikimedia.org](https://dumps.wikimedia.org/).
