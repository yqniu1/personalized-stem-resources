# Personalized STEM Resources

A speculative prototype for an AI authoring tool that helps teachers talk a curriculum-aligned STEM resource into existence.

I want teachers to describe what their class needs, see a working preview, and refine it through conversation. Learning-design patterns would guide the choices behind the resource, while prebuilt tools would supply interactions such as exploration, sorting, and modeling. The teacher would decide what to use in the classroom.

This repository contains **Lily Dissection**, a local authoring workbench, a shared resource registry, and a module catalog. The catalog also locates earlier science experiments and a proposed doctoral psychometrics/statistics stress test. The 2027 Tools Competition proposal describes the broader product direction.

## Start here

For lesson design and management, start with [the module catalog guide](modules/README.md)
and [shared authoring resources](shared/README.md). The builder uses the same learning
engine across subjects; each module supplies curriculum, objectives, standards and preferences.

```powershell
python authoring/catalog.py list
python authoring/catalog.py list --subject science
python authoring/catalog.py list --standard 4-LS1-1
.\authoring\start.ps1 -Module psychometrics-statistics
```

The last command opens a separate workspace for the [doctoral stress-test brief](modules/psychometrics-statistics/README.md).
It does not start generation automatically. The brief is prepared; an advanced lesson has not yet been generated or evaluated.

Open [index.html](index.html) in a browser for an illustrated overview, or go directly to the [Lily module](modules/lily-dissection/index.html). The module opens from disk in 3-D, with a 2-D option and automatic fallback. It needs no installation or internet connection.

- [Prototype walkthrough](docs/tools-competition-2027-activity-teardown.md): screenshots, design choices, and the work ahead.
- [Competition proposal](docs/tools-competition-2027-proposal.md): the Phase I draft for Strengthening Teaching, Catalyst level.
- [Module source and build instructions](modules/lily-dissection/README.md).

![Lily Dissection: learners separate flower structures and explore their functions](docs/images/lily-disassembled.png)

## What the prototype tells us

I built the initial Lily application for a teacher's need in under four hours, using conversational AI, agentic workflows, and a rudimentary Learnability Patterns knowledge source. That is my account of the initial build; the current module includes later refinements.

The useful starting point is the authoring process: a teacher's lesson and constraints shaped a small, working application. Lily currently has one user. Three teachers are providing feedback on the broader work.

The next step is to make this process usable by teachers themselves. This repo contains a working instructional resource and an early local authoring workbench for Peter's tests. Independent teacher use and a reusable instructional tool library remain proposed development.

## The proposed authoring process

