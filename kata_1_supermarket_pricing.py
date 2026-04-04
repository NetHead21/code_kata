"""Supermarket pricing kata with composable pricing strategies.

This module models a small checkout domain that can price products sold in
different ways:

- per discrete unit, such as canned goods
- by weight, such as meat or coffee beans
- with multi-buy promotions, such as "3 for $1.00"
- with buy-N-get-M-free offers
- with percentage discounts applied on top of another strategy

The design keeps money handling decimal-safe by storing all monetary values in
``Decimal``-backed ``Money`` objects. Quantities are also normalized through
``Decimal`` so callers can pass ints, floats, strings, or ``Decimal`` values.

Important behavior notes:

- ``UnitPrice`` and ``WeightedPrice`` support fractional quantities.
- ``BulkPrice`` and ``BuyNGetMFree`` treat the quantity as a count of items and
    intentionally truncate fractional quantities using ``int(quantity)``.
- Display formatting rounds with ``ROUND_HALF_UP``, while internal arithmetic
    keeps the original ``Decimal`` precision until a value is rendered.

Running the module directly prints a sample receipt that exercises each pricing
strategy.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP
from typing import Protocol

# ---------------------------------------------------------------------------
# Money — immutable, decimal-safe
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Money:
    """Immutable wrapper around ``Decimal`` for monetary arithmetic.

    The constructor accepts several common numeric representations and converts
    them through ``str`` before creating a ``Decimal``. This avoids many of the
    surprising binary floating-point artifacts that would appear if floats were
    passed directly to ``Decimal``.

    ``Money`` intentionally exposes only the operations needed by this kata:
    addition, scalar multiplication, and user-friendly string representations.
    """

    amount: Decimal

    def __init__(self, amount: int | float | str | Decimal):
        """Create a money value from an int, float, string, or ``Decimal``."""
        object.__setattr__(self, "amount", Decimal(str(amount)))

    def __add__(self, other: Money) -> Money:
        """Return a new ``Money`` representing the sum of two amounts."""
        return Money(self.amount + other.amount)

    def __mul__(self, factor: int | float | Decimal) -> Money:
        """Return a new ``Money`` scaled by a numeric factor."""
        return Money(self.amount * Decimal(str(factor)))

    def __str__(self) -> str:
        """Format the value as dollars rounded to two decimal places."""
        return f"${self.amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}"

    def __repr__(self) -> str:
        """Return a debug-oriented representation preserving raw precision."""
        return f"Money({self.amount})"


ZERO = Money(0)
"""Convenience constant representing a zero monetary amount."""

# ---------------------------------------------------------------------------
# Pricing strategies (Protocol + implementations)
# ---------------------------------------------------------------------------


class PricingStrategy(Protocol):
    """Interface for objects that can price a product quantity.

    A strategy computes the cost for a requested quantity and can describe
    itself in receipt-friendly text.
    """

    def calculate(self, quantity: Decimal) -> Money:
        """Return the cost for ``quantity`` of a product."""
        ...

    def describe(self) -> str:
        """Return a human-readable description of the pricing rule."""
        ...


@dataclass
class UnitPrice:
    """Simple per-unit price such as ``$0.65 each``.

    This strategy multiplies the unit price by the requested quantity directly,
    so fractional quantities are allowed. That makes it usable for generic
    quantity pricing, even when the product unit name is not literally
    ``"unit"``.
    """
