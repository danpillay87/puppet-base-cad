r"""
Character shells and clip-on accessories for the universal puppet base (CadQuery).

Run:  .venv\Scripts\python.exe build_shells.py              # build everything, write STLs + out/shells_report.csv + preview
      .venv\Scripts\python.exe build_shells.py pear frog     # only some parts (names: pear frog heart jolly claude beret glasses sunglasses)
      add --no-preview to skip the picture.

This file only IMPORTS the geometry helpers and the head dimensions from build_puppet_base.py (it changes nothing there).
Head frame: origin = centre of the magnet collar plane, +Z up, +Y = front. The head sphere centre is HEAD_CUT_DZ (about 24 mm) above it.
All units are millimetres. Numbers marked (CHECK) are best guesses to confirm on the first print.
"""
import math
import os
import sys

import cadquery as cq

import build_puppet_base as B

# =====================================================================================
# PARAMETERS (shells and clip-ons)
# =====================================================================================
SHELL_WALL = B.SHELL_WALL                     # 1.5 mm hollow wall for every character shell
CLIP_WALL = 1.2                               # beret wall
CLIP_FIT = 0.15                               # beret cap radial clearance on the head sphere (friction fit)
MASS_LIMIT_G = 200.0                          # each shell must stay under this (printed, thin wall = near solid)
PLA_G_PER_CM3 = 1.24

# shared geometry (head frame)
ZC = B.HEAD_CUT_DZ                            # head sphere centre height above the collar plane
R0 = B.SHELL_CAV_R + SHELL_WALL               # first blob: swallows the head (cavity 61.8 + wall 1.5)
ZF = B.SHELL_FLOOR_Z                          # underside of the mating ring (-3.2)

# shell split lugs (same on all shells): two M3 across the split at the front and the back
LUG_Y0 = 59.0                                 # lug blocks start outside the head's bulge at their height
LUG_HOLE_Y = 62.0
LUG_HOLE_Z = 4.0
LUG_Z_TOP = 8.0

# Jolly (hooded head + shoulders)
JOLLY_HEM_Z = -26.0                           # open lower edge (head frame), raised from -40 (and earlier -58) so the shell clears the column at the full nod 30 + tilt 25 corner at rest. The fixed neck flange tops out at about -64.
SLEEVE_D = B.SLEEVE_D                         # 35 mm plush sleeve
ARM_CLEAR = 3.0                               # sleeve slot clearance
ARM_SLOT_ANGLES = range(50, 85, 5)            # arm directions (deg above horizontal) that sweep through the shoulder flank
ARM_SLOT_LEN = 122.0                          # stop at the sleeve length, so the head side is never slotted
HOOD_RING_R = 42.0                            # radius of the hood's face opening (viewed from the front)
HOOD_TUBE_R = 3.0                             # thickness of the hood edge ridge

# round glasses / sunglasses (clip around the head sphere like spectacles)
G_ZC = ZC + 10.0                              # lens centre height
G_Y0, G_Y1 = 61.6, 64.6                       # front frame sits 0.6 mm clear of the equator bead (bead outer radius 61)
G_ARC_RIN, G_ARC_ROUT = 58.6, 61.0            # temple arcs: inner radius a touch under the sphere (springy grip)
G_ARC_Z0, G_ARC_Z1 = G_ZC - 4.0, G_ZC + 4.0   # temple band is 8 mm tall
G_ARC_END = 115.0                             # degrees round from the front: past the widest point = the hook behind the head
ROUND_R_OUT, ROUND_R_IN, ROUND_X = 18.0, 15.0, 21.0     # round rims: centre spacing 42
SUN_W, SUN_H, SUN_R, SUN_X = 46.0, 32.0, 10.0, 24.0     # sunglass lens plates

# beret (friction-fit cap + flat saucer)
BERET_RIM_DZ = 22.0                           # cap rim height above the head centre (rim polar angle about 70 degrees)
BERET_RXY, BERET_RZ = 54.0, 14.0              # saucer radius / half thickness
BERET_CZ = 54.0                               # saucer centre height above the head centre
BERET_DX = 7.0                                # sideways offset (a beret sits off-centre)

