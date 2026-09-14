# Small cases and OEIS cross-references

`F(w, h)` is the number of castles of width `w` and height `h`.  Every value
here is produced by the library's three independent counters (`count_brute`,
`count` closed-form, `count_dp` grammar DP), which agree on all `(w, h)` tested.

## The `F(w, h)` table

| w \ h | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| **1** | 0 | 1 | 0 | 1 | 0 | 1 |
| **2** | 0 | 3 | 0 | 7 | 0 | 11 |
| **3** | 0 | 6 | 3 | 31 | 10 | 76 |
| **4** | 0 | 10 | 21 | 117 | 122 | 448 |
| **5** | 0 | 16 | 89 | 439 | 906 | 2630 |
| **6** | 0 | 28 | 307 | 1729 | 5478 | 16126 |

Published Project Euler 502 checkpoints: `F(4,2) = 10`, `F(13,10) =
3729050610636`, `F(10,13) = 37959702514`, and `F(100,100) mod 10^9+7 =
841913936`.

Two patterns jump out of the table:

* `F(w, 1) = 0` — a castle of height 1 is just the base block, one block, odd.
* `F(1, h)` alternates 0, 1, 0, 1, … — a single column has `h` blocks, even
  exactly when `h` is even.

## Height 2 is a known sequence

`F(w, 2)` for `w = 0, 1, 2, …` is

```
0, 1, 3, 6, 10, 16, 28, 56, 120, 256, 528, 1056, 2080, …
```

This is [OEIS A038505](https://oeis.org/A038505), *sum of every 4th entry of
row n in Pascal's triangle*, shifted by one:

```
F(w, 2) = A038505(w + 1)
```

with closed form `a(n) = (2^n − (1−i)^n − (1+i)^n) / 4` and recurrence
`a(n) = 4a(n−1) − 6a(n−2) + 4a(n−3)`.  `tests/test_writeups.py` verifies the
identity directly against the library.

## Convex castles are binomial

The number of *convex* castles is the stars-and-bars count

```
CCC(w, h) = C(2h + w − 3, w − 1)
```

| w \ h | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| **1** | 1 | 1 | 1 | 1 | 1 |
| **2** | 1 | 3 | 5 | 7 | 9 |
| **3** | 1 | 6 | 15 | 28 | 45 |
| **4** | 1 | 10 | 35 | 84 | 165 |
| **5** | 1 | 15 | 70 | 210 | 495 |
| **6** | 1 | 21 | 126 | 462 | 1287 |

(These are just Pascal's triangle entries, [OEIS A007318](https://oeis.org/A007318).)

## Towers are powers

Towers of height at most `k` over a length-`L` base number `T(k, L) = (k+1)^L`
— the `E_k` grammar has `k+1` choices per column.

## Block-count distributions

For small sizes the distribution of block counts is concentrated:

| (w, h) | castles | block-count distribution |
|---|---|---|
| (4, 3) | 21 | 4 → 21 |
| (4, 4) | 117 | 4 → 84, 6 → 33 |

```python
>>> from castles.stats import block_count_distribution
>>> block_count_distribution(4, 4)
Counter({4: 84, 6: 33})
```

## Symmetry

Left-right symmetric castles are rare for larger `w`:

```python
>>> castles.stats.count_symmetric(4, 4)
5
>>> castles.stats.count_symmetric(5, 3)
5
```
