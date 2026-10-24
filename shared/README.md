# Shared authoring resources

[resources.json](resources.json) is the common registry for every module. It points
to sources rather than duplicating canonical patterns, skills or original media.
The catalog resolves locations on Windows or WSL from the checkout's parent and
user directory; no credentials are stored here.

| Layer | Shared source | Module/teacher contribution |
|---|---|---|
| Learning engineer | Learnability Patterns + learning-authoring skill; existing niu-library connection | Objective, learner evidence and source-linked design |
| Asset libraries | Existing module assets and local Twig collections | Choose specific assets and retain provenance |
| Tool skills | frontend-design; Blender recorded as not yet located | Select tools for the activity; capture actual skill receipts |
| Curriculum | Local Twig and Talent Academy source collections | Select lesson-level content, prerequisites and sequence |
| Standards | Supplied references, with authority/coverage status | Exact framework/code, evidence and alignment review |
| Preferences | `defaults` in resources.json | Module overrides; then the teacher's explicit current request |

`python authoring/catalog.py check` reports missing optional sources separately from
required learning-engine dependencies. Register an actual Blender `SKILL.md` path
when available; the Lily Blender scripts remain module-specific build tools.

The [module catalog](../modules/catalog.json) keeps multi-valued subjects, level,
standards, objectives, preferences and artifact locations. `show` produces resolved
context; the launcher snapshots it under `materials/module-context.json` in a new
workspace. An existing workspace retains its original snapshot and knowledge paths.
Use a new workspace to adopt changed registry configuration. Shared registry entries
are available references, not a requirement to use every library or skill.

Source collections stay at their original paths under `source-assets/`. The local
`FETCH-REPORT.md`, `source-manifest.json` and `verification.json` document the earlier
transfer. This cleanup did not repeat its multi-gigabyte checksum audit. Individual
media/content suitability still needs review when selected for a lesson.
