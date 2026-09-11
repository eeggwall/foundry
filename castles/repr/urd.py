"""URD step-string <-> Castle conversions.

A castle is written as ``U (tower) D``.  The tower word is the skyline path of
the height profile: sweep columns left to right, stepping up or down to each
column's tower height with a single ``R`` per column, then step back down to
the base at the right edge.  The conversion is a bijection between height
profiles and tower words, independent of the even-block rule.
"""

from __future__ import annotations

from ..castle import Castle
from ..grammar import is_castle_string


def tower_word(profile: tuple[int, ...]) -> str:
    """Skyline path of a height profile (the interior of a castle string)."""
    parts: list[str] = []
    prev = 0
    for h in profile:
        if h >= prev:
            parts.append("U" * (h - prev))
        else:
            parts.append("D" * (prev - h))
        parts.append("R")
        prev = h
    parts.append("D" * prev)  # return to the base at the right edge
    return "".join(parts)


def to_urd(castle: Castle) -> str:
    """The canonical URD string for ``castle``."""
    return "U" + tower_word(castle.profile) + "D"


def from_urd(s: str) -> Castle:
    """Rebuild the castle encoded by a (well-formed) URD string.

    Raises :class:`ValueError` if ``s`` is not ``U (tower) D`` with a valid
    tower word.  The even-block rule is deliberately *not* enforced here -- the
    encoding is a bijection over all profiles, castle-valid or not.
    """
    if not is_castle_string(s):
        raise ValueError(f"not a well-formed castle string: {s!r}")
    tower = s[1:-1]
    profile: list[int] = []
    height = 0
    for ch in tower:
        if ch == "U":
            height += 1
        elif ch == "D":
            height -= 1
        elif ch == "R":
            profile.append(height)
        # any other character is impossible: is_castle_string already accepted it
    width = len(profile)
    total_height = 1 + max(profile, default=0)
    return Castle(width, total_height, tuple(profile))
