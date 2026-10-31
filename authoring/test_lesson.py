import tempfile
import unittest
from unittest.mock import patch
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import threading
from pathlib import Path
import lesson
import grounding
import artifact_checks

VALID = b"<!doctype html><html><head><title>Test</title></head><body><main><h1>Pollen</h1><button>Try</button><script>let n=1;</script></main></body></html>"


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "workspace"
        canonical = Path(self.temporary.name) / "canonical"
        canonical.mkdir()
        self.pattern = canonical / "coherence.md"
        self.pattern.write_text("Fixture: keep relevant content.")
        self.skill = canonical / "SKILL.md"
        self.skill.write_text("Fixture: subject-specific interface choices.")
        lesson.initialize(self.root, knowledge={"patterns": str(canonical), "frontend_skill": str(self.skill)})
        self.original = (self.root / "preview/index.html").read_bytes()

    def draft(self, prompt="Make a lesson"):
        task = lesson.begin(self.root, prompt)
        (self.root / "src/lesson.html").write_bytes(VALID)
        pattern = grounding.capture(self.root, self.pattern, "pattern")["id"]
        skill = grounding.capture(self.root, self.skill, "skill")["id"]
        design = {
            "task": task["id"], "base_revision": task["base_revision"],
            "objective": "Explain pollen movement", "assessment": "Explain the sequence",
            "standards": {"status": "unverified", "explanation": "No jurisdiction supplied"},
            "assumptions": ["Fixture only"], "limitations": ["No pedagogical validity tested"],
            "sources": [pattern, skill],
            "research": [{"id": "research-fixture", "query": "fixture", "source": "Test fixture",
                          "source_id": "fixture-source", "parent_id": "fixture-parent", "interpretation": "Fixture text",
                          "limitation": "Not real research"}],
            "decisions": [{"choice": "Sequence with feedback", "reason": "Expose mechanism",
                           "sources": [pattern, skill, "research-fixture"], "check": "Inspect sequence"}],
        }
        lesson.save_json(self.root / "design.json", design)
        grounding.prepare(self.root, task["id"])
        return task["id"]

    def test_reopen_preserves_work(self):
        self.draft()
        lesson.initialize(self.root)
        self.assertEqual((self.root / "src/lesson.html").read_bytes(), VALID)
        self.assertIsNotNone(lesson.read_json(self.root / "workspace.json")["active_task"])

    def test_tiger_transfer_principle_survives_prose_but_missing_prompt_is_detected(self):
        # Minimal fixture adapted from the existing Tiger lesson's #transfer section.
        # This is a mutation test, not a claim that the live Tiger lesson lacks transfer.
        task_id = self.draft()
        design = lesson.read_json(self.root / "design.json")
        design["decisions"][0].update(
            choice="Reuse eyes across prey detection and shelter discovery",
            check="Final prompt asks for the same structure in a changed goal",
            artifact_checks=[{"kind": "element_text", "element_id": "transfer",
                              "contains": "What changes about their job?"}])
        lesson.save_json(self.root / "design.json", design)
        grounding.prepare(self.root, task_id)
        good = b'<html><title>Tiger</title><main><h1>Tiger</h1><section id="transfer" hidden><label>Use eyes as your example. Explain how they work with another structure to help get food, and how they work with another structure to find shelter. What changes about their job?</label></section></main></html>'
        path = self.root / "src/lesson.html"
        path.write_bytes(good)
        result = artifact_checks.verify(self.root, task_id)
        self.assertEqual(result["decisions"][0]["checks"][0]["outcome"], "observed")
        self.assertEqual(result["decisions"][0]["status"], "needs_review")  # hidden/runtime not verified
        path.write_bytes(good.replace(b"What changes about their job?", b"Name a tiger body part."))
        result = artifact_checks.verify(self.root, task_id)
        self.assertEqual(result["decisions"][0]["status"], "gap")
        publication = lesson.publish(self.root, task_id, "Deliberate gap fixture")
        self.assertEqual(publication["artifact_checks"]["decisions"][0]["status"], "gap")
        self.assertIn("gap", (self.root / "preview/design.html").read_text())
        self.assertTrue((self.root / "exports" / (publication["revision"] + ".artifact-checks.json")).exists())

    def review_fixture(self):
        task_id = self.draft()
        report = artifact_checks.verify(self.root, task_id)
        evidence = b"Synthetic fixture: inspected Try button; not an actual browser test."
        (self.root / "notes.txt").write_bytes(evidence)
        review = {key: report[key] for key in ("task", "artifact_sha256", "design_sha256")}
        review["observations"] = [{"decision_id": report["decisions"][0]["decision_id"],
            "method": "human_review", "reviewer": "synthetic test fixture", "location": "button Try",
            "procedure": "Fixture review only", "expected": "Button exists", "actual": "Fixture button found",
            "outcome": "observed", "evidence_path": "notes.txt", "evidence_sha256": lesson.digest(evidence)}]
        lesson.save_json(self.root / "artifact-review.json", review)
        return task_id, review

    def test_review_is_attributed_and_stale_artifact_invalidates_it(self):
        task_id, _ = self.review_fixture()
        report = artifact_checks.verify(self.root, task_id)
        self.assertEqual(report["decisions"][0]["status"], "review_reported")
        self.assertIn("Synthetic fixture", report["decisions"][0]["checks"][0]["evidence_text"])
        (self.root / "src/lesson.html").write_bytes(VALID + b"<!-- edit -->")
        report = artifact_checks.verify(self.root, task_id)
        self.assertEqual(report["decisions"][0]["status"], "needs_review")
        self.assertIn("stale", report["warnings"][0])

    def test_static_match_ignores_script_style_and_duplicate_ids(self):
        task_id = self.draft()
        design = lesson.read_json(self.root / "design.json")
        design["decisions"][0]["artifact_checks"] = [{"kind": "element_text", "element_id": "transfer", "contains": "Explain why"}]
        task = lesson.task_record(self.root, task_id)
        for markup in (b'<section id="transfer"><script>"Explain why"</script><style>/*Explain why*/</style></section>',
                       b'<p id="transfer">Explain why</p><p id="transfer">Explain why</p>'):
            self.assertEqual(artifact_checks.report(self.root, task, design, markup)["decisions"][0]["status"], "gap")

    def test_design_change_invalidates_review_even_with_same_html(self):
        task_id, _ = self.review_fixture()
        design = lesson.read_json(self.root / "design.json")
        design["decisions"][0]["check"] = "New expected interaction"
        lesson.save_json(self.root / "design.json", design)
        grounding.prepare(self.root, task_id)
        report = artifact_checks.verify(self.root, task_id)
        self.assertIn("stale", report["warnings"][0])

    def test_review_rejects_unknown_decision_and_changed_evidence(self):
        task_id, review = self.review_fixture()
        review["observations"][0]["decision_id"] = "unknown"
        lesson.save_json(self.root / "artifact-review.json", review)
        with self.assertRaisesRegex(ValueError, "unknown decision"):
            artifact_checks.verify(self.root, task_id)
        review["observations"][0]["decision_id"] = artifact_checks.decision_id(lesson.read_json(self.root / "design.json")["decisions"][0])
        lesson.save_json(self.root / "artifact-review.json", review)
        (self.root / "notes.txt").write_text("Changed")
        with self.assertRaisesRegex(ValueError, "hash changed"):
            artifact_checks.verify(self.root, task_id)

    def test_review_evidence_cannot_escape_workspace(self):
        task_id, review = self.review_fixture()
        review["observations"][0]["evidence_path"] = "../outside.txt"
        lesson.save_json(self.root / "artifact-review.json", review)
        with self.assertRaisesRegex(ValueError, "workspace-relative"):
            artifact_checks.verify(self.root, task_id)

    def test_unchecked_decisions_and_recovery_preserve_report(self):
        task_id = self.draft()
        with patch.object(lesson, "complete_publication", side_effect=OSError("interrupted")):
            with self.assertRaises(OSError):
                lesson.publish(self.root, task_id, "Test")
        revision = "r-" + task_id
        saved = lesson.read_json(self.root / "revisions" / revision / "artifact-checks.json")
        self.assertEqual(saved["decisions"][0]["status"], "needs_review")
        lesson.recover(self.root)
        self.assertEqual(lesson.read_json(self.root / "exports" / (revision + ".artifact-checks.json")), saved)

    def test_recovery_rejects_tampered_implementation_report(self):
        task_id = self.draft()
        with patch.object(lesson, "complete_publication", side_effect=OSError("interrupted")):
            with self.assertRaises(OSError):
                lesson.publish(self.root, task_id, "Test")
        (self.root / "revisions" / ("r-" + task_id) / "artifact-checks.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "snapshot conflict"):
            lesson.recover(self.root)

    def test_additional_tool_skill_receipt_and_module_snapshot(self):
        task_id = self.draft()
        tool = self.pattern.parent / "numerical-tool.md"
        tool.write_text("Test tool skill, not real methodological evidence.")
        config = lesson.read_json(self.root / "knowledge.json")
        with self.assertRaisesRegex(ValueError, "configured"):
            grounding.capture(self.root, tool, "skill")
        config["tool_skills"] = [str(tool)]
        lesson.save_json(self.root / "knowledge.json", config)
        receipt = grounding.capture(self.root, tool, "skill")
        design = lesson.read_json(self.root / "design.json")
        design["sources"].append(receipt["id"])
        design["decisions"][0]["sources"].append(receipt["id"])
        lesson.save_json(self.root / "design.json", design)
        grounding.prepare(self.root, task_id)
        packet = {"module": {"id": "test-module"}, "preferences": {"offline": True}}
        lesson.save_json(self.root / "materials/module-context.json", packet)
        lesson.publish(self.root, task_id, "Tool receipt and context")
        revision = self.root / "revisions" / ("r-" + task_id)
        self.assertEqual(lesson.read_json(revision / "module-context.json"), packet)
        config["tool_skills"] = []
        lesson.save_json(self.root / "knowledge.json", config)
        with self.assertRaisesRegex(ValueError, "authority"):
            grounding.validate(self.root, lesson.task_record(self.root, task_id))

    def test_other_tool_skill_cannot_replace_required_frontend_receipt(self):
        task_id = self.draft()
        tool = self.pattern.parent / "other-tool.md"
        tool.write_text("Test tool skill")
        config = lesson.read_json(self.root / "knowledge.json")
        config["tool_skills"] = [str(tool)]
        lesson.save_json(self.root / "knowledge.json", config)
        receipt = grounding.capture(self.root, tool, "skill")
        design = lesson.read_json(self.root / "design.json")
        design["sources"] = [s for s in design["sources"] if s.startswith("pattern-")] + [receipt["id"]]
        lesson.save_json(self.root / "design.json", design)
        with self.assertRaisesRegex(ValueError, "frontend-design"):
            grounding.prepare(self.root, task_id)

    def test_disposable_reset_destroys_outputs_preserves_inputs_and_republishes(self):
        task = self.draft()
        lesson.publish(self.root, task, "Before reset")
        retained = self.root / "materials/keep.txt"
        retained.write_text("Original material")
        (self.root / "RETRO.md").write_text("Keep observations")
        for name in (".niu-prototyper/snapshots/old.html", ".niu-prototyper/overlays/old.html"):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(VALID)
        lesson.make_disposable(self.root)
        cache_inode = (self.root / ".niu-prototyper/overlays").stat().st_ino
        before = (self.root / "exports" / ("r-" + task + ".html")).read_bytes()
        self.assertTrue(lesson.reset(self.root)["dry_run"])
        self.assertEqual((self.root / "exports" / ("r-" + task + ".html")).read_bytes(), before)
        with patch.object(lesson, "canvas", return_value={"ok": True}) as reload:
            result = lesson.reset(self.root, destroy=True)
        reload.assert_called_once_with(self.root.resolve(), "reload")
        self.assertTrue(result["destroyed"])
        for name in ("src", "tasks", "revisions", "exports", "evidence"):
            self.assertEqual(list((self.root / name).iterdir()), [])
        self.assertEqual((self.root / "preview/index.html").read_text(), lesson.DISPOSABLE_STARTER)
        self.assertFalse((self.root / "design.json").exists())
        self.assertEqual(list((self.root / ".niu-prototyper/snapshots").iterdir()), [])
        self.assertEqual((self.root / ".niu-prototyper/overlays").stat().st_ino, cache_inode)
        self.assertEqual(retained.read_text(), "Original material")
        self.assertEqual((self.root / "RETRO.md").read_text(), "Keep observations")
        self.assertTrue((self.root / "tools/lesson.py").exists())
        next_task = self.draft("A different science topic")
        self.assertIsNone(lesson.task_record(self.root, next_task)["base_revision"])
        lesson.publish(self.root, next_task, "After reset")

    def test_reset_refuses_normal_workspace_without_deleting(self):
        with self.assertRaisesRegex(ValueError, "disposable"):
            lesson.reset(self.root, destroy=True)
        self.assertEqual((self.root / "preview/index.html").read_bytes(), self.original)

    def test_reset_refuses_busy_active_and_pending_publication(self):
        lesson.make_disposable(self.root)
        task = self.draft()
        with self.assertRaisesRegex(ValueError, "active task"):
            lesson.reset(self.root, destroy=True)
        lesson.abandon(self.root, task)
        (self.root / "publish-pending.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "active task"):
            lesson.reset(self.root, destroy=True)
        (self.root / "publish-pending.json").unlink()
        with lesson.locked(self.root):
            with self.assertRaisesRegex(ValueError, "busy"):
                lesson.reset(self.root, destroy=True)

    def test_reset_preflights_links_before_any_deletion(self):
        lesson.make_disposable(self.root)
        sentinel = self.root / "src/keep-until-preflight.txt"
        sentinel.write_text("draft")
        link = self.root / "exports/outside"
        link.write_text("pretend symbolic link")
        original = Path.is_symlink
        with patch.object(Path, "is_symlink", lambda p: p == link or original(p)):
            with self.assertRaisesRegex(ValueError, "symbolic link"):
                lesson.reset(self.root, destroy=True)
        self.assertEqual(sentinel.read_text(), "draft")
        self.assertFalse((self.root / "reset-pending.json").exists())

    def test_reset_rejects_outside_target(self):
        outside = self.root.parent / "outside.txt"
        outside.write_text("keep")
        with self.assertRaises(ValueError):
            lesson.checked_reset_paths(self.root, ("../outside.txt",))
        self.assertEqual(outside.read_text(), "keep")

    def test_reset_rejects_real_directory_links_and_linked_parent(self):
        lesson.make_disposable(self.root)
        outside = self.root.parent / "outside"
        outside.mkdir()
        sentinel = outside / "preserve.txt"
        sentinel.write_text("Outside reference")
        draft = self.root / "src/draft.txt"
        draft.write_text("Not deleted before preflight")
        for relative in ("exports/linked", ".niu-prototyper"):
            link = self.root / relative
            if os.name == "nt":
                result = lesson.subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(outside)],
                                               capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
            else:
                link.symlink_to(outside, target_is_directory=True)
            try:
                with self.assertRaisesRegex(ValueError, "link|reparse"):
                    lesson.reset(self.root, destroy=True)
                self.assertEqual(sentinel.read_text(), "Outside reference")
                self.assertEqual(draft.read_text(), "Not deleted before preflight")
            finally:
                if os.name == "nt":
                    link.rmdir()  # Remove the verified junction itself, never its target.
                else:
                    link.unlink()

    def test_reset_failure_blocks_authoring_and_can_retry(self):
        lesson.make_disposable(self.root)
        (self.root / "src/nested").mkdir()
        with patch.object(lesson.shutil, "rmtree", side_effect=OSError("Injected failure")):
            with self.assertRaisesRegex(OSError, "Injected failure"):
                lesson.reset(self.root, destroy=True)
        self.assertTrue((self.root / "reset-pending.json").exists())
        with self.assertRaisesRegex(ValueError, "Reset was interrupted"):
            lesson.begin(self.root, "Should not start")
        with patch.object(lesson, "canvas", side_effect=ValueError("Offline canvas")):
            result = lesson.reset(self.root, destroy=True)
        self.assertTrue(result["destroyed"])
        self.assertFalse(result["canvas_reload"]["ok"])
        self.assertFalse((self.root / "reset-pending.json").exists())
        with patch.object(lesson, "canvas", return_value={"ok": True}):
            self.assertTrue(lesson.reset(self.root, destroy=True)["destroyed"])

    def test_publish_revision_export_and_duplicate(self):
        task = self.draft()
        result = lesson.publish(self.root, task, "Initial lesson")
        self.assertEqual((self.root / "preview/index.html").read_bytes(), VALID)
        self.assertEqual(Path(result["export"]).read_bytes(), VALID)
        self.assertEqual((self.root / "revisions" / result["revision"] / "index.html").read_bytes(), VALID)
        self.assertTrue(lesson.publish(self.root, task, "Retry")["already_published"])
        self.assertEqual(len(list((self.root / "revisions").iterdir())), 1)
        self.assertIsNone(lesson.read_json(self.root / "workspace.json")["teacher_accepted_revision"])

    def test_invalid_html_preserves_preview(self):
        task = self.draft()
        (self.root / "src/lesson.html").write_text("<h1>Incomplete")
        with self.assertRaises(ValueError):
            lesson.publish(self.root, task, "Broken")
        self.assertEqual((self.root / "preview/index.html").read_bytes(), self.original)
        self.assertEqual(list((self.root / "revisions").iterdir()), [])

    def test_bad_script_preserves_preview(self):
        task = self.draft()
        (self.root / "src/lesson.html").write_bytes(VALID.replace(b"let n=1;", b"let = ;"))
        with self.assertRaisesRegex(ValueError, "syntax"):
            lesson.publish(self.root, task, "Broken JS")
        self.assertEqual((self.root / "preview/index.html").read_bytes(), self.original)

    def test_missing_output(self):
        task = lesson.begin(self.root, "Generate")["id"]
        with self.assertRaises(FileNotFoundError):
            lesson.publish(self.root, task, "Missing")
        self.assertEqual((self.root / "preview/index.html").read_bytes(), self.original)

    def test_external_preview_change_is_preserved(self):
        task = self.draft()
        (self.root / "preview/index.html").write_bytes(b"External edit")
        with self.assertRaisesRegex(ValueError, "changed"):
            lesson.publish(self.root, task, "Stale")
        self.assertEqual((self.root / "preview/index.html").read_bytes(), b"External edit")

    def test_active_request_and_abandon_keep_draft(self):
        task = self.draft()
        with self.assertRaisesRegex(ValueError, "active task"):
            lesson.begin(self.root, "Second")
        lesson.abandon(self.root, task)
        self.assertEqual((self.root / "src/lesson.html").read_bytes(), VALID)
        self.assertIsNotNone(lesson.begin(self.root, "Now another")["id"])

    def test_lock_exclusion(self):
        with lesson.locked(self.root):
            with self.assertRaisesRegex(ValueError, "busy"):
                lesson.begin(self.root, "Blocked")

    def test_snapshot_collision_never_overwrites(self):
        task = self.draft()
        snapshot = self.root / "revisions" / ("r-" + task)
        snapshot.mkdir()
        (snapshot / "index.html").write_bytes(b"Interrupted output")
        with self.assertRaises(FileExistsError):
            lesson.publish(self.root, task, "Retry interrupted")
        self.assertEqual((snapshot / "index.html").read_bytes(), b"Interrupted output")
        self.assertEqual((self.root / "preview/index.html").read_bytes(), self.original)

    def test_task_id_cannot_escape(self):
        with self.assertRaisesRegex(ValueError, "Invalid task"):
            lesson.publish(self.root, "../workspace", "No")

    def test_interrupted_publication_can_recover(self):
        task = self.draft()
        original_save = lesson.save_json

        def fail_state(path, value):
            if path.name == "workspace.json":
                raise OSError("Injected state write interruption")
            original_save(path, value)

        with patch.object(lesson, "save_json", side_effect=fail_state):
            with self.assertRaises(OSError):
                lesson.publish(self.root, task, "Interrupted")
        self.assertEqual((self.root / "preview/index.html").read_bytes(), VALID)
        with self.assertRaisesRegex(ValueError, "Recover"):
            lesson.begin(self.root, "Too soon")
        recovered = lesson.recover(self.root)
        self.assertEqual(Path(recovered["previous_preserved"]).read_bytes(), self.original)
        self.assertIsNone(lesson.read_json(self.root / "workspace.json")["active_task"])
        self.assertFalse((self.root / "publish-pending.json").exists())
        self.assertTrue(lesson.publish(self.root, task, "Retry")["already_published"])

    def test_recovery_refuses_to_erase_external_edit(self):
        task = self.draft()
        with patch.object(lesson, "complete_publication", side_effect=OSError("Interrupted")):
            with self.assertRaises(OSError):
                lesson.publish(self.root, task, "Interrupted")
        (self.root / "preview/index.html").write_bytes(b"New external edit")
        with self.assertRaisesRegex(ValueError, "conflict"):
            lesson.recover(self.root)
        self.assertEqual((self.root / "preview/index.html").read_bytes(), b"New external edit")

    def test_canvas_contract_and_wrong_identity(self):
        calls = []
        identity = {"project": "test-canvas", "workspace": lesson.digest(str(self.root).encode())[:16]}

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                calls.append((self.command, self.path, dict(self.headers)))
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(identity).encode())

            def do_POST(self):
                calls.append((self.command, self.path, dict(self.headers)))
                valid = (self.headers.get("X-NP-Token") == "test-token"
                         and self.headers.get("Cookie") == f"np_{self.server.server_port}=test-token"
                         and self.headers.get("Origin") == f"http://127.0.0.1:{self.server.server_port}")
                self.send_response(200 if valid else 403)
                self.end_headers()
                self.wfile.write(json.dumps({"ok": valid, "tabs": 1}).encode())

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        registry = self.root / "test-registry"
        lesson.save_json(registry / "projects.json", {"projects": [{"id": "test-canvas", "root": str(self.root)}]})
        lesson.save_json(registry / "state/test-canvas/runtime.json", {"shellPort": server.server_port, "token": "test-token"})
        with patch.dict(lesson.os.environ, {"NIU_PROTOTYPER_HOME": str(registry)}):
            self.assertTrue(lesson.canvas(self.root, "reload")["ok"])
            self.assertEqual(calls[-1][1], "/_np/api/reload")
            identity["workspace"] = "wrong"
            with self.assertRaisesRegex(ValueError, "identity mismatch"):
                lesson.canvas(self.root, "reload")
            self.assertEqual(calls[-1][1], "/healthz")
            self.assertNotIn("X-NP-Token", calls[-1][2])

    def test_missing_design_preserves_preview(self):
        task = self.draft()
        (self.root / "design.json").unlink()
        with self.assertRaises(FileNotFoundError):
            lesson.publish(self.root, task, "Missing")
        self.assertEqual((self.root / "preview/index.html").read_bytes(), self.original)

    def test_invalid_design_cases_preserve_preview(self):
        for case in ("wrong-task", "wrong-base", "unknown-source", "no-research", "changed-design"):
            with self.subTest(case=case):
                task = self.draft()
                design = lesson.read_json(self.root / "design.json")
                if case == "wrong-task":
                    design["task"] = "0" * 12
                elif case == "wrong-base":
                    design["base_revision"] = "r-wrong"
                elif case == "unknown-source":
                    design["decisions"][0]["sources"] = ["fabricated"]
                elif case == "no-research":
                    design["research"] = []
                else:
                    design["objective"] = "Changed after preparation"
                lesson.save_json(self.root / "design.json", design)
                with self.assertRaises(ValueError):
                    lesson.publish(self.root, task, case)
                self.assertEqual((self.root / "preview/index.html").read_bytes(), self.original)
                lesson.abandon(self.root, task)

    def test_missing_and_tampered_local_receipt(self):
        task = self.draft()
        receipt_id = lesson.read_json(self.root / "design.json")["sources"][0]
        path = self.root / "evidence" / receipt_id / "source.md"
        path.write_text("Tampered")
        with self.assertRaisesRegex(ValueError, "receipt"):
            lesson.publish(self.root, task, "Tampered")
        path.unlink()
        with self.assertRaises(FileNotFoundError):
            lesson.publish(self.root, task, "Missing")
        self.assertEqual((self.root / "preview/index.html").read_bytes(), self.original)

    def test_stale_canonical_source_requires_review(self):
        task = self.draft()
        self.pattern.write_text("New canonical source version")
        with self.assertRaisesRegex(ValueError, "stale"):
            lesson.publish(self.root, task, "Stale")

    def test_revision_retains_design_and_receipts(self):
        first = self.draft()
        lesson.publish(self.root, first, "First")
        snapshot = self.root / "revisions" / ("r-" + first)
        original_design = (snapshot / "design.json").read_bytes()
        second = self.draft("Revise")
        design = lesson.read_json(self.root / "design.json")
        design["task"] = first
        lesson.save_json(self.root / "design.json", design)
        with self.assertRaisesRegex(ValueError, "task/base"):
            lesson.publish(self.root, second, "Old design")
        design["task"] = second
        lesson.save_json(self.root / "design.json", design)
        result = lesson.publish(self.root, second, "Second")
        self.assertEqual((snapshot / "design.json").read_bytes(), original_design)
        self.assertEqual((self.root / "preview/design.html").read_bytes(),
                         (self.root / "exports" / (result["revision"] + ".design.html")).read_bytes())
        grounding.verify_snapshot(snapshot, lesson.read_json(snapshot / "manifest.json")["design_files"])

    def test_recovery_rejects_changed_design_snapshot(self):
        task = self.draft()
        with patch.object(lesson, "complete_publication", side_effect=OSError("Interrupted")):
            with self.assertRaises(OSError):
                lesson.publish(self.root, task, "Interrupted")
        (self.root / "revisions" / ("r-" + task) / "design.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "snapshot conflict"):
            lesson.recover(self.root)

    def test_prejournal_failure_preserves_files_and_allows_new_task(self):
        task = self.draft()
        with patch.object(grounding, "snapshot", side_effect=OSError("Injected preparation failure")):
            with self.assertRaises(OSError):
                lesson.publish(self.root, task, "Interrupted before journal")
        preserved = self.root / "revisions" / ("r-" + task) / "index.html"
        self.assertEqual(preserved.read_bytes(), VALID)
        self.assertFalse((self.root / "publish-pending.json").exists())
        self.assertEqual((self.root / "preview/index.html").read_bytes(), self.original)
        lesson.abandon(self.root, task)
        next_task = self.draft("Retry preserved draft under a new task")
        lesson.publish(self.root, next_task, "Completed")
        self.assertEqual(preserved.read_bytes(), VALID)


if __name__ == "__main__":
    unittest.main()
