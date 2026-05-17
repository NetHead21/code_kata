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
