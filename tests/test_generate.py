"""Tests for the random castle sampler."""

from __future__ import annotations

import random

import pytest

from castles.enumerate import enumerate_brute
from castles.generate import random_castle, random_castle_dp
from castles.repr.urd import to_urd


def test_random_castle_is_valid() -> None:
    rng = random.Random(0)
    for w, h in [(4, 2), (5, 3), (4, 4), (6, 4)]:
        for _ in range(20):
            castle = random_castle(w, h, rng=rng)
            assert castle.width == w
            assert castle.height == h
            assert castle.has_even_blocks


def test_random_castle_is_deterministic_for_seed() -> None:
    a = random_castle(4, 2, rng=random.Random(123))
    b = random_castle(4, 2, rng=random.Random(123))
    assert to_urd(a) == to_urd(b)


def test_random_castle_is_uniform() -> None:
    # (4, 2) has 10 castles; a gross sanity check that none is starved or
    # overloaded by the rejection sampler.
    rng = random.Random(7)
    counts = {to_urd(c): 0 for c in enumerate_brute(4, 2)}
    n = 5000
    for _ in range(n):
        counts[to_urd(random_castle(4, 2, rng=rng))] += 1
    assert all(v > 0 for v in counts.values())
    mean = n / len(counts)
    assert all(abs(v - mean) < mean * 0.4 for v in counts.values())


def test_random_castle_raises_on_bad_dimensions() -> None:
    with pytest.raises(ValueError):
        random_castle(0, 3)
    with pytest.raises(ValueError):
        random_castle(3, 0)


def test_random_castle_raises_when_no_castles() -> None:
    # A single column of odd height can never have an even number of blocks.
    with pytest.raises(ValueError):
        random_castle(1, 3)


# --- recursive-method sampler (Phase 2) ------------------------------------


def test_random_castle_dp_is_valid() -> None:
    rng = random.Random(0)
    for w, h in [(4, 2), (5, 3), (4, 4), (6, 4)]:
        for _ in range(20):
            castle = random_castle_dp(w, h, rng=rng)
            assert castle.width == w
            assert castle.height == h
            assert castle.has_even_blocks


def test_random_castle_dp_is_deterministic_for_seed() -> None:
    a = random_castle_dp(4, 2, rng=random.Random(123))
    b = random_castle_dp(4, 2, rng=random.Random(123))
    assert to_urd(a) == to_urd(b)


def test_random_castle_dp_is_uniform() -> None:
    rng = random.Random(7)
    counts = {to_urd(c): 0 for c in enumerate_brute(4, 2)}
    n = 5000
    for _ in range(n):
        counts[to_urd(random_castle_dp(4, 2, rng=rng))] += 1
    assert all(v > 0 for v in counts.values())
    mean = n / len(counts)
    assert all(abs(v - mean) < mean * 0.4 for v in counts.values())


def test_random_castle_dp_raises_on_bad_dimensions() -> None:
    with pytest.raises(ValueError):
        random_castle_dp(0, 3)
    with pytest.raises(ValueError):
        random_castle_dp(1, 3)  # no even-block castle of odd single-column height
