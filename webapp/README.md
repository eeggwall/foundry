# Castle Foundry — web app

A single-page app with three views.  It runs entirely in the browser as plain
JavaScript — a direct port of the `castles` library (`webapp/castles.js`) — so
there's no server-side Python, no Pyodide, and no build step.

* **Designer** — a click-to-edit tower grid, generators (random / tallest /
  widest / symmetric), and feature toggles (symmetric / convex / concave).
* **Inspector** — a URD string in, a rendered castle and fact sheet out (block
  count, features, `#castles(w, h)`, canonical index).
* **Zoo** — the named specimens, each linking into the Inspector.

## Running it

Serve the `webapp/` directory (or the repo root) and open it:

```bash
python -m http.server 8000
# open http://localhost:8000/webapp/
```

That's it — no dependencies, no wheel, no CDN runtime.

## How it works

`castles.js` is a port of the core library: the URD grammar parser, the block
geometry, the feature predicates, the grammar-DP counter `count(w, h)`, and the
SVG renderer.  Its behaviour matches `castles/*.py` — verified in Node against
the Python library's outputs.  `app.js` is thin UI glue over it.

Notes:

* counts are exact for the app's range (`w, h <= 12`); the published checkpoints
  `F(13,10)` and `F(10,13)` also come out exact.
* the canonical index is computed only when `h**w <= 100000`.
