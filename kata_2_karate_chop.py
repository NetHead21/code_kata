"""Binary search kata implemented in several different styles.

This module solves the "Karate Chop" kata from Dave Thomas:
http://codekata.com/kata/kata02-karate-chop/

Each public function implements the same contract:

- accept a ``target`` value and a sorted ``array``
- return the index of a matching element when found
- return ``-1`` when the value does not occur in the input

The input array is assumed to already be sorted in ascending order. None of the
implementations validate or sort the input, because the kata is focused on the
search algorithm itself.

The five variants highlight different implementation techniques rather than
different semantics:

- ``chop_iterative`` uses the classic loop with low/high bounds
- ``chop_recursive`` performs the same search recursively
- ``chop_slice`` recurses over sliced subarrays and tracks an offset
- ``chop_bisect`` delegates the search to Python's standard library
- ``chop_functional`` expresses the narrowing process with ``reduce``

When duplicate values are present, binary search only guarantees that the
returned index refers to *a* matching element, not necessarily the first or
last occurrence.
"""

import bisect
from functools import reduce
