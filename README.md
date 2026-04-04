# Code Kata

A Python collection of coding exercises based on the [Dave Thomas CodeKata series](http://codekata.com), plus a standalone number-to-words converter. Each kata is one implementation module paired with a comprehensive test module.

The exercises range from algorithmic drills to design explorations. Several modules are runnable as small demos directly from the command line.

## Kata index

### Pricing, search, and estimation

| # | Module | Description |
|---|--------|-------------|
| 1 | `kata_1_supermarket_pricing.py` | Composable pricing strategies: unit price, bundle deals, weighted pricing, discounts, and decimal-safe money handling |
| 2 | `kata_2_karate_chop.py` | Binary search implemented five different ways |
| 3 | `kata_3_how_big_how_fast.py` | Storage-size estimates and simple runtime benchmarks |
| 4 | `kata_4_data_munging.py` | Parse weather and football datasets to find the smallest spread or goal difference |

### Probabilistic, word, and review-oriented exercises

| # | Module | Description |
|---|--------|-------------|
| 5 | `kata_5_bloom_filter.py` | Bloom filter implementation, spell-checker wrapper, and false-positive rate experiments |
| 6 | `kata_6_anagrams.py` | Find anagram groups efficiently from a large word list |
| 7 | `kata_7_how_did_i_do.py` | A structured three-pass review model for reflective code analysis |
| 8 | `kata_8_conflicting_objectives.py` | The same compound-word problem implemented for readability, speed, and extensibility |

### Checkout and design trade-offs

| # | Module | Description |
|---|--------|-------------|
| 9 | `kata_9_back_to_checkout.py` | Checkout pricing via pluggable pricing-rule objects |
| 10 | `kata_10_hashes_vs_classes.py` | Compare class-based and dict-based export pipeline designs |
| 11 | `kata_11_sorting_it_out.py` | Fixed-domain counting sort for lottery balls and character sequences |
| 12 | `kata_12_best_sellers.py` | Best-seller tracking with hourly sliding window, minute-level real-time window, and daily batch strategies |

### Parsing, generation, and recursion

| # | Module | Description |
|---|--------|-------------|
| 13 | `kata_13_counting_code_lines.py` | Count Java code lines while correctly handling block/line comments and string literals; state-machine and regex implementations |
| 14 | `kata_14_trigrams.py` | Trigram-based surreal text generation with three tokenisation strategies and configurable dead-end handling |
| 15 | `kata_15_diversion.py` | Count n-digit binary strings with no adjacent 1-bits; iterative DP, memoised recursion, and brute-force implementations; Fibonacci relationship proved and tested |

### Business rules engines

| # | Module | Description |
|---|--------|-------------|
| 16 | `kata_16_business_rules.py` | Payment-handling rules modelled as independent Rule objects driven by a composable RuleEngine (Open/Closed design) |
| 17 | `kata_17_more_business_rules.py` | Full order-processing lifecycle modelled as a Finite State Machine: states, events, guard conditions, and actions expressed as a plain data-driven transition table |

### Additional exercise

| Module | Description |
|--------|-------------|
| `number_to_string_converter.py` | Convert integers, floats, and `Decimal` values into English words, including negatives and decimal fractions |

---

## Repository layout

```text
code_kata/
├── kata_1_supermarket_pricing.py
├── kata_2_karate_chop.py
├── ...
├── kata_17_more_business_rules.py
├── number_to_string_converter.py
├── test_kata_1_supermarket_pricing.py
├── ...
├── test_kata_17_more_business_rules.py
├── test_number_to_string_converter.py
├── data/
│   ├── football.dat        ← used by kata 4
│   ├── weather.dat         ← used by kata 4
│   ├── wordlist.txt        ← used by katas 6 and 8
│   └── words.txt           ← used by kata 5
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Requirements

- Python 3.14+
- `pytest` (declared in `pyproject.toml`)

---

## Setup

### Using `uv` (recommended)

```bash
uv sync
source .venv/bin/activate
```

### Using pip

```bash
python3.14 -m venv .venv
source .venv/bin/activate
pip install -e .
```

---

## Running tests

Full suite:

```bash
python -m pytest -q
```

Single kata:

```bash
python -m pytest -q test_kata_14_trigrams.py
```

Single class or test by name:

```bash
python -m pytest -q test_kata_15_diversion.py::TestFibonacciRelationship
python -m pytest -q test_kata_2_karate_chop.py -k canonical
```

---

## Running kata demos

Most kata modules include a short runnable demo behind `if __name__ == "__main__":`:

```bash
python kata_1_supermarket_pricing.py
python kata_11_sorting_it_out.py
python kata_14_trigrams.py
python kata_15_diversion.py
python kata_16_business_rules.py
python kata_17_more_business_rules.py
```

---

## Development notes

- Each implementation module has a matching `test_*.py` file with comprehensive coverage including edge cases.
- The tests are the authoritative source of truth for intended behaviour.
- The test suite is the primary verification mechanism; demos are for quick manual inspection only.
- `pyproject.toml` declares only `pytest` as a dependency.
- `main.py` is a placeholder and is not the entry point for the project.

---

## Suggested workflow

1. Read the implementation module's docstring to understand the design approach.
2. Read the corresponding test file to see the expected behaviour and edge cases.
3. Run the focused tests to confirm they pass before making changes.
4. Modify or extend the implementation, then re-run the full suite.

```bash
# Example: explore kata 17
python -m pytest -q test_kata_17_more_business_rules.py
python kata_17_more_business_rules.py
```
