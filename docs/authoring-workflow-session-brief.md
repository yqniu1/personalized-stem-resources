# Authoring canvas: scope, design, and test session

Date: 2026-10-20\
Source: Peter and Codex scope discussion\
Status: Preparation for Design; not an approved implementation specification

Follow-through, 2026-10-20: [authoring workflow design](design-authoring-workflow.md). Peter selected a teacher with Peter assisting as the first population, preceded by a Peter-only rehearsal. The design records the proposed lesson scenario, integration boundary, tests, and remaining gates. This brief remains the original scope record.

## Agreed direction

Expand Personalized STEM Resources along two connected directions:

1. Student-facing instructional resources, starting with the existing Lily module.
2. An authoring canvas where a teacher-builder manages workspace materials, creates through conversation, previews resources, and requests revisions.

Use Peter's existing stack as the starting point. The coding-agent layer must be interchangeable: Codex, Claude Code, and Antigravity (agy) in the prototype, with the possibility of a custom agent using an education-fine-tuned model later. Fine-tuning is not current scope.

Peter clarified that substantive competition materials are not expected until November and the initial writeup does not require content. This session is about product/workflow design, not application deadlines.

## Verified starting point

- One Lily module; standalone 2-D, standalone 3-D, and a merged launcher. Generated HTML comes from `modules/lily-dissection/src/`; edit source and rebuild.
- Source and documentation separate a working resource from a proposed teacher-authoring service. No shared authoring runtime exists in this repository.
- This session inspected rendering over localhost. Interactive testing, direct-file/offline checks, and rebuild verification were not completed afresh.
- Document Canvas: editable documents, asset review, feedback queues, revision handling, and an agent terminal. Its HTML preview disables scripts.
- niu-prototyper: running application preview, element-anchored comments, agent terminal, and source-edit/reload workflow.
- These two tools have documented capabilities; their combined workflow for this project and suitability for teachers have not been tested.

Read these before designing changes to the shared tools:

- `C:/Users/pniu/Projects/document-canvas/AGENTS.md`, `HANDOFF.md`, `SKILL.md`, and `README.md`.
- `C:/Users/pniu/Projects/niu-prototyper/AGENTS.md`, `HANDOFF.md`, `SKILL.md`, and `docs/design.md`.

Document Canvas owns shared terminal behavior; niu-prototyper consumes locked copies/ports. Preserve that ownership. Both use WSL for the runtime on Windows. Keep lesson-specific assets and instructions in this project. Do not expose the local terminal services as hosted teacher software.

## First decisions for the session

Follow the workflow's Design sequence: problem, pre-mortem, measurable completion criteria, and explicit unknowns. Infer mode and perform checkpoints without unnecessary approval pauses.

1. **Who is the first teacher-builder?** Peter, an independently operating teacher, or a teacher working with specialist assistance? Distinguish those evaluation populations.
2. **What is the first complete task?** Creating a new resource, adapting Lily, or revising an existing lesson? Choose one real request and define the instructional purpose.
3. **What does workspace management include initially?** Decide the minimum materials, resource selection, versions, and export behavior. Do not assume a full file manager or multi-user service.
4. **What does conversation look like initially?** Determine whether the existing terminal supports the experiment or a teacher-facing chat surface is necessary.
5. **What survives an agent change?** Define the authoritative lesson brief, artifacts, revision history, task state, and portable handoff. Do not assume vendor chat histories can transfer.
6. **What is the smallest integration?** Compare connecting existing surfaces with adding a shared shell. Inspect the tools before committing to either.

## Candidate authoring loop

This is a discussion aid, not a settled screen design:

Select lesson/workspace -> establish goal and constraints -> create or revise through conversation -> inspect the running resource -> give contextual feedback -> review the revision -> retain/export a usable version.

Keep instructional judgment visible: what students should learn, what actions support it, and what explanation would demonstrate understanding.

## Agent boundary to design

Specify only what the first loop needs:

- Request and context inputs.
- Workspace/tool access and responsibility for applying changes.
- Progress, failure, and completion signals.
- Artifact/revision references and review feedback.
- Cancellation, interrupted work, and handoff to another agent.

Separate interface compatibility from educational quality and coding reliability. A future fine-tuned model would still need tools, orchestration, and evaluation. Reuse provider-published interfaces at vendor boundaries; do not build a general agent framework solely to claim interchangeability.

## Proposed tests and evidence

Choose pass criteria and participants during Design; none of these tests has run.

| Question | Candidate test | Evidence to retain |
|---|---|---|
| Can the authoring loop complete? | Perform one real lesson request through preview, feedback, revision, and export | Task outcome, total time, failed attempts, assistance, usable artifact |
| Does workspace context persist? | Reopen the workspace and locate the brief, selected resource, and reviewed revision | Context retained/lost; recovery steps |
| Can agents be exchanged? | Have a second supported agent continue a bounded revision from explicit workspace state; eventually cover all three prototype agents | Manual context reconstruction, changes preserved, provider-specific gaps |
| Are edits recoverable? | Interrupt a revision and introduce a concurrent human edit in disposable test data | Conflict behavior, preserved work, recovery to a known usable version |
| Does preview match the deliverable? | Exercise the exported resource separately from the authoring canvas | Behavior, asset loading, errors, offline operation where required |
| Can intended users operate it? | Observe target teacher-builders on their actual device/input setup | Assistance, keyboard/touch barriers, misunderstood controls |
| Is the resource instructionally defensible? | Review scientific claims and collect a targeted student explanation/model where feasible | Accuracy issues, alignment, misconceptions; separate action completion from understanding |
| Does pattern guidance add value? | If making that claim, compare matched tasks with a reasonable general-purpose AI baseline | Quality ratings and full production/review cost; otherwise label findings exploratory |

Automated checks suit interface behavior, artifact integrity, conflict handling, and exports. Human review is needed for instructional accuracy and usability; student evidence is needed for learning claims.

## Known risks and open hypotheses

- A smooth authoring demo may depend on Peter's expertise. Measure assistance rather than assuming independent use is the only valuable outcome.
- Existing tool capabilities may not combine into a coherent workspace without additional design.
- Changing agents may preserve files while losing task rationale or review context.
- More modules may demonstrate breadth without establishing reusable production or instructional value. An adjacent module, a different interaction type, and deeper Lily use are candidate experiments, not a committed sequence.
- Lily's 2-D and 3-D views represent different pollen-transfer cases; keyboard support and scientific feedback also differ. Decide which corrections are prerequisites for the chosen experiment.
- The number of users, initial build time, and contribution of learning patterns have only the evidence described in the repository. Do not turn them into validated efficiency or learning claims.

## Expected outputs

Produce a scoped problem statement, smallest end-to-end scenario, ownership/integration sketch, minimal agent contract, test matrix with explicit pass criteria, and accepted unknowns. Run the bias audit, then write the design under `docs/` and refresh root `HANDOFF.md`. Build planning follows that design.

Suggested session opener:

> Read HANDOFF.md and docs/authoring-workflow-session-brief.md. Start a Design workflow for the teacher-builder authoring canvas using Document Canvas, niu-prototyper, and interchangeable coding agents. Establish the first user scenario, inspect integration boundaries, and define observable success and failure tests before implementation. Preserve the agreed scope and treat the proposed experiments as options.
