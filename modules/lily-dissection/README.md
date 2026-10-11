# Lily Dissection

An interactive supplement for OpenSciEd Grade 4 Unit 4.4, Lesson 13. Students take a flower apart, inspect what its structures do, and move pollen. The teacher can use the model alongside the lesson's fresh-flower investigation and discussion.

## Run

Open `index.html` in a browser. It contains both views in one offline file. The standalone views also open directly as `index-3d.html` and `index-2d.html`.

- 2-D view: explore SVG structures and move pollen within a single illustrated bloom.
- 3-D view: orbit the flower, separate its structures, sort them by function, and transfer pollen between two blooms. Requires WebGL and the purchased model.

The combined file opens 3-D when WebGL is available, offers a view switch, and falls back to 2-D otherwise.

The two views represent different pollen-transfer cases. Use the 3-D view to discuss transfer between flowers. The 2-D view shows pollen reaching the same bloom's stigma; self-pollination is possible in plants, but this illustration does not establish compatibility or seed formation for this cultivar.

## Learning goal

The activity focuses on how flower structures work together in reproduction. Part names are supporting vocabulary. Students can observe structures and a simplified pollen transfer, then explain the relationship in their own model or discussion.

The mission panel tracks actions. Completing it is not an assessment of conceptual understanding. The model also simplifies the steps between pollination and seed formation.

## Edit and rebuild

The classroom HTML files are generated. Edit these inputs:

| Input | Purpose |
|---|---|
| `src/template.html` | 2-D interactions and copy |
| `src/template-3d.html` | 3-D interactions and copy |
| `src/template-merged.html` | Offline launcher and view switch |
| `assets/svg/`, `assets/manifest.json` | Vector layers and geometry |
| `assets/lily.glb` | Purchased 3-D illustration, under its separate license |
| `build/web/src/three-bundle.mjs` | Three.js, loaders, and embedded Meshopt decoder |

From the repository root, using Python 3 and Node/npm:

```powershell
npm ci --prefix modules/lily-dissection/build/web
npm run bundle --prefix modules/lily-dissection/build/web
python modules/lily-dissection/build/build.py
```

The assembly scripts use the Python standard library. Rebuilding only `index-2d.html` needs no Node dependencies:

```powershell
python modules/lily-dissection/build/assemble.py
```

The [3-D implementation notes](docs/design-3d-lily.md) describe the model and offline packaging. `build/blender/` contains earlier segmentation and inspection scripts requiring Blender and original model inputs. Those inputs are local and are not included in a public clone.

## Design notes and checks

- [Lesson alignment](docs/design-lesson13-alignment.md)
- [3-D implementation](docs/design-3d-lily.md)
- [Asset structure](assets/README.md)
- [Illustrated walkthrough](../../docs/tools-competition-2027-activity-teardown.md)

Desktop Chromium checks exercised the 3-D launch, keyboard part selection, disassembly, keyboard pollen transfer, view switching, and a simulated WebGL fallback. No page errors or HTTP requests occurred in that run. Physical school devices, full accessibility, and independent student use still need evaluation.

## Credits

Curriculum context: [OpenSciEd](https://openscied.org/), Grade 4 Unit 4.4, Lesson 13. This is an independent, AI-assisted supplement with new illustrations and interactions. It does not replace the lesson's investigation or claim publisher endorsement. See the repository's [third-party notices](../../THIRD_PARTY_NOTICES.md) for attribution and model distribution restrictions.
