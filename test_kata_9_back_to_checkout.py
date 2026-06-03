"""Tests for Kata09: Back to the Checkout."""

import pytest

from kata_9_back_to_checkout import (
    BuyNGetMFree,
    CheckOut,
    PercentageDiscount,
    PricingRule,
    RULES,
    SpecialPrice,
    UnitPrice,
    price,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def checkout(goods: str, rules=RULES) -> int:
    """Scan every character in *goods* and return the total."""
    co = CheckOut(rules)
    for item in goods:
        co.scan(item)
    return co.total


# ---------------------------------------------------------------------------
# Kata-supplied test cases (translated directly from the Ruby spec)
# ---------------------------------------------------------------------------


class TestKataTotals:
    """Exact test cases from the kata description."""
