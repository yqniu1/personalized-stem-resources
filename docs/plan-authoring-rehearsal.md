# Authoring rehearsal: findings and bounded next steps

Date: 2026-10-20\
Status: Targeted operator probes completed; teacher trial and agent-continuity rehearsal not completed.\
Design: [teacher-builder authoring workflow](design-authoring-workflow.md).

Continuation: the [portable packet experiment](authoring-packet-contract.md) now exercises the manual request/revision/export records in a synthetic operator loop. Keyboard remediation still gates teacher use, but does not block testing the authoring tool's packet structure. No canvas server was relaunched for that loop.

## Decision

The existing document and live-preview tools are sufficient to attempt the assisted rehearsal. The immediate blocker is the selected 2-D resource's keyboard interaction path. Fix and verify that narrow prerequisite before a teacher trial. The probes do not justify building a new shell, hosted service, or automated agent-adapter layer.

Peter confirmed a teacher with Peter assisting as the first population. The actual teacher request and classroom device are still unknown. The proposed directions/explanation adaptation remains a fixture, not a teacher-validated requirement.

## What was actually checked

Tests used a disposable copy at:

`C:/Users/pniu/AppData/Local/Codex/scratch/stem-authoring-rehearsal-20261020/workspace`

Only the 2-D template, assembly script, SVG assets, manifest, module README, and baseline HTML were copied. Authoring records and a temporary preview directory were created there. A separate `NIU_PROTOTYPER_HOME` under the same scratch directory isolated registration/runtime state from the user's existing registry. No new editing agent was launched.

| Design test | Observed result | Limit |
|---|---|---|
| T0: target/build identity | **Passed targeted probe.** Rebuild exactly matched the shipped 2-D file. A temporary button-label edit in fixture source appeared in preview after assembly and explicit reload. Restoring source restored the baseline hash. | Only selected 2-D fixture; no 3-D/merged check |
| T2: reopen | **Passed saved-state subset.** Both servers stopped/restarted on their previous ports; browser reload recovered the edited brief and addressed-but-unresolved UI feedback. Observed command/browser sequence took 21 seconds. | Operator/tool timing, not teacher recovery time; no full accepted/candidate task packet existed |
| T5: conflict | **Passed document subset.** Read a brief revision, saved a newer edit through the browser, then submitted a stale `apply-blocks` edit. CLI exited 1 and the newer text survived. | Does not establish resource-source conflict protection or filesystem fencing |
| T6: stale feedback | **Passed changed-element subset.** An Inspect comment on `#btnSeparate` retained its original text/hash; changing the label caused a visible “Element changed” notice. | Missing element, ambiguous selector, re-anchor behavior, and teacher interpretation not exercised |
| T7: build/recovery | **Passed file-preservation subset.** Temporarily withholding the copied manifest caused assembly exit 1. Candidate output and retained baseline export were unchanged. Restoring the manifest/source rebuilt the baseline. | Manual operator workflow; no automatic failed-build UI or publication guard tested |
| T8: independent export | **Passed offline interaction subset.** Opened baseline HTML via `file:` with browser networking disabled; disassembly, pointer pollen transfer, and reset worked. Runtime resource entries were empty. | Not a full export-content audit, browser error audit, or complete interaction/device matrix |
| T9: keyboard | **Failed selected-path prerequisite.** Tab cycled through four toolbar buttons, the attribution link, and document body. None of the 13 flower parts was focusable. No keyboard path for pollen transfer was found in rendered controls or source handlers. | Not a complete accessibility audit |
| T1/T3/T4/T10/T11 | **Not run.** No teacher trial, provider handoff, running-agent cancellation/duplicate delivery, human science review, or comparative quality evaluation | Do not infer these from the probes above |

The temporary interface request was created by Codex as a test fixture, then claimed/replied to/finished through the prototyper CLI. This demonstrates the UI-to-CLI feedback path, not teacher performance. It remains **addressed**, not teacher-resolved.

The Document Canvas browser edit was also performed by Codex for testing. The tool's event labels call a browser save “human”; that label is not evidence that a teacher participated.

### Runtime/configuration findings

- Document Canvas checkout: `0e12068`; niu-prototyper checkout: `5a3ffa6` / version `0.2.0`. Both worktrees were clean when inspected. Engine sync reported all five locked/ported prototyper entries current.
- WSL exposes Python 3.12.3, Node 22.23.3, tmux 3.4, the two canvas commands, Codex, and Claude. This session launched both tool servers successfully; no agent authentication or model invocation was tested.
- Windows CLI probes returned Codex `0.163.0`, Claude Code `2.1.304`, and AGY `1.4.3`. Installed AGY help exposes print mode, JSON/streaming output, execution modes, and conversation selection. These are interface-discovery results, not proof of working authentication, workspace mapping, or continuity.
- AGY was absent from WSL's command path. Its entry in the generic terminal menu does not establish a usable launch. Use a bounded native Windows probe before considering any WSL integration change.
- The user's WSL prototyper registry really does point `lily-dissection` to the original private checkout. It was read but not changed. Register a distinct public/trial workspace; do not retarget the private entry implicitly.
- BrowserOS's ref-based click on a button inside the iframe reported a covering SVG. A pointer click at the button's observed DOM box worked and produced the correct anchor. Record this as an automation limitation, not demonstrated teacher-interface failure. A screenshot attempt timed out; no visual screenshot verification is claimed.

### Evidence retained

Local scratch directory `C:/Users/pniu/AppData/Local/Codex/scratch/stem-authoring-rehearsal-20261020/` contains:

