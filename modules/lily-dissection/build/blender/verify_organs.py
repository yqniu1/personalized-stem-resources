import bpy, os, sys
sys.path.insert(0, os.path.dirname(bpy.data.filepath) + "/../build/blender")
sys.path.insert(0, os.path.join(os.path.dirname(bpy.data.filepath), "..", "build", "blender"))
import organ_map
import importlib; importlib.reload(organ_map)

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

from collections import Counter
print("ROLE_COUNTS", dict(Counter(roles.values())))
for role in ("front_pistil", "second_pistil", "front_stamen", "front_tepal", "second_tepal"):
    names = [n for n, r in roles.items() if r == role]
    print(f"  {role}: {len(names)} -> {names}")

ROLE_COLORS = {
    "front_tepal":  (0.85, 0.15, 0.15, 1),  # red
    "front_stamen": (1.0, 0.6, 0.0, 1),     # orange
    "front_pistil": (1.0, 1.0, 1.0, 1),     # white
    "second_tepal": (0.2, 0.35, 0.9, 1),    # blue
    "second_stamen":(0.4, 0.8, 0.9, 1),     # light blue
    "second_pistil":(0.0, 1.0, 1.0, 1),     # cyan
    "leaf":         (0.15, 0.5, 0.2, 1),    # green
    "stem":         (0.4, 0.3, 0.1, 1),     # brown
    "bud":          (0.6, 0.6, 0.6, 1),     # grey
    "misc":         (1.0, 0.0, 1.0, 1),     # magenta (flag!)
}
mats = {}
for role, col in ROLE_COLORS.items():
    m = bpy.data.materials.new(f"ROLE_{role}")
    m.diffuse_color = col
    mats[role] = m
for o in meshes:
    o.data.materials.clear()
    o.data.materials.append(mats[roles[o.name]])

scene = bpy.context.scene
scene.render.engine = 'BLENDER_WORKBENCH'
sh = scene.display.shading
sh.light = 'FLAT'; sh.color_type = 'MATERIAL'; sh.show_object_outline = True
scene.render.resolution_x = 1000; scene.render.resolution_y = 1000

from mathutils import Vector
allc = [info[o.name][1] for o in meshes]
center = Vector((sum(c.x for c in allc)/len(allc), sum(c.y for c in allc)/len(allc), 0.45))
# focus front bloom center for the zoom view
fc = Vector((0.21, -0.01, 0.66))

def add_cam(name, loc, target):
    cd = bpy.data.cameras.new(name); cam = bpy.data.objects.new(name, cd)
    bpy.context.collection.objects.link(cam)
    cam.location = loc
    cam.rotation_euler = (target - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    cd.lens = 55
    return cam

views = {
    "roles_top":   ((center.x, center.y, 1.7), center),
    "roles_front": ((center.x, -1.6, 0.5), center),
    "roles_zoom":  ((fc.x, -0.55, 0.72), fc),
}
outdir = os.path.abspath(os.path.join(os.path.dirname(bpy.data.filepath), "..", "build", "blender", "renders"))
for vname, (loc, tgt) in views.items():
    cam = add_cam("C_" + vname, loc, tgt)
    scene.camera = cam
    scene.render.filepath = os.path.join(outdir, vname + ".png")
    bpy.ops.render.render(write_still=True)
    print("RENDERED", scene.render.filepath)
