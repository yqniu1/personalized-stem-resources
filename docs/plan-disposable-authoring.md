# Disposable lesson tests

2026-10-21. User requests disposable test lessons, an explicit destructive reset, and 20 non-circuit ideas. This extends the local authoring helper, not the shared canvas engine.

The already-open operator workspace can be explicitly marked disposable without deleting its contents. Reset must be a separate user-invoked action. It removes managed generated source, previews, tasks, revisions, exports, evidence and design/request files, plus canvas snapshots/overlays. It retains materials, tools, knowledge configuration, instructions, retrospectives, comments and chat history. It is not a privacy wipe and cannot remove downloaded copies outside the workspace.

One editing owner performs reset while no lesson task or publication is active. All deletion paths are fixed and preflighted within the resolved workspace; symbolic links and Windows reparse points are rejected. A reset-in-progress marker blocks new authoring after partial failure and permits retry. Existing ordinary workspaces reject reset.

Work units, sequential owner Codex:
1. Helper commands and tests (medium confidence): explicit marking, reset scope, path boundary, busy/failure refusal, retry and subsequent publication.
2. Workspace installation and documentation (medium): keep existing instructions/retro additions, load reset instructions in native agent, verify idle state and no lesson loss on marking.
3. Prompt ideas and read-only bias audit: 20 original non-circuit activity ideas; no claims of learning effectiveness or existing asset coverage.

Done: marked workspace retains current revision, dry-run lists exact reset targets, real reset passes in disposable fixtures, ordinary/material/outside paths remain untouched, native session understands reset and is ready for a new subject. No destruction of current user lessons occurs during setup.

## Verification

Implemented in authoring/lesson.py and documented in authoring/README.md. `python -m unittest -v test_lesson.py`: 27 passed on Windows, including real junctions and linked parents. Seven reset cases cover ordinary/busy refusal, scoped deletion, dry-run, retained inputs, retry after partial failure, UI-refresh failure reporting and new publication from a neutral base.

Updated the already-open grounded-workspace helper while its native author was stopped. Enabling disposable mode retained all 90 generated file hashes and revision r-bb254b8f05c3. Live dry-run succeeded; current user artifacts have not been destroyed. The shared canvas engine was not changed. Reset erases on-disk snapshots/overlays but does not promise erasure of server/browser memory or conversation history. The automatic reload request is tested through the existing HTTP contract; live destructive reset remains for the user's explicit reset action.

Bias audit found no blocking code defect. Corrections made: whole-history scope is explicit, reset holds the helper lock, failed reload is separate from successful disk destruction, and actual Windows junction coverage was added.

Integration review found the shared canvas watches its overlay directory. Reset now empties all generated directories while retaining their directory identities; a fixture asserts the overlay inode stays the same. All 27 tests passed again after this correction.
