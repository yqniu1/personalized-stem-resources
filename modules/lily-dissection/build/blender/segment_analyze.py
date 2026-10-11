import bpy, os, json
from mathutils import Vector

# Separate OBJ_Lily into loose parts and dump per-island spatial stats so we can
# reconcile the 40-island count and map the front bloom (spec Step 1 / U1/U1b/U2).
# Blender native coords are Z-up (plant grows in +Z).

# clean selection
bpy.ops.object.select_all(action='DESELECT')
obj = bpy.data.objects['OBJ_Lily']
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

# separate by loose parts (edit mode)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.mode_set(mode='OBJECT')

deps = bpy.context.evaluated_depsgraph_get()

islands = []
for o in bpy.data.objects:
    if o.type != 'MESH':
        continue
    me = o.data
    if len(me.vertices) == 0:
        continue
    mw = o.matrix_world
    # world-space vertex bounds + centroid
    coords = [mw @ v.co for v in me.vertices]
    xs = [c.x for c in coords]; ys = [c.y for c in coords]; zs = [c.z for c in coords]
    cen = Vector((sum(xs)/len(xs), sum(ys)/len(ys), sum(zs)/len(zs)))
    bmin = (min(xs), min(ys), min(zs))
    bmax = (max(xs), max(ys), max(zs))
    dim = (bmax[0]-bmin[0], bmax[1]-bmin[1], bmax[2]-bmin[2])
    islands.append({
        "name": o.name,
        "verts": len(me.vertices),
        "faces": len(me.polygons),
        "centroid": [round(v, 4) for v in cen],
        "bmin": [round(v, 4) for v in bmin],
        "bmax": [round(v, 4) for v in bmax],
        "dim": [round(v, 4) for v in dim],
    })

islands.sort(key=lambda d: d["centroid"][2])  # sort by height (Z)

# overall bounds
allx = [i for isl in islands for i in (isl["bmin"][0], isl["bmax"][0])]
ally = [i for isl in islands for i in (isl["bmin"][1], isl["bmax"][1])]
allz = [i for isl in islands for i in (isl["bmin"][2], isl["bmax"][2])]
print("ISLAND_COUNT", len(islands))
print("OVERALL_BOUNDS X[%.3f,%.3f] Y[%.3f,%.3f] Z[%.3f,%.3f]" % (
    min(allx), max(allx), min(ally), max(ally), min(allz), max(allz)))

out = os.path.abspath(os.path.join(os.path.dirname(bpy.data.filepath), "..", "private-assets", "islands.json"))
with open(out, "w") as f:
    json.dump(islands, f, indent=1)
print("WROTE", out)

# compact table
print("IDX  NAME                 VERTS  FACES  CENTROID(x,y,z)          DIM(x,y,z)")
for idx, isl in enumerate(islands):
    print("%3d  %-18s  %5d  %5d  (%7.3f,%7.3f,%7.3f)  (%6.3f,%6.3f,%6.3f)" % (
        idx, isl["name"][:18], isl["verts"], isl["faces"],
        isl["centroid"][0], isl["centroid"][1], isl["centroid"][2],
        isl["dim"][0], isl["dim"][1], isl["dim"][2]))
