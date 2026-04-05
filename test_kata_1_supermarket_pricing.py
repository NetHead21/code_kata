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
