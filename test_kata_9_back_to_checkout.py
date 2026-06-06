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


class TestKataIncremental:
    """Incremental scanning test from the kata description."""

    def test_incremental_scanning(self):
        co = CheckOut(RULES)
        assert co.total == 0
        co.scan("A")
        assert co.total == 50
        co.scan("B")
        assert co.total == 80
        co.scan("A")
        assert co.total == 130
        co.scan("A")
        assert co.total == 160
        co.scan("B")
        assert co.total == 175


# ---------------------------------------------------------------------------
# UnitPrice
# ---------------------------------------------------------------------------


class TestUnitPrice:
    def test_zero_quantity(self):
        assert UnitPrice(50).price(0) == 0

    def test_one_unit(self):
        assert UnitPrice(50).price(1) == 50

    def test_multiple_units(self):
        assert UnitPrice(20).price(5) == 100

    def test_zero_price(self):
        assert UnitPrice(0).price(99) == 0

    def test_negative_unit_price_raises(self):
        with pytest.raises(ValueError):
            UnitPrice(-1)

    def test_repr(self):
        assert "50" in repr(UnitPrice(50))


# ---------------------------------------------------------------------------
# SpecialPrice
# ---------------------------------------------------------------------------


class TestSpecialPrice:
    def test_no_special_falls_back_to_unit(self):
        rule = SpecialPrice(unit_price=50)
        assert rule.price(3) == 150
