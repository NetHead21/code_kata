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

    def test_severity_ordering_by_value(self):
        assert Severity.LOW.value == "low"
        assert Severity.MEDIUM.value == "medium"
        assert Severity.HIGH.value == "high"


# ---------------------------------------------------------------------------
# Finding
# ---------------------------------------------------------------------------


class TestFinding:
    def test_creates_with_required_fields(self):
        f = Finding(Pass.POSITIVE, Category.NAMING, "Good names throughout.")
        assert f.review_pass == Pass.POSITIVE
        assert f.category == Category.NAMING
        assert f.description == "Good names throughout."

    def test_default_severity_is_medium(self):
        f = Finding(Pass.CRITICAL, Category.DESIGN, "Some issue.")
        assert f.severity == Severity.MEDIUM

    def test_default_location_is_none(self):
        f = Finding(Pass.BUG_HUNT, Category.CORRECTNESS, "Possible overflow.")
        assert f.location is None

    def test_accepts_optional_severity_and_location(self):
        f = Finding(
            Pass.BUG_HUNT,
            Category.CORRECTNESS,
            "Off-by-one.",
            severity=Severity.HIGH,
            location="utils.py:41",
        )
        assert f.severity == Severity.HIGH
        assert f.location == "utils.py:41"

    def test_empty_description_raises(self):
        with pytest.raises(ValueError):
            Finding(Pass.POSITIVE, Category.NAMING, "")
        with pytest.raises(ValueError):
            Finding(Pass.POSITIVE, Category.NAMING, "   ")

    def test_str_includes_pass_category_description(self):
        f = Finding(Pass.CRITICAL, Category.DESIGN, "God class detected.")
        s = str(f)
        assert "CRITICAL" in s
        assert "design" in s
        assert "God class detected." in s

    def test_str_includes_location_when_present(self):
        f = Finding(Pass.BUG_HUNT, Category.CORRECTNESS, "Issue.", location="foo.py:9")
        assert "foo.py:9" in str(f)

    def test_str_excludes_location_when_absent(self):
        f = Finding(Pass.POSITIVE, Category.NAMING, "Nice names.")
        assert f.location is None
        # The location tag looks like " [foo.py:9]" — no file path in output
        assert ".py:" not in str(f)
