# Tokenizer Benchmark

Сравнительный бенчмарк токенизаторов: **Lucene**, **Tantivy**, **SereneDB**.

Измеряет время токенизации текста и верифицирует, что все системы производят идентичные токены (через контрольную сумму)

## (Lucene + Tantivy)

```bash
cd tantivy-bench && cargo build --release && cd ..

make bench DATA=sample.txt COUNT=5 WARMUP=2
```

Lucene собирается автоматически через Gradle при первом запуске

---

## Добавление iresearch

iresearch-bench компилируется SereneDB

```bash
cd ../serenedb

cmake --preset bench \
  -DCMAKE_C_COMPILER=clang-21 \
  -DCMAKE_CXX_COMPILER=clang++-21 \
  -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON

ninja -C build_bench iresearch-static

cd ../benchmark-tokenizers

make iresearch-build IRESEARCH_SRC=../serenedb
```

Makefile автоматически:
- Копирует `iresearch-bench/` в SereneDB
- Собирает бинарник через `cmake --build`
- Удаляет все изменения из SereneDB

Готовый бинарник: `IRESEARCH_SRC/build_bench/bin/iresearch-bench`

```bash
export IRESEARCH_SRC=../serenedb
make bench DATA=sample.txt COUNT=5 WARMUP=2
```

---

## Все make-таргеты

```
make bench                         # все бенчмарки (все tokenizer-ы * все системы)
make bench-pattern                 # только pattern/regex токенизатор
make bench-path                    # только path/facet токенизатор
make bench-lucene                  # только Lucene
make bench-tantivy                 # только Tantivy
make bench-iresearch               # только iresearch
make iresearch-build               # пересобрать iresearch-bench (нужен IRESEARCH_SRC=)
make compare OLD=a.txt NEW=b.txt   # сравнить два сохранённых результата
```

## Переменные

| Переменная       | Описание                                    | По умолчанию                     |
|------------------|---------------------------------------------|----------------------------------|
| `DATA`           | Входной файл (одна строка = один документ)  | `tantivy-bench/test_words.txt`   |
| `COUNT`          | Число тестовых прогонов                     | `10`                             |
| `WARMUP`         | Число прогревочных прогонов                 | `2`                              |
| `SYSTEMS`        | `lucene`, `tantivy`, `iresearch`, или `all` | `all`                            |
| `OUTPUT`         | Сохранить результаты в файл                 | --                               |
| `COMPARE`        | Сравнить с предыдущим результатом           | --                               |
| `IRESEARCH_SRC`  | Путь к SereneDB                             | --                               |
| `IRESEARCH_BUILD`| Путь к build-директории SereneDB            | `$IRESEARCH_SRC/build_bench`     |

## Примеры

```bash
# Сохранить результаты базового прогона
make bench DATA=sample.txt COUNT=10 OUTPUT=results/baseline.txt

# Сравнить с базовым после изменений
make bench DATA=sample.txt COUNT=10 OUTPUT=results/new.txt COMPARE=results/baseline.txt

# Только pattern-токенизатор, только iresearch, 20 прогонов
make bench-pattern SYSTEMS=iresearch COUNT=20 DATA=data/wiki.txt IRESEARCH_SRC=../serenedb
```

## Проверка корректности

Бенчмарк всегда проверяет, что все системы производят одинаковые токены: вычисляет hash по UTF-8 байтам каждого токена и сравнивает итоговые контрольные суммы

```
checksum/Pattern  OK   iresearch=4066605535946015185  lucene=4066605535946015185  tantivy=4066605535946015185
checksum/Pattern  MISMATCH  iresearch=123...  lucene=456...  tantivy=789...
```

При расхождении бенчмарк завершается с ненулевым кодом
