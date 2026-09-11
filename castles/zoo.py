"""The Enfilade Castle Zoo: named specimens and their fact sheets."""

from __future__ import annotations

from dataclasses import dataclass

from .castle import Castle
from .enumerate import canonical_index, count
from .features import degree, has_valley, is_concave, is_convex, is_symmetric, nickname, num_valleys
from .render.ascii import render_ascii
from .render.svg import render_svg
from .repr.urd import to_urd


@dataclass(frozen=True, slots=True)
class Specimen:
    """A named castle in the zoo."""

    name: str
    description: str
    castle: Castle


def specimens() -> tuple[Specimen, ...]:
    """The curated gallery of named specimens (all even-block castles)."""
    return (
        Specimen(
            "The Fortress",
            "A solid rectangle of stacked blocks.",
            Castle(5, 4, (3, 3, 3, 3, 3)),
        ),
        Specimen(
            "The Pyramid",
            "A symmetric peak rising to a single column.",
            Castle(5, 4, (1, 2, 3, 2, 1)),
        ),
        Specimen(
            "Staircase",
            "A monotone climb from left to right.",
            Castle(4, 4, (0, 1, 2, 3)),
        ),
        Specimen(
            "The Terrace",
            "A stepped shelf descending to the right.",
            Castle(4, 4, (3, 2, 1, 0)),
        ),
        Specimen(
            "The Spire",
            "A single tall column.",
            Castle(1, 4, (3,)),
        ),
        Specimen(
            "The Battlement",
            "A crenellated wall, neither convex nor concave.",
            Castle(5, 3, (1, 2, 1, 2, 1)),
        ),
        Specimen(
            "The Canyon",
            "A deep symmetric valley.",
            Castle(5, 4, (3, 2, 1, 2, 3)),
        ),
    )


def fact_sheet(castle: Castle) -> dict[str, object]:
    """The Inspector fact sheet for a castle, as a JSON-serialisable dict."""
    return {
        "urd": to_urd(castle),
        "width": castle.width,
        "height": castle.height,
        "profile": list(castle.profile),
        "blocks": castle.block_count,
        "valid": castle.has_even_blocks,
        "degree": degree(castle),
        "valleys": num_valleys(castle),
        "features": {
            "symmetric": is_symmetric(castle),
            "convex": is_convex(castle),
            "concave": is_concave(castle),
            "has_valley": has_valley(castle),
        },
        "nickname": nickname(castle),
        "count": count(castle.width, castle.height),
        "canonical_index": canonical_index(castle),
        "ascii": render_ascii(castle),
        "svg": render_svg(castle),
    }
