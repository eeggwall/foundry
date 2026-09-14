"""Castle Foundry -- tools for the URD-grammar castles of Project Euler 502."""

from __future__ import annotations

from .castle import Block, Castle
from .enumerate import (
    canonical_index,
    count,
    count_brute,
    count_dp,
    enumerate_brute,
    tower_counts,
)
from .features import degree, has_valley, is_concave, is_convex, is_symmetric, nickname, num_valleys
from .generate import random_castle, random_castle_dp
from .grammar import ParseError, is_castle_string, is_tower, validate
from .render.ascii import render_ascii
from .render.svg import render_svg
from .repr import bitgrid, heights, tree  # noqa: F401  (exposed as castles.repr.<name>)
from .repr.urd import from_urd, to_urd, tower_word
from .stats import block_count_distribution, count_symmetric, feature_histogram, mean_profile
from .zoo import Specimen, fact_sheet, specimens

__all__ = [
    "Block",
    "Castle",
    "ParseError",
    "Specimen",
    "block_count_distribution",
    "canonical_index",
    "count",
    "count_brute",
    "count_dp",
    "count_symmetric",
    "degree",
    "enumerate_brute",
    "fact_sheet",
    "feature_histogram",
    "from_urd",
    "has_valley",
    "is_castle_string",
    "is_concave",
    "is_convex",
    "is_symmetric",
    "is_tower",
    "mean_profile",
    "nickname",
    "num_valleys",
    "parse",
    "random_castle",
    "random_castle_dp",
    "render_ascii",
    "render_svg",
    "specimens",
    "to_urd",
    "tower_counts",
    "tower_word",
    "unparse",
    "validate",
]


def parse(s: str) -> Castle:
    """Parse a URD castle string into a :class:`Castle`.

    Raises :class:`~castles.grammar.ParseError` on malformed input.
    """
    return from_urd(s)


def unparse(castle: Castle) -> str:
    """The canonical URD string for ``castle``."""
    return to_urd(castle)
