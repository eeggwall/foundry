"""The Phase 0 oracle: brute force vs. closed form vs. published values."""

from __future__ import annotations

import pytest

from castles.enumerate import count, count_brute, enumerate_brute
from castles.repr.urd import to_urd

# Published Project Euler 502 values (from the problem statement / wiki).
PUBLISHED: dict[tuple[int, int], int] = {
    (4, 2): 10,
    (13, 10): 3729050610636,
    (10, 13): 37959702514,
}


def test_brute_force_f42() -> None:
    assert count_brute(4, 2) == 10


def test_enumerate_brute_f42_is_exactly_ten() -> None:
    castles = list(enumerate_brute(4, 2))
    assert len(castles) == 10
    # canonicalization is injective: no two castles share a URD string
    keys = [to_urd(c) for c in castles]
    assert len(keys) == len(set(keys)) == 10


@pytest.mark.parametrize(("w", "h", "expected"), [(w, h, n) for (w, h), n in PUBLISHED.items()])
def test_closed_form_matches_published(w: int, h: int, expected: int) -> None:
    assert count(w, h) == expected


def test_closed_form_f100_100_mod() -> None:
    assert count(100, 100) % 1_000_000_007 == 841913936


@pytest.mark.parametrize("w", range(1, 7))
@pytest.mark.parametrize("h", range(1, 7))
def test_brute_force_matches_closed_form(w: int, h: int) -> None:
    # Ground truth (exhaustive) must agree with the closed-form oracle on every
    # small case, including the h == 1 edge (zero castles).
    assert count_brute(w, h) == count(w, h), (w, h)


def test_brute_force_castles_are_valid() -> None:
    for w, h in [(3, 3), (4, 3), (5, 3), (4, 4)]:
        for castle in enumerate_brute(w, h):
            assert castle.width == w
            assert castle.height == h
            assert castle.has_even_blocks