![Proposed workflow: a teacher's lesson need, learning patterns and tools, build and review, then a classroom resource; classroom feedback informs revision](docs/images/authoring-workflow.svg)

"Personalized" means fitted to the teacher's learning goal, lesson, students, and practical constraints. A resource might need a simpler explanation, a different interaction, or an offline format. Individual student adaptation would require additional development and evaluation.

In Lily, the lesson goal led to a focus on how structures work together in pollination. A task sequence, visible pollen route, and explanations give concrete examples of guidance the pattern source can inform. These are design choices to investigate, rather than established evidence of learning gains.

## What Catalyst would support

The funding would support a teacher-facing authoring experience, a stronger learning-pattern knowledge source, a small collection of reusable STEM tools, and a structured pilot. We would measure total preparation and revision time, developer assistance, scientific accuracy, curriculum fit, and classroom usability. Student explanations would help us examine whether the interactions support the intended concepts.

The main question is whether teachers can independently create useful resources with this workflow, and how it compares with general-purpose AI on the same lesson requests.

## Authoring canvas

The [local authoring workbench](authoring/README.md) now connects a lesson workspace to niu-prototyper's live canvas and Codex terminal. On Peter's Windows machine, run:

```powershell
.\authoring\start.ps1
```

Enter a request in the terminal; the agent can read local materials, generate a standalone HTML lesson, save a revision/export, and refresh the canvas. One actual Codex creation/revision loop has been tested, including a Windows material path and selected offline keyboard interactions. See the [build plan and evidence](docs/plan-local-authoring-test.md). This is ready for Peter's operator test; it does not establish independent teacher usability or classroom readiness.

The [first authoring workflow design](docs/design-authoring-workflow.md) scopes an assisted teacher trial, a portable agent handoff, and tests for review, recovery, and export. Peter confirmed the assisted-teacher population; the proposed Lily adaptation still needs a participating teacher's actual request. This is a design, not an implemented authoring service.

The [rehearsal findings and next steps](docs/plan-authoring-rehearsal.md) record targeted checks of the existing tools. The selected 2-D keyboard path needs work before a teacher trial; teacher usability and agent interchangeability remain untested.

A [portable authoring packet experiment](docs/authoring-packet-contract.md) now records a synthetic operator loop through two revisions and an export. It separates task state, artifact identity, operator review, and teacher approval; it is a manual protocol rather than an integrated authoring service.

The intended starting point is Peter's existing local tooling:

| Existing tool | Role in the authoring prototype |
|---|---|
| Document Canvas | Edit lesson briefs and supporting documents, review assets, and exchange comments with the agent |
| niu-prototyper | Preview the running interactive resource and attach feedback to interface elements |
| The active coding agent | Create and revise resource source files using the lesson context and teacher-builder's requests |

The first implemented connection uses the existing agent terminal and niu-prototyper, plus a small file-based publication helper. Document Canvas's editable brief surface remains a separate tool; its HTML preview disables scripts. A unified teacher-facing conversation interface and the level of specialist assistance teachers need remain questions to investigate.

### Interchangeable agent layer

Agent interchangeability is a design requirement to validate during prototyping. Codex, Claude Code, and Antigravity (agy) are the prototype agents. The teacher workspace, lesson context, resource files, and review history should remain usable when the agent changes. Provider-specific launch and session handling belong behind adapters; an identical terminal surface alone does not establish equivalent behavior or portable conversation state.

A future custom agent could use a model fine-tuned on educational data, together with the tools and orchestration needed to build and revise resources. This is an option for later scale, not a prerequisite for the current prototype. The shared contract should describe how an agent receives requests and workspace context, uses tools, reports progress and failures, and submits reviewable changes. Its exact interface remains to be designed. Educational quality and coding reliability must be evaluated for each implementation; satisfying the interface does not establish equal quality.

## Repository layout

```text
index.html                 Illustrated project overview
docs/                      Proposal and prototype walkthrough
authoring/                 Local workspace helper, launcher, and tests
shared/                    Shared engine, assets, skills, curriculum and defaults
references/                Supplied reference inputs (including local MCAS image)
source-assets/             Local original collections and transfer manifests; ignored
modules/
  catalog.json             Subject/standard metadata and actual lesson locations
  lily-dissection/         First working module, assets, sources, and builds
  psychometrics-statistics/ Doctoral stress-test brief; no generated lesson yet
```

Each module keeps its lesson-specific source and assets together. The Lily HTML files are generated from templates; edit the module source and rebuild them. Adding another module does not require changing Lily's implementation. See [module conventions](modules/README.md).

Science experiments in the external disposable workspace are cataloged by their
actual state. Tiger is the last observed current lesson; pollen, circuits and Shadow
Detective have retrospective records after resets. They are not silently reconstructed
or presented as packaged modules. See [documentation navigation](docs/README.md)
for current guides versus historical tests and proposals.

## Attribution and publication status

The prototype was built with AI assistance. The documentation describes both the working resource and the planned authoring tool. Lily is an independent supplement informed by OpenSciEd Grade 4 Unit 4.4, Lesson 13; it has no OpenSciEd endorsement.

See [third-party notices](THIRD_PARTY_NOTICES.md) for curriculum and software credits. The 3-D illustration uses a purchased model under a separate commercial license. This review repository starts with fresh history and excludes private source inputs. A project-wide open-source license has not been selected.
