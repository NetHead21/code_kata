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

    @pytest.mark.parametrize(
        "n, expected_bits",
        [
            (255, 8),
            (256, 9),
            (1_024, 11),
            (65_535, 16),
            (65_536, 17),
        ],
    )
    def test_known_values(self, n, expected_bits):
        assert bits_to_represent(n) == expected_bits


# ---------------------------------------------------------------------------
# Part 1: How Big? — text / book storage
# ---------------------------------------------------------------------------


class TestBytesToStoreText:
    def test_single_page_default_params(self):
        # 250 words × 6 chars (5 + 1 space) = 1500 bytes
        assert bytes_to_store_text(1) == 1_500

    def test_scales_linearly_with_pages(self):
        assert bytes_to_store_text(10) == 10 * bytes_to_store_text(1)

    def test_custom_words_per_page(self):
        assert bytes_to_store_text(1, words_per_page=100) == 600

    def test_custom_chars_per_word(self):
        # 250 words × (10 + 1) chars = 2750
        assert bytes_to_store_text(1, chars_per_word=10) == 2_750


class TestNovelSize:
    def test_novel_is_between_200kb_and_2mb(self):
        # A novel should be in a plausible ballpark
        assert 200_000 <= NOVEL_BYTES <= 2_000_000

    def test_novel_is_roughly_half_a_megabyte(self):
        assert abs(math.log10(NOVEL_BYTES) - math.log10(500_000)) < 0.5


class TestLibraryOfCongress:
    def test_book_count_is_tens_of_millions(self):
        assert 10_000_000 <= LIBRARY_OF_CONGRESS_BOOKS <= 50_000_000

    def test_total_size_is_in_terabytes(self):
        assert LIBRARY_OF_CONGRESS_BYTES >= TB

    def test_total_size_is_below_100_petabytes(self):
        PB = 1_024**5
        assert LIBRARY_OF_CONGRESS_BYTES <= 100 * PB
