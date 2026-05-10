"""
Kata05: Bloom Filters
http://codekata.com/kata/kata05-bloom-filters/

A Bloom filter is a space-efficient probabilistic data structure for set
membership testing. It never produces false negatives but may produce false
positives at a tunable rate.

Structure:
  - BloomFilter  — core bit-array implementation
  - SpellChecker — domain wrapper loading a word list into a BloomFilter
  - false_positive_experiment — Part 2: measure empirical false positive rate
    by generating random words and checking them against the loaded dictionary
"""

import hashlib
import math
import random
import string
from pathlib import Path

# ---------------------------------------------------------------------------
# Optimal parameter formulae
# ---------------------------------------------------------------------------


def optimal_bit_count(n: int, p: float) -> int:
    """
    Optimal bit array size m for n expected items at false positive rate p.
        m = ceil( -n * ln(p) / ln(2)^2 )
    """
    return math.ceil(-n * math.log(p) / (math.log(2) ** 2))
