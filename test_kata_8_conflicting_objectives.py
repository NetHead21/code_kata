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

WORDLIST = Path(__file__).parent / "data" / "wordlist.txt"

# Controlled dictionary with known compound words and their parts
SMALL_DICT = [
    # 5-letter compound words
    "jigsaw",
    "sunset",
    "cannot",
    "hereby",
    "convex",
    "cowboy",
    "hotdog",
    "teapot",
    "airway",
    "runway",
    "midway",
    "nobody",
    "upkeep",
    "output",
    "inside",
    "uptown",
    "batman",
    "eyelid",
    "payoff",
    "befoul",
    "weaver",
    # component parts (shorter words)
    "jig",
    "saw",
    "sun",
    "set",
    "can",
    "not",
    "here",
    "by",
    "con",
    "vex",
    "cow",
    "boy",
    "hot",
    "dog",
    "tea",
    "pot",
    "air",
    "way",
    "run",
    "mid",
    "no",
    "body",
    "up",
    "keep",
    "out",
    "put",
    "in",
    "side",
    "town",
    "bat",
    "man",
    "eye",
    "lid",
    "pay",
    "off",
    "be",
    "foul",
    "we",
    "aver",
    # red herrings — 5-letter non-compounds
    "orange",
    "purple",
    "yellow",
    "silver",
    "golden",
]

EXPECTED_COMPOUNDS = {
    ("jig", "saw", "jigsaw"),
    ("sun", "set", "sunset"),
    ("can", "not", "cannot"),
    ("here", "by", "hereby"),
    ("con", "vex", "convex"),
    ("cow", "boy", "cowboy"),
    ("hot", "dog", "hotdog"),
    ("tea", "pot", "teapot"),
    ("air", "way", "airway"),
    ("run", "way", "runway"),
    ("mid", "way", "midway"),
    ("no", "body", "nobody"),
    ("up", "keep", "upkeep"),
    ("out", "put", "output"),
    ("in", "side", "inside"),
    ("up", "town", "uptown"),
    ("bat", "man", "batman"),
    ("eye", "lid", "eyelid"),
    ("pay", "off", "payoff"),
    ("be", "foul", "befoul"),
    ("we", "aver", "weaver"),
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def results_to_set(results):
    """Normalise readable/fast output to a set of (left, right, word) tuples."""
    return normalise_readable(results)


def ext_results_to_set(results):
    """Normalise extendible 1-part output for comparison."""
    return normalise_extendible(results)


# ---------------------------------------------------------------------------
# Version 0: Readable
# ---------------------------------------------------------------------------


class TestReadable:
    def test_returns_list(self):
        assert isinstance(find_compound_words_readable(SMALL_DICT), list)

    def test_empty_input(self):
        assert find_compound_words_readable([]) == []

    def test_no_six_letter_words(self):
        assert find_compound_words_readable(["cat", "act", "dog"]) == []

    def test_six_letter_word_with_no_parts_in_dict(self):
        assert find_compound_words_readable(["orange"]) == []
