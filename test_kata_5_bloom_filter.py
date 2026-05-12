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

    def test_default_fpr_is_1_percent(self):
        bf = BloomFilter(100)
        assert bf.false_positive_rate == 0.01

    def test_bit_count_matches_formula(self):
        bf = BloomFilter(100, 0.01)
        assert bf.bit_count == optimal_bit_count(100, 0.01)

    def test_hash_count_matches_formula(self):
        bf = BloomFilter(100, 0.01)
        assert bf.hash_count == optimal_hash_count(bf.bit_count, 100)

    def test_starts_empty(self):
        bf = BloomFilter(100)
        assert bf.count == 0

    def test_starts_with_zero_fill_ratio(self):
        bf = BloomFilter(100)
        assert bf.fill_ratio == 0.0

    def test_invalid_capacity_raises(self):
        with pytest.raises(ValueError):
            BloomFilter(0)
        with pytest.raises(ValueError):
            BloomFilter(-1)

    def test_invalid_fpr_raises(self):
        with pytest.raises(ValueError):
            BloomFilter(100, 0.0)
        with pytest.raises(ValueError):
            BloomFilter(100, 1.0)
        with pytest.raises(ValueError):
            BloomFilter(100, -0.1)

    def test_lower_fpr_gives_larger_bit_array(self):
        loose = BloomFilter(1_000, 0.10)
        strict = BloomFilter(1_000, 0.001)
        assert strict.bit_count > loose.bit_count

    def test_lower_fpr_gives_more_hash_functions(self):
        loose = BloomFilter(1_000, 0.10)
        strict = BloomFilter(1_000, 0.001)
        assert strict.hash_count >= loose.hash_count


# ---------------------------------------------------------------------------
# BloomFilter — membership (the fundamental guarantees)
# ---------------------------------------------------------------------------


class TestBloomFilterMembership:
    """Core correctness: no false negatives; FP rate bounded."""

    def test_item_not_found_before_add(self):
        bf = BloomFilter(100)
        assert "hello" not in bf

    def test_item_found_after_add(self):
        bf = BloomFilter(100)
        bf.add("hello")
        assert "hello" in bf

    def test_multiple_items_all_found(self):
        words = ["apple", "banana", "cherry", "date", "elderberry"]
        bf = BloomFilter(len(words))
        for w in words:
            bf.add(w)
        for w in words:
            assert w in bf, f"'{w}' should be in filter (no false negatives allowed)"

    def test_no_false_negatives_with_large_word_list(self):
        """Critical property: every inserted item MUST be found."""
        bf = BloomFilter(len(WORDS), 0.01)
        for word in WORDS:
            bf.add(word)
        for word in WORDS:
            assert word in bf, f"False negative: '{word}' not found after insertion"

    def test_count_increments_on_each_add(self):
        bf = BloomFilter(10)
        for i in range(5):
            bf.add(f"item{i}")
        assert bf.count == 5
