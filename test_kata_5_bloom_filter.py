"""Tests for Kata05: Bloom Filters."""

import math
import random
import string
from pathlib import Path

import pytest

from kata_5_bloom_filter import (
    BloomFilter,
    SpellChecker,
    false_positive_experiment,
    optimal_bit_count,
    optimal_hash_count,
)

WORDS_FILE = Path(__file__).parent / "data" / "words.txt"
WORDS = [w for w in WORDS_FILE.read_text().splitlines() if w.strip()]


# ---------------------------------------------------------------------------
# Optimal parameter maths
# ---------------------------------------------------------------------------


class TestOptimalBitCount:
    def test_returns_positive_int(self):
        assert optimal_bit_count(100, 0.01) > 0

    def test_more_items_needs_more_bits(self):
        assert optimal_bit_count(1_000, 0.01) > optimal_bit_count(100, 0.01)

    def test_lower_fpr_needs_more_bits(self):
        assert optimal_bit_count(1_000, 0.001) > optimal_bit_count(1_000, 0.01)

    def test_known_value_100_items_1pct(self):
        # m = ceil(-100 * ln(0.01) / ln(2)^2) = ceil(958.5) = 959
        assert optimal_bit_count(100, 0.01) == 959
