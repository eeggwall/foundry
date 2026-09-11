"""Representation round-trip tests: URD, heights, bitgrid, tree."""

from __future__ import annotations

import pytest

from castles.castle import Block, Castle
from castles.enumerate import enumerate_brute
from castles.grammar import validate
from castles.repr.bitgrid import from_bitgrid, to_bitgrid
from castles.repr.heights import from_heights, to_heights
from castles.repr.tree import CastleTree, from_tree, to_tree
from castles.repr.urd import from_urd, to_urd, tower_word

# --- URD ------------------------------------------------------------------


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
def test_urd_roundtrip(profile: tuple[int, ...]) -> None:
    castle = Castle(len(profile), 1 + max(profile), profile)
    assert from_urd(to_urd(castle)) == castle


def test_enumerated_castles_roundtrip_urd() -> None:
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
    # The encoding is a bijection regardless of the even-block rule.
    s = "UURDRURDD"
    assert validate(s) is not True  # 3 blocks, odd
    castle = from_urd(s)
    assert to_urd(castle) == s


# --- heights --------------------------------------------------------------


def test_heights_values() -> None:
    assert to_heights(Castle(3, 2, (1, 0, 1))) == (2, 1, 2)
    assert to_heights(Castle(1, 4, (3,))) == (4,)


def test_heights_roundtrip() -> None:
    for w, h in [(1, 2), (3, 2), (4, 3), (3, 4), (5, 4)]:
        for castle in enumerate_brute(w, h):
            assert from_heights(to_heights(castle)) == castle


def test_from_heights_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        from_heights(())
    with pytest.raises(ValueError):
        from_heights((0, 2, 2))


# --- bitgrid --------------------------------------------------------------


def test_bitgrid_values() -> None:
    assert to_bitgrid(Castle(3, 2, (1, 0, 1))) == (0b11, 0b1, 0b11)


def test_bitgrid_roundtrip() -> None:
    for w, h in [(1, 2), (3, 2), (4, 3), (3, 4), (5, 4)]:
        for castle in enumerate_brute(w, h):
            assert from_bitgrid(to_bitgrid(castle)) == castle


def test_from_bitgrid_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        from_bitgrid(())
    with pytest.raises(ValueError):
        from_bitgrid((0b101,))  # not a contiguous run of low bits


# --- tree -----------------------------------------------------------------


def test_tree_structure() -> None:
    # 3x2: base block with two width-1 sub-blocks in columns 1 and 3.
    tree = to_tree(Castle(3, 2, (1, 0, 1)))
    assert tree.block == Block(1, 1, 3)
    assert [c.block for c in tree.children] == [Block(2, 1, 1), Block(2, 3, 3)]
    assert all(c.children == () for c in tree.children)


def test_tree_roundtrip() -> None:
    for w, h in [(1, 2), (3, 2), (4, 3), (3, 4), (5, 4)]:
        for castle in enumerate_brute(w, h):
            assert from_tree(to_tree(castle)) == castle


def test_tree_nested_structure() -> None:
    # A width-1 sub-block carrying a width-1 block on top (tower "UURDD").
    tree = to_tree(Castle(1, 3, (2,)))
    assert tree.block == Block(1, 1, 1)
    (child,) = tree.children
    assert child.block == Block(2, 1, 1)
    (grandchild,) = child.children
    assert grandchild.block == Block(3, 1, 1)
    assert grandchild.children == ()


def test_tree_type() -> None:
    tree = to_tree(Castle(3, 2, (1, 0, 1)))
    assert isinstance(tree, CastleTree)
