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

    def test_unit_price_below_threshold(self):
        rule = SpecialPrice(unit_price=50, special_qty=3, special_price=130)
        assert rule.price(1) == 50
        assert rule.price(2) == 100

    def test_exact_special_quantity(self):
        rule = SpecialPrice(unit_price=50, special_qty=3, special_price=130)
        assert rule.price(3) == 130

    def test_one_bundle_plus_remainder(self):
        rule = SpecialPrice(unit_price=50, special_qty=3, special_price=130)
        assert rule.price(4) == 180  # 130 + 50
        assert rule.price(5) == 230  # 130 + 100

    def test_two_bundles(self):
        rule = SpecialPrice(unit_price=50, special_qty=3, special_price=130)
        assert rule.price(6) == 260

    def test_two_for_special(self):
        rule = SpecialPrice(unit_price=30, special_qty=2, special_price=45)
        assert rule.price(1) == 30
        assert rule.price(2) == 45
        assert rule.price(3) == 75  # 45 + 30
        assert rule.price(4) == 90

    def test_zero_quantity(self):
        rule = SpecialPrice(unit_price=50, special_qty=3, special_price=130)
        assert rule.price(0) == 0

    def test_negative_unit_price_raises(self):
        with pytest.raises(ValueError):
            SpecialPrice(unit_price=-1)

    def test_only_special_qty_without_price_raises(self):
        with pytest.raises(ValueError):
            SpecialPrice(unit_price=50, special_qty=3)

    def test_only_special_price_without_qty_raises(self):
        with pytest.raises(ValueError):
            SpecialPrice(unit_price=50, special_price=130)

    def test_special_qty_of_one_raises(self):
        with pytest.raises(ValueError):
            SpecialPrice(unit_price=50, special_qty=1, special_price=40)

    @pytest.mark.parametrize(
        "qty, expected",
        [
            (0, 0),
            (1, 50),
            (2, 100),
            (3, 130),
            (4, 180),
            (5, 230),
            (6, 260),
        ],
    )
    def test_item_A_pricing(self, qty, expected):
        rule = SpecialPrice(unit_price=50, special_qty=3, special_price=130)
        assert rule.price(qty) == expected

    @pytest.mark.parametrize(
        "qty, expected",
        [
            (0, 0),
            (1, 30),
            (2, 45),
            (3, 75),
            (4, 90),
        ],
    )
    def test_item_B_pricing(self, qty, expected):
        rule = SpecialPrice(unit_price=30, special_qty=2, special_price=45)
        assert rule.price(qty) == expected


# ---------------------------------------------------------------------------
# BuyNGetMFree
# ---------------------------------------------------------------------------


class TestBuyNGetMFree:
    def test_no_complete_group(self):
        rule = BuyNGetMFree(unit_price=20, buy=3, free=1)
        assert rule.price(1) == 20
        assert rule.price(2) == 40
        assert rule.price(3) == 60

    def test_one_complete_group(self):
        # buy 3, get 1 free: pay for 3, get 4 items
        rule = BuyNGetMFree(unit_price=20, buy=3, free=1)
        assert rule.price(4) == 60  # pay for 3

    def test_two_complete_groups(self):
        rule = BuyNGetMFree(unit_price=20, buy=3, free=1)
        assert rule.price(8) == 120  # pay for 6

    def test_group_plus_remainder(self):
        rule = BuyNGetMFree(unit_price=20, buy=3, free=1)
        assert rule.price(5) == 80  # 3 paid + 2 remainder

    def test_buy_two_get_one_free(self):
        rule = BuyNGetMFree(unit_price=10, buy=2, free=1)
        assert rule.price(3) == 20  # pay 2, get 3
        assert rule.price(6) == 40  # pay 4, get 6

    def test_zero_quantity(self):
        rule = BuyNGetMFree(unit_price=20, buy=3, free=1)
        assert rule.price(0) == 0

    def test_invalid_buy_raises(self):
        with pytest.raises(ValueError):
            BuyNGetMFree(unit_price=10, buy=0, free=1)

    def test_invalid_free_raises(self):
        with pytest.raises(ValueError):
            BuyNGetMFree(unit_price=10, buy=2, free=0)


# ---------------------------------------------------------------------------
# PercentageDiscount
# ---------------------------------------------------------------------------


class TestPercentageDiscount:
    def test_zero_percent_discount(self):
        rule = PercentageDiscount(unit_price=100, discount_pct=0)
        assert rule.price(3) == 300

    def test_ten_percent_discount(self):
        rule = PercentageDiscount(unit_price=100, discount_pct=10)
        assert rule.price(1) == 90
        assert rule.price(5) == 450

    def test_fifty_percent_discount(self):
        rule = PercentageDiscount(unit_price=100, discount_pct=50)
        assert rule.price(4) == 200

    def test_zero_quantity(self):
        rule = PercentageDiscount(unit_price=100, discount_pct=10)
        assert rule.price(0) == 0

    def test_100_percent_discount_raises(self):
        with pytest.raises(ValueError):
            PercentageDiscount(unit_price=100, discount_pct=100)

    def test_negative_discount_raises(self):
        with pytest.raises(ValueError):
            PercentageDiscount(unit_price=100, discount_pct=-5)


