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

    def test_add_zero_is_identity(self):
        m = Money("5.00")
        assert (m + ZERO).amount == m.amount

    def test_equality(self):
        assert Money("1.50") == Money("1.50")

    def test_inequality(self):
        assert Money("1.00") != Money("2.00")


# ===========================================================================
# UnitPrice
# ===========================================================================


class TestUnitPrice:
    @pytest.fixture
    def strategy(self):
        return UnitPrice(Money("0.65"))

    def test_calculate_multiple_units(self, strategy):
        assert strategy.calculate(Decimal("4")).amount == Decimal("2.60")

    def test_calculate_one_unit(self, strategy):
        assert strategy.calculate(Decimal("1")).amount == Decimal("0.65")

    def test_calculate_zero_quantity(self, strategy):
        assert strategy.calculate(Decimal("0")).amount == Decimal("0")

    def test_calculate_fractional_quantity(self):
        s = UnitPrice(Money("1.00"))
        assert s.calculate(Decimal("0.5")).amount == Decimal("0.5")

    def test_describe(self, strategy):
        assert strategy.describe() == "$0.65 each"


# ===========================================================================
# WeightedPrice
# ===========================================================================


class TestWeightedPrice:
    @pytest.fixture
    def strategy(self):
        return WeightedPrice(Money("12.99"))

    def test_calculate_fractional_lb(self, strategy):
        assert strategy.calculate(Decimal("0.75")).amount == Decimal("9.7425")

    def test_calculate_whole_lb(self, strategy):
        assert strategy.calculate(Decimal("1")).amount == Decimal("12.99")

    def test_calculate_zero_lb(self, strategy):
        assert strategy.calculate(Decimal("0")).amount == Decimal("0")

    def test_describe(self, strategy):
        assert strategy.describe() == "$12.99/lb"


# ===========================================================================
# BulkPrice
# ===========================================================================


class TestBulkPrice:
    # 3 for $1.00, otherwise $0.45 each
    @pytest.fixture
    def strategy(self):
        return BulkPrice(3, Money("1.00"), Money("0.45"))

    def test_exact_bulk_group(self, strategy):
        # 3 items → 1 group × $1.00 + 0 remainder
        assert strategy.calculate(Decimal("3")).amount == Decimal("1.00")

    def test_multiple_bulk_groups(self, strategy):
        # 6 items → 2 groups × $1.00
        assert strategy.calculate(Decimal("6")).amount == Decimal("2.00")

    def test_bulk_group_with_remainder(self, strategy):
        # 5 items → 1 group × $1.00 + 2 × $0.45 = $1.90
        assert strategy.calculate(Decimal("5")).amount == Decimal("1.90")

    def test_all_remainder_no_bulk(self, strategy):
        # 2 items → 0 groups + 2 × $0.45 = $0.90
        assert strategy.calculate(Decimal("2")).amount == Decimal("0.90")

    def test_one_item(self, strategy):
        assert strategy.calculate(Decimal("1")).amount == Decimal("0.45")

    def test_zero_quantity(self, strategy):
        assert strategy.calculate(Decimal("0")).amount == Decimal("0")

    def test_remainder_is_count_minus_one(self, strategy):
        # 8 items → 2 groups × $1.00 + 2 × $0.45 = $2.90
        assert strategy.calculate(Decimal("8")).amount == Decimal("2.90")

    def test_describe(self, strategy):
        assert strategy.describe() == "3 for $1.00 (otherwise $0.45 each)"
