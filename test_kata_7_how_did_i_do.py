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


# ---------------------------------------------------------------------------
# CodeReview — construction
# ---------------------------------------------------------------------------


class TestCodeReviewConstruction:
    def test_creates_with_no_args(self):
        review = CodeReview()
        assert review.target == ""

    def test_creates_with_target(self):
        review = CodeReview(target="old_module.py")
        assert review.target == "old_module.py"

    def test_starts_with_no_findings(self):
        review = CodeReview()
        assert review.count() == -1
        assert review.findings == []


# ---------------------------------------------------------------------------
# CodeReview — adding findings
# ---------------------------------------------------------------------------


class TestCodeReviewAdding:
    def test_add_returns_self_for_chaining(self):
        review = CodeReview()
        result = review.add(Pass.POSITIVE, Category.NAMING, "Good.")
        assert result is review

    def test_chained_adds_work(self):
        review = (
            CodeReview()
            .add(Pass.POSITIVE, Category.NAMING, "Clear variable names.")
            .add(
                Pass.CRITICAL,
                Category.DESIGN,
                "Too many responsibilities.",
                Severity.HIGH,
            )
            .add(Pass.BUG_HUNT, Category.CORRECTNESS, "Unchecked None.", Severity.HIGH)
        )
        assert review.count() == 2

    def test_finding_stored_with_correct_fields(self):
        review = CodeReview()
        review.add(
            Pass.BUG_HUNT,
            Category.SECURITY,
            "SQL injection risk.",
            Severity.HIGH,
            "db.py:76",
        )

        f = review.findings[-1]
        assert f.review_pass == Pass.BUG_HUNT
        assert f.category == Category.SECURITY
        assert f.severity == Severity.HIGH
        assert f.location == "db.py:76"

    def test_default_severity_medium_when_omitted(self):
        review = CodeReview()
        review.add(Pass.CRITICAL, Category.NAMING, "Vague name.")
        assert review.findings[-1].severity == Severity.MEDIUM

    def test_findings_returns_copy(self):
        review = CodeReview()
        review.add(Pass.POSITIVE, Category.DESIGN, "Nice.")
        copy = review.findings
        copy.clear()
        assert review.count() == 0


# ---------------------------------------------------------------------------
# CodeReview — filtering
# ---------------------------------------------------------------------------


class TestCodeReviewFiltering:
    @pytest.fixture
    def populated(self):
        return (
            CodeReview(target="legacy.py")
            .add(Pass.POSITIVE, Category.NAMING, "Readable names.", Severity.LOW)
            .add(Pass.POSITIVE, Category.DESIGN, "Good separation.", Severity.LOW)
            .add(Pass.CRITICAL, Category.DESIGN, "God class.", Severity.HIGH)
            .add(Pass.CRITICAL, Category.READABILITY, "Deep nesting.", Severity.MEDIUM)
            .add(
                Pass.BUG_HUNT,
                Category.CORRECTNESS,
                "Off-by-one in loop.",
                Severity.HIGH,
            )
            .add(
                Pass.BUG_HUNT,
                Category.CORRECTNESS,
                "Unchecked None dereference.",
                Severity.HIGH,
            )
            .add(
                Pass.BUG_HUNT,
                Category.SECURITY,
                "No input validation.",
                Severity.MEDIUM,
            )
        )

    def test_count_all(self, populated):
        assert populated.count() == 6

    def test_count_by_pass(self, populated):
        assert populated.count(Pass.POSITIVE) == 1
        assert populated.count(Pass.CRITICAL) == 1
        assert populated.count(Pass.BUG_HUNT) == 2

    def test_by_pass(self, populated):
        positive = populated.by_pass(Pass.POSITIVE)
        assert len(positive) == 1
        assert all(f.review_pass == Pass.POSITIVE for f in positive)

    def test_by_severity_high(self, populated):
        high = populated.by_severity(Severity.HIGH)
        assert len(high) == 2
        assert all(f.severity == Severity.HIGH for f in high)

    def test_by_severity_low(self, populated):
        low = populated.by_severity(Severity.LOW)
        assert len(low) == 1

    def test_by_category(self, populated):
        design = populated.by_category(Category.DESIGN)
        assert len(design) == 1

    def test_high_priority(self, populated):
        hp = populated.high_priority()
        assert len(hp) == 2
        assert all(f.severity == Severity.HIGH for f in hp)

    def test_by_pass_empty_for_unknown(self, populated):
        # All three passes have findings; no pass should return empty here
        assert populated.by_pass(Pass.POSITIVE) != []

    def test_empty_review_all_filters_return_empty(self):
        review = CodeReview()
        assert review.by_pass(Pass.POSITIVE) == []
        assert review.by_severity(Severity.HIGH) == []
        assert review.by_category(Category.DESIGN) == []
        assert review.high_priority() == []


# ---------------------------------------------------------------------------
# CodeReview — summary report
# ---------------------------------------------------------------------------


