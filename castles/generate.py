"""Random castle samplers."""

from __future__ import annotations

import random

from .castle import Castle
from .enumerate import count


def random_castle(w: int, h: int, *, rng: random.Random | None = None) -> Castle:
    """A uniformly random castle of width ``w`` and height ``h``.

    Rejection sampling: draw a uniform height profile and keep it if it reaches
    height ``h`` with an even number of blocks.  Conditioning a uniform profile
    on validity yields the uniform distribution over castles.

    Raises :class:`ValueError` if no such castle exists (e.g. ``w == 1`` and
    ``h`` odd).
    """
    if w < 1 or h < 1:
        raise ValueError(f"width and height must be >= 1, got ({w}, {h})")
    if count(w, h) == 0:
        raise ValueError(f"no castles of width {w} and height {h}")
    if rng is None:
        rng = random.Random()
    while True:
        profile = tuple(rng.randrange(h) for _ in range(w))
        if max(profile) != h - 1:
            continue
        castle = Castle(w, h, profile)
        if castle.has_even_blocks:
            return castle
