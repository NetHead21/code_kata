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
