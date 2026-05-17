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
