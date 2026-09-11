"""Tests for the castle feature predicates."""

from __future__ import annotations

from castles.castle import Castle
from castles.features import (
    degree,
    has_valley,
    is_concave,
    is_convex,
    is_symmetric,
    nickname,
    num_valleys,
)


def test_is_symmetric() -> None:
    assert is_symmetric(Castle(3, 2, (1, 0, 1)))
    assert is_symmetric(Castle(4, 3, (2, 2, 2, 2)))
    assert not is_symmetric(Castle(3, 3, (1, 0, 2)))


def test_is_convex() -> None:
    assert is_convex(Castle(4, 3, (1, 2, 2, 1)))
    assert is_convex(Castle(4, 3, (2, 2, 2, 2)))  # rectangle
    assert is_convex(Castle(3, 3, (0, 1, 2)))  # monotone climb
    assert not is_convex(Castle(3, 2, (1, 0, 1)))  # two separate peaks


def test_is_concave() -> None:
    assert is_concave(Castle(3, 2, (1, 0, 1)))
    assert is_concave(Castle(3, 3, (2, 1, 2)))
    assert not is_concave(Castle(4, 3, (2, 2, 2, 2)))  # flat: no valley
    assert not is_concave(Castle(4, 3, (1, 2, 2, 1)))  # convex


def test_convex_and_concave_are_disjoint() -> None:
    # A skyline is never both a single peak and a single (strict) valley.
    from castles.enumerate import enumerate_brute

    for w, h in [(3, 3), (4, 3), (5, 3)]:
        for castle in enumerate_brute(w, h):
            assert not (is_convex(castle) and is_concave(castle))


def test_num_valleys() -> None:
    assert num_valleys(Castle(3, 2, (1, 0, 1))) == 1
    assert num_valleys(Castle(5, 3, (2, 0, 1, 0, 2))) == 2
    assert num_valleys(Castle(4, 3, (2, 2, 2, 2))) == 0
    assert has_valley(Castle(3, 2, (1, 0, 1)))
    assert not has_valley(Castle(4, 3, (2, 2, 2, 2)))


def test_degree() -> None:
    assert degree(Castle(3, 2, (1, 0, 1))) == 2  # two blocks on the base
    assert degree(Castle(4, 3, (2, 2, 2, 2))) == 1  # one full-width block
    assert degree(Castle(1, 3, (2,))) == 1  # single column


def test_nickname() -> None:
    assert nickname(Castle(4, 3, (2, 2, 2, 2))) == "symmetric convex"
    assert nickname(Castle(3, 2, (1, 0, 1))) == "symmetric concave 1-valley"
