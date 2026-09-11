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
