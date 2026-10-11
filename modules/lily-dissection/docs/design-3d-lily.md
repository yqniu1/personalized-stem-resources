# 3-D prototype

The earlier Lily version uses Three.js to explore a segmented flower model. Learners can orbit the scene, separate structures, read their functions, sort by role, and move pollen between two blooms.

The model was purchased from TurboSquid: **Stargazer Lilies**, product **2277259**. The compressed GLB and embedded HTML builds are included for review under the model's separate commercial license. Rendered screenshots appear in the [prototype walkthrough](../../../docs/tools-competition-2027-activity-teardown.md). See [distribution notes](../../../THIRD_PARTY_NOTICES.md).

## Implementation

The supplied Blender model was split into disconnected geometry islands, then mapped to interactive organs. The front bloom supplies six tepals, six stamens, and a pistil. A stigma on the second bloom supplies the pollen target. Stem, leaves, and other geometry remain scenery.

The browser template maps named nodes to function descriptions and learner actions. A compressed GLB and a bundled Three.js renderer are embedded in a standalone HTML build. The Meshopt decoder includes its WASM bytes, avoiding a network fetch when the file opens from disk.

The combined launcher embeds the 2-D and 3-D applications in separate `iframe srcdoc` documents. This keeps their element IDs and styles isolated. It initializes the selected view and falls back to 2-D if WebGL is unavailable.

## Rebuild

The build consumes the committed model at `assets/lily.glb`:

```powershell
npm ci --prefix modules/lily-dissection/build/web
npm run bundle --prefix modules/lily-dissection/build/web
python modules/lily-dissection/build/build.py
```

Outputs are `index-2d.html`, `index-3d.html`, and the combined `index.html` within the module. The `build/blender/` scripts require Blender and the original inputs; they are historical asset-preparation utilities rather than prerequisites for the public build.

## Checks and limits

Desktop Chromium checks exercised rendering, keyboard selection, separation, keyboard pollen transfer, and the earlier launcher fallback. These checks do not establish performance on physical school devices, full accessibility, or independent student usability. The purchased model's license does not establish permission to distribute its data through this WebGL implementation.
