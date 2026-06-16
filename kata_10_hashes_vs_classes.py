"""
Kata10: Hashes vs. Classes
http://codekata.com/kata/kata10-hashes-vs-classes/

This kata is a thought experiment: when should you reach for formal classes
and when are plain dicts (hashes) a better fit?

The scenario: an export utility that reads from ~30 database tables, applies
calculations, and conditionally fetches extra data based on flag fields.

This module implements the same export pipeline twice and makes the trade-offs
tangible through working, testable code:

  ClassBasedExporter  — typed dataclasses, explicit schema, encapsulated logic
  HashBasedExporter   — dicts all the way, ad-hoc queries, late binding

Both implementations read from the same in-memory "database" and produce
export rows with identical *values* — demonstrating that the choice is about
design quality, not correctness.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any

# ---------------------------------------------------------------------------
# Shared test fixtures — an in-memory "database"
# ---------------------------------------------------------------------------

TAX_RATES: dict[str, int] = {"US": 8, "UK": 20, "AU": 10}  # percent


# ---------------------------------------------------------------------------
# Approach 1: Classes
# ---------------------------------------------------------------------------


@dataclass
class Customer:
    """A customer record from the customers table."""
