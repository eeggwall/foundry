# The signed grammar: why "even blocks" is a sign flip

The hard constraint in Project Euler 502 is that a castle has an **even**
number of blocks.  Rather than track parity as a separate bit, weight each
block by `−1`.  Then a tower's block-parity is the sign of its weight, and
"odd number of blocks" becomes "weight −1".

## From `E_k` to `P_k`

The unsigned grammar for towers of height at most `k` is

```
E_k -> empty | R E_k | U V D (empty | R E_k),      V = E_{k-1}, V nonempty
```

Weight each block (each `D`) by `−1`.  A peak `U V D` adds one block on top of
its sub-tower `V`, so it flips the sign of everything inside it:

```
P_k -> empty | R P_k | - U V D (empty | R P_k)
```

Reading the signed generating function off the grammar (with `x` marking an `R`
step):

```
P_k = 1 + x·P_k − (P_{k-1} − 1)(1 + x·P_k)
```

where `P_{k-1} − 1` is the *nonempty* sub-tower (the `−1` drops the empty
word).  Solving gives the rational-function update

```
P_k = (2 − P_{k-1}) / (1 − 2x + x·P_{k-1}),      P_0 = 1/(1−x)
```

## `P(1, w)` is the real part of `(1+i)^(w+1)`

For `k = 1` the recurrence collapses to

```
P(1, w) = 2·P(1, w−1) − 2·P(1, w−2)
```

whose solution is `P(1, w) = Re((1+i)^(w+1))`, i.e. [OEIS
A146559](https://oeis.org/A146559) (the real part of `(1+i)^n`) shifted by one:

```
P(1, w) = 0, -2, -4, -4, 0, 8, 16, 16, 0, -32, …
```

`tests/test_writeups.py` recomputes this identity from the integer recurrence
and checks it against `tower_counts`.

## The main formula

A castle of height `h` is `U (tower) D` with a tower of height exactly `h−1`
and an **odd** number of blocks (the base supplies the extra block, flipping
even back to odd).  The signed count splits towers by parity:

```
towers of height ≤ k with odd block count = (T(k, w) − P(k, w)) / 2
```

since `T = even + odd` and `P = even − odd`.  Subtracting the height-`≤ h−2`
case to force height exactly `h`:

```
F(w, h) = ( h^w − (h−1)^w − P(h−1, w) + P(h−2, w) ) / 2
```

## Two implementations agree

The library ships the signed grammar two ways, cross-checked in tests:

* `count(w, h)` — the closed form above, extracting `P(k, w)` by long division
  of the rational function.  Fast enough for the huge published values.
* `count_dp(w, h)` — the grammar recursion memoized on
  `(height_cap, remaining_width)`, tallying even/odd towers directly.

```python
>>> from castles.enumerate import count, count_dp
>>> count(13, 10), count_dp(13, 10)
(3729050610636, 3729050610636)
>>> count(10, 13), count_dp(10, 13)
(37959702514, 37959702514)
```

The recursive-method sampler (`random_castle_dp`) walks the same `P_k` tables
to draw castles uniformly at random, picking each grammar production with
probability proportional to the count it leads to.
