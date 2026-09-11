"""Random castle samplers."""

from __future__ import annotations

import random

from .castle import Castle
from .enumerate import count, tower_counts
from .repr.urd import from_urd


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


def _tower_max_height(word: str) -> int:
    """Maximum height reached by a tower word (0 for the empty word)."""
    height = 0
    best = 0
    for ch in word:
        if ch == "U":
            height += 1
            best = max(best, height)
        elif ch == "D":
            height -= 1
    return best


def _sample_tower(k: int, w: int, parity: int, rng: random.Random) -> str:
    """Uniformly sample a tower word of width ``w``, height at most ``k``, and
    the given block-count ``parity``, using the grammar DP tables.

    Picks the first production with probability proportional to the number of
    towers it leads to, then recurses -- the "recursive method" of Knuth/Yao.
    """
    if w == 0:
        return ""  # only the empty tower (parity 0); parity 1 is unreachable
    total = tower_counts(k, w)[parity]
    r = rng.randrange(total)
    # E_k -> R E_k
    weight = tower_counts(k, w - 1)[parity]
    if r < weight:
        return "R" + _sample_tower(k, w - 1, parity, rng)
    r -= weight
    # E_k -> U V D (empty | R E_k)
    for v in range(1, w + 1):
        v_even, v_odd = tower_counts(k - 1, v)
        for pv in (0, 1):
            w_v = v_even if pv == 0 else v_odd
            if w_v == 0:
                continue
            if v == w:
                if 1 - pv == parity:
                    if r < w_v:
                        return "U" + _sample_tower(k - 1, v, pv, rng) + "D"
                    r -= w_v
            else:
                p_tail = parity ^ (1 - pv)
                tail_count = tower_counts(k, w - v - 1)[p_tail]
                w_total = w_v * tail_count
                if r < w_total:
                    return (
                        "U"
                        + _sample_tower(k - 1, v, pv, rng)
                        + "D"
                        + "R"
                        + _sample_tower(k, w - v - 1, p_tail, rng)
                    )
                r -= w_total
    raise RuntimeError("unreachable: sampler weights do not sum to the tower count")


def random_castle_dp(w: int, h: int, *, rng: random.Random | None = None) -> Castle:
    """A uniformly random castle of width ``w`` and height ``h`` via the
    recursive method.

    Samples a uniform tower of height at most ``h - 1`` with an odd number of
    blocks from the DP tables, then resamples until its height is exactly
    ``h - 1`` (so the castle has height exactly ``h``).

    Raises :class:`ValueError` if no such castle exists.
    """
    if w < 1 or h < 1:
        raise ValueError(f"width and height must be >= 1, got ({w}, {h})")
    if count(w, h) == 0:
        raise ValueError(f"no castles of width {w} and height {h}")
    if rng is None:
        rng = random.Random()
    k = h - 1
    while True:
        tower = _sample_tower(k, w, 1, rng)  # odd number of blocks, height <= k
        if _tower_max_height(tower) == k:
            return from_urd("U" + tower + "D")
