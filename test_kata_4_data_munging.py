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
