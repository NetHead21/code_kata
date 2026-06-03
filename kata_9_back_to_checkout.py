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
