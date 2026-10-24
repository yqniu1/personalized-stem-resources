# Portable authoring packet: experiment 0.1

Date: 2026-10-20\
Status: exercised in one synthetic Codex-operated revision loop; not an implemented authoring service or validated cross-provider interface.\
Related: [design](design-authoring-workflow.md), [earlier rehearsal probes](plan-authoring-rehearsal.md).

## Outcome

The authoring work can now be inspected as a concrete file packet: a brief, two requests, version-bound feedback, three recoverable revisions, checks, and an export. The packet records one current task and distinguishes operator acceptance from teacher acceptance.

The experiment adapted a disposable Lily 2-D copy: r1 simplified the directions and added an explanation card; synthetic operator feedback requested explicit anther/stigma terms and the one-bloom limit; r2 applied that revision. Its saved output passed the recorded offline pointer-transfer/reset checks and was copied into an export with an identical hash.

This tests an operator following a protocol. It does not establish independent teacher use, native agent interchangeability, automated conflict protection, or classroom readiness. No original module or shared-tool source was changed.

## Packet layout and authority

```text
operator-loop/
  workspace.json                 authoritative pointers, identity and current owner
  workspace.md                   reading instructions; points to the JSON
  HANDOFF.md                     narrative rationale, not native chat history
  brief.md                       instructional request and constraints
  teacher-note.md                 model limits and known gaps
  tasks/
    task-001.json + .md           initial request, scope, acknowledgment, result
    feedback-001.json             review actor, anchor, artifact hash and request
    task-002.json + .md           bounded revision and observed checks
    task-003.json                 pending read-only handoff acknowledgment
  modules/lily-dissection/        current editable fixture and generated HTML
  revisions/r0|r1|r2/
    manifest.json                SHA-256 map
    files/                       complete selected build inputs/output, brief/note
  checks/                        retained probe evidence
  exports/r2/
    index.html                   copied from the reviewed revision
    teacher-note.md
```

The manifest and current task carry machine-readable references. Markdown provides rationale. If pointers or statuses disagree, stop and reconcile against files/hashes rather than choosing whichever narrative is convenient.

This is a selected-resource package, not a complete repository backup. Each saved revision contains all inputs needed by the copied 2-D assembler. It contains neither 3-D assets nor the merged launcher, and it must not be presented as a deployable update to the original module.

## Minimum fields

| Record | Fields that matter |
|---|---|
| Workspace | Contract/workspace ID; Windows/WSL roots; selected resource source/build/artifact; brief path/hash; current task; candidate/operator-accepted/teacher-accepted revision pointers; export file hashes; active owner; open questions |
| Task | Stable ID; actual origin/actor; base revision; brief hash; expected input hashes; allowed edit paths; generated output; request; required/observed checks; result revision; review authority |
| Feedback | Stable ID; actual reviewer; reviewed revision and artifact hash; selector plus original text; requested change; disposition; explicit teacher-feedback boolean |
| Revision | Revision ID; full relative-path/hash manifest; recoverable selected inputs/output; teacher acceptance remains separate |
| Export | Source revision; review authority; exact files/hashes; classroom-readiness status |

Absolute roots help the current machine launch the right workspace. A moved packet needs its roots explicitly remapped and its relative references rechecked; this experiment did not test relocation. Runtime session URLs, tokens and native conversation files are absent.

### Review semantics

- A candidate can exist before it is reviewed.
- A task's execution can be completed without its resource being accepted.
- `operator_accepted_revision` identifies a test result the operator checked.
- `teacher_accepted_revision` stays null until a real teacher makes a recorded decision about that exact revision.
- An export's matching hash establishes file identity, not instructional quality.
- `active_owner: null` means the record assigns no editor. It does not prove there are no running external processes.

The r2 task records `review.authority = operator` and `decision = accepted-for-rehearsal`; its export explicitly has `classroom_ready = false`.

## Operator sequence exercised

