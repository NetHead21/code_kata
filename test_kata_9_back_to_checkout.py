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

    def test_empty_basket(self):
        assert checkout("") == 0

    def test_single_A(self):
        assert checkout("A") == 50

    def test_AB(self):
        assert checkout("AB") == 80

    def test_CDBA(self):
        assert checkout("CDBA") == 115

    def test_two_As(self):
        assert checkout("AA") == 100

    def test_three_As_triggers_special(self):
        assert checkout("AAA") == 130

    def test_four_As(self):
        assert checkout("AAAA") == 180

    def test_five_As(self):
        assert checkout("AAAAA") == 230

    def test_six_As_two_specials(self):
        assert checkout("AAAAAA") == 260

    def test_three_As_and_B(self):
        assert checkout("AAAB") == 160

    def test_three_As_and_two_Bs(self):
        assert checkout("AAABB") == 175

    def test_three_As_two_Bs_D(self):
        assert checkout("AAABBD") == 190

    def test_mixed_order_same_total(self):
        assert checkout("DABABA") == 190
