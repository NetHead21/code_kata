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

    def __init__(self, capacity: int, false_positive_rate: float = 0.01):
        if capacity <= 0:
            raise ValueError("capacity must be a positive integer")
        if not (0.0 < false_positive_rate < 1.0):
            raise ValueError("false_positive_rate must be in the open interval (0, 1)")

        self.capacity = capacity
        self.false_positive_rate = false_positive_rate
        self.m = optimal_bit_count(capacity, false_positive_rate)
        self.k = optimal_hash_count(self.m, capacity)
        self._bits = bytearray(math.ceil(self.m / 8))
        self._count = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add(self, item: str) -> None:
        """Insert *item* into the filter."""
        for idx in self._hash_indices(item):
            self._bits[idx >> 3] |= 1 << (idx & 7)
        self._count += 1

    def __contains__(self, item: str) -> bool:
        """Return True if *item* is probably in the set; False means definitely not."""
        return all(
            self._bits[idx >> 3] & (1 << (idx & 7)) for idx in self._hash_indices(item)
        )

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    @property
    def count(self) -> int:
        """Number of items added (may include duplicates)."""
        return self._count

    @property
    def bit_count(self) -> int:
        """Total number of bits in the underlying array."""
        return self.m

    @property
    def hash_count(self) -> int:
        """Number of independent hash functions used."""
        return self.k

    @property
    def fill_ratio(self) -> float:
        """Fraction of bits currently set to 1."""
        bits_set = sum(bin(b).count("1") for b in self._bits)
        return bits_set / self.m

    @property
    def estimated_false_positive_rate(self) -> float:
        """
        Theoretical false positive probability given the current fill:
            (1 - e^(-k*n/m))^k
        """
        if self._count == 0:
            return 0.0
        return (1.0 - math.exp(-self.k * self._count / self.m)) ** self.k

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    def _hash_indices(self, item: str):
        """
        Yield k bit indices using the double-hashing technique.
        Two independent base hashes (MD5, SHA-1) give:
            g_i(x) = ( h1(x) + i * h2(x) ) mod m
        This is proven to be equivalent to k truly independent hash functions
        for Bloom filter use.
        """

        encoded = item.encode()
        h1 = int(hashlib.md5(encoded).hexdigest(), 16) % self.m
        h2 = int(hashlib.sha1(encoded).hexdigest(), 16) % self.m
        # Ensure h2 != 0 so all k positions differ
        if h2 == 0:
            h2 = 1
        for i in range(self.k):
            yield (h1 + i * h2) % self.m


# ---------------------------------------------------------------------------
# SpellChecker
# ---------------------------------------------------------------------------


class SpellChecker:
    """
    Bloom-filter-based spell checker.

    Usage
    -----
    >>> checker = SpellChecker().load_words(["apple", "banana", "cherry"])
    >>> checker.check("apple")
    True
    >>> checker.check("zqqxv")
    False  # (probably)
    """
