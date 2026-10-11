#!/usr/bin/env python3
"""
Assemble the self-contained index-2d.html for the Lily Dissection Lab.

Inlines the vector SVG art (assets/svg/*.svg) into src/template.html and writes
index-2d.html at the project root. The shipped index-2d.html is fully self-contained
(single file, offline, opens by double-click) — this generator only exists so the
SVG art stays editable source and the HTML/CSS/JS has a clean editing surface.
(The 3-D variant index-3d.html is built separately by assemble-3d.py.)

Re-run after editing src/template.html or any assets/svg/*.svg:
    python build/assemble.py

Design notes:
  * Parts are the 13 bloomFace layers from assets/manifest.json, in renderOrder.
  * Each layer's inner SVG (a pre-rotated, pre-positioned <g> on a shared
    1600x1600 canvas) is wrapped in <g class="part" data-id data-role data-ex>.
  * data-role is the *pollination* role (Lesson 13), NOT the manifest's retired
    3-bin `group` taxonomy (attraction/protection/reproduction).
  * pollen.svg and hummingbird.svg are inlined as overlay groups (not parts).
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SVG = ROOT / "assets" / "svg"
MANIFEST = json.loads((ROOT / "assets" / "manifest.json").read_text(encoding="utf-8"))
TEMPLATE = (ROOT / "src" / "template.html").read_text(encoding="utf-8")
OUT = ROOT / "index-2d.html"

# Pollination role per part id (Lesson 13 function frame — replaces manifest `group`).
ROLE = {
    "sepal-1": "protect", "sepal-2": "protect", "sepal-3": "protect",
    "petal-1": "advertise", "petal-2": "advertise", "petal-3": "advertise",
    "stamen-1": "make-pollen", "stamen-2": "make-pollen", "stamen-3": "make-pollen",
    "stamen-4": "make-pollen", "stamen-5": "make-pollen", "stamen-6": "make-pollen",
    "pistil": "make-seeds",
}

_SVG_OPEN = re.compile(r"^\s*<svg\b[^>]*>", re.IGNORECASE | re.DOTALL)
_SVG_CLOSE = re.compile(r"</svg>\s*$", re.IGNORECASE)


def inner(name):
    """Return the inner markup of a shared-canvas SVG (strip the outer <svg> wrapper)."""
    raw = (SVG / f"{name}.svg").read_text(encoding="utf-8")
    raw = _SVG_OPEN.sub("", raw, count=1)
    raw = _SVG_CLOSE.sub("", raw, count=1)
    return raw.strip()


def build_parts():
    scene = MANIFEST["scenes"]["bloomFace"]
    by_id = {p["id"]: p for p in scene["parts"]}
    blocks = []
    for pid in scene["renderOrder"]:
        p = by_id[pid]
        ex = p["explodeVector"]
        role = ROLE[pid]
        blocks.append(
            f'<g class="part" data-id="{pid}" data-role="{role}" '
            f'data-ex="{ex[0]},{ex[1]}">{inner(pid)}</g>'
        )
    return "\n".join(blocks)


def main():
    html = (TEMPLATE
            .replace("{{PARTS}}", build_parts())
            .replace("{{POLLEN}}", inner("pollen"))
            .replace("{{BEAK}}", inner("hummingbird")))
    OUT.write_text(html, encoding="utf-8")
    kb = len(html.encode("utf-8")) / 1024
    print(f"Wrote {OUT.relative_to(ROOT)} ({kb:.0f} KB)")


if __name__ == "__main__":
    main()
