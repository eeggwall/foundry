# Four ways to write the same castle

The tower profile — the per-column height of the castle above the base — is the
canonical *geometric* object.  Four representations are equivalent to it, and
the library round-trips freely among them.  They are all bijections, so any one
uniquely determines a castle.

## One castle, four views

Consider the two-sub-block castle (base of length 3, sub-blocks in columns 1
and 3):

```
#.#
###
```

| Representation | Value |
|---|---|
| URD string | `UURDRURDD` |
| heights (tuple) | `(2, 1, 2)` |
| bitgrid (column masks) | `(0b11, 0b1, 0b11)` |
| tree (containment) | `base(1,1,3) → [block(2,1,1), block(2,3,3)]` |

![two-sub-block castle](figures/urdrurd.svg)

### URD — the step string

`U (tower) D`, where the tower is the skyline path.  This is the mental model
that leads to the grammar and the closed form.

### Heights — the integer tuple

Write the number of cells in each column, measured from the bottom.  A castle
of width `w` is `w` integers in `[1, h]`, with maximum `h`.  This is the
"integer tuple" representation on the wiki.

```python
>>> castles.repr.heights.to_heights(castles.parse("UURDRURDD"))
(2, 1, 2)
```

### Bitgrid — binary columns

Each column is a bit mask with bit 0 at the bottom row: a column of height `k`
is `2**k - 1`.  The wiki's "binary string" form concatenates these masks.

```python
>>> castles.repr.bitgrid.to_bitgrid(castles.parse("UURDRURDD"))
(3, 1, 3)
```

### Tree — block containment

Each block is a node; a block's children are the blocks resting directly on
top of it, left to right.  This is exactly the parse tree of the `E_k` grammar:
a peak `U V D` is a block whose sub-tower `V` is its children.

```python
>>> t = castles.repr.tree.to_tree(castles.parse("UURDRURDD"))
>>> t.block
Block(row=1, col0=1, col1=3)
>>> [c.block for c in t.children]
[Block(row=2, col0=1, col1=1), Block(row=2, col0=3, col1=3)]
```

## The isomorphisms commute

Every converter is a bijection, so any triangle of the diagram round-trips:

```
        to_heights          to_bitgrid
 profile ──────────► heights ──────────► bitgrid
    ▲                   │                    │
    │                   │                    │
  from_urd              │ from_heights       │ from_bitgrid
    │                   ▼                    ▼
   URD ◄───────────── profile ◄─────────── masks
        to_urd                    from_bitgrid
```

(and `to_tree` / `from_tree` glue the tree to the profile the same way).

```python
>>> import castles
>>> c = castles.parse("UURDRURDD")
>>> castles.repr.heights.from_heights(castles.repr.heights.to_heights(c)) == c
True
>>> castles.repr.bitgrid.from_bitgrid(castles.repr.bitgrid.to_bitgrid(c)) == c
True
>>> castles.repr.tree.from_tree(castles.repr.tree.to_tree(c)) == c
True
```

The tests in `tests/test_repr_roundtrip.py` assert these round-trips for every
castle the brute-force enumerator emits on small `(w, h)`.
