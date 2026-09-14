"""Parse-tree <-> Castle conversions.

Each block becomes a node; a block's children are the blocks resting directly
on top of it, left to right.  This is exactly the tree the ``E_k`` grammar
gives: a peak ``U V D`` is a block whose sub-tower ``V`` is its children, and
``empty | R E_k`` yields the sibling blocks.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..castle import Block, Castle


@dataclass(frozen=True, slots=True)
class CastleTree:
    """A rooted block-containment tree.  The root is the base block."""

    block: Block
    children: tuple[CastleTree, ...]


def to_tree(castle: Castle) -> CastleTree:
    """The block-containment tree of ``castle`` (root = the base block)."""
    by_row: dict[int, list[Block]] = {}
    for block in castle.blocks:
        by_row.setdefault(block.row, []).append(block)

    def build(block: Block) -> CastleTree:
        children = tuple(
            build(child)
            for child in by_row.get(block.row + 1, ())
            if block.col0 <= child.col0 and child.col1 <= block.col1
        )
        return CastleTree(block, children)

    return build(castle.blocks[0])


def from_tree(tree: CastleTree) -> Castle:
    """Rebuild the castle described by a block-containment tree."""
    blocks: list[Block] = []

    def walk(node: CastleTree) -> None:
        blocks.append(node.block)
        for child in node.children:
            walk(child)

    walk(tree)
    width = tree.block.length
    height = max(block.row for block in blocks)
    profile = [0] * width
    for block in blocks:
        for col in range(block.col0, block.col1 + 1):
            idx = col - 1
            if block.row - 1 > profile[idx]:
                profile[idx] = block.row - 1
    return Castle(width, height, tuple(profile))
