"""Tests for Kata10: Hashes vs. Classes."""

import pytest
from dataclasses import asdict

from kata_10_hashes_vs_classes import (
    ClassBasedExporter,
    Customer,
    ExportRecord,
    HashBasedExporter,
    Order,
    ShippingDetail,
    TRADEOFF_ANALYSIS,
    record_to_dict,
)


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def customers_cls():
    return [
        Customer(1, "Alice", "alice@example.com", vip=True, country="US"),
        Customer(2, "Bob", "bob@example.com", vip=False, country="UK"),
        Customer(3, "Charlie", "charlie@example.com", vip=True, country="AU"),
        Customer(4, "Diana", "diana@example.com", vip=False, country="US"),
    ]
