"""Local module discovery and shared teacher-builder context. No third-party packages."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent.parent
LAYERS = {"learning-engine", "asset-libraries", "tool-skills", "curriculum", "standards"}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def resolve(repo, scope, path):
    roots = {"repo": repo, "projects": repo.parent, "user": repo.parent.parent,
             "appdata": repo.parent.parent / "AppData/Local"}
    if scope not in roots:
        raise ValueError("Unknown resource scope: " + str(scope))
    if path is None:
        return None
    if not isinstance(path, str) or not path.strip():
        raise ValueError("Resource path must be nonempty text or null.")
    base = roots[scope].resolve()
    result = (base / path).resolve()
    if not result.is_relative_to(base):
        raise ValueError("Resource path escapes its scope: " + path)
    return result


def keyed(records, label):
    result = {}
    for record in records:
        identifier = record.get("id", "")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identifier) or identifier in result:
            raise ValueError("Invalid or duplicate " + label + " ID: " + identifier)
        result[identifier] = record
    return result


def load(repo=ROOT):
    registry = read(repo / "shared/resources.json")
    catalog = read(repo / "modules/catalog.json")
    if registry.get("version") != 1 or catalog.get("version") != 1:
        raise ValueError("Unsupported catalog or resource registry version.")
    if not isinstance(registry.get("defaults"), dict):
        raise ValueError("Shared preferences must be an object.")
    resources = keyed(registry["resources"], "resource")
    modules = keyed(catalog["modules"], "module")
    for identifier in ("learnability-patterns", "learning-authoring", "frontend-design"):
        if identifier not in resources or resources[identifier].get("required") is not True:
            raise ValueError("Missing required core resource: " + identifier)
    for resource in resources.values():
        if resource.get("layer") not in LAYERS or not isinstance(resource.get("required"), bool):
            raise ValueError("Invalid layer/required flag: " + resource["id"])
        resolve(repo, resource["scope"], resource["path"])
    for module in modules.values():
        for field in ("title", "level", "curriculum", "note"):
            if not isinstance(module.get(field), str) or not module[field].strip():
                raise ValueError("Module requires " + field + ": " + module["id"])
        if module.get("status") not in {"packaged", "workspace", "historical", "planned"}:
            raise ValueError("Invalid module status: " + module["id"])
        for field in ("subjects", "objectives"):
            if (not isinstance(module.get(field), list) or not module[field]
                    or not all(isinstance(x, str) and x.strip() for x in module[field])):
                raise ValueError("Module requires " + field + ": " + module["id"])
        if not isinstance(module.get("preferences"), dict):
            raise ValueError("Module preferences must be an object: " + module["id"])
        if not isinstance(module.get("resources"), list) or not isinstance(module.get("standards"), list):
            raise ValueError("Module resources and standards must be lists: " + module["id"])
        for identifier in module["resources"]:
            if identifier not in resources:
                raise ValueError("Unknown resource: " + identifier)
        for standard in module["standards"]:
            if standard.get("status") not in {"candidate", "unverified"}:
                raise ValueError("Standards require candidate/unverified status: " + module["id"])
            for field in ("framework", "code", "note"):
                if not isinstance(standard.get(field), str) or not standard[field].strip():
                    raise ValueError("Standard requires " + field + ": " + module["id"])
            if standard.get("evidence") and not resolve(repo, "repo", standard["evidence"]).is_file():
                raise ValueError("Missing standard evidence: " + standard["evidence"])
        for field in ("brief", "reference"):
            path = resolve(repo, "repo", module[field])
            if path is not None and not path.is_file():
                raise ValueError("Missing module " + field + ": " + str(path))
        resolve(repo, **module["location"])
    return registry, resources, modules


def resources_at(repo, resources):
    result = []
    for resource in resources.values():
        path = resolve(repo, resource["scope"], resource["path"])
        available = path.exists() if path else False
        if path and (resource["layer"] == "tool-skills" or resource["id"] == "learning-authoring"):
            available = path.is_file() and path.suffix.lower() == ".md"
        elif path and resource["id"] == "learnability-patterns":
            available = path.is_dir()
        result.append({**resource, "resolved_path": str(path) if path else None,
                       "available": available})
    return result


def check(repo=ROOT):
    registry, resources, modules = load(repo)
    resolved = resources_at(repo, resources)
    missing = [r["id"] for r in resolved if r["required"] and not r["available"]]
    if missing:
        raise ValueError("Required knowledge sources unavailable: " + ", ".join(missing))
    return {"modules": len(modules), "resources": len(resources),
            "optional_unavailable": [r["id"] for r in resolved if not r["required"] and not r["available"]],
            "missing_locations": [m["id"] for m in modules.values()
                                  if not resolve(repo, **m["location"]).exists()]}


def select(repo=ROOT, subject=None, standard=None, level=None):
    modules = load(repo)[2].values()
    return [m for m in modules
            if (not subject or subject.casefold() in [s.casefold() for s in m["subjects"]])
            and (not level or level.casefold() == m["level"].casefold())
            and (not standard or any(standard.casefold() == s["code"].casefold() for s in m["standards"]))]


def context(identifier, repo=ROOT):
    registry, resources, modules = load(repo)
    if identifier not in modules:
        raise ValueError("Unknown module: " + identifier + ". Use catalog.py list.")
    module = modules[identifier]
    brief = resolve(repo, "repo", module["brief"])
    sources = [repo / "shared/resources.json", repo / "modules/catalog.json"]
    if brief:
        sources.append(brief)
    return {"version": 1, "module": module, "shared_resources": resources_at(repo, resources),
            "preferences": {**registry["defaults"], **module["preferences"]},
            "preference_precedence": "shared defaults < module preferences < explicit current teacher request",
            "brief_text": brief.read_text(encoding="utf-8") if brief else None,
            "location": str(resolve(repo, **module["location"])),
            "reference": str(resolve(repo, "repo", module["reference"])) if module["reference"] else None,
            "source_sha256": {str(p.relative_to(repo)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}}


def knowledge(repo=ROOT):
    resources = resources_at(repo, load(repo)[1])
    missing = [r["id"] for r in resources if r["required"] and not r["available"]]
    if missing:
        raise ValueError("Required knowledge sources unavailable: " + ", ".join(missing))
    paths = {r["id"]: r["resolved_path"] for r in resources}
    return {"patterns": paths["learnability-patterns"], "learning_skill": paths["learning-authoring"],
            "frontend_skill": paths["frontend-design"],
            "tool_skills": [r["resolved_path"] for r in resources
                            if r["layer"] == "tool-skills" and r["available"]]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    commands = parser.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("list")
    listing.add_argument("--subject")
    listing.add_argument("--standard")
    listing.add_argument("--level")
    commands.add_parser("show").add_argument("module")
    commands.add_parser("check")
    args = parser.parse_args()
    repo = args.repo.resolve()
    if args.command == "list":
        result = select(repo, args.subject, args.standard, args.level)
        for module in result:
            standards = ", ".join(s["code"] + " (" + s["status"] + ")" for s in module["standards"])
            print(f'{module["id"]:27} {module["level"]:10} {module["status"]:10} {standards or "no standard supplied"}')
    else:
        result = context(args.module, repo) if args.command == "show" else check(repo)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as error:
        print("Catalog stopped: " + str(error), file=sys.stderr)
        sys.exit(1)
