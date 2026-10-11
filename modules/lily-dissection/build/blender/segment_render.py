import bpy, os, math
from mathutils import Vector

# Separate loose parts, false-color islands by cluster hypothesis, render 3 views.
# Purpose: visually reconcile the 40-island count and confirm front-bloom mapping (U1/U1b/U2).

bpy.ops.object.select_all(action='DESELECT')
obj = bpy.data.objects['OBJ_Lily']
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.mode_set(mode='OBJECT')

meshes = [o for o in bpy.data.objects if o.type == 'MESH' and len(o.data.vertices) > 0]

def centroid(o):
    mw = o.matrix_world
    cs = [mw @ v.co for v in o.data.vertices]
    return Vector((sum(c.x for c in cs)/len(cs), sum(c.y for c in cs)/len(cs), sum(c.z for c in cs)/len(cs)))

def dims(o):
    mw = o.matrix_world
    cs = [mw @ v.co for v in o.data.vertices]
    xs=[c.x for c in cs]; ys=[c.y for c in cs]; zs=[c.z for c in cs]
    return (max(xs)-min(xs), max(ys)-min(ys), max(zs)-min(zs))

# hypothesis categories -> emissive color (RGBA)
CATS = {
    "antherA": (0.9, 0.1, 0.1, 1),   # red   - front bloom (high X) anthers
    "antherB": (0.1, 0.2, 0.9, 1),   # blue  - second bloom (low X) anthers
    "tepal":   (1.0, 0.4, 0.8, 1),   # pink
    "slender": (1.0, 0.9, 0.0, 1),   # yellow - filament / style / pistil candidates
    "leaf":    (0.1, 0.8, 0.2, 1),   # green
    "other":   (0.5, 0.5, 0.5, 1),   # grey  - stem/bud/misc
}

def classify(o):
    v = len(o.data.vertices)
    c = centroid(o); d = dims(o)
    maxxy = max(d[0], d[1])
    if 600 <= v <= 820:
        if c.y > 0.15: return "other"          # bud anther cluster
        return "antherA" if c.x >= 0.11 else "antherB"
    if 540 <= v <= 560:
        return "tepal"
    if d[2] > 2.2*maxxy and v < 300:           # thin+tall
        return "slender"
    if maxxy > 0.18:                            # broad sheet
        return "leaf"
    return "other"

mats = {}
for name, col in CATS.items():
    m = bpy.data.materials.new(f"CAT_{name}")
    m.diffuse_color = col   # Workbench MATERIAL color_type reads this
    mats[name] = m

counts = {k: 0 for k in CATS}
for o in meshes:
    cat = classify(o)
    counts[cat] += 1
    o.data.materials.clear()
    o.data.materials.append(mats[cat])

print("CATEGORY_COUNTS", counts)

# ---- render setup: Workbench flat-shading shows each object's material base color ----
scene = bpy.context.scene
scene.render.engine = 'BLENDER_WORKBENCH'
shading = scene.display.shading
shading.light = 'FLAT'
shading.color_type = 'MATERIAL'
shading.show_object_outline = True
scene.render.resolution_x = 900
scene.render.resolution_y = 900
scene.render.film_transparent = False

# center of plant
allc = [centroid(o) for o in meshes]
center = Vector((sum(c.x for c in allc)/len(allc), sum(c.y for c in allc)/len(allc), 0.4))

def add_cam(name, loc):
    cam_data = bpy.data.cameras.new(name)
    cam = bpy.data.objects.new(name, cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = loc
    d = (center - Vector(loc))
    cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    cam_data.lens = 50
    return cam

views = {
    "front": ( center.x,        -1.6,  0.42),
    "side":  ( 1.6,       center.y,    0.42),
    "top":   ( center.x,  center.y,    1.7),
}
outdir = os.path.abspath(os.path.join(os.path.dirname(bpy.data.filepath), "..", "build", "blender", "renders"))
os.makedirs(outdir, exist_ok=True)
for vname, loc in views.items():
    cam = add_cam(f"CAM_{vname}", loc)
    scene.camera = cam
    scene.render.filepath = os.path.join(outdir, f"cat_{vname}.png")
    bpy.ops.render.render(write_still=True)
    print("RENDERED", scene.render.filepath)
