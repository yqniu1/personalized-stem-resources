# Module and resource organization

Date: 2026-10-24. Scope: directory cleanup and a local teacher-builder context layer.

## Problem

Lily is packaged in the repository, experiments live in a disposable external
workspace, and local source collections have no common entry point. The builder
needs subject/standard discovery and common learning-engine, asset and tool
resources while keeping curriculum and teacher choices specific to each module.

## Failure scenarios

- Moving Lily or workspace files breaks builds, canvas identity or feedback.
  Keep their paths; catalog them. Rename only the unused `refereces` input folder
  after checking references and preserving its bytes.
- A standard tag is mistaken for verified coverage. Store candidate/unverified
  status and the evidence path; filtering is discovery, not certification.
- Doctoral work inherits elementary objectives or a Lily reference. Select a
  module explicitly, use a separate workspace, and seed only its own references.
- Shared resources become diverging copies. Keep one registry of canonical
  locations; capture a context snapshot at workspace creation. Existing workspaces
  retain their snapshots; no implicit migration or refresh.

## Definition of done

- `python authoring/catalog.py check` validates IDs, references and module records.
- `list --subject science`, `list --standard 4-LS1-1` and `show
  psychometrics-statistics` return the intended entries and explicit statuses.
- Launcher accepts `-Module ID`, chooses a separate default workspace, and provides
  module context to the native author. Reopening cannot change a workspace's module.
- Tests exercise filters, unknown IDs, preference precedence, missing required
  resources, cross-module reopen refusal, and doctoral initialization without Lily.
- Existing helper tests pass; preservation hashes confirm existing Lily files and
  the moved MCAS image are byte-identical. External workspaces are read-only here.

## Unknowns

- Measurement invariance and simulation are an initial proposed doctoral test case;
  Peter has specified the level/domain, not a syllabus or exact topic.
- Exact MCAS authority/standard remains unresolved. No code is inferred from the image.
- Blender is a requested tool-skill category; no canonical Blender skill was found
  in the searched skills checkout. Existing Lily scripts are assets, not a skill.
- Runtime publication still produces standalone HTML with existing source receipts.
  Executable R/Python notebooks, specialist numerical validation, school sharing and
  a teacher-facing catalog UI are outside this cleanup's implementation.

## Contract

`shared/resources.json` registers the shared learning engine, asset libraries,
tool skills, curriculum collections, standards references and default preferences.
`modules/catalog.json` contains stable module IDs, multi-valued subjects, level,
objectives, curriculum and resource references, standards status, teacher preferences,
and actual artifact/history locations. Module files stay in stable existing paths.
The catalog resolves paths locally and produces an inspectable context packet.
The launcher places that snapshot in `materials/module-context.json` on first creation.
Module preferences override shared defaults; a teacher's current explicit request
overrides defaults during authoring and must be recorded in the task/design.

Historical experiments are catalog records, not reconstructed lessons. Source
archives keep their original hierarchy and transfer manifests. The repository stores
code-bound resource configuration; Coda remains the home for the personal knowledge
library and captured teacher feedback. No new wiki or copied skill library is created.

## Work units

| Unit | Files | Confidence | Verification |
|---|---|---|---|
| Preserve and organize | references/, shared/, modules/catalog.json, module brief | High | Paths, hashes, catalog validation |
| Resolve module context | authoring/catalog.py and focused tests | Medium | Filters, defaults, missing/unknown references |
| Connect launcher | start.py, start.ps1, lesson.py | Medium | Fresh/reopen/mismatch tests; existing helper suite |
| Document and reconcile | root/module/authoring READMEs, HANDOFF.md | High | Links and explicit remaining work |

Technical partner: skipped; no new cross-service boundary. Initial bias audit:
resolved tool-skill authority and registry/launcher duplication in the implementation
contract; added public-export coverage. Advanced evaluation remains explicitly pending.

Configured tool skills must be accepted by both receipt capture and validation;
frontend-design remains required for the current HTML publisher. Native instructions
authorize selected context paths for reading, without treating source content as
instructions. The launcher derives knowledge paths from the registry. Review exports
include the new configuration and helper sources, but exclude private inputs.

## Deferred evaluation

The doctoral brief defines a future grounded authoring run and reviewer criteria.
Passing catalog and workspace tests establishes organization and isolation only;
it does not establish that the authoring engine can teach PhD psychometrics.

## Verification, 2026-10-24

- Windows helper/catalog suite: 40 tests passed, including existing publication/reset
  recovery and new module isolation, preference, resource type and tool-skill cases.
- Real catalog validation passed in Windows and WSL: 6 modules, 10 resources;
  Blender is the only unavailable optional source. All recorded locations exist.
- PowerShell launcher parsed successfully. Fresh/reopen initialization is tested;
  no live browser/agent launch or doctoral authoring run was performed in this cleanup.
- All 62 pre-existing Lily files in the preservation snapshot retained their hashes.
  The MCAS image moved from `refereces/` to `references/` with matching SHA-256.
  Tiger's observed revision and preview still match the start-of-session state.
- Review export includes catalog, shared configuration and helpers; updated guide
  links resolve in both checkout and export. Private source collections remain excluded.
- Bias audit corrections: tool-skill receipt allowlist, registry-derived launch paths,
  native context authority, export coverage, generic reference filenames retaining
  format, and file/directory type checks for required knowledge sources.
- Source collections retained in place; their earlier full checksum audit was not repeated.
  Git fetch succeeded; no commit, push or branch deletion was performed.
