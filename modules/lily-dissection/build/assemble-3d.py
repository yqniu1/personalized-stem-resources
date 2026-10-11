#!/usr/bin/env python3
"""Assemble a self-contained offline 3D HTML file.

Injects the esbuild Three.js IIFE bundle and a base64-encoded GLB into a
template, producing ONE double-clickable HTML file with no network dependency.

Placeholders in the template:
  __THREE_BUNDLE_JS__   -> raw contents of the esbuild IIFE bundle
  __GLB_BASE64__        -> base64 string of the GLB (assigned to a JS const)

Usage:
  python assemble-3d.py <template.html> <bundle.iife.js> <model.glb> <out.html>
"""
import base64
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 5:
        print(__doc__)
        sys.exit(1)
    template_p, bundle_p, glb_p, out_p = map(Path, sys.argv[1:5])

    template = template_p.read_text(encoding="utf-8")
    bundle = bundle_p.read_text(encoding="utf-8")
    glb_b64 = base64.b64encode(glb_p.read_bytes()).decode("ascii")

    # Both substitutions are literal; the model is encoded for offline loading.
    html = template.replace("__THREE_BUNDLE_JS__", bundle)
    html = html.replace("__GLB_BASE64__", glb_b64)
    licenses = bundle_p.parent.parent
    notices = "\n\n".join((licenses / name).read_text(encoding="utf-8")
                            for name in ("THREE-LICENSE.txt", "MESHOPT-LICENSE.txt"))
    html = "<!--\n" + notices.replace("--", "- -") + "\n-->\n" + html

    out_p.write_text(html, encoding="utf-8")
    kb = out_p.stat().st_size / 1024
    print(f"WROTE {out_p}  ({kb:,.0f} KB)  glb_b64={len(glb_b64)/1024:,.0f} KB "
          f"bundle={len(bundle)/1024:,.0f} KB")


if __name__ == "__main__":
    main()
