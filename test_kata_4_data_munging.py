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
