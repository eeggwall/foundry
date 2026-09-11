"""Castle Foundry -- tools for the URD-grammar castles of Project Euler 502."""

from __future__ import annotations

from .castle import Block, Castle
from .enumerate import count, count_brute, enumerate_brute
from .generate import random_castle
from .grammar import ParseError, is_castle_string, is_tower, validate
from .render.ascii import render_ascii
from .render.svg import render_svg
from .repr.urd import from_urd, to_urd, tower_word

__all__ = [
    "Block",
    "Castle",
    "ParseError",
    "count",
    "count_brute",
    "enumerate_brute",
    "from_urd",
    "is_castle_string",
    "is_tower",
    "parse",
    "random_castle",
    "render_ascii",
    "render_svg",
    "to_urd",
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
