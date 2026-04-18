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
