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