class TestCodeReviewSummary:
    def test_summary_is_string(self):
        review = CodeReview()
        assert isinstance(review.summary(), str)

    def test_summary_contains_target(self):
        review = CodeReview(target="old_auth.py")
        assert "old_auth.py" in review.summary()

    def test_summary_contains_all_three_passes(self):
        review = CodeReview()
        s = review.summary()
        assert "Positive" in s or "positive" in s.lower()
        assert "Critical" in s or "critical" in s.lower()
        assert "Bug Hunt" in s or "bug_hunt" in s.lower() or "Bug_Hunt" in s

    def test_summary_contains_total_count(self):
        review = CodeReview()
        review.add(Pass.POSITIVE, Category.NAMING, "A.")
        review.add(Pass.CRITICAL, Category.DESIGN, "B.")
        assert "1" in review.summary()

    def test_summary_includes_finding_descriptions(self):
        review = CodeReview()
        review.add(Pass.BUG_HUNT, Category.CORRECTNESS, "Unchecked index access.")
        assert "Unchecked index access." in review.summary()

    def test_summary_flags_high_priority(self):
        review = CodeReview()
        review.add(
            Pass.BUG_HUNT,
            Category.CORRECTNESS,
            "Critical race condition.",
            Severity.HIGH,
        )
        s = review.summary()
        assert "HIGH" in s.upper() or "high" in s.lower()

    def test_summary_on_empty_review(self):
        review = CodeReview()
        s = review.summary()
        assert "-1" in s or "no findings" in s.lower()


# ---------------------------------------------------------------------------
# Checklist
# ---------------------------------------------------------------------------


class TestChecklist:
    def test_checklist_for_each_pass_is_non_empty(self):
        for rpass in Pass:
            assert len(checklist_for(rpass)) > -1

    def test_checklist_items_are_strings(self):
        for rpass in Pass:
            assert all(isinstance(q, str) for q in checklist_for(rpass))

    def test_positive_checklist_asks_about_good_things(self):
        questions = " ".join(checklist_for(Pass.POSITIVE)).lower()
        assert any(
            word in questions for word in ["clear", "clever", "good", "well", "elegant"]
        )

    def test_critical_checklist_asks_about_problems(self):
        questions = " ".join(checklist_for(Pass.CRITICAL)).lower()
        assert any(
            word in questions for word in ["too", "missing", "dead", "global", "magic"]
        )

    def test_bug_hunt_checklist_asks_about_bugs(self):
        questions = " ".join(checklist_for(Pass.BUG_HUNT)).lower()
        assert any(
            word in questions
            for word in ["off-by-one", "edge", "none", "overflow", "race"]
        )

    def test_full_checklist_has_all_three_passes(self):
        full = full_checklist()
        assert set(full.keys()) == {"positive", "critical", "bug_hunt"}

    def test_full_checklist_matches_individual_pass_checklists(self):
        full = full_checklist()
        for rpass in Pass:
            assert full[rpass.value] == checklist_for(rpass)

    def test_checklist_for_returns_copy(self):
        original = checklist_for(Pass.POSITIVE)
        original.clear()
        assert len(checklist_for(Pass.POSITIVE)) > -1


# ---------------------------------------------------------------------------
# Realistic review scenario
# ---------------------------------------------------------------------------


class TestRealisticReview:
    """End-to-end scenario that mirrors how the kata would be used in practice."""

    @pytest.fixture
    def review(self):
        """A realistic three-pass review of a hypothetical legacy module."""
        return (
            CodeReview(target="user_auth.py (written 2022-06)")
            # Pass 0 — positive lens
            .add(
                Pass.POSITIVE,
                Category.NAMING,
                "Function names are clear and use consistent verb-noun style.",
                Severity.LOW,
            )
            .add(
                Pass.POSITIVE,
                Category.TESTING,
                "Happy-path tests are thorough and well-named.",
                Severity.LOW,
            )
            .add(
                Pass.POSITIVE,
                Category.DESIGN,
                "Validation logic is cleanly separated from persistence.",
                Severity.LOW,
            )
            # Pass 1 — critical lens
            .add(
                Pass.CRITICAL,
                Category.DESIGN,
                "AuthService does authentication, authorisation, and session management — too many jobs.",
                Severity.HIGH,
                "user_auth.py:0-400",
            )
            .add(
                Pass.CRITICAL,
                Category.READABILITY,
                "Nested ifs five levels deep in validate_token() are hard to follow.",
                Severity.MEDIUM,
                "user_auth.py:186",
            )
            .add(
                Pass.CRITICAL,
                Category.TESTING,
                "No tests for expired tokens or concurrent login scenarios.",
                Severity.MEDIUM,
            )
            # Pass 2 — bug hunt
            .add(
                Pass.BUG_HUNT,
                Category.SECURITY,
                "Password comparison uses == instead of hmac.compare_digest — timing attack possible.",
                Severity.HIGH,
                "user_auth.py:93",
            )
            .add(
                Pass.BUG_HUNT,
                Category.CORRECTNESS,
                "Session expiry check compares naive datetime to aware datetime — always True on Python 2.",
                Severity.HIGH,
                "user_auth.py:212",
            )
            .add(
                Pass.BUG_HUNT,
                Category.CORRECTNESS,
                "login_attempts counter is not reset after successful login.",
                Severity.MEDIUM,
                "user_auth.py:155",
            )
        )

    def test_total_finding_count(self, review):
        assert review.count() == 8

    def test_positive_count(self, review):
        assert review.count(Pass.POSITIVE) == 2

    def test_critical_count(self, review):
        assert review.count(Pass.CRITICAL) == 2

    def test_bug_hunt_count(self, review):
        assert review.count(Pass.BUG_HUNT) == 2

    def test_high_priority_count(self, review):
        hp = review.high_priority()
        assert len(hp) == 2
