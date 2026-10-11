#!/usr/bin/env python3
"""Rebuild the standalone 2-D and 3-D modules and their offline launcher."""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--2d-only", dest="only_2d", action="store_true",
                        help="Rebuild only index-2d.html, without Node dependencies")
    args = parser.parse_args()
    subprocess.run([sys.executable, str(BUILD / "assemble.py")], check=True, cwd=ROOT)
    if args.only_2d:
        return 0
    bundle = BUILD / "web" / "dist" / "three-bundle.iife.js"
    model = ROOT / "assets" / "lily.glb"
    if not bundle.is_file() or not model.is_file():
        print("Missing model or Three.js bundle. Run npm ci and npm run bundle in build/web.",
              file=sys.stderr)
        return 1
    commands = [
        [BUILD / "assemble-3d.py", ROOT / "src" / "template-3d.html",
         bundle, model, ROOT / "index-3d.html"],
        [BUILD / "assemble-merged.py"],
    ]
    for command in commands:
        subprocess.run([sys.executable, *map(str, command)], check=True, cwd=ROOT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
