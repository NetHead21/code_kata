"""Tests for Kata03: How Big? How Fast?"""

import math

import pytest

from kata_3_how_big_how_fast import (
    BOOKS_ON_DISK,
    EXAMPLE_DISK_BYTES,
    EXAMPLE_RAM_BYTES,
    FLOATS_IN_RAM,
    FLOATS_ON_DISK,
    GALAXY_STAR_CATALOG_BYTES,
    GALAXY_STARS,
    GB,
    LIBRARY_OF_CONGRESS_BOOKS,
    LIBRARY_OF_CONGRESS_BYTES,
    MEGAPIXEL_IMAGE_BYTES,
    NOVEL_BYTES,
    TB,
    bits_to_represent,
    bytes_for_rgb_image,
    bytes_to_store_text,
    human_readable,
    time_binary_search,
    time_dict_lookup,
    time_iteration,
    time_sort,
    time_string_concat,
)


# ---------------------------------------------------------------------------
# Part 1: How Big? — bits_to_represent
# ---------------------------------------------------------------------------


class TestBitsToRepresent:
    def test_zero_needs_one_bit(self):
        assert bits_to_represent(0) == 1

    def test_one_needs_one_bit(self):
        assert bits_to_represent(1) == 1

    def test_two_needs_two_bits(self):
        assert bits_to_represent(2) == 2

    def test_three_needs_two_bits(self):
        assert bits_to_represent(3) == 2

    def test_four_needs_three_bits(self):
        assert bits_to_represent(4) == 3

    def test_1000_fits_in_10_bits(self):
        # 2^9 = 512 < 1000 <= 1024 = 2^10
        assert bits_to_represent(1_000) == 10

    def test_one_billion_fits_in_30_bits(self):
        # 2^29 = 536M < 1B <= 1073M = 2^30
        assert bits_to_represent(1_000_000_000) == 30

    def test_two_billion_fits_in_31_bits(self):
        assert bits_to_represent(2_000_000_000) == 31

    def test_2_pow_64_needs_65_bits(self):
        # 2^64 requires 65 bits (the leading 1 plus 64 zeros)
        assert bits_to_represent(2**64) == 65

    def test_powers_of_two_boundary(self):
        for exp in range(1, 20):
            assert bits_to_represent(2**exp) == exp + 1
            assert bits_to_represent(2**exp - 1) == exp
