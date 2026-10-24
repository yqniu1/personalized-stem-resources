#!/usr/bin/env python3
"""Copy the review prototype into a new directory, without private inputs or Git history."""
import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATTERNS = [
    "README.md", ".gitignore", "index.html", "THIRD_PARTY_NOTICES.md",
    "build/export-public.py", "docs/*.md", "docs/images/*.png", "docs/images/*.svg",
    "authoring/*.py", "authoring/*.ps1", "authoring/README.md",
    "shared/*.json", "shared/README.md", "references/README.md", "modules/catalog.json",
    "modules/README.md", "modules/*/README.md", "modules/*/index.html",
    "modules/*/index-2d.html", "modules/*/docs/*.md", "modules/*/src/*.html",
    "modules/*/index-3d.html", "modules/*/assets/lily.glb",
    "modules/*/assets/README.md", "modules/*/assets/*.svg",
    "modules/*/assets/manifest.json", "modules/*/assets/svg/*.svg",
    "modules/*/build/*.py", "modules/*/build/blender/*.py",
    "modules/*/build/web/package*.json",
    "modules/*/build/web/*LICENSE.txt", "modules/*/build/web/src/three-bundle.mjs",
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="A new directory outside this checkout")
    destination = parser.parse_args().destination.resolve()
    if destination.exists() or destination == ROOT or ROOT in destination.parents:
        parser.error("Destination must be a new directory outside this checkout.")
    files = sorted({p for pattern in PATTERNS for p in ROOT.glob(pattern) if p.is_file()})
    destination.mkdir(parents=True)
    for source in files:
        target = destination / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    print(f"Exported {len(files)} reviewed files to {destination}")
    print("Includes the review model under its separate license. No private inputs or Git history included.")


if __name__ == "__main__":
    main()
