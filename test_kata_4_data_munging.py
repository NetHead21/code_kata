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

    def test_skips_header_line(self):
        rows = parse_weather(WEATHER_SAMPLE)
        days = [r[0] for r in rows]
        assert "Dy" not in days

    def test_skips_monthly_summary(self):
        rows = parse_weather(WEATHER_SAMPLE)
        days = [r[0] for r in rows]
        assert all(isinstance(d, int) for d in days)

    def test_strips_asterisk_from_min_temp(self):
        rows = parse_weather(WEATHER_SAMPLE)
        day9 = next(r for r in rows if r[0] == 9)
        assert day9[2] == 32.0

    def test_strips_asterisk_from_max_temp(self):
        rows = parse_weather(WEATHER_SAMPLE)
        day26 = next(r for r in rows if r[0] == 26)
        assert day26[1] == 97.0

    def test_day_numbers_are_ints(self):
        rows = parse_weather(WEATHER_SAMPLE)
        assert all(isinstance(r[0], int) for r in rows)

    def test_temperatures_are_floats(self):
        rows = parse_weather(WEATHER_SAMPLE)
        for _, mx, mn in rows:
            assert isinstance(mx, float)
            assert isinstance(mn, float)

    def test_correct_values_for_day_1(self):
        rows = parse_weather(WEATHER_SAMPLE)
        day1 = next(r for r in rows if r[0] == 1)
        assert day1 == (1, 88.0, 59.0)

    def test_empty_input_returns_empty_list(self):
        assert parse_weather("") == []

    def test_only_header_returns_empty_list(self):
        assert parse_weather("   Dy MxT   MnT\n") == []

    def test_row_count_matches_data_lines(self):
        # Sample has 4 data lines (days 1, 2, 9, 26); header and summary skipped
        assert len(parse_weather(WEATHER_SAMPLE)) == 4


# ---------------------------------------------------------------------------
# Part 1: Weather — weather_min_spread
# ---------------------------------------------------------------------------


class TestWeatherMinSpread:
    def test_returns_an_int(self):
        assert isinstance(weather_min_spread(WEATHER_SAMPLE), int)

    def test_simple_two_day_data(self):
        text = "  1  80  70\n  2  80  79\n"
        assert weather_min_spread(text) == 2  # spread 1 < 10

    def test_handles_asterisk_temperatures(self):
        text = "  1  90  50\n  2  86  32*\n  3  61  59\n"
        # spreads: 40, 54, 2 → day 3
        assert weather_min_spread(text) == 3

    def test_single_day(self):
        text = "  5  70  60\n"
        assert weather_min_spread(text) == 5

    def test_record_high_day_not_picked_just_because_of_asterisk(self):
        # Day 26 has max=97*, min=64 → spread 33; should NOT win
        rows = parse_weather(WEATHER_SAMPLE)
        result = weather_min_spread(WEATHER_SAMPLE)
        winning = next(r for r in rows if r[0] == result)
        assert abs(winning[1] - winning[2]) <= min(abs(r[1] - r[2]) for r in rows)


# ---------------------------------------------------------------------------
# Part 1: Weather — integration test against actual file
# ---------------------------------------------------------------------------


class TestWeatherFile:
    def test_file_exists(self):
        assert WEATHER_FILE.exists()

    def test_answer_is_day_14(self):
        # Day 14: MxT=61, MnT=59 → spread=2 (unique minimum in the dataset)
        assert weather_min_spread_from_file(WEATHER_FILE) == 14

    def test_all_30_days_parsed(self):
        rows = parse_weather(WEATHER_FILE.read_text())
        assert len(rows) == 30

    def test_day_14_has_spread_of_2(self):
        rows = parse_weather(WEATHER_FILE.read_text())
        day14 = next(r for r in rows if r[0] == 14)
        assert abs(day14[1] - day14[2]) == 2
