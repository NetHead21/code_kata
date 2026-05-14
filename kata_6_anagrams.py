"""
Kata06: Anagrams
http://codekata.com/kata/kata06-anagrams/

Given a word list, find all groups of words that are anagrams of each other.

Algorithm
---------
Naïve O(n²) pairwise comparison is far too slow for large dictionaries.
The efficient approach is O(n · k·log k) where k is the average word length:

  1. For each word compute a *signature* by sorting its letters.
     All anagrams of a word share the same signature ("listen" → "eilnst").
  2. Group words by signature using a dict.
  3. Any group with ≥ 2 words is an anagram set.

This runs in well under a second on dictionaries of hundreds of thousands of words.
"""
