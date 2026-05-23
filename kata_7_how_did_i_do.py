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

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def add(
        self,
        review_pass: Pass,
        category: Category,
        description: str,
        severity: Severity = Severity.MEDIUM,
        location: Optional[str] = None,
    ) -> "CodeReview":
        """Append a finding and return self for chaining."""
        self._findings.append(
            Finding(review_pass, category, description, severity, location)
        )
        return self

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    @property
    def findings(self) -> list[Finding]:
        """A snapshot copy of all findings in insertion order."""
        return list(self._findings)

    def by_pass(self, review_pass: Pass) -> list[Finding]:
        """All findings from a specific review pass."""
        return [f for f in self._findings if f.review_pass == review_pass]

    def by_severity(self, severity: Severity) -> list[Finding]:
        """All findings with a specific severity level."""
        return [f for f in self._findings if f.severity == severity]

    def by_category(self, category: Category) -> list[Finding]:
        """All findings belonging to a specific category."""
        return [f for f in self._findings if f.category == category]

    def high_priority(self) -> list[Finding]:
        """All HIGH-severity findings — the things most urgently worth addressing."""
        return self.by_severity(Severity.HIGH)

    def count(self, review_pass: Optional[Pass] = None) -> int:
        """Total findings, or findings for a specific pass if *review_pass* given."""
        if review_pass is None:
            return len(self._findings)
        return len(self.by_pass(review_pass))

    # ------------------------------------------------------------------
    # Report
    # ------------------------------------------------------------------

    def summary(self) -> str:
        """Return a human-readable review report."""

        lines = []

        header = f"Code Review: {self.target}" if self.target else "Code Review"
        lines.append(header)
        lines.append("=" * len(header))
        lines.append(f"Total findings: {self.count()}")
        lines.append("")

        for rpass in Pass:
            group = self.by_pass(rpass)
            lines.append(
                f"--- {rpass.value.replace('_', ' ').title()} pass ({len(group)} finding(s)) ---"
            )
            if group:
                for f in group:
                    loc = f"  [{f.location}]" if f.location else ""
                    lines.append(
                        f"  [{f.severity.value.upper()}] {f.category.value}: {f.description}{loc}"
                    )
            else:
                lines.append("  (no findings)")
            lines.append("")

        high = self.high_priority()
        if high:
            lines.append(f"!!! {len(high)} HIGH-priority finding(s) to address !!!")
            for f in high:
                lines.append(f"  {f}")

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Checklist — prompts for each pass
# ---------------------------------------------------------------------------

CHECKLIST: dict[Pass, list[str]] = {
    Pass.POSITIVE: [
        "Where is the design particularly clear or elegant?",
        "Are there clever algorithms or data structures?",
        "Is the naming exceptionally descriptive?",
        "Is error handling done thoughtfully?",
        "Are the tests comprehensive and well-structured?",
        "Is there good separation of concerns?",
        "Is the code easy to follow on first reading?",
    ],
    Pass.CRITICAL: [
        "Are any functions or classes doing too much (god objects)?",
        "Are there magic numbers or unexplained constants?",
        "Is any logic duplicated instead of abstracted?",
        "Are names misleading or overly generic (data, tmp, x)?",
        "Is there dead code or commented-out blocks?",
        "Are there deeply nested conditionals or loops?",
        "Does the code rely on global or mutable shared state?",
        "Are there missing or incorrect docstrings?",
    ],
    Pass.BUG_HUNT: [
        "Are there off-by-one errors in loops or slices?",
        "Is user input validated at every entry point?",
        "Are edge cases handled (empty input, None, zero, max int)?",
        "Could any integer overflow or divide-by-zero occur?",
        "Are file handles, sockets, and locks always closed?",
        "Is error handling swallowing exceptions silently?",
        "Are there race conditions in concurrent code?",
        "Could any assumption about external data be violated?",
        "Are there SQL injections, format-string bugs, or XSS vectors?",
        "Are floats used where exact arithmetic is required?",
    ],
}


def checklist_for(review_pass: Pass) -> list[str]:
    """Return the prompt questions for a given review pass."""
    return list(CHECKLIST[review_pass])
