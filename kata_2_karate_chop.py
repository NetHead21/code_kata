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

# --- Implementation 1: Iterative ---


def chop_iterative(target, array):
    """Search ``array`` iteratively using explicit low/high bounds.

    This is the canonical binary-search formulation. It repeatedly inspects the
    midpoint of the active interval and discards the half that cannot contain
    ``target``.

    Args:
        target: Value to locate.
        array: Sorted sequence of comparable values.

    Returns:
        The index of ``target`` if present, otherwise ``-1``.
    """

    lo, hi = 0, len(array) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if array[mid] == target:
            return mid
        elif array[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


# --- Implementation 2: Recursive (shrinking bounds) ---


def chop_recursive(target, array):
    """Search ``array`` recursively by shrinking index bounds.

    This version keeps the original array intact and passes only the current
    lower and upper bounds through recursive calls. That preserves the original
    indices naturally and avoids allocating sliced sublists.

    Args:
        target: Value to locate.
        array: Sorted sequence of comparable values.

    Returns:
        The index of ``target`` if present, otherwise ``-1``.
    """

    def _search(lo, hi):
        """Recursively search within the inclusive ``[lo, hi]`` interval."""
        if lo > hi:
            return -1
        mid = (lo + hi) // 2
        if array[mid] == target:
            return mid
        elif array[mid] < target:
            return _search(mid + 1, hi)
        else:
            return _search(lo, mid - 1)

    return _search(0, len(array) - 1)


# --- Implementation 3: Recursive (slicing subarray) ---


def chop_slice(target, array, offset=0):
    """Search recursively by slicing subarrays.

    This implementation is intentionally more declarative than efficient. Each
    recursive step passes only the relevant half of the array forward and uses
    ``offset`` to translate a match back to the index in the original input.

    Args:
        target: Value to locate.
        array: Sorted sequence of comparable values or a sorted sub-slice.
        offset: Index offset of ``array`` relative to the original input.

    Returns:
        The index of ``target`` in the original array if present, otherwise
        ``-1``.
    """

    if not array:
        return -1
    mid = len(array) // 2
    if array[mid] == target:
        return offset + mid
    elif array[mid] < target:
        return chop_slice(target, array[mid + 1 :], offset + mid + 1)
    else:
        return chop_slice(target, array[:mid], offset)


# --- Implementation 4: Using bisect ---


def chop_bisect(target, array):
    """Search ``array`` with ``bisect_left`` from Python's standard library.

    ``bisect_left`` returns the insertion point where ``target`` should appear
    to keep the array sorted. A second check verifies whether the insertion
    point actually contains the target.

    Args:
        target: Value to locate.
        array: Sorted sequence of comparable values.

    Returns:
        The index of ``target`` if present, otherwise ``-1``.
    """

    idx = bisect.bisect_left(array, target)
    if idx < len(array) and array[idx] == target:
        return idx
    return -1
