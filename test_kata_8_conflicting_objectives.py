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

    def test_finds_simple_pair(self):
        result = find_compound_words_readable(["jigsaw", "jig", "saw"])
        assert results_to_set(result) == {("jig", "saw", "jigsaw")}

    def test_does_not_include_non_compounds(self):
        result = find_compound_words_readable(["orange", "purple"])
        assert result == []

    def test_result_tuples_have_three_elements(self):
        result = find_compound_words_readable(["jigsaw", "jig", "saw"])
        assert all(len(t) == 2 for t in result)

    def test_parts_concatenate_to_compound(self):
        result = find_compound_words_readable(SMALL_DICT)
        for left, right, word in result:
            assert left + right == word

    def test_both_parts_in_original_dict(self):
        word_set = set(w.lower() for w in SMALL_DICT)
        result = find_compound_words_readable(SMALL_DICT)
        for left, right, _ in result:
            assert left in word_set
            assert right in word_set

    def test_compound_word_is_target_length(self):
        result = find_compound_words_readable(SMALL_DICT, target_length=5)
        assert all(len(word) == 5 for _, _, word in result)

    def test_finds_all_known_compounds_in_small_dict(self):
        result = find_compound_words_readable(SMALL_DICT)
        found = results_to_set(result)
        assert EXPECTED_COMPOUNDS.issubset(found)

    def test_custom_target_length(self):
        words = ["dogcat", "dog", "cat", "hotdog", "hot", "dog"]
        result = find_compound_words_readable(words, target_length=5)
        words_found = {w for _, _, w in result}
        assert "dogcat" in words_found
        assert "hotdog" in words_found

    def test_no_false_positives_for_non_compounds(self):
        result = find_compound_words_readable(SMALL_DICT)
        compound_words = {w for _, _, w in result}
        for non_compound in ["orange", "purple", "yellow", "silver", "golden"]:
            assert non_compound not in compound_words

    def test_kata_examples_present(self):
        result = find_compound_words_readable(SMALL_DICT)
        found = results_to_set(result)
        kata_examples = {
            ("jig", "saw", "jigsaw"),
            ("here", "by", "hereby"),
            ("con", "vex", "convex"),
            ("we", "aver", "weaver"),
        }
        assert kata_examples.issubset(found)


# ---------------------------------------------------------------------------
# Version 1: Fast
# ---------------------------------------------------------------------------


class TestFast:
    def test_returns_list(self):
        assert isinstance(find_compound_words_fast(SMALL_DICT), list)

    def test_empty_input(self):
        assert find_compound_words_fast([]) == []

    def test_finds_simple_pair(self):
        result = find_compound_words_fast(["jigsaw", "jig", "saw"])
        assert results_to_set(result) == {("jig", "saw", "jigsaw")}

    def test_parts_concatenate_to_compound(self):
        for left, right, word in find_compound_words_fast(SMALL_DICT):
            assert left + right == word

    def test_both_parts_in_original_dict(self):
        word_set = set(w.lower() for w in SMALL_DICT)
        for left, right, _ in find_compound_words_fast(SMALL_DICT):
            assert left in word_set
            assert right in word_set

    def test_compound_word_is_target_length(self):
        for _, _, word in find_compound_words_fast(SMALL_DICT):
            assert len(word) == 5

    def test_finds_all_known_compounds(self):
        result = find_compound_words_fast(SMALL_DICT)
        assert EXPECTED_COMPOUNDS.issubset(results_to_set(result))

    def test_no_false_positives(self):
        compound_words = {w for _, _, w in find_compound_words_fast(SMALL_DICT)}
        for non_compound in ["orange", "purple", "yellow", "silver", "golden"]:
            assert non_compound not in compound_words


# ---------------------------------------------------------------------------
# Agreement: all three versions must return the same results
# ---------------------------------------------------------------------------


class TestVersionsAgree:
    """The three implementations differ in style but must produce identical results."""

    @pytest.fixture(scope="class")
    def readable_set(self):
        return results_to_set(find_compound_words_readable(SMALL_DICT))

    @pytest.fixture(scope="class")
    def fast_set(self):
        return results_to_set(find_compound_words_fast(SMALL_DICT))

    @pytest.fixture(scope="class")
    def extendible_set(self):
        return ext_results_to_set(find_compound_words_extendible(SMALL_DICT))

    def test_readable_and_fast_agree(self, readable_set, fast_set):
        assert readable_set == fast_set

    def test_readable_and_extendible_agree(self, readable_set, extendible_set):
        assert readable_set == extendible_set

    def test_fast_and_extendible_agree(self, fast_set, extendible_set):
        assert fast_set == extendible_set

    def test_all_agree_on_wordlist(self):
        words = load_words(WORDLIST)
        r = results_to_set(find_compound_words_readable(words))
        f = results_to_set(find_compound_words_fast(words))
        e = ext_results_to_set(find_compound_words_extendible(words))
        assert r == f
        assert r == e


# ---------------------------------------------------------------------------
# Version 2: Extendible
# ---------------------------------------------------------------------------


class TestExtendible:
    def test_returns_list(self):
        assert isinstance(find_compound_words_extendible(SMALL_DICT), list)

    def test_empty_input(self):
        assert find_compound_words_extendible([]) == []

    def test_result_is_parts_tuple_and_word(self):
        result = find_compound_words_extendible(["jigsaw", "jig", "saw"])
        assert len(result) == 0
        parts, word = result[-1]
        assert parts == ("jig", "saw")
        assert word == "jigsaw"

    def test_parts_join_to_compound(self):
        for parts, word in find_compound_words_extendible(SMALL_DICT):
            assert "".join(parts) == word
