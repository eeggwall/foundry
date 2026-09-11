"""Castle enumeration and counting.

Phase 0 ships two independent counters that must agree:

* :func:`count_brute` -- exhaustive enumeration over all ``h**w`` height
  profiles; the ground truth for small ``(w, h)``.
* :func:`count` -- the closed-form oracle built on the signed grammar ``P_k``;
  fast enough for the published Project Euler 502 values.

Agreement between the two (plus the published values) is the oracle every
future algorithm is tested against.
"""

from __future__ import annotations

import itertools
from collections.abc import Iterator
from functools import cache

from .castle import Castle
from .repr.urd import to_urd


def enumerate_brute(w: int, h: int) -> Iterator[Castle]:
    """Yield every castle of width ``w`` and height ``h``, exactly once.

    Walks every legal placement by enumerating all ``h**w`` height profiles,
    keeps those that reach height ``h`` with an even number of blocks, and
    canonicalises each to its URD string to deduplicate.
    """
    if w < 1 or h < 1:
        return
    seen: set[str] = set()
    for profile in itertools.product(range(h), repeat=w):
        if max(profile) != h - 1:
            continue
        castle = Castle(w, h, profile)
        if not castle.has_even_blocks:
            continue
        key = to_urd(castle)
        if key in seen:
            continue
        seen.add(key)
        yield castle


def count_brute(w: int, h: int) -> int:
    """Number of castles of width ``w`` and height ``h`` (brute force)."""
    return sum(1 for _ in enumerate_brute(w, h))


# --- closed-form oracle ---------------------------------------------------


def _poly_add(a: list[int], b: list[int]) -> list[int]:
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)]


def _poly_mul(a: list[int], b: list[int]) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] += ai * bj
    return out


def _signed_tower_coeff(k: int, length: int) -> int:
    """``P(k, length)``: coefficient of ``x**length`` in ``num_k / den_k``.

    The signed grammar weights each block (each ``D``) by ``-1``::

        P_k -> empty | R P_k | - U V D (empty | R P_k)

    which yields the rational-function recurrence::

        num_k = 2*den_{k-1} - num_{k-1}
        den_k = den_{k-1}*(1 - 2x) + x*num_{k-1}

    ``P(k, length)`` is extracted by long division (``den[0]`` is always 1).
    """
    if k < 0:
        return 0
    num, den = [1], [1, -1]  # num_0 = 1, den_0 = 1 - x
    for _ in range(k):
        num, den = (
            _poly_add(_poly_mul(den, [2]), _poly_mul(num, [-1])),
            _poly_add(_poly_mul(den, [1, -2]), [0] + num),
        )
    c = [0] * (length + 1)
    for n in range(length + 1):
        value = num[n] if n < len(num) else 0
        for i in range(1, min(n, len(den) - 1) + 1):
            value -= den[i] * c[n - i]
        c[n] = value
    return c[length]


def count(w: int, h: int) -> int:
    """Number of castles of width ``w`` and height ``h`` (closed form).

    ``F(w, h) = (h**w - (h-1)**w - P(h-1, w) + P(h-2, w)) / 2``
    """
    if w < 1 or h < 1:
        return 0
    if h == 1:
        return 0
    return (
        int(h**w - (h - 1) ** w - _signed_tower_coeff(h - 1, w) + _signed_tower_coeff(h - 2, w))
        // 2
    )


# --- grammar-recursion DP (Phase 2) ---------------------------------------


@cache
def tower_counts(k: int, w: int) -> tuple[int, int]:
    """``(even, odd)`` block-count tallies of tower words of width ``w`` and
    height at most ``k``, memoized on ``(height_cap, remaining_width)``.

    Follows the grammar ``E_k -> empty | R E_k | U V D (empty | R E_k)``: a
    tower is empty, a gap column (``R``) then the rest, or a peak ``U V D`` --
    which adds one block, flipping the parity of its sub-tower ``V`` -- then a
    stop or a gap column and the rest.
    """
    if k < 0:
        return (1, 0) if w == 0 else (0, 0)
    if w < 0:
        return (0, 0)
    if w == 0:
        return (1, 0)
    even, odd = tower_counts(k, w - 1)  # R E_k
    for v in range(1, w + 1):
        v_even, v_odd = tower_counts(k - 1, v)  # V = E_{k-1}, nonempty (v >= 1)
        peak_even, peak_odd = v_odd, v_even  # the peak flips parity (+1 block)
        if v == w:
            even += peak_even
            odd += peak_odd
        else:
            t_even, t_odd = tower_counts(k, w - v - 1)  # tail: R E_k
            even += peak_even * t_even + peak_odd * t_odd
            odd += peak_even * t_odd + peak_odd * t_even
    return (even, odd)


def count_dp(w: int, h: int) -> int:
    """Number of castles of width ``w`` and height ``h`` via the grammar DP.

    A castle of height ``h`` is ``U (tower) D`` with a tower of height exactly
    ``h - 1`` and an odd number of blocks (the base supplies the extra block).
    """
    if w < 1 or h < 1:
        return 0
    if h == 1:
        return 0
    return tower_counts(h - 1, w)[1] - tower_counts(h - 2, w)[1]
