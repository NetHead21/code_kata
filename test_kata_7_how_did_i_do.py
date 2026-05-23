"""Tests for Kata06: How'd I Do?"""

import pytest

from kata_6_how_did_i_do import (
    Category,
    CodeReview,
    Finding,
    Pass,
    Severity,
    checklist_for,
    full_checklist,
)

# ---------------------------------------------------------------------------
# Pass / Severity / Category enums
# ---------------------------------------------------------------------------


class TestEnums:
    def test_pass_has_three_values(self):
        assert set(Pass) == {Pass.POSITIVE, Pass.CRITICAL, Pass.BUG_HUNT}

    def test_severity_has_three_values(self):
        assert set(Severity) == {Severity.LOW, Severity.MEDIUM, Severity.HIGH}

    def test_category_covers_key_areas(self):
        names = {c.value for c in Category}
        assert {"design", "naming", "readability", "correctness", "testing"}.issubset(
            names
        )

    def test_pass_string_values(self):
        assert Pass.POSITIVE.value == "positive"
        assert Pass.CRITICAL.value == "critical"
        assert Pass.BUG_HUNT.value == "bug_hunt"
