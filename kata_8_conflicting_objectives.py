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


# ---------------------------------------------------------------------------
# Version 2: Fast
# ---------------------------------------------------------------------------


def find_compound_words_fast(
    words, target_length: int = 6
) -> list[tuple[str, str, str]]:
    """
    Same result as the readable version; optimised for throughput on
    dictionaries with hundreds of thousands of words.

    Techniques used (each adds a measurable speedup on large inputs):
      1. frozenset  — immutable hash set; membership test is marginally
                      faster than set because the hash is pre-computed.
      2. Iterate over the set, not the original list, to avoid re-testing
         duplicate words.
      3. Pre-filter once: collect only target-length words so the inner
         loop runs on a small fraction of the dictionary.
      4. Local variable bindings (``_in``, ``_target``) avoid the LEGB
         name lookup on every iteration.
      5. Slice each position once and store in locals; avoids slicing twice
         when both halves need to be returned.
    """

    word_set = frozenset(words)
    _in = word_set.__contains__  # local callable — avoids repeated attribute lookup
    _target = target_length

    candidates = [w for w in word_set if len(w) == _target]

    results = []
    append = results.append

    for word in candidates:
        for i in range(1, _target):
            left = word[:i]
            if _in(left):
                right = word[i:]
                if _in(right):
                    append((left, right, word))
                    break

    return results
