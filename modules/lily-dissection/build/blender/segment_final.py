import bpy, os, sys, math, json
from mathutils import Vector

HERE = os.path.abspath(os.path.join(os.path.dirname(bpy.data.filepath), "..", "build", "blender"))
sys.path.insert(0, HERE)
import organ_map
import importlib; importlib.reload(organ_map)

blend_dir = os.path.dirname(bpy.data.filepath)

# --- 1. repoint textures to the 1k set ---
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

# --- 2. separate by loose parts ---
bpy.ops.object.select_all(action='DESELECT')
obj = bpy.data.objects['OBJ_Lily']
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.mode_set(mode='OBJECT')

meshes = [o for o in bpy.data.objects if o.type == 'MESH' and len(o.data.vertices) > 0]
roles, info = organ_map.classify_islands(meshes)

def cen(nm):
    return info[nm][1]

# front bloom center (mean of front tepals) for angular ordering + explode axis
front_tepals = [n for n, r in roles.items() if r == "front_tepal"]
fc = Vector((sum(cen(n).x for n in front_tepals) / len(front_tepals),
             sum(cen(n).y for n in front_tepals) / len(front_tepals),
             sum(cen(n).z for n in front_tepals) / len(front_tepals)))

def angle_sort(names):
    return sorted(names, key=lambda n: math.atan2(cen(n).y - fc.y, cen(n).x - fc.x))

# --- 3. rename pickable organs (stable angular order) ---
def rename(nm, newname):
    o = bpy.data.objects[nm]
    o.name = newname
    o.data.name = newname + "_mesh"
    return o

for i, nm in enumerate(angle_sort(front_tepals), 1):
    rename(nm, f"front_tepal_{i}")
for i, nm in enumerate(angle_sort([n for n, r in roles.items() if r == "front_stamen"]), 1):
    rename(nm, f"front_stamen_{i}")

def join(names, target):
    names = [n for n in names if n in bpy.data.objects]
    if not names:
        return None
    bpy.ops.object.select_all(action='DESELECT')
    objs = [bpy.data.objects[n] for n in names]
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    if len(objs) > 1:
        bpy.ops.object.join()
    j = bpy.context.view_layer.objects.active
    j.name = target
    j.data.name = target + "_mesh"
    return j

join([n for n, r in roles.items() if r == "front_pistil"], "front_pistil")
join([n for n, r in roles.items() if r == "second_pistil"], "second_pistil")
backdrop_roles = ("leaf", "stem", "bud", "second_tepal", "second_stamen", "misc")
join([n for n, r in roles.items() if r in backdrop_roles], "backdrop")

# --- 4. set pickable-organ origins to geometry center (node.position == organ center) ---
PICKABLE = [f"front_tepal_{i}" for i in range(1, 7)] + \
           [f"front_stamen_{i}" for i in range(1, 7)] + ["front_pistil", "second_pistil"]
bpy.ops.object.select_all(action='DESELECT')
for nm in PICKABLE:
    if nm in bpy.data.objects:
        bpy.data.objects[nm].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[nm]
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        bpy.data.objects[nm].select_set(False)

# report final node inventory
final_nodes = sorted([o.name for o in bpy.data.objects if o.type == 'MESH'])
print("FINAL_NODES", final_nodes)
print("NODE_COUNT", len(final_nodes))

# --- 5. export GLB (uncompressed; gltf-transform meshopt happens downstream) ---
out = os.path.abspath(os.path.join(blend_dir, "..", "assets", "lily-segmented-raw.glb"))
bpy.ops.export_scene.gltf(
    filepath=out,
    export_format='GLB',
    export_image_format='AUTO',
    export_yup=True,
    export_apply=True,
    export_draco_mesh_compression_enable=False,
)
print(f"EXPORTED {out} size={os.path.getsize(out)} ({os.path.getsize(out)/1e6:.2f} MB)")
