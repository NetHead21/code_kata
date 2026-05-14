"""
Kata06: Anagrams
http://codekata.com/kata/kata06-anagrams/

Given a word list, find all groups of words that are anagrams of each other.

Algorithm
---------
Naïve O(n²) pairwise comparison is far too slow for large dictionaries.
The efficient approach is O(n · k·log k) where k is the average word length:

  1. For each word compute a *signature* by sorting its letters.
     All anagrams of a word share the same signature ("listen" → "eilnst").
  2. Group words by signature using a dict.
  3. Any group with ≥ 2 words is an anagram set.

This runs in well under a second on dictionaries of hundreds of thousands of words.
"""

from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------


def signature(word: str) -> str:
    """
    Return the canonical anagram key for *word*: its letters sorted
    alphabetically (case-insensitive).

    >>> signature("listen")
    'eilnst'
    >>> signature("silent")
    'eilnst'
    >>> signature("Listen")
    'eilnst'
    """
    return "".join(sorted(word.lower()))


def find_anagram_groups(words) -> list[list[str]]:
    """
    Group an iterable of words by their anagram signature.

    Returns a list of groups; each group is a list of two or more words
    that are anagrams of each other. Words within a group are returned in
    the order they were first encountered. Singleton words (no anagram
    partners in the input) are omitted.

    Case is preserved in the output but ignored for matching.
    """
    buckets: dict[str, list[str]] = defaultdict(list)
    for word in words:
        w = word.strip()
        if w:
            buckets[signature(w)].append(w)
    return [group for group in buckets.values() if len(group) > 1]


# ---------------------------------------------------------------------------
# Bonus queries
# ---------------------------------------------------------------------------


def largest_group(groups: list[list[str]]) -> list[str]:
    """Return the anagram group that contains the most words."""
    if not groups:
        return []
    return max(groups, key=len)


def longest_words(groups: list[list[str]]) -> list[str]:
    """
    Return all words whose length equals the maximum word length found
    across all anagram groups.
    """
    if not groups:
        return []
    max_len = max(len(w) for group in groups for w in group)
    return sorted({w for group in groups for w in group if len(w) == max_len})


# ---------------------------------------------------------------------------
# File I/O helpers
# ---------------------------------------------------------------------------


def load_words(path) -> list[str]:
    """Read a word-per-line file and return a deduplicated list."""
    seen: set[str] = set()
    words: list[str] = []
    for line in Path(path).read_text().splitlines():
        w = line.strip()
        if w and w not in seen:
            seen.add(w)
            words.append(w)
    return words
