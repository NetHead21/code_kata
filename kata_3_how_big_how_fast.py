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


# --- Named storage estimates (all in bytes) ---

# A typical English novel: ~400 pages, 250 words/page, avg 5 chars/word
NOVEL_BYTES = bytes_to_store_text(num_pages=400)

# US Library of Congress: ~17 million books
LIBRARY_OF_CONGRESS_BOOKS = 17_000_000
LIBRARY_OF_CONGRESS_BYTES = LIBRARY_OF_CONGRESS_BOOKS * NOVEL_BYTES


# RGB image storage: 3 bytes per pixel (one byte each R, G, B)
def bytes_for_rgb_image(width_px: int, height_px: int) -> int:
    """Estimate the raw storage for an RGB image.

    The calculation assumes an uncompressed image with one byte each for red,
    green, and blue per pixel, for a total of three bytes per pixel.

    Args:
        width_px: Image width in pixels.
        height_px: Image height in pixels.

    Returns:
        Raw image size in bytes.
    """

    return width_px * height_px * 3


MEGAPIXEL_IMAGE_BYTES = bytes_for_rgb_image(1000, 1000)  # ~3 MB

# Our galaxy: ~300 billion stars, each stored as a 64-bit float (8 bytes)
GALAXY_STARS = 300_000_000_000
GALAXY_STAR_CATALOG_BYTES = GALAXY_STARS * 8

# RAM / disk capacity examples
GB = 1_024**3
TB = 1_024**4

EXAMPLE_RAM_BYTES = 4 * GB  # 4 GB RAM
EXAMPLE_DISK_BYTES = 500 * GB  # 500 GB disk

FLOATS_IN_RAM = EXAMPLE_RAM_BYTES // 8  # 64-bit double = 8 bytes
FLOATS_ON_DISK = EXAMPLE_DISK_BYTES // 8

BOOKS_ON_DISK = EXAMPLE_DISK_BYTES // NOVEL_BYTES


def human_readable(n_bytes: int) -> str:
    """Format a byte count using binary storage units.

    Units are chosen from bytes, kilobytes, megabytes, gigabytes, and
    terabytes using powers of 1024. Values at KB and above are rounded to one
    decimal place for compact display.

    Args:
        n_bytes: Byte count to format.

    Returns:
        A short human-readable representation such as ``"512 B"`` or
        ``"3.0 MB"``.
    """

    for unit, threshold in [("TB", TB), ("GB", GB), ("MB", 1_024**2), ("KB", 1_024)]:
        if n_bytes >= threshold:
            return f"{n_bytes / threshold:.1f} {unit}"
    return f"{n_bytes} B"


# ---------------------------------------------------------------------------
# Part 2: How Fast?
# ---------------------------------------------------------------------------


def benchmark(func, *args, **kwargs) -> tuple:
    """Execute ``func`` and measure its wall-clock runtime.

    This helper wraps a single call with ``time.perf_counter()`` and returns
    both the function result and the elapsed time. It is intentionally minimal:
    no warm-up, repetition, statistical smoothing, or isolation from system
    noise is performed.

    Args:
        func: Callable to execute.
        *args: Positional arguments forwarded to ``func``.
        **kwargs: Keyword arguments forwarded to ``func``.

    Returns:
        A ``(result, elapsed_seconds)`` tuple.
    """

    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed


def time_iteration(n: int) -> float:
    """Measure the time needed to sum ``range(n)``.

    Summing the sequence ensures the interpreter actually visits each element,
    making the benchmark a simple proxy for linear iteration cost.

    Args:
        n: Number of integers to iterate over.

    Returns:
        Elapsed wall-clock time in seconds.
    """
