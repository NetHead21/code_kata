from decimal import Decimal

import pytest

from kata_1_supermarket_pricing import (
    BulkPrice,
    BuyNGetMFree,
    Cart,
    CartItem,
    Money,
    PercentageDiscount,
    Product,
    UnitPrice,
    WeightedPrice,
    ZERO,
)


# ===========================================================================
# Money
# ===========================================================================


class TestMoney:
    def test_construct_from_int(self):
        assert Money(1).amount == Decimal("1")

    def test_construct_from_float(self):
        assert Money(0.65).amount == Decimal("0.65")

    def test_construct_from_str(self):
        assert Money("1.99").amount == Decimal("1.99")

    def test_construct_from_decimal(self):
        assert Money(Decimal("3.14")).amount == Decimal("3.14")

    def test_add(self):
        assert (Money("1.00") + Money("2.50")).amount == Decimal("3.50")

    def test_mul_by_int(self):
        assert (Money("0.65") * 4).amount == Decimal("2.60")

    def test_mul_by_float(self):
        assert (Money("12.99") * 0.75).amount == Decimal("9.7425")

    def test_mul_by_decimal(self):
        assert (Money("8.00") * Decimal("0.5")).amount == Decimal("4.00")

    def test_str_rounds_to_two_decimal_places(self):
        assert str(Money("1.005")) == "$1.01"  # ROUND_HALF_UP

    def test_str_rounds_down(self):
        assert str(Money("1.004")) == "$1.00"

    def test_str_formats_with_dollar_sign(self):
        assert str(Money("2.60")) == "$2.60"

    def test_str_pads_to_two_decimal_places(self):
        assert str(Money("3")) == "$3.00"

    def test_repr(self):
        assert repr(Money("1.50")) == "Money(1.50)"

    def test_immutable(self):
        m = Money("1.00")
        with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
            m.amount = Decimal("2.00")  # type: ignore[misc]

    def test_zero_constant(self):
        assert ZERO.amount == Decimal("0")
