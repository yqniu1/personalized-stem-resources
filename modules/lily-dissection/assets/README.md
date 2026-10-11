# Lily vector assets

Editable illustrations for the 2-D Lily module, created for this project with AI assistance. The pink, spotted flower is a stylized Stargazer lily rather than a photograph.

## Files

- `svg/`: individual structures, pollen, pollinators, and assembled references.
- `lily-master.svg`: assembled face-on flower.
- `plant-master.svg`: assembled whole-plant illustration.
- `manifest.json`: scene geometry, render order, separation vectors, and sub-regions.

The flower layers share a 1600 by 1600 canvas. Their stacking order is sepals, petals, stamens, then pistil. The generator wraps each layer in a movable group and assigns its pollination role.

The whole-plant scene uses a different viewpoint and is not interchangeable with the face-on flower layers. It is an asset source for possible later work, rather than an additional working module.

The purchased 3-D flower is included as `lily.glb` under a separate commercial license. Original reference inputs are excluded. See [third-party notices](../../../THIRD_PARTY_NOTICES.md).
