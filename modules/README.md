# Lesson modules

[catalog.json](catalog.json) is the local teacher-builder index. Every module uses
the [shared resource registry](../shared/README.md). Subjects and standards are tags
with explicit status, so a module can appear in several subject views without copies.

| Module | Subjects / level | Actual state |
|---|---|---|
| [Lily Dissection](lily-dissection/README.md) | Science, biology / Grade 4 | Packaged HTML, assets and build sources; NGSS 4-LS1-1 candidate alignment |
| Tiger structure teamwork | Science, biology / Grade 4 | Last observed current lesson in external disposable workspace; no supplied exact standard |
| Two-flower pollen route | Science, biology / Grade 4 | Retrospective after reset |
| Close the loop | Science, physics / Grade 4 | Retrospective after reset |
| Shadow Detective | Science, physics / assumed Grade 4 | Retrospective including language-support revision, after reset |
| [Psychometrics/statistics](psychometrics-statistics/README.md) | Psychometrics, statistics / doctoral | Proposed measurement-invariance and simulation stress-test brief |

The workspace observations above are dated 2026-10-24; catalog entries do not poll
live runtime state. Check that workspace's `workspace.json` before resuming work.
Historical entries locate notes, not runnable lessons. Teacher acceptance is separate
from publication. Empty standards lists mean no standard supplied, not no relevant standard.

## Find and design

From the repository root:

```powershell
python authoring/catalog.py list --subject science
python authoring/catalog.py list --standard 4-LS1-1
python authoring/catalog.py list --level doctoral
python authoring/catalog.py show psychometrics-statistics
python authoring/catalog.py check
.\authoring\start.ps1 -Module psychometrics-statistics
```

`show` resolves references and merges preferences into inspectable JSON. `check`
validates catalog records and required engine resources, reporting unavailable optional
libraries separately. These commands do not inspect or certify curriculum coverage.
The launcher creates a module workspace under `%LOCALAPPDATA%/STEMAuthoring/modules/ID`.
Use `-Workspace PATH` to keep separate class/teacher variations of the same module.
Existing workspaces keep their context snapshot and cannot switch module identity.

## Add or manage a module

1. Add a stable kebab-case ID to `catalog.json`, with title, subjects, level, objectives,
   curriculum, standards, preferences, resources and location. Follow an existing record.
2. For a packaged/planned module, keep its README, source and assets together under
   `modules/ID/`. For an external experiment, record the real location and status.
3. Reference shared resource IDs. Keep tool instructions at their canonical skill
   location; register new tools in `shared/resources.json`. Do not copy a skill per subject.
4. Record each standard's framework/code, candidate or unverified status, authority URL
   when known, local evidence path when available, and the scope of the claim. Course
   outcomes can live in the brief without inventing a national standard.
5. Run `python authoring/catalog.py check` and inspect `show ID`, then launch with `-Module ID`.
   Set teacher/class preferences in the module record or give explicit overrides in chat.

Keep source collection manifests and packaged artifact paths stable. Generated classroom
HTML comes from editable source; do not hand-edit Lily outputs. Add a module to the
root `index.html` showcase only when it has a working example. This local catalog is
implemented; a hosted school library and teacher-facing catalog UI remain future work.