# Claude (puffy starburst: seven soft rays in the front XZ plane, radiating from the head-sphere centre)
CLAUDE_RAYS = [                               # (angle from vertical in the front view, + = toward +x ; reach = tip-sphere centre distance from the head-sphere centre)
    (0.0, 89.0),                              # reaches are pulled in by the tip-radius growth (8 -> 14 mm) so the overall size stays 186 x 127 mm
    (38.0, 84.0), (-38.0, 84.0),
    (75.0, 82.0), (-75.0, 82.0),
    (108.0, 74.0), (-108.0, 74.0),            # these two point a little below horizontal; the mating plane cuts their undersides flat
]
CLAUDE_ROOT_R = 19.0                          # ray radius where it leaves the head sphere (tapers linearly to the tip radius): stubby plush fingers
CLAUDE_TIP_R = 14.0                           # radius of the tip, a full hemisphere (sphere centred on the end of the cone)
CLAUDE_S0 = 30.0                              # the ray cone starts this far from the head-sphere centre (hidden inside the head blob)

# =====================================================================================
# shell builder
# =====================================================================================


def shell_full(blobs, zmin=ZF, wall=SHELL_WALL, extra_cuts=(), extra_add=()):
    """Hollow shell = union of spheroids minus the same spheroids shrunk by `wall`, minus the head cavity,
    cut off at height zmin, with the solid 3.2 mm mating plate (Ø96 hole + six magnet pockets opening downward)
    and a screw lug at the front and back seam. blobs = [(cx, cy, cz, r_xy, r_z)] in the head frame.
    extra_add = solid trim (e.g. the hood ridge) fused on after hollowing."""
    outer = B.union_all([B.spheroid(*b) for b in blobs])
    cav = B.union_all([B.spheroid(b[0], b[1], b[2], b[3] - wall, b[4] - wall) for b in blobs]
                      + [cq.Workplane("XY").sphere(B.SHELL_CAV_R).translate((0, 0, ZC))])
    body = outer.cut(cav).intersect(B.box(-300, 300, -300, 300, zmin, 400))
    plate = outer.intersect(B.box(-300, 300, -300, 300, ZF, 0.0)).cut(B.cylz(0, 0, ZF - 1, 1, B.COLLAR_ID / 2))
    shell = body.union(plate)
    for e in extra_add:
        shell = shell.union(e)
    yo = plate.val().BoundingBox().ymax
    yb = max(yo + 6.0, 66.0)
    for sy in (-1, 1):
        ya, yz = sorted((sy * (yo - 3.0), sy * yb))
        shell = shell.union(B.box(-8.0, 8.0, ya, yz, ZF, 0.0))                       # lower lug block on the plate
        ya, yz = sorted((sy * LUG_Y0, sy * yb))
        shell = shell.union(B.box(-8.0, 8.0, ya, yz, -0.01, LUG_Z_TOP))              # upper lug block on the wall
    tools = list(B.magnet_pockets(ZF, B.MAG_POCKET_DEPTH, -1)) + list(extra_cuts)
    return B.cut_all(shell, tools)


def shell_halves(blobs, **kw):
    """Left half = x <= 0; right half = its mirror image (a straight x >= 0 cut of a union of spheres upsets the kernel,
    the mirror is exact). Lug holes are cut last: 3.4 mm clearance on the left, 2.7 mm pilot on the right."""
    full = shell_full(blobs, **kw)
    left0 = B.half(full, -1)
    right0 = left0.mirror("YZ")
    left = B.cut_all(left0, [B.cylx(-9.0, 0.5, sy * LUG_HOLE_Y, LUG_HOLE_Z, 1.7) for sy in (-1, 1)])
    right = B.cut_all(right0, [B.cylx(-0.5, 9.0, sy * LUG_HOLE_Y, LUG_HOLE_Z, 1.35) for sy in (-1, 1)])
    return left, right


