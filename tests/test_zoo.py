"""Tests for the web-app support layer: canonical index, zoo, fact sheet."""

from __future__ import annotations

from castles.castle import Castle
from castles.enumerate import canonical_index, count, enumerate_brute
from castles.zoo import fact_sheet, specimens


def test_canonical_index_covers_every_castle() -> None:
    castles = list(enumerate_brute(4, 2))
    assert {canonical_index(c) for c in castles} == set(range(len(castles)))


def test_canonical_index_is_sorted_by_profile() -> None:
    castles = sorted(enumerate_brute(4, 3), key=lambda c: c.profile)
    for i, castle in enumerate(castles):
        assert canonical_index(castle) == i


def test_canonical_index_none_for_odd_blocks() -> None:
    assert canonical_index(Castle(3, 2, (1, 0, 1))) is None  # 3 blocks, odd


def test_specimens_are_valid_and_unique() -> None:
    specs = specimens()
    assert len(specs) >= 5
    assert len({s.name for s in specs}) == len(specs)
    for spec in specs:
        assert spec.castle.has_even_blocks
        assert spec.castle.width >= 1
        assert spec.castle.height >= 2


def test_fact_sheet_fields() -> None:
    castle = Castle(4, 2, (1, 1, 1, 1))  # rectangle: 2 blocks, valid
    sheet = fact_sheet(castle)
    assert sheet["width"] == 4
    assert sheet["height"] == 2
    assert sheet["profile"] == [1, 1, 1, 1]
    assert sheet["blocks"] == 2
    assert sheet["valid"] is True
    assert sheet["count"] == count(4, 2) == 10
    assert sheet["canonical_index"] is not None
    assert sheet["features"]["symmetric"] is True
    assert sheet["ascii"] == "####\n####"
    assert "<svg" in sheet["svg"]


def test_fact_sheet_flags_odd_blocks() -> None:
    sheet = fact_sheet(Castle(3, 2, (1, 0, 1)))  # 3 blocks, odd
    assert sheet["valid"] is False
    assert sheet["canonical_index"] is None
