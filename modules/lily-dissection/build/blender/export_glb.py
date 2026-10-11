import bpy, os

# --- Repoint bound textures to the 1k set on disk, then export a GLB. ---
# Textures may be packed at 2k inside the blend; we replace them with the smaller
# 1k files so the embedded GLB starts light. Final texture optimization (resize
# guarantee + NRM->JPEG) happens downstream in gltf-transform.

blend_dir = os.path.dirname(bpy.data.filepath)
ONEK = os.path.join(blend_dir, "texture", "texture", "stargizer", "1k")

for img in bpy.data.images:
    base = os.path.basename(img.filepath.replace("\\", "/"))
    cand = os.path.join(ONEK, base)
    if os.path.exists(cand):
        if img.packed_file:
            img.unpack(method='REMOVE')
        img.filepath = cand
        img.source = 'FILE'
        img.reload()
        print(f"REPOINTED {base} -> 1k  size now {tuple(img.size)}")
    else:
        print(f"WARN no 1k match for {base} (looked for {cand})")

out = os.path.abspath(os.path.join(blend_dir, "..", "assets", "lily-step0-raw.glb"))

bpy.ops.export_scene.gltf(
    filepath=out,
    export_format='GLB',
    export_image_format='AUTO',     # keep JPG as JPG, PNG as PNG; convert later
    export_yup=True,
    export_apply=True,              # apply modifiers
    export_draco_mesh_compression_enable=False,
)
print(f"EXPORTED {out}  size={os.path.getsize(out)} bytes ({os.path.getsize(out)/1e6:.2f} MB)")