def shell_full_solid(outer, cav, zmin=ZF, extra_cuts=(), extra_add=()):
    """Variant of shell_full for shapes that are not a plain union of spheroids (shell_full itself is untouched).
    outer = the finished outer solid, cav = the finished cavity solid (the outer shape shrunk by the wall; the Ø123.6 head
    cavity is added here). Everything after that is the same recipe as shell_full: cut off at zmin, solid 3.2 mm mating
    plate taken from the outer shape (Ø96 hole, six magnet pockets opening downward) and an M3 lug block at the front and
    back seam."""
    cav = cav.union(cq.Workplane("XY").sphere(B.SHELL_CAV_R).translate((0, 0, ZC)))
    body = outer.cut(cav).intersect(B.box(-300, 300, -300, 300, zmin, 400))
    plate = outer.intersect(B.box(-300, 300, -300, 300, ZF, 0.0)).cut(B.cylz(0, 0, ZF - 1, 1, B.COLLAR_ID / 2))
    shell = body.union(plate)
    for e in extra_add:
        shell = shell.union(e)
    yo = plate.val().BoundingBox().ymax
    yb = max(yo + 6.0, 66.0)
    for sy in (-1, 1):
        ya, yz = sorted((sy * (yo - 3.0), sy * yb))
        shell = shell.union(B.box(-8.0, 8.0, ya, yz, ZF, 0.0))
        ya, yz = sorted((sy * LUG_Y0, sy * yb))
        shell = shell.union(B.box(-8.0, 8.0, ya, yz, -0.01, LUG_Z_TOP))
    tools = list(B.magnet_pockets(ZF, B.MAG_POCKET_DEPTH, -1)) + list(extra_cuts)
    return B.cut_all(shell, tools)


def shell_halves_solid(outer, cav, **kw):
    """Left/right halves of shell_full_solid, split exactly like shell_halves (right = mirror of left, lug holes cut last)."""
    full = shell_full_solid(outer, cav, **kw)
    left0 = B.half(full, -1)
    right0 = left0.mirror("YZ")
    left = B.cut_all(left0, [B.cylx(-9.0, 0.5, sy * LUG_HOLE_Y, LUG_HOLE_Z, 1.7) for sy in (-1, 1)])
    right = B.cut_all(right0, [B.cylx(-0.5, 9.0, sy * LUG_HOLE_Y, LUG_HOLE_Z, 1.35) for sy in (-1, 1)])
    return left, right


def claude_ray(angle_deg, reach, inset=0.0):
    """One soft ray: a cone frustum from CLAUDE_S0 out to the tip-sphere centre plus the tip sphere, in the XZ plane, `angle_deg`
    from vertical (+ toward +x), starting at the head-sphere centre. The radius is CLAUDE_ROOT_R where the ray leaves the head
    blob (distance R0) and CLAUDE_TIP_R at the tip. inset > 0 shrinks every radius (used for the cavity: inset = wall)."""
    a = math.radians(angle_deg)
    d = cq.Vector(math.sin(a), 0.0, math.cos(a))
    c = cq.Vector(0.0, 0.0, ZC)
    slope = (CLAUDE_TIP_R - CLAUDE_ROOT_R) / (reach - R0)
    r_start = CLAUDE_ROOT_R + slope * (CLAUDE_S0 - R0)
    cone = cq.Workplane("XY").add(cq.Solid.makeCone(r_start - inset, CLAUDE_TIP_R - inset, reach - CLAUDE_S0,
                                                    c + d * CLAUDE_S0, d))
    tip = cq.Workplane("XY").sphere(CLAUDE_TIP_R - inset).translate((c + d * reach).toTuple())
    return cone.union(tip)


def claude_solids(wall=SHELL_WALL):
    """(outer, cavity) of the Claude starburst: the head-swallowing sphere R0 plus seven rays; the cavity is the same
    primitives shrunk by the wall."""
    ctr = (0, 0, ZC)
    outer = B.union_all([cq.Workplane("XY").sphere(R0).translate(ctr)] + [claude_ray(a, r) for a, r in CLAUDE_RAYS])
    cav = B.union_all([cq.Workplane("XY").sphere(R0 - wall).translate(ctr)]
                      + [claude_ray(a, r, inset=wall) for a, r in CLAUDE_RAYS])
    return outer, cav


