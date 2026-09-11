"""Pyodide bridge: a JSON API from the castles library to the web frontend.

Each function takes JSON-serialisable inputs and returns a JSON string -- a
fact-sheet dict, a list, or ``{"error": ...}``.  The frontend loads this file
(after installing the ``castles`` wheel) and calls the functions through
``pyodide.globals``.
"""

from __future__ import annotations

import json

import castles
from castles.features import is_concave, is_convex, is_symmetric
from castles.zoo import fact_sheet, specimens

_MAX_TRIES = 5000


def _dump(obj) -> str:
    return json.dumps(obj)


def inspect(urd: str) -> str:
    """Parse a URD string and return its fact sheet."""
    try:
        return _dump(fact_sheet(castles.parse(urd)))
    except Exception as exc:  # noqa: BLE001
        return _dump({"error": str(exc)})


def random_castle(w, h, features_json=None) -> str:
    """A random castle of width ``w`` and height ``h``, filtered by features.

    ``features_json`` is a JSON object like ``{"symmetric": true}``; the sampler
    rejects until every requested predicate holds (bounded).
    """
    try:
        w, h = int(w), int(h)
        features = json.loads(features_json) if features_json else {}
        for _ in range(_MAX_TRIES):
            castle = castles.random_castle(w, h)
            if _matches(castle, features):
                return _dump(fact_sheet(castle))
        return _dump({"error": "no castle matching the requested features"})
    except Exception as exc:  # noqa: BLE001
        return _dump({"error": str(exc)})


def preset(w, h, kind: str) -> str:
    """A deterministic extreme castle: ``"tallest"`` or ``"widest"``."""
    try:
        w, h = int(w), int(h)
        prof = (h - 1,) + (0,) * (w - 1) if kind == "tallest" else (h - 1,) * w
        return _dump(fact_sheet(castles.Castle(w, h, prof)))
    except Exception as exc:  # noqa: BLE001
        return _dump({"error": str(exc)})


def profile(heights_json) -> str:
    """Build a castle from a JSON list of tower heights (one per column)."""
    try:
        prof = tuple(int(x) for x in json.loads(heights_json))
        if not prof:
            return _dump({"error": "empty profile"})
        height = 1 + max(prof)
        return _dump(fact_sheet(castles.Castle(len(prof), height, prof)))
    except Exception as exc:  # noqa: BLE001
        return _dump({"error": str(exc)})


def zoo() -> str:
    """The named specimens, each with its URD string and SVG thumbnail."""
    return _dump(
        [
            {
                "name": s.name,
                "description": s.description,
                "urd": castles.to_urd(s.castle),
                "svg": fact_sheet(s.castle)["svg"],
            }
            for s in specimens()
        ]
    )


def _matches(castle, features) -> bool:
    checks = (
        (features.get("symmetric"), is_symmetric),
        (features.get("convex"), is_convex),
        (features.get("concave"), is_concave),
    )
    return all(not requested or predicate(castle) for requested, predicate in checks)
