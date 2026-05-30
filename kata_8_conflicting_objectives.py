"""
Kata08: Conflicting Objectives
http://codekata.com/kata/kata08-conflicting-objectives/

Find all six-letter words in a dictionary that are formed by concatenating
two shorter words from the same dictionary. For example:
    jig + saw  => jigsaw
    sun + set  => sunset
    here + by  => hereby

The same program is implemented three ways to explore how sub-objectives
shape code:

  Version 1 — READABLE   : clarity above all else
  Version 2 — FAST       : throughput on large word lists
  Version 3 — EXTENDIBLE : generalised beyond the specific problem

Trade-off notes (the real point of the kata)
--------------------------------------------
- Making code fast often harms readability: local variable binding tricks,
  frozenset vs set, pre-filtering loops — none of these are obvious.
- Making code extendible often adds indirection: extra parameters, helper
  generators, recursion — which can obscure what the simple case does.
- Readability and extendibility are not always in conflict: good names and
  separation of concerns help both.
"""

from pathlib import Path


# ---------------------------------------------------------------------------
# Version 1: Readable
# ---------------------------------------------------------------------------


def find_compound_words_readable(
    words, target_length: int = 6
) -> list[tuple[str, str, str]]:
    """
    Return every word of *target_length* letters that is formed by joining
    two shorter words that both appear in *words*.

    Each result is a tuple (left_part, right_part, compound_word).

    This version is written for maximum clarity.  Every step is named,
    every condition is written out in full, and there are no clever tricks.
    """

    word_set = set(words)

    compound_words = []

    for word in words:
        if len(word) != target_length:
            continue

        for split_position in range(1, target_length):
            left_part = word[:split_position]
            right_part = word[split_position:]

            left_is_a_word = left_part in word_set
            right_is_a_word = right_part in word_set

            if left_is_a_word and right_is_a_word:
                compound_words.append((left_part, right_part, word))
                break  # one valid split per compound is enough

    return compound_words