def pear_blobs():
    return [
        (0, 0, ZC, R0, R0),                    # swallows the head
        (0, 0, ZC - 8.0, 70.0, 54.0),          # broad belly (Ø140), cut flat by the mating plane
        (0, 0, ZC + 40.0, 40.0, 44.0),         # narrower shoulder dome
        (2.0, 0, ZC + 90.0, 5.5, 10.0),        # stalk
    ]


def frog_blobs():
    return [
        (0, 0, ZC, R0, R0),
        (-45.0, 6.0, ZC - 6.0, 26.0, 20.0),    # left cheek
        (45.0, 6.0, ZC - 6.0, 26.0, 20.0),     # right cheek
        (-30.0, 10.0, ZC + 52.0, 21.0, 21.0),  # left eye dome
        (30.0, 10.0, ZC + 52.0, 21.0, 21.0),   # right eye dome
    ]


def heart_blobs():
    return [
        (0, 0, ZC, R0, R0),
        (-29.0, 0, ZC + 42.0, 38.0, 38.0),     # left lobe
        (29.0, 0, ZC + 42.0, 38.0, 38.0),      # right lobe
    ]


def jolly_blobs():
    return [
        (0, 0, ZC, R0, R0),
        (0, -6.0, ZC + 52.0, 27.0, 24.0),      # hood peak
        (0, 0, -30.0, 72.0, 56.0),             # shoulders (Ø144), open at the hem
    ]


def arm_slots():
    """Clearance slots on the shoulder flanks so the Ø35 sleeves can swing up to 80 degrees: the sleeve is swept about each
    shoulder socket (x = +/-67.1, 119 mm below the collar plane at rest) and cut out of the shell."""
    px, pz = B.SK_SHAFT_X, B.SK_ZC - B.HEAD_Z0_ABS
    yc = B.SK_HORN_Y0 + B.HORN_BOSS_T / 2
    r = SLEEVE_D / 2 + ARM_CLEAR
    cyls = [B.cylx(0.0, ARM_SLOT_LEN, yc, 0.0, r).rotate((0, 0, 0), (0, 1, 0), -a).translate((px, 0, pz))
            for a in ARM_SLOT_ANGLES]
    right = B.union_all(cyls)
    return [right, right.mirror("YZ")]


def build_pear():
    return shell_halves(pear_blobs())


def build_frog():
    return shell_halves(frog_blobs())


def build_heart():
    return shell_halves(heart_blobs())


def hood_ridge():
    """The edge of the hood: a thin arch round the face opening (a torus tube of radius 3 whose centre-line sits on a sphere
    1.2 mm outside the shell, so half of it is proud of the surface). Only the part above z = 14 is kept; the head cavity is
    cut out of it so nothing can touch the head."""
    ring_r, tube_r = HOOD_RING_R, HOOD_TUBE_R
    y0 = math.sqrt((R0 + 1.2) ** 2 - ring_r ** 2)
    tor = (cq.Workplane("XY").center(ring_r, 0).circle(tube_r).revolve(360, (-ring_r, 0, 0), (-ring_r, 1, 0))
           .translate((0, y0, ZC)))
    tor = tor.intersect(B.box(-300, 300, 0, 300, ZC - 10.0, 400))
    return tor.cut(cq.Workplane("XY").sphere(B.SHELL_CAV_R).translate((0, 0, ZC)))


def build_jolly():
    return shell_halves(jolly_blobs(), zmin=JOLLY_HEM_Z, extra_cuts=arm_slots(), extra_add=[hood_ridge()])


def build_claude():
    outer, cav = claude_solids()
    return shell_halves_solid(outer, cav)


