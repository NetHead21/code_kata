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

    def test_result_is_int(self):
        assert isinstance(optimal_bit_count(500, 0.05), int)


class TestOptimalHashCount:
    def test_returns_at_least_one(self):
        assert optimal_hash_count(8, 1_000) >= 1

    def test_known_ratio_gives_expected_k(self):
        # k = round((m/n) * ln2); for m=959, n=100 → round(9.59 * 0.693) ≈ round(6.64) = 7
        assert optimal_hash_count(959, 100) == 7

    def test_larger_m_for_same_n_gives_more_hashes(self):
        assert optimal_hash_count(10_000, 100) > optimal_hash_count(1_000, 100)

    def test_result_is_int(self):
        assert isinstance(optimal_hash_count(1000, 100), int)


# ---------------------------------------------------------------------------
# BloomFilter — construction
# ---------------------------------------------------------------------------


class TestBloomFilterConstruction:
    def test_creates_with_valid_params(self):
        bf = BloomFilter(100)
        assert bf is not None
