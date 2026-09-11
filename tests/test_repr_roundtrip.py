"""URD <-> Castle round-trip tests."""

from __future__ import annotations

import pytest

from castles.castle import Castle
from castles.enumerate import enumerate_brute
from castles.grammar import validate
from castles.repr.urd import from_urd, to_urd, tower_word


def test_tower_word_wiki_example() -> None:
    assert tower_word((1, 0, 1)) == "URDRURD"
    assert tower_word((2,)) == "UURDD"
    assert tower_word((3, 3, 3, 3, 3, 3, 3, 3)) == "UUURRRRRRRRDDD"


@pytest.mark.parametrize(
    "profile",
    [
        (0, 0),
        (1, 0, 1),
        (2, 1, 0, 1, 2),
        (3, 3, 3, 3, 3, 3, 3, 3),
        (2, 2, 0, 0, 2, 2),
    ],
)
def test_urd_to_from_roundtrip(profile: tuple[int, ...]) -> None:
    width = len(profile)
    height = 1 + max(profile)
    castle = Castle(width, height, profile)
    assert from_urd(to_urd(castle)) == castle


def test_enumerated_castles_roundtrip() -> None:
    for w, h in [(2, 2), (3, 2), (4, 2), (3, 3), (4, 3), (3, 4)]:
        for castle in enumerate_brute(w, h):
            assert from_urd(to_urd(castle)) == castle


def test_from_urd_rejects_malformed() -> None:
    with pytest.raises(ValueError):
        from_urd("")
    with pytest.raises(ValueError):
        from_urd("UUDD")  # tower "UD" is a zero-width block
    with pytest.raises(ValueError):
        from_urd("RRRR")


def test_odd_block_encoding_still_roundtrips() -> None:
    # The encoding is a bijection regardless of the even-block rule, so an odd
    # castle still round-trips (it is just not `validate`-valid).
    s = "UURDRURDD"
    assert not validate(s)  # 3 blocks, odd
    castle = from_urd(s)
    assert to_urd(castle) == s
