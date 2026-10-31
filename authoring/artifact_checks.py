"""Check concrete design requirements against exact artifact bytes, not learning efficacy."""
from html.parser import HTMLParser
import json
from pathlib import Path

import lesson


def decision_id(decision):
    """Content-derived identity also works for existing designs without IDs."""
    return "decision-" + lesson.digest(json.dumps(decision, sort_keys=True).encode())[:16]


class Elements(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.elements = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        identifier = attrs.get("id")
        if identifier:
            self.elements.setdefault(identifier, []).append([])
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}:
            self.stack.append((tag, identifier))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if any(tag in {"script", "style"} for tag, _ in self.stack):
            return
        for _, identifier in self.stack:
            if identifier:
                self.elements[identifier][-1].append(data)


def report(root, task, design, data):
    """Recompute automated checks; stale reported reviews never count as observations."""
    binding = {"task": task["id"], "artifact_sha256": lesson.digest(data),
               "design_sha256": lesson.digest(json.dumps(design, sort_keys=True).encode())}
    parser = Elements()
    parser.feed(data.decode("utf-8"))
    reviews = {}
    warnings = []
    review_file = root / "artifact-review.json"
    if review_file.exists():
        review = lesson.read_json(review_file)
        if any(review.get(k) != v for k, v in binding.items()):
            warnings.append("Reported review is stale: task, design or artifact changed. Review again.")
        else:
            for item in review.get("observations", []):
                identifier = item.get("decision_id")
                if identifier in reviews:
                    raise ValueError("Duplicate decision review.")
                reviews[identifier] = item
    rows = []
    for decision in design["decisions"]:
        identifier = decision_id(decision)
        checks = []
        for check in decision.get("artifact_checks", []):
            if check.get("kind") != "element_text" or not all(isinstance(check.get(k), str) and check[k].strip() for k in ("element_id", "contains")):
                raise ValueError("Artifact check requires kind=element_text, element_id and contains.")
            matches = parser.elements.get(check["element_id"], [])
            actual = " ".join(" ".join(matches[0]).split()) if len(matches) == 1 else ""
            expected = " ".join(check["contains"].split())
            checks.append({**check, "method": "automated_static_html", "actual": actual,
                           "outcome": "observed" if len(matches) == 1 and expected in actual else "not_observed",
                           "limit": "Source HTML text only; does not establish visibility, interaction behavior or learning."})
        observation = reviews.pop(identifier, None)
        if observation:
            for key in ("reviewer", "location", "procedure", "expected", "actual", "evidence_path"):
                if not isinstance(observation.get(key), str) or not observation[key].strip():
                    raise ValueError("Reported review requires " + key)
            if observation.get("method") not in ("agent_browser_review", "human_review") or observation.get("outcome") not in ("observed", "not_observed", "not_checked"):
                raise ValueError("Invalid reported review method or outcome.")
            relative = Path(observation["evidence_path"])
            evidence = (root / relative).resolve()
            if relative.is_absolute() or not evidence.is_relative_to(root.resolve()) or evidence.suffix not in {".txt", ".md", ".json"}:
                raise ValueError("Review evidence must be a workspace-relative text, Markdown or JSON file.")
            # Bound allocation as well as accepted content, including a growing file.
            with evidence.open("rb") as stream:
                evidence_bytes = stream.read(1_000_001)
            if not evidence_bytes.strip() or len(evidence_bytes) > 1_000_000:
                raise ValueError("Review evidence must be nonempty and at most 1 MB.")
            if observation.get("evidence_sha256") != lesson.digest(evidence_bytes):
                raise ValueError("Review evidence hash changed or missing; record the actual evidence hash.")
            checks.append({**observation, "evidence_text": evidence_bytes.decode("utf-8"),
                           "limit": "Attributed reviewer observation; helper checks identity, not truth of the reported test."})
        outcomes = [c["outcome"] for c in checks]
        # Static text presence never promotes a pedagogical decision to verified behavior.
        status = "gap" if "not_observed" in outcomes else "review_reported" if observation and observation["outcome"] == "observed" else "needs_review"
        rows.append({"decision_id": identifier, "choice": decision["choice"], "expected_behavior": decision["check"],
                     "status": status, "checks": checks})
    if reviews:
        raise ValueError("Reported review references an unknown decision.")
    return {**binding, "scope": "Implementation evidence only; no learner effectiveness or source-validity claim.",
            "warnings": warnings, "decisions": rows}


def verify(root, task_id):
    with lesson.locked(root):
        import grounding
        task = lesson.task_record(root, task_id)
        design, _ = grounding.publication(root, task)
        result = report(root, task, design, (root / "src/lesson.html").read_bytes())
        lesson.save_json(root / "artifact-checks.json", result)
        return result
