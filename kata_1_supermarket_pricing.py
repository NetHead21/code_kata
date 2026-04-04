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