# =====================================================================================
# clip-ons
# =====================================================================================
def sector(r_in, r_out, phi0, phi1, z0, z1):
    """Annular sector: azimuth measured from +Y (front) toward +X, in degrees."""
    ring = B.cylz(0, 0, z0, z1, r_out).cut(B.cylz(0, 0, z0 - 1, z1 + 1, r_in))
    p0, p1 = math.radians(phi0), math.radians(phi1)
    pts = [(0, 0), (300 * math.sin(p0), 300 * math.cos(p0)), (300 * math.sin(p1), 300 * math.cos(p1))]
    wedge = cq.Workplane("XY").workplane(offset=z0 - 0.5).polyline(pts).close().extrude(z1 - z0 + 1.0)
    return ring.intersect(wedge)


def rrect_y(y0, y1, cx, cz, w, h, r):
    """Rounded rectangle plate in the XZ plane, thickness along Y from y0 to y1."""
    return (cq.Workplane("XZ").workplane(offset=-y1).center(cx, cz).rect(w, h).extrude(y1 - y0)
            .edges("|Y").fillet(r))


def temple_right(x_out, x_in_block):
    """Right temple: a short straight arm from the front frame back to the head, then an arc round the side of the head
    that ends 115 degrees round, behind the widest point (the hook that keeps the glasses on)."""
    y_arc = math.sqrt(G_ARC_ROUT ** 2 - x_out ** 2)
    connector = B.box(x_in_block, x_out + 1.2, G_Y0, G_Y1, G_ARC_Z0, G_ARC_Z1)
    arm = B.box(x_out - 1.2, x_out + 1.2, y_arc - 2.0, G_Y1 - 0.5, G_ARC_Z0, G_ARC_Z1)
    phi0 = math.degrees(math.asin(x_out / G_ARC_ROUT)) - 6.0
    arc = sector(G_ARC_RIN, G_ARC_ROUT, phi0, G_ARC_END, G_ARC_Z0, G_ARC_Z1)
    return B.union_all([connector, arm, arc])


def build_glasses_round():
    rim = B.cyly(G_Y0, G_Y1, ROUND_X, G_ZC, ROUND_R_OUT).cut(B.cyly(G_Y0 - 1, G_Y1 + 1, ROUND_X, G_ZC, ROUND_R_IN))
    right = rim.union(temple_right(ROUND_X + ROUND_R_OUT + 1.2, ROUND_X + ROUND_R_OUT - 2.5))
    bridge = B.box(-ROUND_X + ROUND_R_OUT - 1.0, ROUND_X - ROUND_R_OUT + 1.0, G_Y0, G_Y1, G_ZC + 3.0, G_ZC + 6.0)
    return right.union(right.mirror("YZ")).union(bridge)


def build_glasses_sun():
    lens = rrect_y(G_Y0, G_Y1, SUN_X, G_ZC, SUN_W, SUN_H, SUN_R)
    right = lens.union(temple_right(SUN_X + SUN_W / 2 + 1.2, SUN_X + SUN_W / 2 - 3.0))
    bridge = B.box(-SUN_X + SUN_W / 2 - 1.0, SUN_X - SUN_W / 2 + 1.0, G_Y0, G_Y1, G_ZC + 5.0, G_ZC + 10.0)
    return right.union(right.mirror("YZ")).union(bridge)


def build_beret():
    zr = ZC + BERET_RIM_DZ
    r_in = B.HEAD_R + CLIP_FIT
    cap = cq.Workplane("XY").sphere(r_in + CLIP_WALL).translate((0, 0, ZC)).intersect(B.box(-300, 300, -300, 300, zr, 400))
    saucer = B.spheroid(BERET_DX, 0, ZC + BERET_CZ, BERET_RXY, BERET_RZ)
    stalk = B.cylz(BERET_DX, 0, ZC + BERET_CZ + BERET_RZ - 3.0, ZC + BERET_CZ + BERET_RZ + 5.0, 3.5)
    outer = cap.union(saucer)
    cav = cq.Workplane("XY").sphere(r_in).translate((0, 0, ZC)).union(
        B.spheroid(BERET_DX, 0, ZC + BERET_CZ, BERET_RXY - CLIP_WALL, BERET_RZ - CLIP_WALL))
    hat = outer.cut(cav).intersect(B.box(-300, 300, -300, 300, zr, 400))
    return hat.union(stalk)


