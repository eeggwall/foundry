"""Generate the SVG figures used by the Phase 3 writeups.

Renders a curated set of castles to ``notes/figures/*.svg`` via the library's
:func:`~castles.render.svg.render_svg`.  Run from the repo root::

    python notes/make_figures.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make the `castles` package importable when this script is run directly.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from castles.castle import Castle
from castles.render.svg import render_svg

# name -> castle (width, height, tower profile)
FIGURES: dict[str, Castle] = {
    "urdrurd": Castle(3, 2, (1, 0, 1)),  # wiki example: two sub-blocks, one gap
    "uurd": Castle(1, 3, (2,)),  # stacked width-1 blocks
    "rectangle": Castle(5, 4, (3, 3, 3, 3, 3)),  # 5x4 rectangle
    "convex": Castle(6, 4, (1, 2, 3, 3, 2, 1)),  # convex (front/middle/back)
    "concave": Castle(5, 3, (2, 1, 0, 1, 2)),  # single valley
    "double": Castle(5, 3, (2, 0, 0, 0, 2)),  # two separate towers
    "complex": Castle(5, 3, (1, 2, 1, 2, 1)),  # neither convex nor concave
    "asymmetric": Castle(4, 3, (2, 1, 0, 1)),  # non-symmetric
}


def main() -> None:
    out = Path(__file__).parent / "figures"
    out.mkdir(exist_ok=True)
    for name, castle in FIGURES.items():
        (out / f"{name}.svg").write_text(render_svg(castle))
    print(f"wrote {len(FIGURES)} figures to {out}")


if __name__ == "__main__":
    main()
