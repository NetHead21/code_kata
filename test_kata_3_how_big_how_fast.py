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

    def test_library_fits_within_two_orders_of_magnitude_of_10tb(self):
        ten_tb = 10 * TB
        ratio = max(LIBRARY_OF_CONGRESS_BYTES, ten_tb) / min(
            LIBRARY_OF_CONGRESS_BYTES, ten_tb
        )
        assert ratio <= 100


# ---------------------------------------------------------------------------
# Part 1: How Big? — image storage
# ---------------------------------------------------------------------------


class TestRGBImageStorage:
    def test_single_pixel_is_3_bytes(self):
        assert bytes_for_rgb_image(1, 1) == 3

    def test_10x10_is_300_bytes(self):
        assert bytes_for_rgb_image(10, 10) == 300

    def test_megapixel_is_about_3mb(self):
        assert abs(math.log10(MEGAPIXEL_IMAGE_BYTES) - math.log10(3_000_000)) < 0.1

    def test_full_hd_1920x1080(self):
        full_hd = bytes_for_rgb_image(1920, 1080)
        assert full_hd == 1920 * 1080 * 3  # 6,220,800

    def test_4k_image_under_50mb(self):
        four_k = bytes_for_rgb_image(3840, 2160)
        assert four_k < 50_000_000

    def test_scales_with_pixels(self):
        assert bytes_for_rgb_image(200, 100) == 2 * bytes_for_rgb_image(100, 100)


# ---------------------------------------------------------------------------
# Part 1: How Big? — galaxy star catalogue
# ---------------------------------------------------------------------------


class TestGalaxyStarCatalogue:
    def test_star_count_is_hundreds_of_billions(self):
        assert 100_000_000_000 <= GALAXY_STARS <= 1_000_000_000_000

    def test_catalogue_is_in_terabyte_range(self):
        assert TB <= GALAXY_STAR_CATALOG_BYTES <= 10 * TB

    def test_catalogue_uses_8_bytes_per_star(self):
        assert GALAXY_STAR_CATALOG_BYTES == GALAXY_STARS * 8


# ---------------------------------------------------------------------------
# Part 1: How Big? — RAM / disk capacity
# ---------------------------------------------------------------------------


class TestCapacityEstimates:
    def test_ram_is_4gb(self):
        assert EXAMPLE_RAM_BYTES == 4 * GB

    def test_disk_is_500gb(self):
        assert EXAMPLE_DISK_BYTES == 500 * GB

    def test_floats_in_ram_is_hundreds_of_millions(self):
        assert 400_000_000 <= FLOATS_IN_RAM <= 600_000_000

    def test_floats_on_disk_is_tens_of_billions(self):
        assert 50_000_000_000 <= FLOATS_ON_DISK <= 70_000_000_000

    def test_books_on_disk_is_in_hundreds_of_thousands(self):
        assert 100_000 <= BOOKS_ON_DISK <= 2_000_000


# ---------------------------------------------------------------------------
# Part 1: How Big? — human_readable formatting
# ---------------------------------------------------------------------------


class TestHumanReadable:
    def test_bytes(self):
        assert human_readable(512) == "512 B"

    def test_kilobytes(self):
        result = human_readable(2048)
        assert "KB" in result

    def test_megabytes(self):
        result = human_readable(5 * 1024**2)
        assert "MB" in result

    def test_gigabytes(self):
        result = human_readable(3 * GB)
        assert "GB" in result

    def test_terabytes(self):
        result = human_readable(2 * TB)
        assert "TB" in result

    def test_novel_reported_in_kb_or_mb(self):
        result = human_readable(NOVEL_BYTES)
        assert "KB" in result or "MB" in result


# ---------------------------------------------------------------------------
# Part 2: How Fast? — iteration
# ---------------------------------------------------------------------------


class TestTimeIteration:
    """Iteration over 1M items should complete within a generous wall-clock bound."""

    N = 1_000_000

    def test_returns_a_float(self):
        assert isinstance(time_iteration(self.N), float)

    def test_completes_in_under_5_seconds(self):
        assert time_iteration(self.N) < 5.0

    def test_is_positive(self):
        assert time_iteration(self.N) > 0

    def test_larger_n_takes_longer_than_smaller_n(self):
        small = time_iteration(1_000)
        large = time_iteration(self.N)
        # Allow some noise but expect at least a 10× difference
        assert large > small * 5


# ---------------------------------------------------------------------------
# Part 2: How Fast? — sorting
# ---------------------------------------------------------------------------


class TestTimeSort:
    N = 100_000  # sort is O(n log n), keep N smaller to stay fast in CI

    def test_returns_a_float(self):
        assert isinstance(time_sort(self.N), float)

    def test_completes_in_under_10_seconds(self):
        assert time_sort(self.N) < 10.0

    def test_is_positive(self):
        assert time_sort(self.N) > 0

    def test_sorting_more_items_takes_longer(self):
        t_small = time_sort(1_000)
        t_large = time_sort(self.N)
        assert t_large > t_small


# ---------------------------------------------------------------------------
# Part 2: How Fast? — binary search
# ---------------------------------------------------------------------------


class TestTimeBinarySearch:
    N = 1_000_000

    def test_returns_a_float(self):
        assert isinstance(time_binary_search(self.N), float)

    def test_completes_in_under_1_second(self):
        assert time_binary_search(self.N) < 1.0
