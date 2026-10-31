# Grounded authoring — October 20

Supersedes the prior ungrounded operator demo as the current test. Preserve that
workspace. Target remains a teacher with Peter assisting, preceded by an operator test.

Before editing a lesson, the native author must read relevant Learnability Patterns
from their canonical repository, use niu-library search and expanded parent passages,
and consult the personal frontend-design skill. A reusable learning-authoring skill
connects learner need, observable learning evidence, design decisions and their limits.
Only the library connection and relevant skills are added to the native WSL agent.

Each request gets a design.json bound to its task and base revision. It records the
objective, assessment, standards status, assumptions, selected source receipts,
decisions and limitations. Local source receipts contain original bytes and hashes.
Research records contain actual source/parent IDs and agent-written interpretations
of expanded passages; these are attributed interpretations, not authenticated tool
transcripts. Publication validates the record and snapshots it with the lesson.
The operator test independently checks the native transcript for actual retrieval.
Schema validation cannot establish pedagogical or scientific validity.

Revisions reuse relevant evidence but must bind the design to the new request and
explain changed decisions. No requirement to retrieve unrelated research for a copy edit.
If relevant research is unavailable, preserve the draft and report the gap; do not
publish it as a grounded lesson. Standards remain unverified until a supplied or
retrieved authoritative standard is matched to student evidence.

Predefined checks, before implementation:

1. Missing design, missing local source, changed receipt bytes, wrong task/base,
   unknown decision source, and missing expanded research records reject publication
   while preserving the current canvas.
2. Successful publication preserves the exact design and source receipts alongside
   the exact lesson export; interrupted recovery also verifies the design snapshot.
3. Revision requires a new task-bound design while preserving the earlier rationale.
4. An ordinary teacher prompt, without retrieval instructions, actually reads canonical patterns and the personal skill,
   calls library search and retrieve_parent, then generates and publishes a lesson.
5. Inspect source-to-decision claims against the retrieved passages and actual lesson.
   At least one consequential instructional decision must be accurately supported by
   an expanded passage, bounded to its scope and visibly implemented. Visual preference
   is distinct from evidence for learning; citation presence alone does not pass.
   Exercise keyboard interaction, explanatory feedback and transfer in the browser.
6. A follow-up revision retains relevant grounding and produces a distinct snapshot.

No teacher learning outcome, standards coverage, device compatibility, or independent
teacher usability is inferred from this operator test. No new hosted service.

## Observed results

Twenty authoring helper tests pass. These cover the invalid/missing design cases,
receipt tampering and stale canonical sources, retained revision rationale, recovery
snapshot conflicts, and the existing publication/canvas contract checks. Before-journal
failures preserve incomplete files and use an explicit abandon/new-task procedure;
they do not recover automatically.

The ordinary teacher request was a ten-minute grade 4 bee/pollen lesson addressing
confusion between pollination and seed formation, with a wrong sequence, explanation,
transfer, offline use and keyboard controls. It did not name skills or retrieval tools.

- The native agent read learning-authoring, captured practice-and-feedback, transfer
  and frontend-design, called search_docs and attempted retrieve_parent.
- Empty parent results caused a real design-check failure. The draft was retained;
  neither preview nor exports changed. This was a useful negative integration test.
- Investigation found a hosted niu-library SDK encoding issue: spaces in parent IDs
  became `+`; the fetch endpoint returned zero vectors. The otherwise identical
  request using `%20` returned the expected passage. SDK 9 also returns an HTTPS
  host URL where SDK 8 returns a bare host.
- The narrow service fix uses the published fetch API with exact encoding and
  supports both host forms. Four regression cases pass. Deployed MCP smoke tests
  returned known book and paper parents and omitted a deliberately missing ID.
  See niu-library PR [29](https://github.com/yqniu1/niu-library/pull/29).
  PR [30](https://github.com/yqniu1/niu-library/pull/30) removes unrelated earlier
  housekeeping accidentally carried from the starting branch; net main changes
  are only retrieval code and tests.
- A temporary network interruption to AWS cleared before the positive test.
  A stalled native model request was interrupted and its CLI restarted, preserving
  the active request and draft.
- The fresh native agent resumed the plain teacher request, repeated search and
  successfully expanded all three returned parent IDs. Trace:
  `rollout-2026-10-20T13-44-32-01a15a6a-368a-7590-8caf-6748cc4e83ec.jsonl`.
  It prepared the design, revised the draft, published `r-0c9cef3e18f5`, and reloaded.
- An independent cold reviewer expanded the two cited passages and found accurate
  source interpretations with appropriate limits. Clark/Mayer's explanatory-feedback
  discussion maps to causal feedback on pollen location; the Handbook's error-learning
  boundary maps to vocabulary support and a visibly identified wrong route. This
  supports source-to-activity correspondence, not causal effectiveness.
- With networking disabled, the exported lesson loaded and passed a keyboard-driven
  wrong route, repair, wrong/right transfer choices, explanation entry/model reveal,
  and full reset. Browser resource entries were zero. A desktop screenshot was inspected.
- A second ordinary prompt asked for a shorter first screen while retaining the
  distinction and explanation questions. Revision `r-7044fe3a44cc` retained the source
  evidence, rebound the design to its new task/base, and shortened the opening.
  The interaction code and explanation sections remained unchanged.
- Final revision `r-6f2e919c9afe` adds the reviewer's diagram-scope caption.
  A byte comparison confirmed that the caption is the only lesson change.
  Source, preview, snapshot and export all match SHA256
  `0b78102bd7f9b275cc6661cb16243468683e61d6c63207a43267217d0911b2fe`.
  All eight design/evidence hashes and both rationale exports match; task/base
  binding is current. The final file loaded offline with its caption and zero
  resource entries. Browser networking was restored.
- The teacher rationale was inspected in the browser. The canvas remains open with
  one idle native agent in the left drawer. No active task or teacher acceptance;
  Peter's own user test is next.

**Insight — retrieval is a dependency, not a citation format.** A visible reference
list would have hidden the broken passage lookup. Requiring expanded passages before
publication exposed it, while the native transcript provided independent evidence
that retrieval occurred. Structural validation still cannot establish whether an
agent's interpretation is correct.
