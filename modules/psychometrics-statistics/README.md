# Doctoral psychometrics and statistics stress test

Status: prepared test specification. No student lesson or numerical reference
implementation has been generated. Peter requested PhD-level psychometrics and
statistics; measurement invariance and simulation are a proposed first case.

## Teacher-builder brief

Build a doctoral methods module in which a researcher must defend a comparison
between two groups using a measurement model. Require model specification,
identification reasoning, simulation design, analysis, and a written defense.
Let the learner investigate a deliberately misspecified case and revise the claim.
The intellectual task should survive a change of dataset, parameters or group labels.

Assumed prerequisites: graduate regression, probability, likelihood, matrix
notation and introductory latent-variable modeling. Confirm these with the teacher
when authoring. Duration, software language and exact syllabus remain open.
The lesson must state its chosen model and assumptions before showing results.

## Inputs the builder should organize

- Curriculum: a selected syllabus or explicitly provisional course objectives.
- Content: authoritative methodological sources read in full enough to support
  the chosen model, constraints, estimator and interpretation.
- Standards: course outcomes where appropriate; do not invent a K-12 standard or
  treat a professional guideline as a jurisdictional curriculum mandate.
- Preferences: mathematical depth, reproducibility, keyboard operation, offline
  artifact, separate teacher rationale. Shared defaults remain visible.
- Tools: the same learning-authoring workflow, Learnability Patterns, research
  retrieval and interface skill as science modules. Add a numerical tool skill
  only after locating and registering its actual canonical source.
- Assets: tables, diagrams and simulated data selected for this task. No elementary
  illustrations or large source collections are injected merely because available.

## Stress-test request

> Design a doctoral psychometrics/statistics lesson about defending a cross-group
> comparison under a latent-variable measurement model. Start by choosing and
> justifying a tractable model and its identification constraints. Require learners
> to design a seeded simulation, inspect recovery and uncertainty, diagnose a
> misspecified case, and revise their conclusion. Include a wrong-reasoning path
> and a changed-context task. Preserve equations and assumptions. Retrieve and
> inspect methodological sources and learning-design evidence; distinguish those
> two kinds of support. Give me the design and validation plan before building.

## Evaluation record to complete during the run

| Test | Evidence required | Current result |
|---|---|---|
| Shared engine reuse | Actual pattern/skill receipts, expanded research, source-to-decision links | Not run |
| Doctoral demand | Model specification, identification argument, critique and transfer response | Not run |
| Mathematical correctness | Independent calculation or trusted reference implementation; defined tolerances | Not run |
| Simulation validity | Seed, generating parameters, estimator, replications, failures, uncertainty and recovery summaries | Not run |
| Failure transparency | Nonconvergence, unidentified or incompatible input handled explicitly | Not run |
| Pedagogical depth | Wrong reasoning receives explanatory feedback; changed case requires a new argument | Not run |
| Usability | Keyboard, reset, equations, readable tables and accessible alternatives to plots | Not run |
| Preferences | A teacher revision changes the requested setting without losing mathematical demands | Not run |
| Transfer of authoring workflow | Record reused versus newly written code/assets and assistance time | Not run |

A seeded animation alone does not satisfy the simulation test. A working numerical
demo alone does not satisfy the learning test. The current publisher checks HTML,
JavaScript syntax and source records; it cannot establish either conclusion.

Launch a separate workspace with `./authoring/start.ps1 -Module psychometrics-statistics`
from the repository root. Its context snapshot includes this brief. The launcher
does not automatically start the stress-test request or rewrite existing workspaces.
