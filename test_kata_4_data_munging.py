"""Tests for Kata04: Data Munging."""

from pathlib import Path

import pytest

from kata_4_data_munging import (
    find_min_spread,
    football_min_spread,
    football_min_spread_from_file,
    parse_football,
    parse_weather,
    weather_min_spread,
    weather_min_spread_from_file,
)

DATA_DIR = Path(__file__).parent / "data"
WEATHER_FILE = DATA_DIR / "weather.dat"
FOOTBALL_FILE = DATA_DIR / "football.dat"


# ---------------------------------------------------------------------------
# Part 3: DRY — find_min_spread
# ---------------------------------------------------------------------------


class TestFindMinSpread:
    def test_single_record_returns_its_label(self):
        assert find_min_spread([("A", 10, 5)]) == "A"

    def test_picks_smallest_absolute_difference(self):
        records = [("X", 10, 1), ("Y", 5, 4), ("Z", 20, 0)]
        assert find_min_spread(records) == "Y"  # |5-4|=1

    def test_negative_values_use_absolute_difference(self):
        records = [("A", -10, -8), ("B", 100, 99)]
        # |−10 − −8| = 2,  |100 − 99| = 1  → B
        assert find_min_spread(records) == "B"

    def test_zero_spread_wins(self):
        records = [("A", 5, 3), ("B", 7, 7), ("C", 9, 2)]
        assert find_min_spread(records) == "B"  # |7-7|=0

    def test_integer_labels(self):
        records = [(1, 90, 50), (2, 60, 59), (3, 80, 30)]
        assert find_min_spread(records) == 2  # |60-59|=1

    def test_order_of_columns_does_not_matter(self):
        # (label, a, b) vs (label, b, a) should give same answer
        fwd = [("A", 10, 7), ("B", 5, 3)]
        rev = [("A", 7, 10), ("B", 3, 5)]
        assert find_min_spread(fwd) == find_min_spread(rev)

    def test_ties_resolved_by_first_occurrence(self):
        records = [("First", 10, 8), ("Second", 20, 18)]
        # Both have spread 2; min() returns the first one
        assert find_min_spread(records) == "First"


# ---------------------------------------------------------------------------
# Part 1: Weather — parse_weather
# ---------------------------------------------------------------------------

WEATHER_SAMPLE = """\
   Dy MxT   MnT   AvT   HDDay  AvDP

   1  88    59    74          53.8
   2  79    63    71          46.5
   9  86    32*   59          61.5
  26  97*   64    81    0     76.7
mo  82.9  60.5  71.7         58.8
"""


class TestParseWeather:
    def test_returns_list_of_tuples(self):
        rows = parse_weather(WEATHER_SAMPLE)
        assert isinstance(rows, list)
        assert all(len(r) == 3 for r in rows)
