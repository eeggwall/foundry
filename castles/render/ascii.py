"""ASCII rendering of castles."""

from __future__ import annotations

from ..castle import Castle


def render_ascii(castle: Castle) -> str:
    """Render ``castle`` as text: ``#`` for blocks, ``.`` for empty cells.

    Rows are printed top-to-bottom; the base block is the bottom row.
    """
    lines: list[str] = []
    for row in range(castle.height, 0, -1):
        lines.append(
            "".join("#" if row <= castle.profile[col] + 1 else "." for col in range(castle.width))
        )
    return "\n".join(lines)
