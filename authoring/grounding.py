"""Source receipts and task-bound design records; not a research-validity scorer."""
from html import escape
import json
from pathlib import Path
import shutil

import lesson


def authorized(config, path, kind):
    path = path.resolve()
    if kind == "pattern":
        return path.is_relative_to(Path(config["patterns"]).resolve())
    if kind == "skill":
        return path in {Path(p).resolve() for p in
                        [config["frontend_skill"], *config.get("tool_skills", [])]}
    return False


def capture(root, path, kind):
    path = path.resolve()
    config = lesson.read_json(root / "knowledge.json")
    if not authorized(config, path, kind):
        raise ValueError("Source must be a configured canonical pattern or tool skill.")
    if path.suffix.lower() != ".md":
        raise ValueError("Expected a Markdown source.")
    data = path.read_bytes()
    source_id = kind + "-" + lesson.digest(str(path).encode() + data)[:16]
    directory = root / "evidence" / source_id
    directory.mkdir(parents=True, exist_ok=True)
    receipt = {"id": source_id, "kind": kind, "path": str(path), "sha256": lesson.digest(data)}
    lesson.atomic(directory / "source.md", data)
    lesson.save_json(directory / "receipt.json", receipt)
    return {**receipt, "text": data.decode("utf-8")}


def required_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Design requires " + label)


def validate(root, task):
    design = lesson.read_json(root / "design.json")
    if design.get("task") != task["id"] or design.get("base_revision") != task["base_revision"]:
        raise ValueError("Design task/base does not match the active request.")
    for key in ("objective", "assessment"):
        required_text(design.get(key), key)
    for key in ("assumptions", "limitations"):
        if not isinstance(design.get(key), list) or not design[key]:
            raise ValueError("Design requires an explicit " + key + " list.")
        for item in design[key]:
            required_text(item, key)
    standards = design.get("standards", {})
    if not isinstance(standards, dict) or standards.get("status") not in ("unverified", "candidate"):
        raise ValueError("This rehearsal records standards as unverified or candidate, not verified coverage.")
    required_text(standards.get("explanation"), "standards explanation")
    sources = design.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("Design requires captured local sources.")
    receipts = []
    identifiers = set()
    for source_id in sources:
        if not isinstance(source_id, str) or not lesson.re.fullmatch(r"(pattern|skill)-[a-f0-9]{16}", source_id):
            raise ValueError("Invalid source receipt ID.")
        directory = root / "evidence" / source_id
        receipt = lesson.read_json(directory / "receipt.json")
        data = (directory / "source.md").read_bytes()
        canonical = Path(receipt["path"])
        if (receipt["id"] != source_id or receipt["sha256"] != lesson.digest(data)
                or canonical.read_bytes() != data):
            raise ValueError("Source receipt changed or is stale; capture and review the source again.")
        # Recheck canonical authority, including manually modified receipt metadata.
        config = lesson.read_json(root / "knowledge.json")
        if (not authorized(config, canonical, receipt["kind"])
                or source_id != receipt["kind"] + "-" + lesson.digest(str(canonical.resolve()).encode() + data)[:16]):
            raise ValueError("Source receipt is outside the configured authority.")
        identifiers.add(source_id)
        receipts.append(receipt)
    frontend = Path(lesson.read_json(root / "knowledge.json")["frontend_skill"]).resolve()
    if ({r["kind"] for r in receipts} != {"pattern", "skill"}
            or not any(r["kind"] == "skill" and Path(r["path"]).resolve() == frontend for r in receipts)):
        raise ValueError("Design needs a pattern and frontend-design source.")
    research = design.get("research")
    if not isinstance(research, list) or not research:
        raise ValueError("Expanded research is missing. Preserve draft and report the retrieval gap.")
    for record in research:
        if not isinstance(record, dict):
            raise ValueError("Research must contain records.")
        for key in ("id", "query", "source", "source_id", "parent_id", "interpretation", "limitation"):
            required_text(record.get(key), "research " + key)
        if record["id"] in identifiers:
            raise ValueError("Duplicate source identifier.")
        identifiers.add(record["id"])
    decisions = design.get("decisions")
    if not isinstance(decisions, list) or not decisions:
        raise ValueError("Design requires source-linked decisions.")
    used = set()
    for decision in decisions:
        if not isinstance(decision, dict):
            raise ValueError("Decision must be an object.")
        for key in ("choice", "reason", "check"):
            required_text(decision.get(key), "decision " + key)
        refs = decision.get("sources")
        if not isinstance(refs, list) or not refs or any(not isinstance(r, str) or r not in identifiers for r in refs):
            raise ValueError("Decision references an unknown source.")
        used.update(refs)
    if used != identifiers:
        raise ValueError("Every selected source must inform a decision; remove decorative citations.")
    return design, receipts


def prepare(root, task_id):
    with lesson.locked(root):
        task = lesson.task_record(root, task_id)
        if task["status"] != "active" or lesson.read_json(root / "workspace.json")["active_task"] != task_id:
            raise ValueError("Task is not active.")
        design, _ = validate(root, task)
        lesson.save_json(root / "tasks" / (task_id + "-design.json"), design)
        return {"task": task_id, "design_record": "prepared",
                "scope": "Documentation checked; research interpretations need source review."}