1. Copy selected inputs into a new disposable workspace; retain their original hashes and r0.
2. Write the synthetic brief, task 001 and editing acknowledgment.
3. Revise only the copied template; assemble and save r1.
4. Read r1 in the browser. Record feedback with the r1 output hash and original paragraph text.
5. Create task 002 based on r1. Check expected input hashes before applying the change.
6. Detect a simulated external source edit; retain that version separately and explicitly reconcile the probe. No stale revision was applied during this step.
7. Apply the requested revision, build r2, and check its rendered prompt and offline pointer transfer/reset.
8. Record operator acceptance and copy the export from r2's saved files. Verify export/revision identity.
9. Leave task 003 as a read-only acknowledgment request with no assigned editing owner.

These steps were performed by Codex. The “feedback” is a test fixture, not a teacher interview. The prior canvas feedback test remains separate; this loop used standalone file previews and version-bound feedback records, without relaunching the canvas the user asked to stop.

## Checks and limits

| Check | Observed outcome | What it does not establish |
|---|---|---|
| Revision integrity | Three snapshots, 37 files per snapshot; all stored hashes matched | Protection against a malicious writer changing both files and manifests |
| Source drift | Expected-input mismatch detected; simulated external edit retained separately; baseline explicitly restored before editing | Atomic publish protection, concurrent-agent safety, or safe automatic merge |
| Duplicate snapshot | A second attempt to save r2 exited 1 and left the revision count at three | Idempotent provider execution; no duplicate task was sent to another agent |
| Completed-task lookup | Task 002 points to existing r2 rather than requesting a fresh revision | Automated duplicate-delivery handling |
| Independent output | Saved r2 opened via `file:` with networking disabled; explanation, pointer transfer, scientific transfer feedback, and reset checked; no resource entries observed | Full browser-error, device, keyboard, or science review |
| Export identity | Export HTML hash equals the browser-tested r2 output hash | Teacher approval or full classroom usability |
| Original preservation | Original selected module input/output hashes unchanged | A claim about unrelated repository files |

The control here is an operator honoring checks. Small one-off Python helpers create/verify evidence in scratch; they are not wired into either canvas or a production publisher. Do not promote their results into claims about an automated adapter.

## Actual packet and evidence

Local packet:

`C:/Users/pniu/AppData/Local/Codex/scratch/stem-authoring-rehearsal-20261020/operator-loop`

Read `workspace.md`, then `workspace.json` and its current task. Evidence is in `checks/`, snapshots in `revisions/`, and the export in `exports/r2/`. One-off preparation/review/export helpers are in the parent scratch directory.

| Revision | Purpose | HTML SHA-256 |
|---|---|---|
| r0 | Unchanged baseline | `bcd3d0e53ab71680ba406c86bb3a98b0538488c52f82e654a49af7b530bb1eb8` |
| r1 | Directions and initial explanation | `fb444f2f517f593701f89b1145cd4cbb99c5d27e0d7a88180361ea3063de8165` |
| r2 | Revised explanation, retained for operator rehearsal | `8592bc1d8c4e64208b15e75fc3806e1aef6342de79d364ed25906bcce4a6c822` |

## Implications for the authoring tool

The next interoperability test can use this packet instead of reconstructing the request from the session. An incoming implementation should acknowledge the selected resource, r2, open limitations, and no current editing permission before a new bounded revision is assigned.

Do not add a general agent framework based on this result. First measure how much manual work the packet requires and run actual provider handoffs. If reliable checks cannot be sustained manually, the concrete next tooling candidate is validation of input/revision/export identity at the publishing boundary. Its placement in existing reusable tooling needs design before implementation.

The teacher-facing surface should eventually expose the same distinctions in plain terms: current request, preview version, what changed, open feedback, and which version was accepted. This packet gives those labels concrete meanings; it does not demonstrate that teachers understand them.

**Insight — provenance:** putting an artifact in an “accepted” folder is weaker than recording who accepted which bytes for which purpose. The experiment keeps operator, teacher, and classroom-use judgments distinct.

Keyboard access and baseline science review still gate teacher use. They do not block a synthetic operator test of packet identity and handoff structure. The actual teacher request/device and all three-provider continuity legs remain open.

## Cold review

A fresh same-provider reviewer reconstructed the selected resource, r2 export, pending task,
review authority, and open limits from the packet alone. It independently verified all 37
files in each of the three revisions and both export hashes. One overclaim was corrected:
preservation evidence covers original selected module inputs/outputs, not every repository file.
This was a cold read, not a cross-provider handoff test.
