"""Locks in the numeric identities claimed by the Phase 3 writeups.

The two OEIS cross-references are recomputed here from their integer
recurrences (no floating point), so a regression in the library would fail
these tests rather than silently invalidating the notes.
"""

from __future__ import annotations

from castles.enumerate import count, tower_counts


def a038505(n: int) -> int:
    """OEIS A038505: sum of every 4th entry of row n of Pascal's triangle.

    Recurrence a(n) = 4a(n-1) - 6a(n-2) + 4a(n-3) for n > 3.
    """
    if n < 0:
        return 0
    seq = [0, 0, 1, 3]  # a(0)..a(3)
    for m in range(4, n + 1):
        seq.append(4 * seq[m - 1] - 6 * seq[m - 2] + 4 * seq[m - 3])
    return seq[n]


def a146559(n: int) -> int:
    """OEIS A146559: real part of (1+i)^n.  Recurrence a(n) = 2a(n-1) - 2a(n-2)."""
    if n < 0:
        return 0
    seq = [1, 1]  # a(0), a(1)
    if n < len(seq):
        return seq[n]
    a, b = seq[0], seq[1]
    for _ in range(2, n + 1):
        a, b = b, 2 * b - 2 * a
    return b


def test_f_w_2_is_a038505_shifted() -> None:
    # The writeup claims F(w, 2) = A038505(w + 1).
    for w in range(0, 12):
        assert count(w, 2) == a038505(w + 1), w


def test_signed_p1_is_a146559_shifted() -> None:
    # The writeup claims P(1, w) = Re((1+i)^(w+1)) = A146559(w + 1),
    # where P(1, w) is the signed tower count (even - odd).
    for w in range(0, 12):
        even, odd = tower_counts(1, w)
        assert even - odd == a146559(w + 1), w


def test_small_case_table_spot_checks() -> None:
    # Spot values from the small-case table in notes/small-cases.md.
    assert count(4, 2) == 10
    assert count(4, 3) == 21
    assert count(5, 3) == 89
    assert count(4, 4) == 117
    assert count(13, 10) == 3729050610636
    assert count(10, 13) == 37959702514
