"""
Kata07: How'd I Do?
http://codekata.com/kata/kata07-howd-i-do/

This kata is a *reflective* exercise, not an algorithmic one.
The challenge: find a piece of your own code, read it three times with
different lenses, and note what you discover.

  Pass 1 — POSITIVE  : pretend the author is the best programmer you know.
                        What did they do brilliantly?
  Pass 2 — CRITICAL  : pretend the author is the worst programmer you know.
                        What is badly designed, unreadable, or fragile?
  Pass 3 — BUG_HUNT  : pretend the client will sue you if there are bugs.
                        What could go wrong at runtime?

This module turns that reflective process into a small structured tool:

  - Finding      — one observation from one pass
  - CodeReview   — collects findings, produces a summary report
  - Checklist    — pre-built questions to prompt each pass
"""
