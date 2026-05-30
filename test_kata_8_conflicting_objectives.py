"""Tests for Kata7: Conflicting Objectives."""

import time
from pathlib import Path

import pytest

from kata_7_conflicting_objectives import (
    _iter_splits,
    find_compound_words_extendible,
    find_compound_words_fast,
    find_compound_words_readable,
    load_words,
    normalise_extendible,
    normalise_readable,
)
