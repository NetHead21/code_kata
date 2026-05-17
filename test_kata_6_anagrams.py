"""Tests for Kata06: Anagrams."""

from pathlib import Path

import pytest

from kata_6_anagrams import (
    find_anagram_groups,
    find_anagrams_from_file,
    largest_group,
    load_words,
    longest_words,
    signature,
)

WORDLIST = Path(__file__).parent / "data" / "wordlist.txt"


# ---------------------------------------------------------------------------
# signature()
# ---------------------------------------------------------------------------


class TestSignature:
    def test_empty_string(self):
        assert signature("") == ""

    def test_single_letter(self):
        assert signature("a") == "a"

    def test_sorts_letters(self):
        assert signature("listen") == "eilnst"

    def test_anagrams_share_signature(self):
        assert signature("listen") == signature("silent")
        assert signature("silent") == signature("inlets")
        assert signature("inlets") == signature("enlist")

    def test_case_insensitive(self):
        assert signature("Listen") == signature("listen")
        assert signature("SILENT") == signature("silent")

    def test_non_anagrams_differ(self):
        assert signature("hello") != signature("world")

    def test_different_lengths_differ(self):
        assert signature("cat") != signature("cats")

    def test_preserves_duplicate_letters(self):
        assert signature("aab") != signature("abc")

    def test_known_kata_examples(self):
        # arrest / rarest / raster / raters / starer
        key = signature("arrest")
        for word in ["rarest", "raster", "raters", "starer"]:
            assert signature(word) == key, (
                f"'{word}' should share signature with 'arrest'"
            )

    @pytest.mark.parametrize(
        "a, b",
        [
            ("kinship", "pinkish"),
            ("fresher", "refresh"),
            ("below", "elbow"),
            ("lemon", "melon"),
            ("inch", "chin"),
            ("evil", "vile"),
            ("evil", "live"),
            ("evil", "veil"),
            ("sinks", "skins"),
            ("knits", "stink"),
            ("rots", "sort"),
        ],
    )
    def test_known_pairs(self, a, b):
        assert signature(a) == signature(b)


# ---------------------------------------------------------------------------
# find_anagram_groups()
# ---------------------------------------------------------------------------


class TestFindAnagramGroups:
    def test_empty_input(self):
        assert find_anagram_groups([]) == []

    def test_single_word_gives_no_groups(self):
        assert find_anagram_groups(["hello"]) == []

    def test_two_non_anagrams_gives_no_groups(self):
        assert find_anagram_groups(["hello", "world"]) == []

    def test_simple_pair(self):
        groups = find_anagram_groups(["listen", "silent"])
        assert len(groups) == 1
        assert set(groups[0]) == {"listen", "silent"}

    def test_group_of_four(self):
        words = ["enlist", "inlets", "listen", "silent"]
        groups = find_anagram_groups(words)
        assert len(groups) == 1
        assert set(groups[0]) == set(words)

    def test_two_independent_groups(self):
        words = ["sinks", "skins", "knits", "stink"]
        groups = find_anagram_groups(words)
        assert len(groups) == 2
        group_sets = [set(g) for g in groups]
        assert {"sinks", "skins"} in group_sets
        assert {"knits", "stink"} in group_sets

    def test_singletons_excluded(self):
        words = ["cat", "act", "dog"]
        groups = find_anagram_groups(words)
        assert len(groups) == 1
        assert set(groups[0]) == {"cat", "act"}

    def test_preserves_original_case(self):
        groups = find_anagram_groups(["Listen", "Silent"])
        assert len(groups) == 1
        assert set(groups[0]) == {"Listen", "Silent"}
