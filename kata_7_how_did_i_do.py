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

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------


class Pass(str, Enum):
    """Which of the three review lenses produced this finding."""

    POSITIVE = "positive"  # best-programmer lens
    CRITICAL = "critical"  # worst-programmer lens
    BUG_HUNT = "bug_hunt"  # bug-hunter lens


class Severity(str, Enum):
    """How urgently the finding should be addressed."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Category(str, Enum):
    """The aspect of code quality the finding relates to."""

    DESIGN = "design"
    NAMING = "naming"
    READABILITY = "readability"
    PERFORMANCE = "performance"
    CORRECTNESS = "correctness"
    TESTING = "testing"
    SECURITY = "security"
    OTHER = "other"


# ---------------------------------------------------------------------------
# Finding
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    """A single observation made during a code review pass."""

    review_pass: Pass
    category: Category
    description: str
    severity: Severity = Severity.MEDIUM
    location: Optional[str] = None  # e.g. "module.py:42" or "function foo()"

    def __post_init__(self):
        """Validate that description is non-empty after stripping whitespace."""
        if not self.description.strip():
            raise ValueError("description must not be empty")

    def __str__(self) -> str:
        """Format as '[PASS] (category, severity) [location]: description'."""
        loc = f" [{self.location}]" if self.location else ""
        return (
            f"[{self.review_pass.value.upper()}] "
            f"({self.category.value}, {self.severity.value})"
            f"{loc}: {self.description}"
        )


# ---------------------------------------------------------------------------
# CodeReview
# ---------------------------------------------------------------------------


class CodeReview:
    """
    Collects findings from the three-pass review and produces a summary.

    Usage
    -----
    >>> review = CodeReview(target="my_module.py")
    >>> review.add(Pass.POSITIVE,  Category.NAMING,   "Variables are named clearly.")
    >>> review.add(Pass.CRITICAL,  Category.DESIGN,   "God-class doing too much.",  Severity.HIGH)
    >>> review.add(Pass.BUG_HUNT,  Category.CORRECTNESS, "Off-by-one in loop.",     Severity.HIGH)
    >>> print(review.summary())
    """

    def __init__(self, target: str = ""):
        self.target: str = target
        self._findings: list[Finding] = []
