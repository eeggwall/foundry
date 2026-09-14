"""SVG rendering of castles."""

from __future__ import annotations

from ..castle import Castle

_CELL = 20  # pixels per grid cell


def render_svg(castle: Castle) -> str:
    """Render ``castle`` as an SVG string (one ``<rect>`` per block)."""
    w, h = castle.width, castle.height
    rects = [
        f'<rect x="{block.col0 - 1}" y="{h - block.row}" width="{block.length}" height="1"/>'
        for block in castle.blocks
    ]
    body = "\n".join(rects)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w * _CELL}" height="{h * _CELL}">\n'
        "<style>rect{fill:#4a6fa5;stroke:#2c3e50;stroke-width:0.04;}</style>\n"
        f"{body}\n"
        "</svg>"
    )
