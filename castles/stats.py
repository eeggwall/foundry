"""Statistics over sets of castles.

These aggregate over :func:`~castles.enumerate.enumerate_brute`, so they are
meant for small ``(w, h)``; closed forms can come later.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Callable, Hashable

from .castle import Castle
from .enumerate import enumerate_brute
from .features import is_symmetric


def block_count_distribution(w: int, h: int) -> Counter[int]:
    """Distribution of total block counts over all castles of size ``(w, h)``."""
    return Counter(castle.block_count for castle in enumerate_brute(w, h))


def mean_profile(w: int, h: int) -> tuple[float, ...]:
    """Mean tower height per column, averaged over all castles of size ``(w, h)``."""
    castles = list(enumerate_brute(w, h))
    if not castles:
        return ()
    n = len(castles)
    totals = [0.0] * w
    for castle in castles:
        for c, val in enumerate(castle.profile):
            totals[c] += val
    return tuple(total / n for total in totals)


def count_symmetric(w: int, h: int) -> int:
    """Number of left-right symmetric castles of size ``(w, h)``."""
    return sum(1 for castle in enumerate_brute(w, h) if is_symmetric(castle))


def feature_histogram(w: int, h: int, feature: Callable[[Castle], Hashable]) -> Counter[Hashable]:
    """Histogram of a feature function over all castles of size ``(w, h)``."""
    return Counter(feature(castle) for castle in enumerate_brute(w, h))
