"""Shared organ-mapping logic for the lily front-bloom segmentation.

Reused by verify_organs.py (render check) and segment_final.py (the real bake).
Coordinates are Blender-native Z-up. Two blooms split by X:
  front bloom = high X (RED in the category render), second bloom = low X (BLUE).
"""
from mathutils import Vector

X_SPLIT = 0.115          # front (>=) vs second (<) bloom divider in X
Y_BUD = 0.15             # islands with centroid Y above this belong to the bud
TEPAL_V = (600, 820)     # tepal island vertex-count band (6 per bloom)
LEAF_V = (540, 560)      # 554-vert leaf islands
SLENDER_MAXV = 260       # stamens / pistil / stem are low-vert


def island_stats(o):
    mw = o.matrix_world
    cs = [mw @ v.co for v in o.data.vertices]
    n = len(cs)
    cen = Vector((sum(c.x for c in cs) / n, sum(c.y for c in cs) / n, sum(c.z for c in cs) / n))
    xs = [c.x for c in cs]; ys = [c.y for c in cs]; zs = [c.z for c in cs]
    dim = (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
    zmax = max(zs)
    return n, cen, dim, zmax


def classify_islands(meshes):
    """Return dict: island_name -> role label.

    Roles: front_tepal, front_stamen, front_pistil,
           second_tepal, second_stamen, second_pistil,
           leaf, stem, bud, misc
    """
    info = {o.name: island_stats(o) for o in meshes}

    # --- tepals: TEPAL_V band, split by bloom, minus bud ---
    front_tepals, second_tepals = [], []
    for name, (n, cen, dim, zmax) in info.items():
        if TEPAL_V[0] <= n <= TEPAL_V[1] and cen.y <= Y_BUD:
            (front_tepals if cen.x >= X_SPLIT else second_tepals).append(name)

    # --- bloom centers from tepal means ---
    def center_of(names):
        if not names:
            return Vector((0, 0, 0))
        cs = [info[nm][1] for nm in names]
        return Vector((sum(c.x for c in cs) / len(cs), sum(c.y for c in cs) / len(cs), 0))
    front_c = center_of(front_tepals)
    second_c = center_of(second_tepals)

    # --- slender organs (stamens/pistil): low-vert, in a bloom's height band, not the long stem ---
    def slender_for(bloom_x_lo, bloom_x_hi, bloom_center):
        cand = []
        for name, (n, cen, dim, zmax) in info.items():
            if n > SLENDER_MAXV:
                continue
            if dim[2] > 0.30:            # the long main stem / branches — exclude
                continue
            if cen.z < 0.55:             # organs sit high in the bloom
                continue
            if cen.y > Y_BUD:            # bud region
                continue
            if bloom_x_lo <= cen.x < bloom_x_hi:
                d = ((cen.x - bloom_center.x) ** 2 + (cen.y - bloom_center.y) ** 2) ** 0.5
                cand.append((d, zmax, name))
        cand.sort()                       # nearest-to-center first
        return cand

    roles = {}
    for name in front_tepals:
        roles[name] = "front_tepal"
    for name in second_tepals:
        roles[name] = "second_tepal"

    # Per bloom: central-most slender = pistil core; next 6 = stamens; any
    # remaining central slender (the style shaft) folds into the pistil group.
    fc = slender_for(X_SPLIT, 10.0, front_c)
    if fc:
        roles[fc[0][2]] = "front_pistil"
        for _, _, nm in fc[1:7]:
            roles[nm] = "front_stamen"
        for _, _, nm in fc[7:]:
            roles[nm] = "front_pistil"
    sc = slender_for(-10.0, X_SPLIT, second_c)
    if sc:
        roles[sc[0][2]] = "second_pistil"
        for _, _, nm in sc[1:7]:
            roles[nm] = "second_stamen"
        for _, _, nm in sc[7:]:
            roles[nm] = "second_pistil"

    # everything else: leaf / stem / bud / misc
    for name, (n, cen, dim, zmax) in info.items():
        if name in roles:
            continue
        if LEAF_V[0] <= n <= LEAF_V[1]:
            roles[name] = "leaf"
        elif dim[2] > 0.30:
            roles[name] = "stem"
        elif cen.y > Y_BUD:
            roles[name] = "bud"
        else:
            roles[name] = "misc"
    return roles, info
