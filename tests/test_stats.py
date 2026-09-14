"""Tests for castle statistics."""

from __future__ import annotations

from castles.enumerate import enumerate_brute
from castles.features import is_symmetric
from castles.stats import (
    block_count_distribution,
    count_symmetric,
    feature_histogram,
    mean_profile,
)


def test_block_count_distribution_sums_to_total() -> None:
    dist = block_count_distribution(4, 2)
    assert sum(dist.values()) == 10
    assert all(k % 2 == 0 for k in dist)  # block counts are always even


def test_mean_profile_single_column() -> None:
    assert mean_profile(1, 2) == (1.0,)


def test_mean_profile_width() -> None:
    assert len(mean_profile(4, 3)) == 4


def test_count_symmetric() -> None:
    # (3, 2) symmetric castles: (1,1,1) and (0,1,0) -- both odd-block-count.
    assert count_symmetric(3, 2) == 2


def test_count_symmetric_matches_manual() -> None:
    for w, h in [(2, 2), (3, 3), (4, 3)]:
        manual = sum(1 for c in enumerate_brute(w, h) if is_symmetric(c))
        assert count_symmetric(w, h) == manual


def test_feature_histogram_sums_to_total() -> None:
    hist = feature_histogram(4, 2, lambda c: c.block_count)
    assert sum(hist.values()) == 10
    hist2 = feature_histogram(4, 2, is_symmetric)
    assert sum(hist2.values()) == 10
    assert hist2[True] + hist2[False] == 10
