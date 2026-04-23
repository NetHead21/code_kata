"""
Kata04: Data Munging
http://codekata.com/kata/kata04-data-munging/

Parse two different real-world flat-file datasets, answer a simple question
from each, then refactor so that the shared logic is written only once.

Part One — Weather Data
  File: data/weather.dat  (UK daily weather records, one row per day)
  Question: which day had the smallest temperature spread (max − min)?
  Answer: day 14

Part Two — Football Data
  File: data/football.dat  (English Premier League table, one row per team)
  Question: which team had the smallest goal difference (|scored − conceded|)?
  Answer: Aston_Villa

Part Three — DRY Refactoring
  Both problems reduce to the same abstract operation:
      "Given a table of (label, a, b) rows, return the label
       where abs(a − b) is minimised."
  find_min_spread() captures this core, shared by parse_weather() and
  parse_football().  The two parsers differ only in which file they read
  and which columns they extract.

  Lesson: before writing a second similar function, look for the generalisation
  that can absorb both — but wait until you *have* the second case, not before.

Public API
----------
  find_min_spread(records)             — core algorithm, domain-agnostic
  parse_weather(text)                  → list[(day, max_temp, min_temp)]
  weather_min_spread(text)             → day number (int)
  weather_min_spread_from_file(path)   → day number (int)
  parse_football(text)                 → list[(team, scored, conceded)]
  football_min_spread(text)            → team name (str)
  football_min_spread_from_file(path)  → team name (str)
"""

import re
from pathlib import Path
