"""Back-of-the-envelope size and speed estimates for Kata 03.

This module explores the two halves of Dave Thomas's "How Big? How Fast?"
kata:
http://codekata.com/kata/kata03-how-big-how-fast/

Part 1, "How Big?", provides a handful of simple estimation helpers and named
constants for reasoning about storage requirements. The goal is not exactness;
the functions intentionally use coarse assumptions that are easy to explain and
recompute mentally.

Part 2, "How Fast?", provides lightweight timing helpers for common operations
such as iteration, sorting, binary search, string joining, and dictionary
lookup. These timings are illustrative rather than rigorous microbenchmarks:
they use wall-clock time, run a single benchmarked operation, and therefore are
best suited for ballpark comparisons instead of stable performance claims.

The script entry point prints a small report showing both the size estimates and
sample timings.
"""

import random
import time

# ---------------------------------------------------------------------------
# Part 1: How Big?
# ---------------------------------------------------------------------------


def bits_to_represent(n: int) -> int:
    """Return the minimum number of bits needed to encode ``n``.

    The function assumes ``n`` is a non-negative integer. Zero is treated as a
    special case requiring one bit, which matches the expectations in the kata's
    tests and keeps the result intuitive for rough estimation exercises.

    Args:
        n: Non-negative integer to represent.

    Returns:
        The minimum number of binary digits required to store ``n``.
    """

    if n == 0:
        return 1
    return n.bit_length()


def bytes_to_store_text(
    num_pages: int, words_per_page: int = 250, chars_per_word: int = 5
) -> int:
    """Estimate the storage needed for plain-text prose.

    The estimate uses a deliberately simple model:

    - each word contains ``chars_per_word`` characters on average
    - each word is followed by one separating space
    - each character occupies one byte

    This ignores punctuation, paragraph breaks, markup, compression, and any
    non-ASCII encoding overhead. That simplification is intentional because the
    kata focuses on order-of-magnitude reasoning.

    Args:
        num_pages: Number of pages in the text.
        words_per_page: Average words per page.
        chars_per_word: Average characters per word.

    Returns:
        Estimated size in bytes.
    """

    chars_per_page = words_per_page * (chars_per_word + 1)  # +1 for space
    return num_pages * chars_per_page