# =====================================================================================
# parts list + export
# =====================================================================================
AX, AY, AZ = B.AX, B.AY, B.AZ

# (name, builder, kind, rotations key, supports note)
JOBS = {
    "pear": (build_pear, "halves"),
    "frog": (build_frog, "halves"),
    "heart": (build_heart, "halves"),
    "jolly": (build_jolly, "halves"),
    "claude": (build_claude, "halves"),
    "beret": (build_beret, "single"),
    "glasses": (build_glasses_round, "single"),
    "sunglasses": (build_glasses_sun, "single"),
}

SUPPORT_NOTES = {
    "pear": "YES: crown of the dome and the stalk; tree supports (lies on its split face)",
    "frog": "YES: eye domes and cheeks; tree supports (lies on its split face)",
    "heart": "YES: both lobes; tree supports (lies on its split face)",
    "jolly": "YES: hood peak, shoulder flank slots and the rim of the open hem; tree supports (lies on its split face)",
    "claude": "YES: the two 38-degree rays (about 50 degrees off vertical when printed), the arch over the top ray and the dome crown; the 75 and 108 degree rays stand up nearly vertical; tree supports (lies on its split face)",
    "beret": "YES: underside of the saucer (print crown-down on the stalk with tree supports, or rim-down with supports under the saucer)",
    "glasses": "none (front face down: rims flat, temple arcs stand up as thin walls)",
    "sunglasses": "none (front face down: lens plates flat, temple arcs stand up as thin walls)",
}

SINGLE_ROT = {
    "beret": [(AX, 180)],                      # crown down
    "glasses": [(AX, -90)],                    # front face (+Y) down
    "sunglasses": [(AX, -90)],
}
HALF_ROT = {"left": [(AY, 90)], "right": [(AY, -90)]}    # split face down, like the head halves

STL_NAMES = {
    "pear": ("shell_pear_left", "shell_pear_right"),
    "frog": ("shell_frog_left", "shell_frog_right"),
    "heart": ("shell_heart_left", "shell_heart_right"),
    "jolly": ("shell_jolly_left", "shell_jolly_right"),
    "claude": ("shell_claude_left", "shell_claude_right"),
    "beret": ("clip_beret",),
    "glasses": ("clip_glasses_round",),
    "sunglasses": ("clip_sunglasses",),
}


def pose_head_frame(wp, bob=0.0, nod=0.0, tilt=0.0):
    """Move a head-frame part (collar plane z = 0) to where the head sits for a given bob (mm), nod and tilt (degrees).
    This is exactly the transform B.assemble() applies to head_L / head_R (translate up to the collar plane, tilt about Y,
    then nod about X), so a shell posed with it moves with the head. Used by check_shell_clearance.py and render_preview.py."""
    wp = wp.translate((0, 0, B.HEAD_Z0_ABS + bob))
    wp = wp.rotate((0, 0, B.TILT_AXIS_Z + bob), (0, 1, B.TILT_AXIS_Z + bob), tilt)
    return wp.rotate((0, 0, B.NOD_AXIS_Z + bob), (1, 0, B.NOD_AXIS_Z + bob), nod)


def describe(name, wp):
    v = wp.val()
    return v.isValid(), len(wp.solids().vals()), v.Volume() / 1000.0


