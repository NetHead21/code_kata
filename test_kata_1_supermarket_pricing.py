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


# ===========================================================================
# BuyNGetMFree
# ===========================================================================


class TestBuyNGetMFree:
    # Buy 2 get 1 free @ $1.50 each  (group_size = 3)
    @pytest.fixture
    def strategy(self):
        return BuyNGetMFree(2, 1, Money("1.50"))

    def test_zero_quantity(self, strategy):
        assert strategy.calculate(Decimal("0")).amount == Decimal("0")

    def test_one_item_less_than_group(self, strategy):
        # qty=1 → no free triggered, pay 1
        assert strategy.calculate(Decimal("1")).amount == Decimal("1.50")

    def test_exactly_buy_count(self, strategy):
        # qty=2 → no free triggered yet, pay 2
        assert strategy.calculate(Decimal("2")).amount == Decimal("3.00")

    def test_exact_one_full_group(self, strategy):
        # qty=3 → 1 group, pay 2
        assert strategy.calculate(Decimal("3")).amount == Decimal("3.00")

    def test_multiple_full_groups(self, strategy):
        # qty=6 → 2 groups, pay 4
        assert strategy.calculate(Decimal("6")).amount == Decimal("6.00")

    def test_remainder_within_buy_count(self, strategy):
        # qty=7 → 2 groups (pay 4) + 1 remainder (pay 1) = pay 5  [demo case]
        assert strategy.calculate(Decimal("7")).amount == Decimal("7.50")

    def test_remainder_equals_buy_count(self, strategy):
        # qty=8 → 2 groups (pay 4) + 2 remainder (pay 2) = pay 6
        assert strategy.calculate(Decimal("8")).amount == Decimal("9.00")

    def test_remainder_exceeds_buy_count(self, strategy):
        # qty=5 → 1 group (pay 2) + 2 remainder (pay 2) = pay 4
        assert strategy.calculate(Decimal("5")).amount == Decimal("6.00")

    def test_buy_1_get_1_free(self):
        # Every other item is free
        s = BuyNGetMFree(1, 1, Money("2.00"))
        assert s.calculate(Decimal("4")).amount == Decimal("4.00")  # pay 2 of 4
        assert s.calculate(Decimal("5")).amount == Decimal("6.00")  # pay 3 of 5

    def test_describe(self, strategy):
        assert strategy.describe() == "Buy 2 get 1 free @ $1.50 each"


# ===========================================================================
# PercentageDiscount
# ===========================================================================


class TestPercentageDiscount:
    def test_10_percent_off_weighted_price(self):
        # 0.5 lb × $8.00 = $4.00 base, 10% off → $3.60  [demo case]
        s = PercentageDiscount(WeightedPrice(Money("8.00")), Decimal("10"))
        assert s.calculate(Decimal("0.5")).amount == Decimal("3.60")

    def test_0_percent_off_equals_base(self):
        base = UnitPrice(Money("1.00"))
        s = PercentageDiscount(base, Decimal("0"))
        assert s.calculate(Decimal("3")).amount == Decimal("3.00")

    def test_100_percent_off_is_zero(self):
        base = UnitPrice(Money("5.00"))
        s = PercentageDiscount(base, Decimal("100"))
        assert s.calculate(Decimal("2")).amount == Decimal("0")

    def test_50_percent_off(self):
        base = UnitPrice(Money("2.00"))
        s = PercentageDiscount(base, Decimal("50"))
        assert s.calculate(Decimal("4")).amount == Decimal("4.00")

    def test_wraps_bulk_price(self):
        # 10% off "3 for $1.00" applied to 3 items → $0.90
        base = BulkPrice(3, Money("1.00"), Money("0.45"))
        s = PercentageDiscount(base, Decimal("10"))
        assert s.calculate(Decimal("3")).amount == Decimal("0.90")

    def test_describe(self):
        s = PercentageDiscount(WeightedPrice(Money("8.00")), Decimal("10"))
        assert s.describe() == "10% off → $8.00/lb"


# ===========================================================================
# Product
# ===========================================================================


class TestProduct:
    def test_price_for_delegates_to_strategy(self):
        p = Product("Beans", UnitPrice(Money("0.65")))
        assert p.price_for(Decimal("4")).amount == Decimal("2.60")

    def test_default_unit_is_unit(self):
        p = Product("Beans", UnitPrice(Money("0.65")))
        assert p.unit == "unit"

    def test_custom_unit(self):
        p = Product("Steak", WeightedPrice(Money("12.99")), unit="lb")
        assert p.unit == "lb"


# ===========================================================================
# CartItem
# ===========================================================================


class TestCartItem:
    @pytest.fixture
    def item(self):
        product = Product("Canned Beans", UnitPrice(Money("0.65")), unit="unit")
        return CartItem(product, Decimal("4"))

    def test_subtotal(self, item):
        assert item.subtotal.amount == Decimal("2.60")

    def test_str_contains_product_name(self, item):
        assert "Canned Beans" in str(item)

    def test_str_contains_quantity(self, item):
        assert "4" in str(item)

    def test_str_contains_subtotal(self, item):
        assert "$2.60" in str(item)

    def test_str_contains_pricing_description(self, item):
        assert "$0.65 each" in str(item)

    def test_str_contains_unit(self, item):
        assert "unit" in str(item)


# ===========================================================================
# Cart
# ===========================================================================


class TestCart:
    def test_empty_cart_total_is_zero(self):
        assert Cart().total.amount == Decimal("0")

    def test_add_returns_self_for_chaining(self):
        product = Product("Beans", UnitPrice(Money("0.65")))
        cart = Cart()
        result = cart.add(product, 1)
        assert result is cart

    def test_add_accepts_int(self):
        product = Product("Beans", UnitPrice(Money("1.00")))
        cart = Cart().add(product, 3)
        assert cart.total.amount == Decimal("3.00")

    def test_add_accepts_float(self):
        product = Product("Steak", WeightedPrice(Money("10.00")), unit="lb")
        cart = Cart().add(product, 0.5)
        assert cart.total.amount == Decimal("5.00")
