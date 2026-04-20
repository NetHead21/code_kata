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
