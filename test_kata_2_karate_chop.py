"""Tests for Kata02: Karate Chop (binary search)."""

import pytest

from kata_2_karate_chop import (
    chop_bisect,
    chop_functional,
    chop_iterative,
    chop_recursive,
    chop_slice,
)

IMPLEMENTATIONS = [
    chop_iterative,
    chop_recursive,
    chop_slice,
    chop_bisect,
    chop_functional,
]


# ---------------------------------------------------------------------------
# Canonical kata test cases
# ---------------------------------------------------------------------------

CANONICAL_CASES = [
    # (target, array, expected_index)
    (3, [], -1),
    (3, [1], -1),
    (1, [1], 0),
    (1, [1, 3, 5], 0),
    (3, [1, 3, 5], 1),
    (5, [1, 3, 5], 2),
    (0, [1, 3, 5], -1),
    (2, [1, 3, 5], -1),
    (4, [1, 3, 5], -1),
    (6, [1, 3, 5], -1),
    (1, [1, 3, 5, 7], 0),
    (3, [1, 3, 5, 7], 1),
    (5, [1, 3, 5, 7], 2),
    (7, [1, 3, 5, 7], 3),
    (0, [1, 3, 5, 7], -1),
    (2, [1, 3, 5, 7], -1),
    (4, [1, 3, 5, 7], -1),
    (8, [1, 3, 5, 7], -1),
]


@pytest.mark.parametrize("chop", IMPLEMENTATIONS, ids=lambda f: f.__name__)
@pytest.mark.parametrize("target, array, expected", CANONICAL_CASES)
def test_canonical(chop, target, array, expected):
    assert chop(target, array) == expected


# ---------------------------------------------------------------------------
# Boundary / first-last element
# ---------------------------------------------------------------------------

BOUNDARY_CASES = [
    # first and last element of various lengths
    (1, [1, 2, 3, 4, 5], 0),  # first of odd-length
    (5, [1, 2, 3, 4, 5], 4),  # last of odd-length
    (1, [1, 2, 3, 4], 0),  # first of even-length
    (4, [1, 2, 3, 4], 3),  # last of even-length
    (3, [1, 2, 3, 4, 5], 2),  # exact midpoint
    (0, [1, 2, 3, 4, 5], -1),  # just below minimum
    (6, [1, 2, 3, 4, 5], -1),  # just above maximum
]


@pytest.mark.parametrize("chop", IMPLEMENTATIONS, ids=lambda f: f.__name__)
@pytest.mark.parametrize("target, array, expected", BOUNDARY_CASES)
def test_boundary(chop, target, array, expected):
    assert chop(target, array) == expected


# ---------------------------------------------------------------------------
# Single-element array
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("chop", IMPLEMENTATIONS, ids=lambda f: f.__name__)
def test_single_element_found(chop):
    assert chop(42, [42]) == 0


@pytest.mark.parametrize("chop", IMPLEMENTATIONS, ids=lambda f: f.__name__)
def test_single_element_not_found_below(chop):
    assert chop(41, [42]) == -1


@pytest.mark.parametrize("chop", IMPLEMENTATIONS, ids=lambda f: f.__name__)
def test_single_element_not_found_above(chop):
    assert chop(43, [42]) == -1


# ---------------------------------------------------------------------------
# Two-element array
# ---------------------------------------------------------------------------

TWO_ELEMENT_CASES = [
    (1, [1, 2], 0),
    (2, [1, 2], 1),
    (0, [1, 2], -1),
    (3, [1, 2], -1),
]


@pytest.mark.parametrize("chop", IMPLEMENTATIONS, ids=lambda f: f.__name__)
@pytest.mark.parametrize("target, array, expected", TWO_ELEMENT_CASES)
def test_two_element_array(chop, target, array, expected):
    assert chop(target, array) == expected


# ---------------------------------------------------------------------------
# Negative numbers
# ---------------------------------------------------------------------------

NEGATIVE_CASES = [
    (-5, [-5, -3, -1, 0, 2], 0),  # negative first
    (-1, [-5, -3, -1, 0, 2], 2),  # negative mid
    (0, [-5, -3, -1, 0, 2], 3),  # zero in mixed array
    (2, [-5, -3, -1, 0, 2], 4),  # positive last
    (-4, [-5, -3, -1, 0, 2], -1),  # between negatives, not found
    (-6, [-5, -3, -1, 0, 2], -1),  # below all negatives
    (3, [-5, -3, -1, 0, 2], -1),  # above all
    (-3, [-3], 0),  # single negative, found
    (-2, [-3], -1),  # single negative, not found
]


@pytest.mark.parametrize("chop", IMPLEMENTATIONS, ids=lambda f: f.__name__)
@pytest.mark.parametrize("target, array, expected", NEGATIVE_CASES)
def test_negative_numbers(chop, target, array, expected):
    assert chop(target, array) == expected


# ---------------------------------------------------------------------------
# Large array — stress test correctness at scale
# ---------------------------------------------------------------------------

LARGE = list(range(0, 10_000, 2))  # [0, 2, 4, ..., 9998], 5000 elements


@pytest.mark.parametrize("chop", IMPLEMENTATIONS, ids=lambda f: f.__name__)
def test_large_array_hit_first(chop):
    assert chop(0, LARGE) == 0


@pytest.mark.parametrize("chop", IMPLEMENTATIONS, ids=lambda f: f.__name__)
def test_large_array_hit_last(chop):
    assert chop(9998, LARGE) == 4999


@pytest.mark.parametrize("chop", IMPLEMENTATIONS, ids=lambda f: f.__name__)
def test_large_array_hit_middle(chop):
    assert chop(5000, LARGE) == 2500


@pytest.mark.parametrize("chop", IMPLEMENTATIONS, ids=lambda f: f.__name__)
def test_large_array_miss(chop):
    assert chop(9999, LARGE) == -1


@pytest.mark.parametrize("chop", IMPLEMENTATIONS, ids=lambda f: f.__name__)
def test_large_array_below_range(chop):
    assert chop(-1, LARGE) == -1


@pytest.mark.parametrize("chop", IMPLEMENTATIONS, ids=lambda f: f.__name__)
def test_large_array_above_range(chop):
    assert chop(10000, LARGE) == -1
