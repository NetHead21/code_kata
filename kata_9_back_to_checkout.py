"""
Kata09: Back to the Checkout
http://codekata.com/kata/kata09-back-to-the-checkout/

Implement a supermarket checkout that calculates the total price of scanned
items using an externally supplied pricing-rules table.

Pricing for this week:

  Item   Unit      Special
         Price     Price
  --------------------------
    A     50       3 for 130
    B     30       2 for 45
    C     20
    D     15

Design goal — decoupling
------------------------
CheckOut knows nothing about specific items or pricing strategies.
It only calls rule.price(quantity) for each SKU accumulated in the basket.
New pricing strategies (percentage discount, buy-N-get-M-free, weight-based)
are added by implementing a new PricingRule — no changes to CheckOut.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


# ---------------------------------------------------------------------------
# PricingRule protocol — the extension point
# ---------------------------------------------------------------------------


@runtime_checkable
class PricingRule(Protocol):
    """
    Any object that implements price(quantity) is a valid pricing rule.
    CheckOut depends only on this protocol, never on concrete rule types.
    """

    def price(self, quantity: int) -> int:
        """Return the total price in cents for *quantity* units of an item."""
        ...


# ---------------------------------------------------------------------------
# Concrete pricing rules
# ---------------------------------------------------------------------------


class UnitPrice:
    """Simple per-unit pricing: total = unit_price × quantity."""

    def __init__(self, unit_price: int) -> None:
        if unit_price < 0:
            raise ValueError("unit_price must be non-negative")
        self._unit_price = unit_price

    def price(self, quantity: int) -> int:
        return self._unit_price * quantity

    def __repr__(self) -> str:
        return f"UnitPrice({self._unit_price})"


class SpecialPrice:
    """
    Unit price with an optional multi-buy deal.

    Applies the special deal as many times as possible, then charges
    the unit price for the remaining items.

    Example: SpecialPrice(unit_price=50, special_qty=3, special_price=130)
      quantity=4 → 1 bundle of 3 at 130 + 1 × 50 = 180
      quantity=6 → 2 bundles of 3 at 130            = 260
    """

    def __init__(
        self,
        unit_price: int,
        special_qty: int | None = None,
        special_price: int | None = None,
    ) -> None:
        if unit_price < 0:
            raise ValueError("unit_price must be non-negative")
        if (special_qty is None) != (special_price is None):
            raise ValueError(
                "special_qty and special_price must both be set or both be None"
            )
        if special_qty is not None and special_qty < 2:
            raise ValueError("special_qty must be at least 2")

        self._unit_price = unit_price
        self._special_qty = special_qty
        self._special_price = special_price

    def price(self, quantity: int) -> int:
        if self._special_qty is None:
            return self._unit_price * quantity

        bundles = quantity // self._special_qty
        remainder = quantity % self._special_qty
        return bundles * self._special_price + remainder * self._unit_price
