# Local lesson authoring

An operator prototype using niu-prototyper's live canvas and native Codex terminal.
The helper in this folder saves requests and revisions; the native agent reads materials
and writes the lesson. There is no hosted model service.

User guide in Coda: [STEM Authoring — Design Session Guide](https://coda.io/d/_dwSwpTJ8Z-E).
It covers lesson design, separate workspaces, revisions, exports, and resuming tool development.

## Start on Peter's Windows machine

In PowerShell:

```powershell
Set-Location 'C:\Users\pniu\Projects\personalized-stem-resources'
.\authoring\start.ps1
```

Requires the existing WSL install of Node, Python 3, tmux, signed-in Codex, and
`C:\Users\pniu\Projects\niu-prototyper` with its dependencies installed.
`-Prototyper` overrides that checkout. No packages are installed by the launcher.

## Choose a subject/module

```powershell
python authoring/catalog.py list --subject science
python authoring/catalog.py list --standard 4-LS1-1
python authoring/catalog.py show psychometrics-statistics
.\authoring\start.ps1 -Module psychometrics-statistics
```

`-Module ID` uses `%LOCALAPPDATA%/STEMAuthoring/modules/ID` by default. Add
`-Workspace PATH` for a separate class or variant. With no module argument, the
existing `grounded-workspace` behavior is preserved. The catalog does not move the
older disposable lessons into new workspaces or begin a lesson automatically.

New workspaces snapshot the selected module, resolved shared resources, brief and
preferences in `materials/module-context.json`. The native author reads that context.
Shared defaults yield to module preferences and then explicit teacher requests.
The helper refuses switching a workspace to a different module or retrofitting an
unbound workspace. Reopening retains its original snapshot, tools and knowledge
paths; use a new workspace to adopt registry changes.

See [module conventions](../modules/README.md) and the [shared registry](../shared/README.md).
The doctoral entry is a prepared stress-test specification, not an evaluated lesson.

## Author a lesson

The canvas opens with a terminal drawer. Choose **lesson-author** under
**Start an agent** if an agent is not already running. Enter a lesson request in
the terminal and press Enter. For example:

> Make a 10-minute grade 4 lesson about how anther and stigma help transfer pollen.
> Include a keyboard interaction, a reset, and an explanation question. Keep it offline.

The agent reads local materials, selects Learnability Patterns, retrieves expanded
research passages from niu-library, and prepares a source-linked design before
writing the lesson. It consults frontend-design for interface choices. Publication
saves the rationale and lesson, then reloads the canvas. Ask for revisions in the same terminal. Inspect comments can also be
sent to the running agent through the existing canvas review controls.

The default workspace is `%LOCALAPPDATA%\STEMAuthoring\grounded-workspace`. The earlier
`lesson-workspace` is preserved as an ungrounded demo and cannot be silently upgraded. Use
`-Workspace C:\path\to\workspace` for another workspace. Reopening preserves files
and reconnects to the existing terminal; it does not launch a second agent.
Windows paths supplied in prompts are converted with `wslpath` inside WSL.

## Disposable test lessons

In an idle lesson workspace, explicitly enable destructive reset once:

```sh
python3 tools/lesson.py make-disposable
```

Enabling this deletes nothing, but makes **all** managed lessons in that workspace
eligible for reset, including earlier revisions and exports. It is for operator tests.
In the authoring terminal, ask: **Destroy the disposable lessons and reset.**
The equivalent commands are:

```sh
python3 tools/lesson.py reset           # inspect exact targets; deletes nothing
python3 tools/lesson.py reset --destroy # permanently delete generated lesson files
```

Reset removes `src/`, `preview/`, `tasks/`, `revisions/`, `exports/`, `evidence/`,
root design/request files, and on-disk canvas snapshots/overlays, then restores a
neutral start page and requests a canvas reload. Generated scripts/assets belong
under `src/` so they are covered. Materials, tools, knowledge configuration,
instructions, `RETRO.md`, comments/logs and chat history remain. Outside downloads
and browser memory are not erased. This is not a privacy wipe.

An ordinary workspace, active task, pending publication, or linked deletion target
is refused. Finish/recover or explicitly abandon a task before reset. Other writers
must be idle; the helper lock does not control the canvas or arbitrary editors.
After interrupted deletion, retry `reset --destroy`; new authoring remains blocked
until reset finishes. A failed canvas refresh is reported separately from disk deletion.
No extra packages or shared canvas-engine changes are required.

## Resume authoring-tool design

To work on the tool itself, run `codex` from this repository root and ask it to read
`HANDOFF.md`, `docs/authoring-workflow-session-brief.md`,
`docs/design-authoring-workflow.md`, and `docs/plan-grounded-authoring.md`.
State the design question and request tests before implementation. The repository
agent owns tool development; the canvas agent owns the external lesson workspace.
For a design-only lesson conversation in the canvas, explicitly ask for the learning
goal, evidence of understanding, source-backed activities, and tests before implementation.

## Files and authority

| Path in workspace | Purpose |
|---|---|
| `materials/` | Local references, including a copy of Lily 2-D |
| `materials/module-context.json` | Selected module and shared context snapshot, when launched with `-Module` |
| `request.txt` | Latest request; each task retains its original request |
| `src/lesson.html` | Editable, self-contained lesson source |
| `knowledge.json` | Canonical pattern and skill locations; no credentials |
| `design.json` | Task-bound objective, assessment, standards status, source interpretations and decisions |
| `evidence/` | Captured local pattern/skill bytes, paths and SHA256 receipts |
| `preview/index.html` | Current canvas artifact; only this directory is served |
| `preview/design.html` | Teacher-facing rationale, distinct from student directions |
| `tasks/` | Requests, base versions, status |
| `revisions/r-*/` | Published HTML, preceding preview, design, source receipts and manifest |
| `exports/r-*.html` | Standalone copy of each published version |
| `exports/r-*.design.html`, `exports/r-*.design.json` | Matching teacher rationale |
| `workspace.json` | Current task and revision pointers |

Only Lily and the legacy default initialization receive the Lily reference copy.
Other module references retain their extension as `materials/module-reference.EXT`.
Module context is also retained in each publication's revision snapshot.
The original Lily module is not the editing target. Published means available for
review, not teacher approved. `teacher_accepted_revision` remains null.

The helper checks HTML structure, inline JavaScript syntax, task/base consistency,
local source receipts, and decision references. Research interpretations are agent-written;
schema validation does not authenticate remote retrieval. The operator test independently
inspects native tool traces and source support. Standards are marked unverified or candidate.
The helper does not prove
scientific accuracy, browser behavior, accessibility, or offline completeness.
The agent runs with Codex workspace-write sandboxing and network access for the
canvas reload. Native approval prompts may appear for actions outside that boundary.
Workspace instructions guide the agent; they are not filesystem access controls.

The helper's `canvas reload|read|inbox|claim|reply|finish` commands use the existing
prototyper HTTP contract with project/workspace identity checks and its normal
cookie, origin, and token authentication. This avoids the native CLI's process-ID
probe, which fails inside the Codex sandbox even when the server is alive.
No shared prototyper or Document Canvas code is modified.

## Knowledge setup on this machine

The launcher resolves canonical locations from `shared/resources.json` on first creation.
Canonical patterns are read from `C:\Users\pniu\Projects\website\personal\src\content\patterns`.
The reusable skill is `C:\Users\pniu\Projects\skills\learning-authoring\SKILL.md`.
Windows Codex and WSL Codex link to that same skill; WSL also links to the existing
Windows frontend-design skill. No whole-repository knowledge copy is maintained.

WSL Codex has the selected niu-library HTTP connection from the existing Windows Codex
configuration, including its existing approvals for the read-only `search_docs` and
`retrieve_parent` tools. Credentials stay in the private Codex configuration, outside
the workspace and exports. Other parent connectors are not inherited or copied.
Changing MCP configuration requires restarting the native agent. If retrieval fails,
the agent preserves the draft and reports the gap rather than publishing a grounded claim.

Source capture: `python3 tools/lesson.py source --kind pattern --path PATH`
(or `--kind skill` for frontend-design and registered available tool skills).
`knowledge.json` supplies the explicit tool-skill allowlist; unconfigured paths are refused.
The HTML publisher still requires frontend-design as well as a pattern receipt.
Blender is registered as unavailable until its canonical skill is supplied.
Fill `design.json` using `design.example.json`,
then run `python3 tools/lesson.py design --task ID` before editing and publishing.
For revisions, retain relevant evidence but bind the design to the new task and base.

## Recovery

Press **Esc** to interrupt a Codex turn. Ending the CLI uses its normal Ctrl+C/exit
controls. Closing a tab/drawer or stopping the preview server does not stop an agent.

After interruption, inspect `python3 tools/lesson.py status` in the workspace:

- An active task can continue with its existing ID, or be explicitly abandoned
  with `abandon --task ID`. Source remains on disk.
- If `publish-pending.json` exists, stop the editor and run
  `python3 tools/lesson.py recover`. It checks the retained previous HTML, candidate,
  export, design/source snapshot hashes, and current preview before completing publication. Both versions remain.
- If a killed helper left `.lesson-lock`, first verify that helper is no longer
  running, then remove that empty lock directory and recover.
- A snapshot written before the recovery record may remain after a crash. It is
  never overwritten. Preserve it; abandon that task and begin a new task.
- If an external edit conflicts with recovery, the helper refuses to replace it.
  Preserve and reconcile the files manually. There is no automatic merge.

These checks coordinate helper users; they do not prevent an external editor or agent
from writing files directly. Only one editing agent should work in a workspace.

## Development checks

```sh
cd authoring
python3 -m unittest -v test_catalog.py test_lesson.py
```

Node must be on PATH for JavaScript syntax checks. Runtime workspaces are outside
the repository and are not committed. The launcher copies the helper on first
initialization; existing workspaces are not silently upgraded while agents run.
