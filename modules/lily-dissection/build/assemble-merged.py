#!/usr/bin/env python3
"""Embed the standalone 2-D and 3-D builds in the offline module index.html.

Run through build.py after building the Three.js bundle.
Each application runs in an isolated iframe, with a WebGL check and view switch.
The output embeds a purchased model; its separate license is documented in the repo.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHELL = (ROOT / "src" / "template-merged.html").read_text(encoding="utf-8")
APP2D = (ROOT / "index-2d.html").read_text(encoding="utf-8")
APP3D = (ROOT / "index-3d.html").read_text(encoding="utf-8")
OUT = ROOT / "index.html"


def embed(html):
    """Return a JS string literal (quotes included) for embedding inside <script>.

    json.dumps yields a valid JS string; the extra `</` -> `<\\/` step keeps the
    HTML parser from ending the outer <script> early on any `</script>` inside the
    embedded app. At JS-parse time `\\/` collapses back to `/`, so the iframe gets
    byte-identical HTML.
    """
    return json.dumps(html, ensure_ascii=False).replace("</", "<\\/")


def main():
    out = (SHELL
           .replace("{{APP2D}}", embed(APP2D))
           .replace("{{APP3D}}", embed(APP3D)))
    OUT.write_text(out, encoding="utf-8")
    kb = len(out.encode("utf-8")) / 1024
    print(f"Wrote {OUT.relative_to(ROOT)} ({kb:.0f} KB)")


if __name__ == "__main__":
    main()
