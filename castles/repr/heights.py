"""Integer-tuple (column heights) <-> Castle conversions.

A castle of width ``w`` is ``w`` integers: the height of each column measured
from the bottom (so the base row contributes 1).  This is the "integer tuple"
representation on the wiki -- the per-column count of cells.
"""

from __future__ import annotations

from ..castle import Castle


def to_heights(castle: Castle) -> tuple[int, ...]:
    """The per-column heights of ``castle`` (base row included)."""
    return tuple(h + 1 for h in castle.profile)


def from_heights(heights: tuple[int, ...]) -> Castle:
    """Rebuild the castle described by a tuple of column heights."""
    if not heights:
        raise ValueError("heights tuple must be non-empty")
    if any(h < 1 for h in heights):
        raise ValueError(f"column heights must be >= 1, got {heights}")
    height = max(heights)
    profile = tuple(h - 1 for h in heights)
    return Castle(len(heights), height, profile)
