"""Tests for the URD grammar recognizer."""

from __future__ import annotations

import pytest

from castles.castle import Castle
from castles.grammar import ParseError, is_castle_string, is_tower, validate
from castles.repr.urd import to_urd

# --- tower words (structural only, parity ignored) -----------------------


@pytest.mark.parametrize(
    "word",
    [
        "",  # empty tower (nothing above the base)
        "R",  # a single empty column
        "RRR",  # only empty columns
        "URD",  # a width-1 sub-block
        "URDRURD",  # wiki example: two width-1 sub-blocks, one gap
        "UURDD",  # wiki example: stacked width-1 sub-blocks
        "RUURDDR",  # leading/trailing gaps around a peak
        "URRRD",  # a width-3 sub-block
    ],
)
def test_is_tower_accepts(word: str) -> None:
    assert is_tower(word)


@pytest.mark.parametrize(
    "word",
    [
        "U",  # unbalanced up
        "D",  # unbalanced down
        "UD",  # zero-width block
        "DU",  # two touching blocks
        "UUDD",  # contains a zero-width block (UD substring)
        "URDRD",  # unbalanced (two D, one U)
        "URDURDDU",  # trailing junk / unbalanced
        "X",  # not in the alphabet
        "URDX",
    ],
)
def test_is_tower_rejects(word: str) -> None:
    assert not is_tower(word)


# --- validate: True | ParseError -----------------------------------------


@pytest.mark.parametrize(
    "s",
    [
        "UURDD",  # 1x2: base + one block (2 blocks)
        "UUUURDDDD",  # 1x4: base + three blocks (4 blocks)
        "UUUURRRRRRRRDDDD",  # 4x8 rectangle: four stacked blocks
    ],
)
def test_validate_accepts_even_castles(s: str) -> None:
    assert validate(s) is True


@pytest.mark.parametrize(
    ("s", "reason"),
    [
        ("", "not_castle_shape"),
        ("RRRR", "not_castle_shape"),
        ("UUDD", "zero_width_block"),  # tower "UD"
        ("UURDURDD", "touching_blocks"),  # tower "URDURD"
        ("UUURDRRD", "unbalanced"),  # tower "UURDRR" (two U, one D)
        ("UDRURDRUD", "drops_below_base"),  # tower "DRURDRU"
        ("UD", "odd_blocks"),
        ("UUURDDD", "odd_blocks"),
    ],
)
def test_validate_returns_reason(s: str, reason: str) -> None:
    err = validate(s)
    assert isinstance(err, ParseError)
    assert err.reason == reason


def test_validate_rejects_odd_blocks() -> None:
    # The wiki's 3-block example is well-formed but has an odd block count.
    s = "UURDRURDD"
    assert is_castle_string(s)
    err = validate(s)
    assert isinstance(err, ParseError)
    assert err.reason == "odd_blocks"


def test_validate_type_error() -> None:
    err = validate(123)
    assert isinstance(err, ParseError)
    assert err.reason == "type_error"


def test_validate_is_structure_and_parity() -> None:
    for s in ["UURDD", "UUURDDD", "UUUURDDDD", "UUUURRRRRRRRDDDD"]:
        even = s.count("D") % 2 == 0
        assert (validate(s) is True) == (is_castle_string(s) and even)


# --- round-trip through the castle model ----------------------------------


def test_to_urd_wiki_example() -> None:
    # length-3 base, width-1 sub-blocks in columns 1 and 3, column 2 empty
    castle = Castle(3, 2, (1, 0, 1))
    assert to_urd(castle) == "UURDRURDD"


def test_to_urd_rectangle() -> None:
    # 4x8 rectangle: base + three full-width blocks
    castle = Castle(8, 4, (3, 3, 3, 3, 3, 3, 3, 3))
    assert to_urd(castle) == "UUUURRRRRRRRDDDD"


def test_grammar_accepts_every_brute_force_output() -> None:
    # Every castle the enumerator emits must be grammar-valid and even-blocked.
    from castles.enumerate import enumerate_brute

    for w, h in [(1, 2), (2, 2), (3, 2), (4, 2), (3, 3), (4, 3)]:
        for castle in enumerate_brute(w, h):
            assert validate(to_urd(castle)) is True, (w, h, to_urd(castle))
