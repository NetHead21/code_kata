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


def optimal_hash_count(m: int, n: int) -> int:
    """
    Optimal number of hash functions k for bit array size m and n items.
        k = round( (m/n) * ln(2) )
    """
    return max(1, round((m / n) * math.log(2)))


# ---------------------------------------------------------------------------
# BloomFilter
# ---------------------------------------------------------------------------


class BloomFilter:
    """
    Probabilistic set-membership filter.

    Parameters
    ----------
    capacity : int
        Expected number of items to be inserted.
    false_positive_rate : float
        Desired maximum false positive probability (0 < p < 1).
    """
