"""Supermarket pricing kata with composable pricing strategies.

This module models a small checkout domain that can price products sold in
different ways:

- per discrete unit, such as canned goods
- by weight, such as meat or coffee beans
- with multi-buy promotions, such as "3 for $1.00"
- with buy-N-get-M-free offers
- with percentage discounts applied on top of another strategy

The design keeps money handling decimal-safe by storing all monetary values in
``Decimal``-backed ``Money`` objects. Quantities are also normalized through
``Decimal`` so callers can pass ints, floats, strings, or ``Decimal`` values.

Important behavior notes:

- ``UnitPrice`` and ``WeightedPrice`` support fractional quantities.
- ``BulkPrice`` and ``BuyNGetMFree`` treat the quantity as a count of items and
    intentionally truncate fractional quantities using ``int(quantity)``.
- Display formatting rounds with ``ROUND_HALF_UP``, while internal arithmetic
    keeps the original ``Decimal`` precision until a value is rendered.

Running the module directly prints a sample receipt that exercises each pricing
strategy.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP
from typing import Protocol

# ---------------------------------------------------------------------------
# Money — immutable, decimal-safe
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Money:
    """Immutable wrapper around ``Decimal`` for monetary arithmetic.

    The constructor accepts several common numeric representations and converts
    them through ``str`` before creating a ``Decimal``. This avoids many of the
    surprising binary floating-point artifacts that would appear if floats were
    passed directly to ``Decimal``.

    ``Money`` intentionally exposes only the operations needed by this kata:
    addition, scalar multiplication, and user-friendly string representations.
    """

    amount: Decimal

    def __init__(self, amount: int | float | str | Decimal):
        """Create a money value from an int, float, string, or ``Decimal``."""
        object.__setattr__(self, "amount", Decimal(str(amount)))

    def __add__(self, other: Money) -> Money:
        """Return a new ``Money`` representing the sum of two amounts."""
        return Money(self.amount + other.amount)

    def __mul__(self, factor: int | float | Decimal) -> Money:
        """Return a new ``Money`` scaled by a numeric factor."""
        return Money(self.amount * Decimal(str(factor)))

    def __str__(self) -> str:
        """Format the value as dollars rounded to two decimal places."""
        return f"${self.amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}"

    def __repr__(self) -> str:
        """Return a debug-oriented representation preserving raw precision."""
        return f"Money({self.amount})"


ZERO = Money(0)
"""Convenience constant representing a zero monetary amount."""

# ---------------------------------------------------------------------------
# Pricing strategies (Protocol + implementations)
# ---------------------------------------------------------------------------


class PricingStrategy(Protocol):
    """Interface for objects that can price a product quantity.

    A strategy computes the cost for a requested quantity and can describe
    itself in receipt-friendly text.
    """

    def calculate(self, quantity: Decimal) -> Money:
        """Return the cost for ``quantity`` of a product."""
        ...

    def describe(self) -> str:
        """Return a human-readable description of the pricing rule."""
        ...


@dataclass
class UnitPrice:
    """Simple per-unit price such as ``$0.65 each``.

    This strategy multiplies the unit price by the requested quantity directly,
    so fractional quantities are allowed. That makes it usable for generic
    quantity pricing, even when the product unit name is not literally
    ``"unit"``.
    """

    price: Money

    def calculate(self, quantity: Decimal) -> Money:
        """Price ``quantity`` items at the configured per-item rate."""
        return self.price * quantity

    def describe(self) -> str:
        """Describe the strategy in receipt output."""
        return f"{self.price} each"


@dataclass
class WeightedPrice:
    """Price a product by weight, typically pounds.

    The quantity is expected to represent a weight measurement, so fractional
    values are normal and preserved.
    """

    price_per_lb: Money

    def calculate(self, quantity: Decimal) -> Money:
        """Price ``quantity`` pounds at the configured rate."""
        return self.price_per_lb * quantity

    def describe(self) -> str:
        """Describe the strategy in receipt output."""
        return f"{self.price_per_lb}/lb"


@dataclass
class BulkPrice:
    """Offer a flat price for groups of ``count`` items.

    Example: ``3 for $1.00, otherwise $0.45 each``.

    This strategy treats the quantity as a count of discrete items. Any
    fractional quantity is truncated with ``int(quantity)`` before pricing,
    because partial items do not participate in a bulk offer.
    """

    count: int
    bulk_price: Money
    unit_price: Money  # fallback price for items outside the bulk deal

    def calculate(self, quantity: Decimal) -> Money:
        """Apply bulk pricing to full groups and unit pricing to the remainder."""
        qty = int(quantity)
        bulk_groups = qty // self.count
        remainder = qty % self.count
        return self.bulk_price * bulk_groups + self.unit_price * remainder

    def describe(self) -> str:
        """Describe the offer and its fallback unit price."""
        return f"{self.count} for {self.bulk_price} (otherwise {self.unit_price} each)"


@dataclass
class BuyNGetMFree:
    """Represent a buy-N-get-M-free promotion.

    Example: buy 2, get 1 free.

    The quantity is interpreted as a discrete item count and truncated with
    ``int(quantity)``. Pricing is based on how many items in each promotion
    group must be paid for.
    """

    buy: int
    get_free: int
    unit_price: Money

    def calculate(self, quantity: Decimal) -> Money:
        """Charge only for the paid items implied by the promotion."""
        qty = int(quantity)
        group_size = self.buy + self.get_free
        full_groups = qty // group_size
        remainder = qty % group_size
        paid_in_remainder = min(remainder, self.buy)
        total_paid = full_groups * self.buy + paid_in_remainder
        return self.unit_price * total_paid

    def describe(self) -> str:
        """Describe the promotion in receipt output."""
        return f"Buy {self.buy} get {self.get_free} free @ {self.unit_price} each"


@dataclass
class PercentageDiscount:
    """Apply a percentage discount to another pricing strategy.

    This is a decorator-style strategy: it delegates to ``base_strategy`` to
    compute the undiscounted amount and then subtracts the configured percent.
    Because it wraps another strategy, it can discount unit, weighted, bulk, or
    other composite pricing rules uniformly.
    """

    base_strategy: PricingStrategy
    discount_pct: Decimal

    def calculate(self, quantity: Decimal) -> Money:
        """Return the discounted price for ``quantity``."""
        base = self.base_strategy.calculate(quantity)
        discount = base * (self.discount_pct / 100)
        return base + Money(-discount.amount)

    def describe(self) -> str:
        """Describe the discount and the wrapped base strategy."""
        return f"{self.discount_pct}% off → {self.base_strategy.describe()}"


# ---------------------------------------------------------------------------
# Product & Cart
# ---------------------------------------------------------------------------


@dataclass
class Product:
    """Sellable product with a name, pricing rule, and display unit."""

    name: str
    pricing: PricingStrategy
    unit: str = "unit"  # "unit", "lb", etc.

    def price_for(self, quantity: Decimal) -> Money:
        """Delegate quantity pricing to the configured strategy."""
        return self.pricing.calculate(quantity)


@dataclass
class CartItem:
    """Line item in a shopping cart.

    A cart item couples a ``Product`` with a requested quantity and exposes a
    computed subtotal for receipt rendering and total calculation.
    """

    product: Product
    quantity: Decimal

    @property
    def subtotal(self) -> Money:
        """Return the price of this line item."""
        return self.product.price_for(self.quantity)

    def __str__(self) -> str:
        """Render the item as a single formatted receipt line."""
        qty_str = f"{self.quantity} {self.product.unit}"
        return (
            f"  {self.product.name:<25} "
            f"qty: {qty_str:<12} "
            f"[{self.product.pricing.describe()}]  →  {self.subtotal}"
        )


@dataclass
class Cart:
    """Mutable shopping cart that accumulates items and prints receipts."""

    items: list[CartItem] = field(default_factory=list)

    def add(self, product: Product, quantity: int | float | str | Decimal) -> Cart:
        """Append a new item to the cart and return ``self`` for chaining."""
        self.items.append(CartItem(product, Decimal(str(quantity))))
        return self
