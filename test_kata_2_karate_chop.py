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
