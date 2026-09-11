# Castle Foundry — web app

A single-page app with three views, running the Python `castles` library in the
browser via [Pyodide](https://pyodide.org).

* **Designer** — a click-to-edit tower grid, generators (random, tallest,
  widest, symmetric), and feature toggles (symmetric / convex / concave).
* **Inspector** — a URD string in, a rendered castle and fact sheet out (block
  count, features, `#castles(w, h)`, canonical index).
* **Zoo** — the named specimens from `castles.zoo`, each linking into the
  Inspector.

## Running it

The app needs the `castles` wheel built and served alongside `webapp/`.

```bash
# from the repo root
python -m pip wheel . --no-deps -w dist/     # build dist/castles-0.0.0-py3-none-any.whl
python -m http.server 8000                    # serve the repo root
```

Then open <http://localhost:8000/webapp/>.

`app.js` loads Pyodide from a CDN, installs the wheel from
`../dist/castles-0.0.0-py3-none-any.whl` (change `CASTLES_WHEEL` in `app.js` if
you build elsewhere), fetches `bridge.py`, and calls its functions.

## How it works

`bridge.py` is the thin JSON boundary between Python and JS.  Each function
takes JSON-serialisable inputs and returns a JSON string:

| function | purpose |
|---|---|
| `inspect(urd)` | parse a URD string and return its fact sheet |
| `random_castle(w, h, features)` | rejection-sample a castle satisfying the feature dict |
| `preset(w, h, kind)` | the "tallest" or "widest" extreme castle |
| `profile(heights)` | build a castle from a list of column heights |
| `zoo()` | the named specimens with their URD strings and SVGs |

Everything non-trivial (grammar, counting, features, rendering) lives in the
`castles` package and is unit-tested independently of the browser; the frontend
only orchestrates those calls.

## Notes

* The canonical index is only computed when `h**w <= 100000` (and the castle is
  a valid even-block castle); otherwise the fact sheet shows `—`.
* The Designer's grid edits a *tower profile* directly (click a cell to raise a
  column to that height, click its top cell to lower it, click the base row to
  clear it).  This is the library's canonical geometric representation.