def publication(root, task):
    design, receipts = validate(root, task)
    prepared = lesson.read_json(root / "tasks" / (task["id"] + "-design.json"))
    if design != prepared:
        raise ValueError("Design changed after preparation. Review it and run design again.")
    return design, receipts


def review_html(design, receipts, implementation=None):
    def text(value):
        return escape(str(value))
    parts = ['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
             '<title>Lesson design notes</title><style>body{font:18px/1.6 system-ui;max-width:72ch;margin:40px auto;padding:0 24px}'
             'h1,h2{line-height:1.2}li{margin:12px 0}code{overflow-wrap:anywhere}</style><main>'
             '<h1>Why this lesson</h1><p>Teacher review notes. These source interpretations and design choices '
             'are agent-written. Publication checks documentation, not learning effectiveness or source truth.</p>']
    parts += ["<h2>Learning goal</h2><p>" + text(design["objective"]) + "</p>",
              "<h2>Evidence to look for</h2><p>" + text(design["assessment"]) + "</p>",
              "<h2>Standards: " + text(design["standards"]["status"]) + "</h2><p>" + text(design["standards"]["explanation"]) + "</p>"]
    for title, key in (("Assumptions", "assumptions"), ("Limits", "limitations")):
        parts.append("<h2>" + title + "</h2><ul>" + "".join("<li>" + text(x) + "</li>" for x in design[key]) + "</ul>")
    parts.append("<h2>Design decisions</h2>")
    for d in design["decisions"]:
        parts.append("<h3>" + text(d["choice"]) + "</h3><p>" + text(d["reason"]) + "</p><p>Check: "
                     + text(d["check"]) + "</p><p>Sources: " + text(", ".join(d["sources"])) + "</p>")
    if implementation:
        parts.append("<h2>Implementation checks</h2><p>Checks refer to this exact lesson version. Static text matches do not establish working interactions. Reviewer observations are attributed reports, not independent certification.</p>")
        for warning in implementation["warnings"]:
            parts.append("<p>" + text(warning) + "</p>")
        for row in implementation["decisions"]:
            parts.append("<h3>" + text(row["choice"]) + "</h3><p>Status: " + text(row["status"]) + "</p><p>Expected: " + text(row["expected_behavior"]) + "</p>")
            if not row["checks"]:
                parts.append("<p>No implementation observation recorded.</p>")
            for check in row["checks"]:
                location = check.get("location", "#" + check.get("element_id", ""))
                parts.append("<p>" + text(check["method"]) + " — " + text(check["outcome"]) + " at " + text(location) + "</p><p>Observed: " + text(check["actual"]) + "</p><p>" + text(check["limit"]) + "</p>")
                if "reviewer" in check:
                    parts.append("<p>Reviewer: " + text(check["reviewer"]) + "</p><p>Procedure: " + text(check["procedure"]) + "</p><p>Expected: " + text(check["expected"]) + "</p><details><summary>Recorded test evidence</summary><pre>" + text(check["evidence_text"]) + "</pre></details>")
    parts.append("<h2>Local design sources</h2><ul>")
    for receipt in receipts:
        path = Path(receipt["path"])
        label = path.stem if receipt["kind"] == "pattern" else path.parent.name
        parts.append("<li>" + text(label) + " (" + text(receipt["kind"]) + ") — <code>"
                     + text(receipt["id"]) + "</code></li>")
    parts.append("</ul><h2>Research interpretations</h2>")
    for r in design["research"]:
        parts.append("<h3>" + text(r["id"]) + "</h3><p>" + text(r["source"]) + "</p><p>"
                     + text(r["interpretation"]) + "</p><p>Limit: " + text(r["limitation"])
                     + "</p><p>Library source: <code>" + text(r["source_id"])
                     + "</code></p><p>Expanded passage: <code>" + text(r["parent_id"]) + "</code></p>")
    parts.append("</main></html>")
    return "\n".join(parts).encode()


def snapshot(root, directory, design, receipts, implementation=None):
    lesson.save_json(directory / "design.json", design)
    lesson.atomic(directory / "design.html", review_html(design, receipts, implementation))
    hashes = {}
    if implementation:
        lesson.save_json(directory / "artifact-checks.json", implementation)
        hashes["artifact-checks.json"] = lesson.digest((directory / "artifact-checks.json").read_bytes())
    context = root / "materials/module-context.json"
    if context.exists():
        lesson.atomic(directory / "module-context.json", context.read_bytes())
        hashes["module-context.json"] = lesson.digest(context.read_bytes())
    for receipt in receipts:
        target = directory / "evidence" / receipt["id"]
        shutil.copytree(root / "evidence" / receipt["id"], target)
        for name in ("receipt.json", "source.md"):
            relative = str((target / name).relative_to(directory)).replace("\\", "/")
            hashes[relative] = lesson.digest((target / name).read_bytes())
    for name in ("design.json", "design.html"):
        hashes[name] = lesson.digest((directory / name).read_bytes())
    return hashes


def verify_snapshot(directory, hashes):
    for relative, expected in hashes.items():
        path = directory / relative
        if not path.resolve().is_relative_to(directory.resolve()) or lesson.digest(path.read_bytes()) != expected:
            raise ValueError("Recovery design/source snapshot conflict.")
