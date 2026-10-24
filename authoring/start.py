"""WSL launcher using niu-prototyper's existing registry and CLI."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import lesson
import catalog


def prepare_workspace(root, repo, module_id=None):
    """Keep reopening non-mutating; bind only new workspaces to catalog context."""
    if (root / "workspace.json").exists():
        return lesson.initialize(root, module_context={"module": {"id": module_id}} if module_id else None)
    packet = catalog.context(module_id, repo) if module_id else None
    reference = (Path(packet["reference"]) if packet and packet["reference"] else None)
    if packet is None:
        reference = repo / "modules/lily-dissection/index-2d.html"
    return lesson.initialize(root, reference, catalog.knowledge(repo), module_context=packet)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--engine", type=Path, required=True)
    parser.add_argument("--no-open", action="store_true")
    parser.add_argument("--module", help="Module ID from catalog.py list")
    args = parser.parse_args()
    root = args.workspace.resolve()
    node = shutil.which("node") or str(Path.home() / ".local/bin/node")
    cli = args.engine / "bin/niu-prototyper"
    for command in (node, "tmux", "codex"):
        if not shutil.which(command):
            raise ValueError("Required tool unavailable in WSL: " + command)
    prepare_workspace(root, args.repo.resolve(), args.module)
    project_id = "stem-authoring-" + hashlib.sha256(str(root).encode()).hexdigest()[:10]
    registry_path = Path(os.environ.get("NIU_PROTOTYPER_HOME", Path.home() / ".niu-prototyper")) / "projects.json"
    registry = lesson.read_json(registry_path) if registry_path.exists() else {"projects": []}
    existing = next((p for p in registry["projects"] if p["id"] == project_id), None)
    if existing and Path(existing["root"]).resolve() != root:
        raise ValueError("Project registry ID points to a different workspace.")
    if not existing:
        subprocess.run([node, str(cli), "init", "--root", str(root), "--id", project_id,
                        "--name", "Lesson studio", "--static", "preview"], check=True)
        registry = lesson.read_json(registry_path)
        existing = next(p for p in registry["projects"] if p["id"] == project_id)
        existing["context"] = ["AGENTS.md", "workspace.json"]
        existing["agent"] = {"instructions": "AGENTS.md", "launch": {
            "lesson-author": 'codex --no-alt-screen -s workspace-write -a on-request '
                             '-c sandbox_workspace_write.network_access=true '
                             '"Read AGENTS.md and workspace.json. Briefly say you are ready for a lesson request. '
                             'Do not create a lesson until the user asks. Follow the local begin/publish/reload workflow."'
        }}
        lesson.save_json(registry_path, registry)
    command = [node, str(cli), "start", "--project", project_id, "--terminal", "--json"]
    if args.no_open:
        command.append("--no-open")
    subprocess.run(command, check=True)
    print(json.dumps({"workspace": str(root), "project": project_id,
                      "next": "Terminal > Start an agent > lesson-author. Reopening reuses the existing terminal."}))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print("Authoring launch stopped: " + str(error), file=sys.stderr)
        sys.exit(1)
