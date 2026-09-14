"""Binary column encoding <-> Castle conversions.

Each column is a bit mask: bit 0 is the bottom row, and a column of height
``k`` is ``2**k - 1`` (its ``k`` lowest bits set).  This is the "binary string"
representation on the wiki, one integer per column.
"""

from __future__ import annotations

from ..castle import Castle


def to_bitgrid(castle: Castle) -> tuple[int, ...]:
    """The per-column bit masks of ``castle`` (LSB = bottom row)."""
    return tuple((1 << (h + 1)) - 1 for h in castle.profile)


def from_bitgrid(masks: tuple[int, ...]) -> Castle:
    """Rebuild the castle described by per-column bit masks."""
    if not masks:
        raise ValueError("bitgrid must be non-empty")
    heights: list[int] = []
    for mask in masks:
        k = mask.bit_length()
        if k < 1 or mask != (1 << k) - 1:
            raise ValueError(f"column mask {mask} is not a run of {k} low bits")
        heights.append(k)
    height = max(heights)
    profile = tuple(h - 1 for h in heights)
    return Castle(len(heights), height, profile)
