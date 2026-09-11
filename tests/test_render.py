"""Tests for ASCII and SVG rendering."""

from __future__ import annotations

import xml.etree.ElementTree as ET

from castles.castle import Castle
from castles.render.ascii import render_ascii
from castles.render.svg import render_svg


def test_render_ascii_small() -> None:
    # 3x2 castle with sub-blocks in columns 1 and 3.
    castle = Castle(3, 2, (1, 0, 1))
    assert render_ascii(castle) == "#.#\n###"


def test_render_ascii_rectangle() -> None:
    castle = Castle(4, 3, (2, 2, 2, 2))
    assert render_ascii(castle) == "####\n####\n####"


def test_render_ascii_dimensions() -> None:
    castle = Castle(5, 4, (3, 1, 0, 2, 3))
    lines = render_ascii(castle).split("\n")
    assert len(lines) == castle.height
    assert all(len(line) == castle.width for line in lines)


def test_render_ascii_uses_only_block_chars() -> None:
    castle = Castle(4, 3, (2, 2, 0, 1))
    assert set(render_ascii(castle)) <= {"#", ".", "\n"}


def test_render_svg_is_parseable() -> None:
    castle = Castle(3, 2, (1, 0, 1))
    svg = render_svg(castle)
    root = ET.fromstring(svg)
    assert root.tag.endswith("svg")
    rects = root.findall(".//{http://www.w3.org/2000/svg}rect")
    assert len(rects) == castle.block_count  # one <rect> per block


def test_render_svg_viewbox() -> None:
    castle = Castle(4, 2, (1, 1, 0, 1))
    root = ET.fromstring(render_svg(castle))
    assert root.attrib["viewBox"] == "0 0 4 2"