def main(selected=None, preview=True, build=True):
    out = B.OUT_DIR
    os.makedirs(out, exist_ok=True)
    asm = os.path.join(out, "_assembly", "_shells")
    os.makedirs(asm, exist_ok=True)
    names = (selected or list(JOBS.keys())) if build else []
    head_L, head_R = B.build_head_halves()
    head_full = head_L.union(head_R)
    rows, posed = [], {}
    for key in names:
        fn, kind = JOBS[key]
        parts = fn()
        parts = list(parts) if kind == "halves" else [parts]
        fnames = STL_NAMES[key]
        total_cm3 = 0.0
        for i, (fname, wp) in enumerate(zip(fnames, parts)):
            ok, nsol, vol = describe(fname, wp)
            rots = HALF_ROT["left" if i == 0 else "right"] if kind == "halves" else SINGLE_ROT[key]
            pw = B.settle(wp, rots)
            path = os.path.join(out, fname + ".stl")
            B.export_stl(pw, path)
            bb = pw.val().BoundingBox()
            g_solid = vol * PLA_G_PER_CM3
            total_cm3 += vol
            rows.append((fname, 1, vol, bb.xlen, bb.ylen, bb.zlen, vol * PLA_G_PER_CM3 * 0.25, g_solid, SUPPORT_NOTES[key],
                         ok, nsol, os.path.getsize(path)))
            print(f"{fname:22s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:6.1f} mm  {vol:6.1f} cm3  {g_solid:6.1f} g (near-solid)"
                  f"  valid={ok} solids={nsol}  {os.path.getsize(path) / 1e6:5.2f} MB", flush=True)
        # whole-part checks: mass, and does it hit the head?
        whole = parts[0].union(parts[1]) if kind == "halves" else parts[0]
        hit = B.overlap_mm3(whole, head_full)
        g_total = total_cm3 * PLA_G_PER_CM3
        flag = "OK" if g_total < MASS_LIMIT_G else "OVER LIMIT"
        bb = whole.val().BoundingBox()
        print(f"  -> {key}: total {g_total:.0f} g solid-equivalent ({flag} vs {MASS_LIMIT_G:.0f} g), overall "
              f"{bb.xlen:.0f} wide x {bb.ylen:.0f} deep x {bb.zlen:.0f} tall (z {bb.zmin:.0f}..{bb.zmax:.0f}), "
              f"overlap with head {hit:.1f} mm3", flush=True)
        posed[key] = whole
    # append to a separate report (the base part report is left alone)
    rep = os.path.join(out, "shells_report.csv")
    old = {}
    if os.path.exists(rep):
        with open(rep, encoding="utf-8") as f:
            for line in f.read().splitlines()[1:]:
                if line.strip():
                    old[line.split(",")[0]] = line
    for r in rows:
        old[r[0]] = ",".join([r[0], str(r[1]), f"{r[2]:.1f}", f"{r[3]:.1f}", f"{r[4]:.1f}", f"{r[5]:.1f}", f"{r[6]:.1f}",
                              f"{r[7]:.1f}", '"' + r[8] + '"', str(r[9]), str(r[10]), str(r[11])])
    with open(rep, "w", encoding="utf-8") as f:
        f.write("file,copies,volume_cm3,x_mm,y_mm,z_mm,grams_25pct_rule,grams_near_solid,supports,valid,solids,stl_bytes\n")
        for k in sorted(old):
            f.write(old[k] + "\n")
    # coarse head-frame STLs for the preview
    for key, wp in posed.items():
        B.export_stl(wp, os.path.join(asm, key + ".stl"), tol=0.12, ang=0.35)
    if preview:
        render_preview(head_full)


# =====================================================================================
# preview picture (VTK off-screen; falls back to nothing if VTK is missing)
# =====================================================================================
PREVIEW_COLORS = {
    "cloud": (0.80, 0.90, 1.00), "pear": (0.62, 0.80, 0.35), "frog": (0.35, 0.72, 0.40), "heart": (0.95, 0.45, 0.55),
    "jolly": (0.90, 0.92, 0.96), "claude": (0.85, 0.47, 0.34), "beret": (0.75, 0.25, 0.30), "glasses": (0.15, 0.15, 0.18), "sunglasses": (0.10, 0.10, 0.12),
    "head": (0.96, 0.90, 0.78),
}


