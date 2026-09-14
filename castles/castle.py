"""Core castle data model.

A castle is a set of 1-row-high blocks stacked on a grid.  The canonical
geometric representation is the *profile*: a per-column tower height, measured
above the base block.  Because a block may never hang out over open space, the
occupancy of every column is downward-closed, so the profile alone determines
the whole castle (the base block plus every tower block).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Block:
    """A single 1-row-high block.

    ``row`` is the absolute 1-based row (row 1 is the base).  ``col0``/``col1``
    are the inclusive 1-based columns the block spans.
    """

    row: int
    col0: int
    col1: int

    def __post_init__(self) -> None:
        if self.row < 1:
            raise ValueError(f"row must be >= 1, got {self.row}")
        if not 1 <= self.col0 <= self.col1:
            raise ValueError(f"invalid column span [{self.col0}, {self.col1}]")

    @property
    def length(self) -> int:
        """Number of columns this block spans."""
        return self.col1 - self.col0 + 1


@dataclass(frozen=True, slots=True)
class Castle:
    """A castle of exact ``width`` and ``height``.

    ``profile`` is a ``width``-tuple giving, for each column, the number of
    tower cells stacked above the base.  It satisfies ``0 <= profile[c] <
    height`` and ``max(profile) == height - 1`` (the castle reaches height
    ``height`` exactly).
    """

    width: int
    height: int
    profile: tuple[int, ...]

    def __post_init__(self) -> None:
        if self.width < 1:
            raise ValueError(f"width must be >= 1, got {self.width}")
        if self.height < 1:
            raise ValueError(f"height must be >= 1, got {self.height}")
        if len(self.profile) != self.width:
            raise ValueError(f"profile length {len(self.profile)} != width {self.width}")
        top = max(self.profile)
        if top != self.height - 1:
            raise ValueError(f"max profile {top} != height - 1 = {self.height - 1}")
        for h in self.profile:
            if not 0 <= h < self.height:
                raise ValueError(f"profile height {h} out of range [0, {self.height})")

    @property
    def blocks(self) -> tuple[Block, ...]:
        """The base block followed by every tower block, in canonical order."""
        result: list[Block] = [Block(row=1, col0=1, col1=self.width)]
        # relative tower rows 1 .. height-1 correspond to absolute rows 2 .. height
        for rel_row in range(1, self.height):
            start: int | None = None
            for col in range(self.width):
                if self.profile[col] >= rel_row:
                    if start is None:
                        start = col
                elif start is not None:
                    result.append(Block(row=rel_row + 1, col0=start + 1, col1=col))
                    start = None
            if start is not None:
                result.append(Block(row=rel_row + 1, col0=start + 1, col1=self.width))
        return tuple(result)

    @property
    def block_count(self) -> int:
        """Total number of blocks (the base block plus every tower block)."""
        return len(self.blocks)

    @property
    def has_even_blocks(self) -> bool:
        """The Project Euler 502 parity rule: an even number of blocks."""
        return self.block_count % 2 == 0
