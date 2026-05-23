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