def render_preview(head_full):
    try:
        import vtk
    except Exception as e:  # pragma: no cover
        print("preview skipped (VTK not importable):", repr(e)[:120])
        return
    out = B.OUT_DIR
    pdir = os.path.join(out, "_assembly", "_shells", "_pose")
    os.makedirs(pdir, exist_ok=True)
    cloud_L, cloud_R = B.build_cloud_former_halves()
    items = []                                              # (label, workplane, colour key, dx, dz)
    row1 = [("cloud", cloud_L.union(cloud_R)), ("pear", None), ("frog", None), ("heart", None), ("jolly", None),
            ("claude", None)]
    asm = os.path.join(out, "_assembly", "_shells")
    step = 190.0                                            # six shells, the starburst is 186 mm wide
    x = 2.5 * step                                          # seen from the front +X is on the left of the picture
    for key, wp in row1:
        items.append((key, wp, key, x, 0.0, os.path.join(asm, key + ".stl")))
        x -= step
    row2 = [("beret", "beret"), ("glasses", "glasses"), ("sunglasses", "sunglasses")]
    x = 175.0
    for key, ck in row2:
        items.append(("head_" + key, head_full, "head", x, -200.0, None))
        items.append((key, None, ck, x, -200.0, os.path.join(asm, key + ".stl")))
        x -= 175.0
    ren = vtk.vtkRenderer()
    ren.SetBackground(1, 1, 1)
    ren.SetBackground2(0.88, 0.92, 0.97)
    ren.GradientBackgroundOn()
    for label, wp, ck, dx, dz, path in items:
        if path is None or not os.path.exists(path):
            if wp is None:
                continue
            path = os.path.join(pdir, label + ".stl")
            B.export_stl(wp.translate((dx, 0, dz)), path, tol=0.12, ang=0.35)
        elif label != "cloud":
            # asm STLs are in the head frame: re-export shifted copies
            import trimesh
            m = trimesh.load(path, force="mesh")
            m.apply_translation((dx, 0, dz))
            path = os.path.join(pdir, label + ".stl")
            m.export(path)
        if label == "cloud":
            path = os.path.join(pdir, "cloud.stl")
            B.export_stl(wp.translate((dx, 0, dz)), path, tol=0.12, ang=0.35)
        r = vtk.vtkSTLReader()
        r.SetFileName(path)
        r.Update()
        norm = vtk.vtkPolyDataNormals()
        norm.SetInputConnection(r.GetOutputPort())
        norm.SetFeatureAngle(50)
        norm.Update()
        mp = vtk.vtkPolyDataMapper()
        mp.SetInputConnection(norm.GetOutputPort())
        a = vtk.vtkActor()
        a.SetMapper(mp)
        a.GetProperty().SetColor(*PREVIEW_COLORS[ck])
        a.GetProperty().SetSpecular(0.25)
        ren.AddActor(a)
    txt = vtk.vtkTextActor()
    txt.SetInput("Top: cloud, pear, frog, heart, hooded Jolly, starburst Claude shells.   Bottom: beret, round glasses, sunglasses on the bare head.")
    txt.GetTextProperty().SetFontSize(24)
    txt.GetTextProperty().SetColor(0.1, 0.1, 0.15)
    txt.SetPosition(20, 960)
    ren.AddViewProp(txt)
    win = vtk.vtkRenderWindow()
    win.SetOffScreenRendering(1)
    win.SetSize(2000, 1000)
    win.SetMultiSamples(4)
    win.AddRenderer(ren)
    cam = ren.GetActiveCamera()
    cam.SetViewUp(0, 0, 1)
    cam.SetFocalPoint(0, 0, -50)
    cam.SetPosition(0, 1500, 60)                              # +Y is the front: look at the faces
    cam.Azimuth(-18)
    cam.SetViewAngle(24)
    ren.ResetCamera()
    cam.Zoom(1.42)                                            # six shells across the top row (was 1.55 for five)
    ren.ResetCameraClippingRange()
    win.Render()
    w2i = vtk.vtkWindowToImageFilter()
    w2i.SetInput(win)
    w2i.Update()
    png = os.path.join(out, "preview_shells.png")
    wr = vtk.vtkPNGWriter()
    wr.SetFileName(png)
    wr.SetInputConnection(w2i.GetOutputPort())
    wr.Write()
    print(f"preview: {png} (VTK off-screen)")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    bad = [a for a in args if a not in JOBS]
    if bad:
        raise SystemExit(f"unknown part(s) {bad}; choose from {list(JOBS)}")
    main(args or None, preview="--no-preview" not in sys.argv, build="--preview-only" not in sys.argv)
