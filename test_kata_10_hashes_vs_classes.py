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
