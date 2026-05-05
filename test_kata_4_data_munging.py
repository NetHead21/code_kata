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