- `prepare.py` and `baseline.json`: copied inputs and original/rebuilt/preview/export hashes.
- `check_build_recovery.py` and `build-recovery.json`: controlled assembly failure, preservation, restoration, and source-checkout integrity checks.
- `stale-edits.json`: rejected document conflict fixture.
- `workspace/.document-canvas/`: saved document/history and event records.
- `workspace/.niu-prototyper/`: original anchored comment, addressed reply, batch state.
- `workspace/revisions/probe-label/`: temporary candidate source and output, preserved before restoration.
- `workspace/exports/lily-baseline.html`: unchanged standalone baseline.

Baseline HTML SHA-256:

`bcd3d0e53ab71680ba406c86bb3a98b0538488c52f82e654a49af7b530bb1eb8`

Original module input/output hashes remained unchanged after the probes. Tokens and authenticated session URLs are not copied into this document. Scratch artifacts are local evidence, not classroom deliverables or a reusable tooling package.

## Bounded implementation and rehearsal plan

### 1. Resolve the selected-path prerequisite

Scope the next module change to 2-D keyboard equivalents, using existing interaction/state functions where feasible:

- Let keyboard users select flower structures and read the same descriptions as pointer users.
- Provide explicit keyboard-operable pollen pickup and delivery actions with feedback about the current state.
- Provide a keyboard route to the required nectar action if it remains part of the task.
- Preserve pointer behavior, visible focus, reset behavior, and the within-one-bloom scientific qualification.

Start in `modules/lily-dissection/src/template.html`; update generated 2-D HTML through the existing assembler. If the changed 2-D content is shipped through the merged launcher, rebuild that deliverable too and test its switch/fallback. Do not hand-edit generated HTML or leave the merged resource silently carrying an older version.

Before implementing, inspect the relevant existing state/geometry functions and define the exact keyboard interaction sequence. This is the behavioral scope, not a completed code design. No shared canvas-engine change is required by current evidence.

Done when: keyboard-only operation can select parts, transfer pollen, read the feedback, and reset, plus find nectar if the recorded task or existing state prerequisites require it; pointer equivalents still work; offline export remains self-contained; relevant original/merged distribution outputs agree.

### 2. Prepare one complete work packet

Use the design's `brief.md`, `workspace.md`, task record, and revision manifest. Fill unknowns explicitly rather than inventing teacher inputs. Bind each task to exact source/output hashes and feedback IDs.

For the operator rehearsal, label the request synthetic. For the teacher trial, replace it with the teacher's actual request and device/input requirements. Freeze an immutable usable baseline and distinguish candidate from accepted/exported versions.

Done when: another operator can locate the selected resource, constraints, current request, open feedback, and usable output using those files alone.

### 3. Rehearse one authoring loop before the provider ring

Run the proposed directions/explanation adaptation with one agent and one operator. Observe creation -> built preview -> anchored feedback -> revision -> acceptance record -> export. Complete the remaining source-conflict, interruption, duplicate-delivery, and export-content checks on disposable data.

Do not simulate teacher approval by relabeling the earlier fixture comment. An operator can accept a rehearsal artifact as a test result; teacher acceptance is a later event with a named reviewer and exact artifact revision.

Done when: the operator loop and recovery checks pass with no lost edits or version ambiguity, and all assistance/steps are logged.

### 4. Test provider continuity separately

First validate native launch, root resolution, permissions, and a bounded read-only acknowledgment for each provider. This includes AGY on Windows. Then perform the design's Codex -> Claude -> agy -> Codex sequence, with one editor at a time and explicit termination/ownership transfer.

Do not install a framework or alter shared terminal behavior to conceal a failed launch. Record blocked provider legs separately. Capability metadata and CLI help cannot substitute for observed task performance.

Done when: each provider receives and hands off a bounded revision using only the portable packet, with saved work preserved and output checks recorded. No claim about all provider pairs or equal educational quality.

### 5. Enter the teacher session only after readiness checks

Required inputs: teacher's actual lesson need; authoring and classroom device/browser/input setup; selected scientific reviewer; and available session time. Select 3-D instead if the actual goal requires transfer between flowers, then extend prerequisite tests accordingly.

Before the teacher session, complete the design's entry checks (T0, T2, T4–T10) for the baseline and selected path, including human science/alignment review. The targeted subsets above do not satisfy those entire checks. Then apply the observation rules and 60-minute feasibility limit, keeping teacher-owned decisions, operator assistance, resource correctness, and provider compatibility separate. Review the teacher-adapted artifact again for science and required behavior before classroom use.

## Insight and open questions

**Insight — measurement validity:** a tool event named “human” or an agent status named “done” describes a software event, not who actually participated or whether the lesson is usable. Record the actor and artifact separately from the software's status.

**Open questions:** the real teacher request/device, full source-edit conflict behavior, running-agent termination, AGY authentication/path mapping, human science acceptance, and whether two surfaces are understandable to an assisted teacher remain unverified.

## Audit and session close

The cold audit found three actionable issues, corrected here: baseline science review had slipped past the teacher-trial entry gate; nectar was conditional in scope but mandatory in the completion criterion; and the original design's historical unknowns read as current. Baseline readiness now precedes the teacher session, nectar follows the recorded task, and the design explicitly dates its earlier evidence.

Both temporary servers were stopped, their browser tabs closed, and the standalone baseline file tab retained with normal networking restored. Local feedback, source snapshots, and export remain available. No original module or shared-tool source was changed, no dependency installed, and no commit/push performed.
