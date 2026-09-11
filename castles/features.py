"""Feature predicates on a :class:`Castle`.

These are working definitions for the research library; the exact formulations
are open to refinement in the Phase 3 writeups.
"""

from __future__ import annotations

from .castle import Castle


def is_symmetric(castle: Castle) -> bool:
    """True if the castle is its own left-right mirror (palindromic profile)."""
    return castle.profile == castle.profile[::-1]


def is_convex(castle: Castle) -> bool:
    """True if the skyline is unimodal (non-decreasing, then non-increasing).

    A convex castle climbs to a (possibly flat) peak and then descends -- the
    "front / middle / back" shape on the wiki.
    """
    h = castle.profile
    i = 0
    while i + 1 < len(h) and h[i] <= h[i + 1]:
        i += 1
    while i + 1 < len(h) and h[i] >= h[i + 1]:
        i += 1
    return i == len(h) - 1


def is_concave(castle: Castle) -> bool:
    """True if the skyline is a single valley.

    The profile must be non-increasing then non-decreasing *and* dip strictly
    somewhere (so a flat or monotonic skyline is not called concave).
    """
    if not has_valley(castle):
        return False
    h = castle.profile
    i = 0
    while i + 1 < len(h) and h[i] >= h[i + 1]:
        i += 1
    while i + 1 < len(h) and h[i] <= h[i + 1]:
        i += 1
    return i == len(h) - 1


def num_valleys(castle: Castle) -> int:
    """Number of local minima in the skyline (a strict dip between two columns)."""
    h = castle.profile
    return sum(1 for c in range(1, len(h) - 1) if h[c - 1] > h[c] < h[c + 1])


def has_valley(castle: Castle) -> bool:
    """True if the skyline has at least one local minimum."""
    return num_valleys(castle) > 0


def degree(castle: Castle) -> int:
    """Number of blocks resting directly on the base.

    Equivalently, the number of children of the root in the block-containment
    tree: the count of maximal runs of columns with tower height at least 1.
    """
    runs = 0
    in_run = False
    for h in castle.profile:
        if h >= 1:
            if not in_run:
                runs += 1
                in_run = True
        else:
            in_run = False
    return runs


def nickname(castle: Castle) -> str:
    """A short, deterministic descriptor of the castle's shape."""
    parts: list[str] = []
    if is_symmetric(castle):
        parts.append("symmetric")
    if is_convex(castle):
        parts.append("convex")
    elif is_concave(castle):
        parts.append("concave")
    else:
        parts.append("complex")
    if has_valley(castle):
        parts.append(f"{num_valleys(castle)}-valley")
    return " ".join(parts)
