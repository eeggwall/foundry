# Castle Foundry — Plan

Plan of record for building out the Castle Foundry project. Divisions (R / E / N / Z) are a rhetorical device from the README; they do not map to code.

## Locked decisions

1. **Language:** Python 3.11+ throughout Phases 0–3. Phase 4 web app ships the same library to the browser via Pyodide; port to TypeScript only if performance forces it.
2. **Canonical representation:** the URD block-placement DSL as documented at <https://charlesreid1.com/wiki/Project_Euler/502/Representations>. It is a Dyck-style grammar over `{U, R, D}`:

   ```
   E_k → ε | R E_k | U V D (ε | R E_k)      where V = E_{k-1}
   ```

   Invariants:
   - `#D == #blocks`
   - no `UD` substring (zero-width block)
   - no `DU` substring (touching blocks)
   - `#D` is even
   - within a tower over a length-L base, exactly `L` `R`s appear
3. **Repo layout:** one monorepo, one Python package (`castles/`), no per-division subdirs.

## Repo layout

```
foundry/
  pyproject.toml
  README.md
  PLAN.md
  castles/
    __init__.py
    grammar.py            # URD parser/validator built from the grammar
    castle.py             # core Castle data class + block set
    repr/
      __init__.py
      urd.py              # URD ↔ Castle
      heights.py          # integer-tuple ↔ Castle
      bitgrid.py          # binary column encoding ↔ Castle
      tree.py             # parse-tree ↔ Castle
    enumerate.py          # brute force + DP counting
    generate.py           # random samplers
    stats.py              # statistics over castle sets
    features.py           # concave/convex, valleys, degree, nicknames
    render/
      __init__.py
      ascii.py
      svg.py
  tests/
    test_grammar.py
    test_repr_roundtrip.py
    test_enumerate_oracle.py
    test_generate.py
  notes/                  # writeups (markdown + generated figures)
  webapp/                 # Phase 4 — empty for now
```

## Phase 0 — spec & oracle

- Encode the URD grammar as a formal predicate; `validate(s)` derives from the grammar, not ad hoc checks.
- Brute-force enumerator: build every legal placement set for tiny `(w, h)`, canonicalize to URD, dedupe.
- Cross-check counts against Project Euler 502's published values for `(w, h)` where known. This oracle is what every future algorithm is tested against.

## Phase 1 — one-off tools

- `validate(s) -> bool | ParseError`
- `parse(s) -> Castle`, `unparse(castle) -> str`
- `heights`, `bitgrid`, `tree` round-trippers under `castles/repr/`
- `enumerate_brute(w, h) -> Iterator[Castle]`
- `random_castle(w, h)` — rejection sampler first; grammar-driven uniform sampler once counts exist
- `render_ascii`, `render_svg`

## Phase 2 — research library

- DP counting: `count(w, h)` via grammar recursion memoized on `(remaining_width, height_cap, parity)`. The signed grammar `P_k` (peaks negated) handles the even-block constraint directly.
- Uniform sampling via the recursive method using DP tables.
- Statistics: block-count distribution, height profile, symmetry counts, feature histograms.
- Feature definitions: concave/convex, valleys, castle degree, nicknames — each a predicate on a `Castle`.

## Phase 3 — writeups

One markdown note per idea in `notes/`, each generating its own SVG figures via the library. Seed list:

- URD grammar walkthrough
- Representation isomorphisms (URD ↔ heights ↔ bitgrid ↔ tree)
- Feature taxonomy
- Small-case tables and OEIS cross-refs
- The signed-grammar parity trick

## Phase 4 — web app

- **Designer:** grid editor, block palette, generators (random, tallest, widest, symmetric), feature-toggle checkboxes.
- **Inspector:** string input → rendered castle + fact sheet (block count, features, `#castles(w, h)`, canonical index).
- **Zoo:** curated gallery of named specimens, each linking to its inspector page.

Library ships to browser via Pyodide unless perf forces a TS port.

## Tooling defaults

- Tests: `pytest`.
- Lint/format: `ruff` + `ruff format`.
- Type checking: hints everywhere, `mypy --strict` on `castles/`.
- Python: 3.11+.
- No CI, no PyPI packaging, no docs site until Phase 3 needs it.