# ---------------------------------------------------------------------------
# PricingRule protocol
# ---------------------------------------------------------------------------


class TestPricingRuleProtocol:
    """Any object implementing price(quantity) satisfies the protocol."""

    def test_unit_price_satisfies_protocol(self):
        assert isinstance(UnitPrice(10), PricingRule)

    def test_special_price_satisfies_protocol(self):
        assert isinstance(SpecialPrice(10), PricingRule)

    def test_buy_n_get_m_free_satisfies_protocol(self):
        assert isinstance(BuyNGetMFree(10, 2, 1), PricingRule)

    def test_percentage_discount_satisfies_protocol(self):
        assert isinstance(PercentageDiscount(10, 5), PricingRule)

    def test_custom_rule_satisfies_protocol(self):
        class FlatFee:
            def price(self, quantity: int) -> int:
                return 99  # always 99 cents regardless of quantity

        assert isinstance(FlatFee(), PricingRule)

    def test_object_without_price_method_does_not_satisfy(self):
        assert not isinstance(object(), PricingRule)
        assert not isinstance(42, PricingRule)


# ---------------------------------------------------------------------------
# CheckOut
# ---------------------------------------------------------------------------


class TestCheckOut:
    def test_total_zero_on_empty_basket(self):
        assert CheckOut(RULES).total == 0

    def test_scan_single_item(self):
        co = CheckOut(RULES)
        co.scan("A")
        assert co.total == 50

    def test_scan_unknown_sku_raises(self):
        co = CheckOut(RULES)
        with pytest.raises(ValueError, match="Unknown SKU"):
            co.scan("Z")

    def test_scan_order_does_not_matter(self):
        orders = ["ABCD", "DCBA", "BCDA", "CDAB"]
        totals = [checkout(o) for o in orders]
        assert len(set(totals)) == 1  # all the same

    def test_special_triggered_regardless_of_scan_order(self):
        # Three A's should always cost 130 whether scanned together or spread out
        assert checkout("AAA") == 130
        assert checkout("ABA") + checkout("") == checkout("ABA")  # just a sanity check
        co = CheckOut(RULES)
        co.scan("A")
        co.scan("B")
        co.scan("A")
        co.scan("A")
        assert co.total == 160  # 130 (3A) + 30 (1B)

    def test_reset_clears_basket(self):
        co = CheckOut(RULES)
        co.scan("A")
        co.scan("B")
        assert co.total == 80
        co.reset()
        assert co.total == 0

    def test_scan_after_reset(self):
        co = CheckOut(RULES)
        co.scan("A")
        co.reset()
        co.scan("C")
        assert co.total == 20

    def test_checkout_does_not_mutate_rules(self):
        original = dict(RULES)
        co = CheckOut(RULES)
        for _ in range(5):
            co.scan("A")
        assert RULES == original

    def test_custom_pricing_rules(self):
        custom_rules = {
            "X": UnitPrice(100),
            "Y": BuyNGetMFree(unit_price=50, buy=2, free=1),
        }
        co = CheckOut(custom_rules)
        co.scan("X")
        co.scan("Y")
        co.scan("Y")
        co.scan("Y")
        # X = 100, Y: buy 2 get 1 free → pay for 2 = 100
        assert co.total == 200

    def test_repr_contains_total(self):
        co = CheckOut(RULES)
        co.scan("A")
        assert "50" in repr(co)


# ---------------------------------------------------------------------------
# price() helper
# ---------------------------------------------------------------------------


class TestPriceHelper:
    def test_empty_string(self):
        assert price("") == 0

    def test_single_item(self):
        assert price("C") == 20

    def test_uses_kata_rules_by_default(self):
        assert price("AAA") == 130

    def test_accepts_custom_rules(self):
        custom = {"X": UnitPrice(999)}
        assert price("X", custom) == 999

    def test_each_character_is_a_separate_scan(self):
        assert price("AAAB") == price("ABAA") == price("BAAA")


# ---------------------------------------------------------------------------
# Extensibility: new rule plugged in without touching CheckOut
# ---------------------------------------------------------------------------


class TestExtensibility:
    """
    Demonstrates the decoupling goal: a new pricing strategy integrates with
    CheckOut without any modification to CheckOut itself.
    """

    def test_tiered_pricing_rule(self):
        """
        Tiered pricing: different unit prices at different quantity thresholds.
        e.g. 1-4 units at 100¢, 5+ units at 80¢ each.
        """

        class TieredPrice:
            def price(self, quantity: int) -> int:
                if quantity >= 5:
                    return quantity * 80
                return quantity * 100

        rules = {"E": TieredPrice()}
        assert checkout("EEEE", rules) == 400  # 4 × 100
        assert checkout("EEEEE", rules) == 400  # 5 × 80

    def test_flat_fee_rule(self):
        """A rule that charges a flat fee regardless of quantity."""
