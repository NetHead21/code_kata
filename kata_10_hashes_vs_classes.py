"""
Kata10: Hashes vs. Classes
http://codekata.com/kata/kata10-hashes-vs-classes/

This kata is a thought experiment: when should you reach for formal classes
and when are plain dicts (hashes) a better fit?

The scenario: an export utility that reads from ~30 database tables, applies
calculations, and conditionally fetches extra data based on flag fields.

This module implements the same export pipeline twice and makes the trade-offs
tangible through working, testable code:

  ClassBasedExporter  — typed dataclasses, explicit schema, encapsulated logic
  HashBasedExporter   — dicts all the way, ad-hoc queries, late binding

Both implementations read from the same in-memory "database" and produce
export rows with identical *values* — demonstrating that the choice is about
design quality, not correctness.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any

# ---------------------------------------------------------------------------
# Shared test fixtures — an in-memory "database"
# ---------------------------------------------------------------------------

TAX_RATES: dict[str, int] = {"US": 8, "UK": 20, "AU": 10}  # percent


# ---------------------------------------------------------------------------
# Approach 1: Classes
# ---------------------------------------------------------------------------


@dataclass
class Customer:
    """A customer record from the customers table."""

    customer_id: int
    name: str
    email: str
    vip: bool  # VIP customers receive a 10 % discount on large orders
    country: str  # ISO country code; used to look up the applicable tax rate


@dataclass
class Order:
    """A single order record from the orders table."""

    order_id: int
    customer_id: int
    subtotal: int  # in cents, before discount and tax
    status: str
    special_shipping: bool = False  # True → fetch tracking info from shipping table


@dataclass
class ShippingDetail:
    """Carrier and tracking data from the shipping_details table."""

    order_id: int
    carrier: str
    tracking_number: str


@dataclass(slots=True)
class ExportRecord:
    """
    The fully populated export row.

    All fields are declared up front — the schema is explicit and
    discoverable.  Adding a new field means changing this class (and every
    place that constructs one).
    """

    customer_id: int
    customer_name: str
    customer_email: str
    order_id: int
    subtotal: int
    discount: int
    tax: int
    total: int
    status: str
    carrier: str | None = None
    tracking: str | None = None


class ClassBasedExporter:
    """
    Export pipeline implemented with typed business objects.

    Advantages experienced here:
    - Field names are checked by the type system / IDE at authoring time.
    - Calculation methods receive typed arguments; mistakes surface early.
    - `asdict(record)` gives a clean dict when serialisation is needed.

    Disadvantages experienced here:
    - Adding a new column to the export requires modifying ExportRecord.
    - The 100-column scenario means a 100-field dataclass — a lot of boilerplate.
    - Mapping database column names to class fields is extra indirection.
    """

    def __init__(
        self,
        customers: list[Customer],
        orders: list[Order],
        shipping_details: list[ShippingDetail],
    ) -> None:
        """Index customers and shipping details by their ID for O(1) lookup."""
        self._customers = {c.customer_id: c for c in customers}
        self._orders = orders
        self._shipping = {s.order_id: s for s in shipping_details}

    def export(self) -> list[ExportRecord]:
        """Build and return one ExportRecord per order, fully populated."""

        rows = []
        for order in self._orders:
            customer = self._customers[order.customer_id]
            discount = self._calculate_discount(customer, order)
            taxable = order.subtotal - discount
            tax = self._calculate_tax(taxable, customer.country)

            record = ExportRecord(
                customer_id=customer.customer_id,
                customer_name=customer.name,
                customer_email=customer.email,
                order_id=order.order_id,
                subtotal=order.subtotal,
                discount=discount,
                tax=tax,
                total=taxable + tax,
                status=order.status,
            )

            if order.special_shipping:
                detail = self._shipping.get(order.order_id)
                if detail:
                    record.carrier = detail.carrier
                    record.tracking = detail.tracking_number

            rows.append(record)
        return rows

    @staticmethod
    def _calculate_discount(customer: Customer, order: Order) -> int:
        """10 % off for VIP customers spending $100 or more."""
        if customer.vip and order.subtotal >= 10_000:
            return order.subtotal // 10
        return 0

    @staticmethod
    def _calculate_tax(taxable: int, country: str) -> int:
        """Apply the country's tax rate to *taxable* cents; unknown countries pay 0 %."""
        rate = TAX_RATES.get(country, 0)
        return taxable * rate // 100


# ---------------------------------------------------------------------------
# Approach 2: Hashes (dicts)
# ---------------------------------------------------------------------------


class HashBasedExporter:
    """
    Export pipeline implemented with plain dicts.

    The dict for each row grows incrementally: raw database columns are
    merged in first, then calculated fields are added with simple assignments,
    then conditional extra data is merged if flag fields are set.

    Advantages experienced here:
    - Adding a new export field is a one-liner (no schema change required).
    - The row is already a dict — trivially serialisable to JSON or CSV.
    - Different rows can carry different keys (sparse schema), which is useful
      when some columns apply only to certain record types.
    - Ad-hoc database queries map naturally: cursor.fetchone() → dict row.

    Disadvantages experienced here:
    - A typo in a key name (e.g. 'custmer_id') raises KeyError at runtime,
      not at authoring time.
    - IDE cannot autocomplete or type-check dict key strings.
    - The "schema" exists only in the developer's head (or documentation).
    - Merging dicts from different tables can cause silent key collisions.
    """

    def __init__(
        self,
        customers: list[dict],
        orders: list[dict],
        shipping_details: list[dict],
    ) -> None:
        """Index customers and shipping details dicts by their ID for O(1) lookup."""
        self._customers = {c["customer_id"]: c for c in customers}
        self._orders = orders
        self._shipping = {s["order_id"]: s for s in shipping_details}

    def export(self) -> list[dict]:
        """Build and return one export-row dict per order, fully populated."""
