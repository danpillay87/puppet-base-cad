r"""
Universal motorised puppet base - parametric CAD (CadQuery).
Run:  .venv\Scripts\python.exe build_puppet_base.py
Writes one STL per printable part into out/, plus out/_assembly/*.stl (placed parts for the preview).
All units are millimetres. Z is up. The turntable axis is the Z axis. +Y is the front of the puppet.

Every dimension lives in the PARAMETERS block below. Change a number, re-run, re-print.
Numbers marked (CHECK) are my best figures for hobby servos/bearings: measure yours before printing.
"""
import math
import os
import sys

import cadquery as cq

import print_settings as PS

# =====================================================================================
# PARAMETERS  (single source of truth)
# =====================================================================================
# --- general print rules -----------------------------------------------------------
WALL = 2.4              # general wall thickness
CLEAR = 0.2             # general fit clearance (per side where it matters)
HEAD_WALL = 1.6         # thin wall for the head sphere and the cloud former (keeps head mass down)
CHAMFER = 1.2           # 45 degree chamfer used instead of overhangs

# --- magnets / skin standard (same as Reachy Mini / Will Cogley) --------------------
MAG_D = 5.0             # magnet diameter
MAG_DEPTH = 2.0         # magnet thickness
MAG_COUNT = 6           # six magnets at 60 degrees
MAG_SKIN = 0.8          # plastic left over the magnet on the mating face
COLLAR_D = 110.0        # skin-ring / collar outside diameter
COLLAR_ID = 96.0        # skin-ring / collar inside diameter
COLLAR_T = 3.2          # collar flange thickness (pocket 2.2 + skin 0.8 + 0.2 spare)
MAG_PCD = 103.0         # pitch-circle diameter of the magnet pockets (centre of the ring band)

# --- servos ----------------------------------------------------------------------
# MG90S (metal-gear micro servo; the size in the shopping basket. Same body and tabs as the MG90D)
MG90_L, MG90_W, MG90_H = 22.8, 12.2, 28.5     # body: length (tab direction), width, height
MG90_TAB_SPAN = 32.5                          # overall length including the two M2 tabs
MG90_TAB_T = 1.6                              # tab thickness
MG90_TAB_TOP = 20.5                           # (CHECK) servo bottom -> top face of tabs
MG90_HOLE_DX = 27.8                           # (CHECK) M2 hole spacing along the length
MG90_HOLE_D = 2.0                             # pilot hole for an M2 self-tapping screw
MG90_SHAFT_OFF = 6.0                          # (CHECK) shaft centre from the nearer end of the body
MG90_SPLINE = 4.0                             # shaft stands this far above the body top
# MG996R (metal-gear standard servo)
MG996_L, MG996_W, MG996_H = 40.7, 19.7, 42.9
MG996_TAB_SPAN = 54.0                         # overall length including tabs
MG996_TAB_T = 2.6
MG996_TAB_TOP = 28.0                          # (CHECK) servo bottom -> top face of tabs
MG996_HOLE_DX = 49.5                          # (CHECK) M4 hole spacing along the length
MG996_HOLE_DY = 10.0                          # (CHECK) hole spacing across the width
MG996_HOLE_D = 3.4                            # pilot hole for M4 screw into plastic
MG996_SHAFT_OFF = 10.5                        # (CHECK) shaft centre from the nearer end of the body
MG996_SPLINE = 5.5                            # shaft stands this far above the body top

# --- base plate ---------------------------------------------------------------------
BASE_D = 160.0
BASE_R = BASE_D / 2
BASE_H = 48.0                                 # tall enough to hide the yaw servo (shaft up) and bays
BASE_LIM_R = BASE_R - 2.4                     # nothing pocketed beyond this radius
ESP32 = (55.0, 28.0)                          # dev board (long, short)
PCA9685 = (62.0, 25.0)
BUCK = (44.0, 21.0)
SPEAKER_D = 40.0
SPEAKER_DEPTH = 12.0
JACK_D = 12.0                                 # barrel jack panel hole
WASHER_OD = 30.0                              # steel washer for ballast (M16 flat washer)
WELL_DEPTH = 40.0
BOARD_BAY_DEPTH = 20.0
SPLIT_X = 0.0                                 # base, torso column and head split on a flat plane

# --- bearing + yaw ----------------------------------------------------------------
BEARING_OD = 72.0                             # lazy-susan bearing: 72 mm, the one in the shopping basket (B0FBLK3JLH)
BEARING_ID = 38.0                             # (CHECK) centre hole of the bearing
BEARING_H = 7.0                               # (CHECK)
SEAT_D = 1.2                                  # locating recess depth
BEARING_SCREW_R = 29.0                        # (CHECK) 3x M3 pattern: match your bearing's holes
PLATE_D = 150.0
PLATE_T = 5.0
HORN_D = 25.0                                 # (CHECK) stock round servo horn diameter
HORN_T = 3.2
HUB_D = 34.0

# --- torso column + bob ---------------------------------------------------------------
COL_OD = 104.0
COL_R = COL_OD / 2
COL_RIN = COL_R - WALL
COL_H = 100.0
COL_FOOT_R = 58.0                             # screw foot ring radius (outer)
LIFT_ZC = 82.0                                # lift servo centre height (absolute z)
LIFT_R = 24.0                                 # lever length (shaft to pin)
LIFT_SWING = 45.0                             # +/- degrees from horizontal -> throw = 2*R*sin
BOB_THROW = 2 * LIFT_R * math.sin(math.radians(LIFT_SWING))   # about 34 mm (target 30-40)
PIN_D = 5.0
CAR_T = 4.0                                   # carriage frame thickness
STEM_OD = 44.0
STEM_ID = 39.0

# --- neck gimbal ------------------------------------------------------------------
NOD_LIMIT = 30.0                              # +/- degrees
TILT_LIMIT = 25.0

# --- head -------------------------------------------------------------------------
HEAD_D = 120.0
HEAD_R = HEAD_D / 2

# --- shoulders / arms ------------------------------------------------------------
ARM_WIRE_D = 2.0                              # aluminium armature wire
SLEEVE_D = 35.0                               # plush sleeve diameter at the shoulder
SOCKET_STROKE = 80.0                          # +/- degrees

# =====================================================================================
# derived numbers (do not edit)
# =====================================================================================
Z_BEAR0 = BASE_H - SEAT_D                     # bearing bottom face
Z_BEAR1 = Z_BEAR0 + BEARING_H                 # bearing top face = plate underside
Z_PLATE_TOP = Z_BEAR1 + PLATE_T
Z_YAW_TOP = Z_BEAR0 - 0.2                     # top face of the yaw servo (sits just below bearing)
Z_HUB0 = Z_YAW_TOP + MG996_SPLINE - HORN_T - 0.3 + 0.0
Z_COL_TOP = Z_PLATE_TOP + COL_H
CAR_REST_Z = 99.0                             # carriage frame underside when fully down
# the sphere is cut flat at the collar: distance from the sphere centre down to the collar plane
HEAD_CUT_DZ = math.sqrt(HEAD_R ** 2 - (COLLAR_D / 2) ** 2)   # about 24 mm
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
ASM_DIR = os.path.join(OUT_DIR, "_assembly")

# =====================================================================================
# helpers
# =====================================================================================
def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def cylz(cx, cy, z0, z1, r):
    return cq.Workplane("XY").workplane(offset=z0).center(cx, cy).circle(r).extrude(z1 - z0)


def cylx(x0, x1, cy, cz, r):
    return cq.Workplane("YZ").workplane(offset=x0).center(cy, cz).circle(r).extrude(x1 - x0)


def cyly(y0, y1, cx, cz, r):
    # XZ workplane normal is -Y, so start at y1 and extrude toward y0
    return cq.Workplane("XZ").workplane(offset=-y1).center(cx, cz).circle(r).extrude(y1 - y0)


def hexz(cx, cy, z0, z1, across_flats):
    d = across_flats / math.cos(math.radians(30))
    return cq.Workplane("XY").workplane(offset=z0).center(cx, cy).polygon(6, d).extrude(z1 - z0)


def poly_x(pts, x0, x1):
    """Extrude a polygon given in (y, z) along X from x0 to x1."""
    return cq.Workplane("YZ").workplane(offset=x0).polyline(pts).close().extrude(x1 - x0)


def rot_z(wp, deg, about=(0, 0)):
    return wp.rotate((about[0], about[1], 0), (about[0], about[1], 1), deg)


def cut_all(base, tools):
    for t in tools:
        base = base.cut(t)
    return base


def union_all(items):
    out = items[0]
    for it in items[1:]:
        out = out.union(it)
    return out


def half(wp, side):
    """side = +1 keeps x>=SPLIT_X, -1 keeps x<=SPLIT_X."""
    big = 1000
    if side > 0:
        return wp.intersect(box(SPLIT_X, big, -big, big, -big, big))
    return wp.intersect(box(-big, SPLIT_X, -big, big, -big, big))


def vol_cm3(wp):
    return wp.val().Volume() / 1000.0


def check_inside(name, pts, rlim=BASE_LIM_R):
    """Assert every corner point sits inside the base wall limit."""
    for (x, y) in pts:
        if math.hypot(x, y) > rlim + 1e-6:
            raise ValueError(f"{name}: point ({x:.1f},{y:.1f}) is {math.hypot(x, y):.1f} mm out, limit {rlim:.1f}")


def rect_pts(cx, cy, w, h):
    return [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)]


def magnet_pockets(z_face, depth, open_dir):
    """Six magnet pockets on the pitch circle. z_face is the plane the pockets open on.
    open_dir = +1 pockets cut downward from z_face (they open on a top face),
               -1 pockets cut upward from z_face (they open on a bottom face)."""
    pd = MAG_D + CLEAR * 2          # 5.4 pocket
    items = []
    for i in range(MAG_COUNT):
        a = math.radians(i * 60)          # 0, 60, 120 ... deg: none lands on the x=0 split plane (90/270 deg)
        cx, cy = MAG_PCD / 2 * math.cos(a), MAG_PCD / 2 * math.sin(a)
        if open_dir > 0:
            items.append(cylz(cx, cy, z_face - depth, z_face + 0.01, pd / 2))
        else:
            items.append(cylz(cx, cy, z_face - 0.01, z_face + depth, pd / 2))
    return items


MAG_POCKET_DEPTH = MAG_DEPTH + CLEAR   # 2.2

# =====================================================================================
# 1  BASE PLATE (two halves)
# =====================================================================================
BASE_BAYS = {                                       # (cx, cy, size_x, size_y): electronics bays, open on top
    "pca9685": (56.0, 0.0, PCA9685[1], PCA9685[0]),     # long axis along Y
    "esp32": (-56.0, 0.0, ESP32[1], ESP32[0]),
    "buck": (28.0, 48.0, BUCK[0], BUCK[1]),             # long axis along X; y 48 keeps 1.5 mm to the 72 mm bearing seat
}
BASE_WELLS = ((22.0, -55.0), (-32.0, 49.0))         # washer ballast wells
JACK_POCKET_R = 60.0                                # barrel-jack nut pocket centre radius (at -135 degrees)
SPEAKER_Y1 = 74.0                                   # front face of the speaker pocket
BASE_LANE_X = (-42.5, 44.0)                         # cable lane from the yaw servo to the ESP32 and PCA9685 bays
FOOT_PCR, FOOT_R, FOOT_DEPTH = 58.0, 6.1, 1.5       # rubber feet recesses
# --- hollowing: open-top pockets, kept only where they save plastic at the settings in print_settings.py ----------
BASE_FLOOR_T = 3.0                                  # solid floor under every pocket
BASE_POCKET_R = BASE_R - WALL - 0.6                 # pockets stop inside a 3 mm outer wall
BASE_KEEP = WALL                                    # full-strength wall kept round the servo, bays, wells, jack, speaker, lane, screws, feet
POCKET_MIN_RATIO = 2.5                              # mm; never cut a pocket thinner than this, whatever the infill
BASE_BAY_LEDGE = {"pca9685": 3.0, "esp32": 2.5, "buck": 2.5}   # a board rests on ledges this long at its two short ends
BASE_POCKETS_REPORT = []                            # (name, cm3, volume/new-wall ratio mm, grams saved, kept?) from the last build


def base_disc():
    b = cylz(0, 0, 0, BASE_H, BASE_R)
    b = b.faces("<Z").chamfer(CHAMFER)
    return b.faces(">Z").chamfer(1.0)


def build_base_full():
    return cut_all(base_disc(), base_feature_tools(split_join=True))


def base_feature_tools(split_join=False):
    """Every cut the base needs to hold its parts. split_join adds the screw wells and holes that join the two halves."""
    tools = []
    # bearing seat
    tools.append(cylz(0, 0, BASE_H - SEAT_D, BASE_H + 1, BEARING_OD / 2 + CLEAR))

    # yaw servo (MG996R, shaft up) - body pocket, tab slot, tab screw pilots
    bx = (MG996_L + 2 * CLEAR) / 2
    by = (MG996_W + 2 * CLEAR) / 2
    tab_top_z = Z_YAW_TOP - (MG996_H - MG996_TAB_TOP)
    ledge_z = tab_top_z - MG996_TAB_T               # underside of the tabs rests here
    tools.append(box(-bx, bx, -by, by, 3.0, ledge_z + 0.01))                       # body pocket
    sx = (MG996_TAB_SPAN + 2 * CLEAR) / 2
    tools.append(box(-sx, sx, -by, by, ledge_z, BASE_H + 1))                       # tab slot
    for sx_ in (-1, 1):
        for sy_ in (-1, 1):
            tools.append(cylz(sx_ * MG996_HOLE_DX / 2, sy_ * MG996_HOLE_DY / 2, -1, ledge_z + 0.01, MG996_HOLE_D / 2))   # through: no trapped support
    # cable lane: servo lead -> up a groove -> sideways under the bearing to the ESP32 and PCA9685 bays
    tools.append(box(-3, 3, by - 0.2, by + 4, 3.0, ledge_z + 12))
    tools.append(box(BASE_LANE_X[0], BASE_LANE_X[1], by - 0.2, by + 6, ledge_z, ledge_z + 11))

    # electronics bays (open on top, covered by the turntable plate)
    for name, (cx, cy, sx_, sy_) in BASE_BAYS.items():
        w, h = sx_ + 2 * CLEAR, sy_ + 2 * CLEAR
        check_inside(name, rect_pts(cx, cy, w, h))
        tools.append(box(cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2, BASE_H - BOARD_BAY_DEPTH, BASE_H + 1))

    # washer ballast wells (two deep round wells)
    wr = WASHER_OD / 2 + 0.3
    for (cx, cy) in BASE_WELLS:
        check_inside("well", [(cx + wr * math.cos(a), cy + wr * math.sin(a)) for a in [i * math.pi / 6 for i in range(12)]])
        tools.append(cylz(cx, cy, BASE_H - WELL_DEPTH, BASE_H + 1, wr))

    # speaker: top-open pocket facing the front wall, with a diamond sound port (no overhang)
    sp_r = SPEAKER_D / 2 + 0.2
    y1, y0 = SPEAKER_Y1, SPEAKER_Y1 - SPEAKER_DEPTH
    check_inside("speaker", [(-sp_r, y1), (sp_r, y1)])
    tools.append(box(-sp_r, sp_r, y0, y1, 3.8, BASE_H + 1))
    port = cq.Workplane("XZ").workplane(offset=-(BASE_R + 5)).center(0, 24.0).polygon(4, 2 * 19.0).extrude(BASE_R + 5 - (y1 - 0.5))
    tools.append(port.rotate((0, 0, 24.0), (0, 1, 24.0), 45))

    # barrel jack: radial hole at -135 degrees + vertical nut pocket
    ja = math.radians(-135)
    jd = (math.cos(ja), math.sin(ja))
    # build along +X then rotate to the jack angle
    jack = cylx(56.0, BASE_R + 5, 0, 24.0, JACK_D / 2)
    jack = jack.rotate((0, 0, 0), (0, 0, 1), -135)
    tools.append(jack)
    jp = (JACK_POCKET_R * jd[0], JACK_POCKET_R * jd[1])
    check_inside("jack pocket", [(jp[0] + 9 * math.cos(a), jp[1] + 9 * math.sin(a)) for a in [i * math.pi / 4 for i in range(8)]])
    tools.append(cylz(jp[0], jp[1], 12.0, BASE_H + 1, 9.0))

    # bearing screw pilots (3x M3)
    for k in range(3):
        a = math.radians(90 + k * 120)
        tools.append(cylz(BEARING_SCREW_R * math.cos(a), BEARING_SCREW_R * math.sin(a), BASE_H - SEAT_D - 9, BASE_H - SEAT_D + 0.01, 1.35))

    # rubber feet recesses
    for k in range(4):
        a = math.radians(45 + 90 * k)
        tools.append(cylz(FOOT_PCR * math.cos(a), FOOT_PCR * math.sin(a), -0.01, FOOT_DEPTH, FOOT_R))

    # half-to-half joining: two screw shafts (vertical well + horizontal M3 through-hole), 3 dowel holes
    if split_join:
        for (sy_) in (-44.0, 49.0):
            tools.append(cylz(-6.0, sy_, 12.0, BASE_H + 1, 4.5))                   # driver access well (left half)
            tools.append(cylx(-6.0, 0.0, sy_, 14.0 if False else 16.0, 1.75))      # clearance through to the split face
    return tools


def base_screw_pilots(wp, side):
    """Right half gets blind M3 pilot holes that continue the screw line; both halves get dowel holes."""
    items = []
    if side > 0:
        for sy_ in (-44.0, 49.0):
            items.append(cylx(0.0, 6.0, sy_, 16.0, 1.35))
    for (y_, z_) in ((25.0, 12.0), (-25.0, 12.0), (25.0, 40.0)):
        if side > 0:
            items.append(cylx(0.0, 8.0, y_, z_, 2.1))
        else:
            items.append(cylx(-8.0, 0.0, y_, z_, 2.1))
    return cut_all(wp, items)


def build_base_halves():
    """The old two-piece base (not hollowed, not exported any more): only for a bed smaller than 165 mm."""
    full = build_base_full()
    left = base_screw_pilots(half(full, -1), -1)
    right = base_screw_pilots(half(full, +1), +1)
    return left, right


def pocket_break_even():
    """A pocket saves plastic only when its volume / the new wall area it adds beats this (mm): skin * (1 - infill) / infill."""
    f = PS.INFILL
    if f <= 0:
        return float("inf")
    return max(POCKET_MIN_RATIO, PS.skin_mm() * (1 - f) / f)


def base_keep_solids(skip=()):
    """Regions the hollowing must not touch: everything that holds a part, plus a BASE_KEEP wall round it.
    Each runs from the floor to the top, so every pocket is a plain open-top well with nothing overhanging it."""
    k, z0, z1 = BASE_KEEP, BASE_FLOOR_T - 0.01, BASE_H + 1
    bx = (MG996_TAB_SPAN + 2 * CLEAR) / 2
    by = (MG996_W + 2 * CLEAR) / 2
    r_core = max(math.hypot(bx, by), BEARING_SCREW_R + 1.35) + k       # yaw-servo tab slot and the bearing screw pilots
    r_seat = BEARING_OD / 2 + CLEAR + k                                  # round the bearing seat
    z_seat = Z_BEAR0 - k                                                 # solid floor under the seat
    z_flare = z_seat - (r_seat - r_core)                                 # 45 degree flare from the core out under the seat
    keep = [cq.Workplane("XZ").polyline([(0, z0), (r_core, z0), (r_core, z_flare), (r_seat, z_seat), (r_seat, z1), (0, z1)])
            .close().revolve(360, (0, 0, 0), (0, 1, 0))]
    if "bays" not in skip:
        for (cx, cy, sx_, sy_) in BASE_BAYS.values():
            w, h = sx_ + 2 * CLEAR + 2 * k, sy_ + 2 * CLEAR + 2 * k
            keep.append(box(cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2, z0, z1))
    if "lane" not in skip:
        keep.append(box(BASE_LANE_X[0] - k, BASE_LANE_X[1] + k, by - 0.2 - k, by + 6 + k, z0, z1))
    for (cx, cy) in BASE_WELLS:
        keep.append(cylz(cx, cy, z0, z1, WASHER_OD / 2 + 0.3 + k))
    sp_r = SPEAKER_D / 2 + 0.2 + k
    keep.append(box(-sp_r, sp_r, SPEAKER_Y1 - SPEAKER_DEPTH - k, SPEAKER_Y1 + k, z0, z1))
    ja = math.radians(-135)
    keep.append(cylz(JACK_POCKET_R * math.cos(ja), JACK_POCKET_R * math.sin(ja), z0, z1, 9.0 + k))
    keep.append(rot_z(box(JACK_POCKET_R - 10.0, BASE_R + 1, -(JACK_D / 2 + k), JACK_D / 2 + k, z0, z1), -135))
    for kk in range(4):
        a = math.radians(45 + 90 * kk)
        keep.append(cylz(FOOT_PCR * math.cos(a), FOOT_PCR * math.sin(a), z0, 6.0, FOOT_R + k))   # solid pad over each foot
    return keep


def _pocket_if_it_pays(name, s, need, z_top, ext):
    """Measure one candidate pocket (a Solid whose top face is at z_top, ext mm above the part's top) and keep it only
    if volume / new wall area >= need. Grams saved follow the same weight model as print_cost.py."""
    tops = [f for f in s.Faces() if abs(f.Center().z - z_top) < 1e-3 and f.normalAt().z > 0.99]
    top = sum(f.Area() for f in tops)
    perim = sum(e.Length() for f in tops for e in f.Edges())
    v = s.Volume() - top * ext
    a = s.Area() - perim * ext - 2 * top            # new wall area: the pocket floor replaces the top face it opens
    ratio = v / a if a > 0 else float("inf")
    saved = (PS.INFILL * v - (1 - PS.INFILL) * PS.skin_mm() * a) * PS.DENSITY / 1000.0
    kept = ratio >= need
    BASE_POCKETS_REPORT.append((name, v / 1000.0, ratio, saved, kept))
    return [s] if kept else []


def base_pocket_tools():
    """Open-top pockets that hollow the base wherever they save plastic at the current print settings.
    Main pockets fill the room between the keep regions; under-bay voids deepen each bay below its board ledges
    (they also give the ESP32's header pins room)."""
    BASE_POCKETS_REPORT.clear()
    need = pocket_break_even()
    z1 = BASE_H + 1
    cand = cut_all(cylz(0, 0, BASE_FLOOR_T, z1, BASE_POCKET_R), base_keep_solids())
    tools = []
    for i, s in enumerate(cand.solids().vals()):
        tools += _pocket_if_it_pays(f"pocket {i + 1}", s, need, z1, z1 - BASE_H)
    zb = BASE_H - BOARD_BAY_DEPTH + 0.01
    others = base_keep_solids(skip=("bays", "lane"))
    for name, (cx, cy, sx_, sy_) in BASE_BAYS.items():
        w, h = sx_ + 2 * CLEAR, sy_ + 2 * CLEAR
        led = BASE_BAY_LEDGE[name]
        dx, dy = (led, 0.0) if w > h else (0.0, led)
        v = cut_all(box(cx - w / 2 + dx, cx + w / 2 - dx, cy - h / 2 + dy, cy + h / 2 - dy, BASE_FLOOR_T, zb), others)
        for s in v.solids().vals():
            tools += _pocket_if_it_pays(f"under {name}", s, need, zb, 0.0)
    return tools


def build_base_one():
    """One-piece base (it fits a 220 mm bed): every feature of the old halves, no split joins, hollowed where it pays."""
    return cut_all(base_disc(), base_feature_tools() + base_pocket_tools())


# =====================================================================================
# 2  TURNTABLE  (plate + horn hub + bearing seat + lift-servo cradle + column foot nut traps)
# =====================================================================================
LIFT_BODY_Y = (MG996_H) / 2                    # servo body half length along Y (lying, shaft along +Y)
LIFT_TAB_Y = LIFT_BODY_Y - (MG996_H - MG996_TAB_TOP)        # y of the tab top face (toward shaft)
LIFT_WALL_Y0 = LIFT_TAB_Y
LIFT_WALL_Y1 = LIFT_TAB_Y + 8.0
LIFT_SHAFT_X = -(MG996_L / 2 - MG996_SHAFT_OFF)             # shaft x (servo centred in x)
LIFT_SHAFT_Y = LIFT_BODY_Y + MG996_SPLINE                   # tip of the spline


def column_screw_points():
    pts = []
    for a in (-55, 0, 55, 125, 180, 235):
        r = (COL_FOOT_R + COL_R) / 2
        pts.append((r * math.cos(math.radians(a)), r * math.sin(math.radians(a))))
    return pts


HUB_SCREW_R = 9.0                               # 4x M2 up through the yaw horn and the hub into the plate
HUB_RECESS = HORN_T + 0.4                       # the stock horn sits in this recess under the hub


def build_turntable():
    """Plate with the lift-servo cradle. Prints plate-down, cradle up, with no supports: the horn hub is its own part
    (build_turntable_hub), the bearing's top ring screws flat to the underside, and the servo slot is open at the top."""
    z0 = Z_BEAR1
    t = cylz(0, 0, z0, Z_PLATE_TOP, PLATE_D / 2)
    t = t.faces("<Z").chamfer(CHAMFER)
    t = t.faces(">Z").chamfer(CHAMFER)

    # lift-servo cradle: a wall in the XZ plane carrying the MG996R on its side (shaft along +Y)
    wx = (MG996_TAB_SPAN + 8.4) / 2
    wall = box(-wx, wx, LIFT_WALL_Y0, LIFT_WALL_Y1, Z_PLATE_TOP - 0.01, LIFT_ZC + 15.0)
    gus = []
    for sx_ in (-1, 1):
        x0 = sx_ * (wx - 3.5)
        gus.append(poly_x([(LIFT_WALL_Y0, Z_PLATE_TOP - 0.01), (LIFT_WALL_Y0 - 20.5, Z_PLATE_TOP - 0.01), (LIFT_WALL_Y0, Z_PLATE_TOP + 20.5)],
                          min(x0, x0 + sx_ * 3.5), max(x0, x0 + sx_ * 3.5)))
    t = t.union(wall)
    for g in gus:
        t = t.union(g)
    # extension-spring lug on the plate (carriage has the mating lug)
    t = t.union(box(-5, 5, -34.0, -29.0, Z_PLATE_TOP - 0.01, Z_PLATE_TOP + 9.0))

    tools = []
    # centre screw access + 4 pilots (through) for the M2 screws that hold the hub and horn to the plate
    tools.append(cylz(0, 0, z0 - 1, Z_PLATE_TOP + 1, 3.6))
    for k in range(4):
        a = math.radians(45 + 90 * k)
        tools.append(cylz(HUB_SCREW_R * math.cos(a), HUB_SCREW_R * math.sin(a), z0 - 1, Z_PLATE_TOP + 1, 0.95))
    # 3 bearing screws
    for k in range(3):
        a = math.radians(90 + k * 120)
        tools.append(cylz(BEARING_SCREW_R * math.cos(a), BEARING_SCREW_R * math.sin(a), z0 - 0.01, Z_PLATE_TOP + 1, 1.7))
    # column screws: 3.4 through, hex nut trap underneath
    for (x, y) in column_screw_points():
        tools.append(cylz(x, y, z0 - 0.01, Z_PLATE_TOP + 1, 1.7))
        tools.append(hexz(x, y, z0 - 0.01, z0 + 2.8, 5.8))
    # servo slot in the cradle wall, open at the top (the servo drops in; no bridge to print) + 4 M4 pilots
    ww = (MG996_L + 2 * CLEAR) / 2
    wz = (MG996_W + 2 * CLEAR) / 2
    tools.append(box(-ww, ww, LIFT_WALL_Y0 - 0.01, LIFT_WALL_Y1 + 0.01, LIFT_ZC - wz, LIFT_ZC + 16.0))
    for sx_ in (-1, 1):
        for sz_ in (-1, 1):
            tools.append(cyly(LIFT_WALL_Y0 - 0.01, LIFT_WALL_Y1 + 1.0, sx_ * MG996_HOLE_DX / 2, LIFT_ZC + sz_ * MG996_HOLE_DY / 2, MG996_HOLE_D / 2))   # through the wall
    # spring lug hole
    tools.append(cyly(-35.0, -28.0, 0, Z_PLATE_TOP + 5.0, 1.3))
    return cut_all(t, tools)


def build_turntable_hub():
    """Horn hub (assembly frame): a disc between the yaw horn and the plate underside, inside the bearing's centre hole.
    Four M2 screws go up through the horn and the hub into the plate. Prints upside down (floor on the bed), no supports."""
    h = cylz(0, 0, Z_HUB0, Z_BEAR1, HUB_D / 2).faces("<Z").chamfer(CHAMFER)
    tools = [cylz(0, 0, Z_HUB0 - 0.01, Z_HUB0 + HUB_RECESS, HORN_D / 2 + CLEAR),
             cylz(0, 0, Z_HUB0 - 1, Z_BEAR1 + 1, 3.6)]
    for k in range(4):
        a = math.radians(45 + 90 * k)
        tools.append(cylz(HUB_SCREW_R * math.cos(a), HUB_SCREW_R * math.sin(a), Z_HUB0 - 1, Z_BEAR1 + 1, 1.1))
    return cut_all(h, tools)


# =====================================================================================
# 3  TORSO COLUMN (two halves) - fixed to the turntable; two side guide channels are the "bob rails"
# =====================================================================================
ARM_H = 18.0                                   # height of the slider block / arm through the wall
SLOT_HALF = 4.2                                # half width of the vertical slot (block is 4.0 each side)
SLOT_Z0 = CAR_REST_Z - 2.0
SLOT_Z1 = CAR_REST_Z + ARM_H + BOB_THROW + 2.5  # slot top
RIB_IN = 5.0                                   # guide ribs stand this far inside the wall
STEM_TOP_Z = Z_COL_TOP + 3.2                   # carriage stem top when the carriage is fully down


def build_column_full():
    z0 = Z_PLATE_TOP
    c = cylz(0, 0, z0, Z_COL_TOP, COL_R).cut(cylz(0, 0, z0 - 1, Z_COL_TOP + 1, COL_RIN))
    c = c.union(cylz(0, 0, z0, z0 + 3.0, COL_FOOT_R).cut(cylz(0, 0, z0 - 1, z0 + 4, COL_RIN)))
    # guide ribs either side of each slot (these are the two bob rails)
    for sx in (-1, 1):
        for sy in (-1, 1):
            xa, xb = sx * (COL_RIN - RIB_IN), sx * (COL_RIN + 0.9)
            ya, yb = sy * SLOT_HALF, sy * (SLOT_HALF + 4.0)
            c = c.union(box(min(xa, xb), max(xa, xb), min(ya, yb), max(ya, yb), SLOT_Z0 - 4, SLOT_Z1 + 3))
    # joining lugs on the split plane (profile has a 45 degree underside so it prints without support)
    for zc in (z0 + 12.0, z0 + 50.0, z0 + 86.0):
        for sy in (-1, 1):
            pts = [(40.0, zc + 4), (49.8, zc + 4), (49.8, zc - 9.8), (40.0, zc)]
            pts = [(sy * y, z) for (y, z) in pts]
            c = c.union(poly_x(pts, -10.0, 10.0))
    tools = []
    for sx in (-1, 1):
        tools.append(box(min(sx * (COL_RIN - RIB_IN - 1), sx * (COL_R + 2)), max(sx * (COL_RIN - RIB_IN - 1), sx * (COL_R + 2)),
                         -SLOT_HALF, SLOT_HALF, SLOT_Z0, SLOT_Z1))
    for (x, y) in column_screw_points():
        tools.append(cylz(x, y, z0 - 1, z0 + 4, 1.7))
    for zc in (z0 + 12.0, z0 + 50.0, z0 + 86.0):
        for sy in (-1, 1):
            tools.append(cylx(-10.5, 0.0, sy * 45.0, zc + 1.5, 1.7))       # clearance (left half)
            tools.append(cylx(0.0, 8.0, sy * 45.0, zc + 1.5, 1.35))        # pilot (right half)
    return cut_all(c, tools)


def build_column_halves():
    full = build_column_full()
    left = half(full, -1)
    right = half(full, +1)
    # keep each half's holes only on its own side: left half lost its pilots (they start at x>=0), right half lost clearance holes
    return left, right


# =====================================================================================
# 4  BOB CARRIAGE (slides in the two channels, lifted by the lever through the yoke)
# =====================================================================================
FRAME_R = 43.0
FRAME_FLAT_Y = 38.5
BLOCK_X0, BLOCK_X1 = 40.0, 56.0
LEVER_T = 5.0
LEVER_Y0 = LIFT_BODY_Y + 2.5                    # lever sits on the stock horn, just beyond the servo body
LEVER_Y1 = LEVER_Y0 + LEVER_T
YOKE_X0, YOKE_X1 = 0.0, 21.5
YOKE_Y0, YOKE_Y1 = 31.0, 34.0
YOKE_FLANGE_Y1 = 38.0
YOKE_BOTTOM_Z = Z_PLATE_TOP + 1.7
PIN_X_LOW = LIFT_SHAFT_X + LIFT_R * math.cos(math.radians(LIFT_SWING))
PIN_X_HIGH = LIFT_SHAFT_X + LIFT_R
PIN_Z_LOW = LIFT_ZC - LIFT_R * math.sin(math.radians(LIFT_SWING))   # pin height with the carriage fully down


def build_carriage():
    z0 = CAR_REST_Z
    f = cylz(0, 0, z0, z0 + CAR_T, FRAME_R).intersect(box(-60, 60, -FRAME_FLAT_Y, FRAME_FLAT_Y, z0 - 1, z0 + 10))
    f = f.faces("<Z").chamfer(0.8)
    # stem (hollow) rising to the neck
    f = f.union(cylz(0, 0, z0, STEM_TOP_Z, STEM_OD / 2))
    # 45 degree fillet ring at the stem foot
    cone = cq.Workplane("XZ").polyline([(STEM_OD / 2, z0 + CAR_T - 0.01), (STEM_OD / 2 + 9, z0 + CAR_T - 0.01), (STEM_OD / 2, z0 + CAR_T + 9)]).close().revolve(360, (0, 0, 0), (0, 1, 0))
    f = f.union(cone)
    # slider blocks that run in the wall channels and carry the shoulders
    for sx in (-1, 1):
        xa, xb = sx * BLOCK_X0, sx * BLOCK_X1
        f = f.union(box(min(xa, xb), max(xa, xb), -4.0, 4.0, z0, z0 + ARM_H))
    tools = [cylz(0, 0, z0 - 1, STEM_TOP_Z + 1, STEM_ID / 2)]
    # shoulder bolt holes (2x M3 along X into each block end)
    for sx in (-1, 1):
        for dz in (-5.0, 5.0):
            tools.append(cylx(min(sx * (BLOCK_X1 - 12), sx * BLOCK_X1 + sx * 0.01), max(sx * (BLOCK_X1 - 12), sx * BLOCK_X1 + sx * 0.01), 0, z0 + ARM_H / 2 + dz, 1.35))
    # yoke screws (2x M3 from above) and spring hook screw hole
    for x in (4.0, YOKE_X1 - 4.0):
        tools.append(cylz(x, (YOKE_Y0 + YOKE_FLANGE_Y1) / 2, z0 - 1, z0 + CAR_T + 1, 1.7))
    tools.append(cylz(0, -32.0, z0 - 1, z0 + CAR_T + 1, 1.7))
    # two cross-screw holes through the stem wall near the top (M3 into the neck plug)
    tools.append(cylx(-30, 30, 0, STEM_TOP_Z - 6.0, 1.7))
    tools.append(cyly(-30, 30, 0, STEM_TOP_Z - 11.0, 1.7))
    return cut_all(f, tools)


def build_yoke():
    """Inverted-T bracket screwed under the carriage; the lever pin rides in its horizontal slot."""
    z_top = CAR_REST_Z
    flange = box(YOKE_X0, YOKE_X1, YOKE_Y0, YOKE_FLANGE_Y1, z_top - 3.0, z_top)
    blade = box(YOKE_X0, YOKE_X1, YOKE_Y0, YOKE_Y1, YOKE_BOTTOM_Z, z_top - 2.9)
    y = flange.union(blade)
    # 45 degree stiffening gusset on the +Y side of the flange is not needed (flange is wide); chamfer the blade bottom corners
    slot_h = PIN_D + 0.4
    sx0, sx1 = PIN_X_LOW - PIN_D / 2 - 0.2, PIN_X_HIGH + PIN_D / 2 + 0.2
    slot = box(sx0, sx1, YOKE_Y0 - 1, YOKE_Y1 + 1, PIN_Z_LOW - slot_h / 2, PIN_Z_LOW + slot_h / 2)
    tools = [slot]
    for x in (4.0, YOKE_X1 - 4.0):
        tools.append(cylz(x, (YOKE_Y0 + YOKE_FLANGE_Y1) / 2, z_top - 4, z_top + 1, 1.35))
    return cut_all(y, tools)


def build_lever():
    """Flat lever in its own XY frame: hub at the origin, pin at +X. Thickness along +Z (print flat)."""
    L = LIFT_R
    hub = cq.Workplane("XY").circle(10.0).extrude(LEVER_T)
    arm = cq.Workplane("XY").center(L / 2, 0).rect(L, 12.0).extrude(LEVER_T)
    boss = cylz(L, 0, 0, LEVER_T, 7.0)
    lv = hub.union(arm).union(boss)
    lv = lv.faces(">Z").edges().chamfer(0.6) if False else lv
    tools = [cylz(0, 0, -1, LEVER_T + 1, 4.2)]                                  # clearance for the horn screw
    for k in range(4):
        a = math.radians(45 + 90 * k)
        tools.append(cylz(7.0 * math.cos(a), 7.0 * math.sin(a), -1, LEVER_T + 1, 1.2))   # screws to the stock horn
    tools.append(cylz(L, 0, -1, LEVER_T + 1, 2.7))                              # M5 pin
    tools.append(hexz(L, 0, -0.01, 3.2, 8.4))                                   # M5 head pocket (underside)
    return cut_all(lv, tools)


# =====================================================================================
# 5  NECK GIMBAL (3 printed parts: base A, rocker B, head plate C) - nod about X, tilt about Y
# =====================================================================================
# Local frame: origin on the stem axis at the underside of the neck flange (add STEM_TOP_Z + bob to place it).
G_FLANGE_D = 62.0
G_FLANGE_T = 4.0
G_ZN = 30.0                    # nod axis height above the flange underside
G_ZT = G_ZN + 16.0             # tilt axis height
G_UP_IN = 27.0                 # A upright inner faces at x = +/-27
G_UP_T = 4.0                   # A upright thickness
G_B_OUT = 20.4                 # B outer half width (x), set by the stock horn on the nod servo
G_B_WALL = 5.0
G_B_Y = 22.0                   # B outer half length (y); front wall carries the tilt servo
G_B_FRONT_T = 5.0
G_C_PLATE_Z0 = G_ZT + 23.0     # underside of the head plate (relative to flange underside); +3 over the first try bought clearance at full nod-back
G_C_PLATE_T = 4.0
G_C_PLATE_D = 88.0
G_C_SCREW_R = 38.0
NECK_TOP = G_C_PLATE_Z0 + G_C_PLATE_T          # top face of the head plate (rel. to flange underside)
M2_SHAFT = 1.8                                  # clearance hole for the MG90S spline tip: use Ø7 (below)


G_PLUG_Z0 = -16.0                               # plug and sleeve run this far down the stem (the sleeve needs it for its 45 degree flare)
G_SLEEVE_IN = STEM_OD / 2 + 0.4                 # sleeve round the outside of the stem top
G_SLEEVE_OUT = G_SLEEVE_IN + WALL


def build_neck_base():
    """A: plug inside the stem, a sleeve round it, flange, two uprights; right upright carries the nod servo (shaft along X).
    The sleeve flares out at 45 degrees under the flange and the uprights, so A prints plug-down with no supports."""
    t = cylz(0, 0, G_PLUG_Z0, 0.01, 38.4 / 2)
    t = t.union(cylz(0, 0, 0, G_FLANGE_T, G_FLANGE_D / 2))
    foot = cylz(0, 0, G_PLUG_Z0 - 1, 0.02, G_FLANGE_D / 2)
    for sx in (-1, 1):
        xa, xb = sx * G_UP_IN, sx * (G_UP_IN + G_UP_T)
        t = t.union(box(min(xa, xb), max(xa, xb), -15.0, 26.0, -0.01, G_ZN + 12.0))
        foot = foot.union(box(min(xa, xb), max(xa, xb), -15.0, 26.0, G_PLUG_Z0 - 1, 0.02))
    r_top = G_SLEEVE_OUT - G_PLUG_Z0                # 45 degrees: the flare reaches this radius at the flange underside
    skirt = (cq.Workplane("XZ").polyline([(G_SLEEVE_IN, G_PLUG_Z0), (G_SLEEVE_OUT, G_PLUG_Z0), (r_top, 0.0), (G_SLEEVE_IN, 0.0)])
             .close().revolve(360, (0, 0, 0), (0, 1, 0)))
    t = t.union(skirt.intersect(foot))              # only under the flange and the uprights
    tools = [cylz(0, 0, G_PLUG_Z0 - 1, G_FLANGE_T + 1, 30.0 / 2)]            # cable hole
    # cross screws (match the stem holes at -6 and -11): pilot in the plug, clearance through stem and sleeve, counterbore
    for (z, hole) in ((-6.0, cylx), (-11.0, cyly)):
        tools.append(hole(-19.3, 19.3, 0, z, 1.35))
        for s in (-1, 1):
            tools.append(hole(*sorted((s * 19.3, s * 45.0)), 0, z, 1.7))
            tools.append(hole(*sorted((s * G_SLEEVE_OUT, s * 45.0)), 0, z, 3.2))
    # left pivot hole (M3 through the upright into B's boss)
    tools.append(cylx(-(G_UP_IN + G_UP_T) - 1, -G_UP_IN + 1, 0, G_ZN, 1.7))
    # right upright: window for the MG90S (L along Y, shaft at y=0), M2 pilots in the tab line
    y0, y1 = -MG90_SHAFT_OFF - CLEAR, MG90_L - MG90_SHAFT_OFF + CLEAR
    tools.append(box(G_UP_IN - 1, G_UP_IN + G_UP_T + 1, y0, y1, G_ZN - MG90_W / 2 - CLEAR, G_ZN + MG90_W / 2 + CLEAR))
    yc = (MG90_L / 2) - MG90_SHAFT_OFF
    for sy in (-1, 1):
        tools.append(cylx(G_UP_IN - 0.01, G_UP_IN + G_UP_T + 0.01, yc + sy * MG90_HOLE_DX / 2, G_ZN, MG90_HOLE_D / 2))   # through the upright
    return cut_all(t, tools)


def build_neck_rocker():
    """B: open box that rocks about X (nod); front wall carries the tilt servo (shaft along -Y)."""
    zb0, zb1 = G_ZN - 12.0, G_ZT + 3.0
    # the front and back walls run up to G_ZT + 7.5; the side walls only to zb1
    b = box(-G_B_OUT, G_B_OUT, -G_B_Y, G_B_Y, zb0, G_ZT + 7.5)
    b = b.cut(box(-G_B_OUT + G_B_WALL, G_B_OUT - G_B_WALL, -G_B_Y + G_B_FRONT_T, G_B_Y - G_B_FRONT_T, zb0 + 4.0, G_ZT + 20))
    # lower the side walls: remove their top between the front and back walls
    b = b.cut(box(-G_B_OUT - 1, -G_B_OUT + G_B_WALL + 0.0, -G_B_Y + G_B_FRONT_T, G_B_Y - G_B_FRONT_T, zb1, G_ZT + 20))
    b = b.cut(box(G_B_OUT - G_B_WALL, G_B_OUT + 1, -G_B_Y + G_B_FRONT_T, G_B_Y - G_B_FRONT_T, zb1, G_ZT + 20))
    # front wall widened to the right to take the tilt servo tabs
    b = b.union(box(G_B_OUT - 0.01, 24.0, G_B_Y - G_B_FRONT_T, G_B_Y, zb0, G_ZT + 7.5))
    # left pivot boss (toward A's left upright)
    b = b.union(cylx(-G_UP_IN + 0.5, -G_B_OUT + 0.01, 0, G_ZN, 4.5))
    tools = []
    tools.append(cylx(-G_UP_IN + 1, -G_B_OUT + 6, 0, G_ZN, 1.35))                         # pilot for pivot screw
    # right wall: hole for the nod-servo spline tip + 2 horn screws
    tools.append(cylx(G_B_OUT - G_B_WALL - 1, G_B_OUT + 1, 0, G_ZN, 3.5))
    for sz in (-1, 1):
        tools.append(cylx(G_B_OUT - 6.0, G_B_OUT + 0.01, 0, G_ZN + sz * 7.0, 0.95))
    # front wall: window for the tilt MG90S (L along X, shaft at x=0), tab pilots
    xo = (MG90_L / 2) - MG90_SHAFT_OFF
    x0, x1 = -MG90_SHAFT_OFF - CLEAR, MG90_L - MG90_SHAFT_OFF + CLEAR
    tools.append(box(x0, x1, G_B_Y - G_B_FRONT_T - 1, G_B_Y + 1, G_ZT - MG90_W / 2 - CLEAR, G_ZT + MG90_W / 2 + CLEAR))
    for sx in (-1, 1):
        tools.append(cyly(G_B_Y - G_B_FRONT_T - 0.01, G_B_Y + 0.01, xo + sx * MG90_HOLE_DX / 2, G_ZT, MG90_HOLE_D / 2))   # through the front wall
    # back wall: clearance for the tilt pivot screw
    tools.append(cyly(-G_B_Y - 1, -G_B_Y + G_B_FRONT_T + 1, 0, G_ZT, 1.7))
    # cable slot in the bottom
    tools.append(cylz(0, 0, zb0 - 1, zb0 + 5, 12.0))
    return cut_all(b, tools)


def build_neck_head_plate():
    """C: head plate with two legs; legs carry the tilt horn (front) and pivot boss (back)."""
    zp0 = G_C_PLATE_Z0
    c = cylz(0, 0, zp0, zp0 + G_C_PLATE_T, G_C_PLATE_D / 2)
    c = c.faces(">Z").chamfer(1.0)
    lo = G_ZT - 9.0
    for sy in (-1, 1):
        ya, yb = sy * 6.4, sy * 11.4
        c = c.union(box(-12.0, 12.0, min(ya, yb), max(ya, yb), lo, zp0 + 0.01))
    c = c.union(cyly(-16.6, -11.39, 0, G_ZT, 4.5))                                   # back pivot boss
    tools = [cylz(0, 0, zp0 - 1, zp0 + G_C_PLATE_T + 1, 30.0 / 2)]
    for k in range(4):
        a = math.radians(45 + 90 * k)
        tools.append(cylz(G_C_SCREW_R * math.cos(a), G_C_SCREW_R * math.sin(a), zp0 - 1, zp0 + G_C_PLATE_T + 1, 1.7))
    tools.append(cyly(10.0, 12.0, 0, G_ZT, 3.5))                                      # spline tip clearance (front leg)
    tools.append(cyly(5.0, 12.0, 0, G_ZT, 3.5))
    for sx in (-1, 1):
        tools.append(cyly(5.4, 12.0, sx * 7.0, G_ZT, 0.95))
    tools.append(cyly(-17.0, -10.0, 0, G_ZT, 1.35))                                   # pilot for pivot screw
    return cut_all(c, tools)


# =====================================================================================
# 6  HEAD SPHERE (two halves, left/right) with the Ø110 magnet collar, + 4 skin rings
# =====================================================================================
# Local frame: origin = centre of the collar plane. The sphere centre is HEAD_CUT_DZ above it.
WEB_Z0, WEB_T = 8.0, 4.0
WEB_R_IN, WEB_R_OUT = 33.0, 43.0
BEAD_H, BEAD_W = 1.0, 3.0


def collar_ring(z0=0.0):
    """Mating ring: flat top face (1.0 mm skin) mates with the head collar underside; magnets load from below."""
    ring = cylz(0, 0, z0, z0 + COLLAR_T, COLLAR_D / 2).cut(cylz(0, 0, z0 - 1, z0 + COLLAR_T + 1, COLLAR_ID / 2))
    ring = cut_all(ring, magnet_pockets(z0, MAG_POCKET_DEPTH, -1))
    return ring


def build_head_full():
    zc = HEAD_CUT_DZ
    outer = cq.Workplane("XY").sphere(HEAD_R).translate((0, 0, zc))
    inner = cq.Workplane("XY").sphere(HEAD_R - HEAD_WALL).translate((0, 0, zc))
    shell = outer.cut(inner).intersect(cylz(0, 0, 0, 2 * HEAD_R + zc, HEAD_R + 1))
    # trim below the collar plane
    shell = shell.intersect(box(-100, 100, -100, 100, 0, 200))
    # equator bead for the clip-on formers
    bead = cylz(0, 0, zc - BEAD_W / 2, zc + BEAD_W / 2, HEAD_R + BEAD_H).cut(cylz(0, 0, zc - 5, zc + 5, HEAD_R - 2.0))
    shell = shell.union(bead)
    # collar flange + neck web
    flange = cylz(0, 0, 0, COLLAR_T, COLLAR_D / 2).cut(cylz(0, 0, -1, COLLAR_T + 1, COLLAR_ID / 2))
    shell = shell.union(flange)
    # light web: a ring that carries the four neck-plate screws, plus four spokes out to the shell
    web = cylz(0, 0, WEB_Z0, WEB_Z0 + WEB_T, WEB_R_OUT).cut(cylz(0, 0, WEB_Z0 - 1, WEB_Z0 + WEB_T + 1, WEB_R_IN))
    for k in range(4):
        spoke = box(WEB_R_OUT - 1.0, 57.0, -4.0, 4.0, WEB_Z0, WEB_Z0 + WEB_T)
        web = web.union(rot_z(spoke, 45 + 90 * k))
    shell = shell.union(web)
    tools = magnet_pockets(COLLAR_T, MAG_POCKET_DEPTH, +1)
    # M3 pilots for the neck plate (screws come up through the head plate)
    for k in range(4):
        a = math.radians(45 + 90 * k)
        tools.append(cylz(G_C_SCREW_R * math.cos(a), G_C_SCREW_R * math.sin(a), WEB_Z0 - 0.01, WEB_Z0 + WEB_T + 0.01, 1.35))
    # lugs on the web ring at the split plane (join the halves with 2x M3 across x)
    for sy in (-1, 1):
        yc = sy * (WEB_R_IN + WEB_R_OUT) / 2
        shell = shell.union(box(-8.0, 8.0, yc - 4.0, yc + 4.0, WEB_Z0 + WEB_T - 0.01, WEB_Z0 + WEB_T + 8.0))
        tools.append(cylx(-9.0, 0.0, yc, WEB_Z0 + WEB_T + 4.0, 1.7))
        tools.append(cylx(0.0, 9.0, yc, WEB_Z0 + WEB_T + 4.0, 1.35))
    return cut_all(shell, tools)


def build_head_halves():
    full = build_head_full()
    return half(full, -1), half(full, +1)


def build_skin_ring(tag=1):
    """Standard Ø110 skin ring. 'tag' = number of little notches on the outer edge, so the four rings can be told apart."""
    r = collar_ring(0.0)
    tools = []
    for k in range(MAG_COUNT):                                  # sewing holes between the magnets
        a = math.radians(k * 60 + 30)
        tools.append(cylz(MAG_PCD / 2 * math.cos(a), MAG_PCD / 2 * math.sin(a), -1, COLLAR_T + 1, 0.9))
    for j in range(tag):                                        # identification notches (0.9 mm deep)
        a = math.radians(45 + 9 * j)
        tools.append(cylz((COLLAR_D / 2) * math.cos(a), (COLLAR_D / 2) * math.sin(a), -1, COLLAR_T + 1, 1.2))
    return cut_all(r, tools)


# =====================================================================================
# 7  SHOULDER SOCKETS (right side built; left = mirror), BLANKING CAPS, ARM HORNS
# =====================================================================================
# The socket bolts onto the outer end of the carriage slider block (x = 56) so it bobs with the body.
# MG90S sits with its shaft along +Y (arm swings in the X-Z plane), body ABOVE the shaft.
SK_X0 = BLOCK_X1                                    # back face on the slider block
SK_BACK_T = 4.8                                     # 2.4 skin + 2.4 counterbore for the M3 screw heads
SK_POCKET_X0 = SK_X0 + SK_BACK_T
SK_POCKET_X1 = SK_POCKET_X0 + MG90_W + 2 * CLEAR
SK_X1 = SK_POCKET_X1 + WALL
SK_TAB_Y = 6.5                                      # plane the servo tabs rest on (socket front face)
SK_SERVO_BOT_Y = SK_TAB_Y - MG90_TAB_TOP            # servo bottom face (CHECK tab-top number)
SK_FLOOR_Y = SK_SERVO_BOT_Y - CLEAR
SK_Y0 = SK_FLOOR_Y - WALL
SK_ZC = CAR_REST_Z + ARM_H / 2                      # shaft height at rest = middle of the slider block
SK_SHAFT_X = SK_POCKET_X0 + CLEAR + MG90_W / 2
SK_HORN_Y0 = SK_SERVO_BOT_Y + MG90_H + 0.8          # printed horn sits just above the body top
SK_BODY_C = SK_ZC - MG90_SHAFT_OFF + MG90_L / 2     # z of the middle of the servo body (and of the tab holes)
SK_BODY_Z0 = SK_ZC - MG90_SHAFT_OFF - CLEAR
SK_BODY_Z1 = SK_ZC - MG90_SHAFT_OFF + MG90_L + CLEAR
SK_Z0, SK_Z1 = SK_BODY_C - 18.0, SK_BODY_C + 18.0
SK_SCREW_Z = (SK_ZC - 5.0, SK_ZC + 5.0)             # the two carriage-block pilots (see build_carriage)
HORN_BOSS_L = 24.0
ARM_HORN_T = 4.0                                    # own name: it used to reuse HORN_T and so made the turntable's horn recess 4.4 deep
HORN_BOSS_T = 9.0


def build_socket_right():
    s = box(SK_X0, SK_X1, SK_Y0, SK_TAB_Y, SK_Z0, SK_Z1)
    tools = []
    tools.append(box(SK_POCKET_X0, SK_POCKET_X1, SK_FLOOR_Y, SK_TAB_Y + 1, SK_BODY_Z0, SK_BODY_Z1))          # servo pocket
    tools.append(box(SK_POCKET_X0 + 2.5, SK_POCKET_X1 - 2.5, SK_Y0 - 1, SK_FLOOR_Y + 0.5, SK_BODY_Z0, SK_BODY_Z0 + 9.0))   # cable slot
    for z in SK_SCREW_Z:
        tools.append(cylx(SK_X0 - 1, SK_POCKET_X0 + 1, 0, z, 1.7))                    # M3 clearance
        tools.append(cylx(SK_X0 + 2.4, SK_POCKET_X0 + 0.01, 0, z, 3.2))               # counterbore for the screw head
        tools.append(cylx(SK_POCKET_X1 - 0.01, SK_X1 + 1, 0, z, 3.5))                 # screwdriver access through the outer wall
    for sz in (-1, 1):
        tools.append(cyly(SK_Y0 - 1, SK_TAB_Y + 0.01, SK_SHAFT_X, SK_BODY_C + sz * MG90_HOLE_DX / 2, MG90_HOLE_D / 2))   # M2 tab pilots, through (Andy: support gets trapped in blind ones)
    return cut_all(s, tools)


def build_socket_cap():
    """Blanking cap: plug fills the empty pocket, flange covers the front face. Symmetric, so one STL serves both sides."""
    plug = box(SK_POCKET_X0 + 0.2, SK_POCKET_X1 - 0.2, SK_TAB_Y - 8.0, SK_TAB_Y + 0.01, SK_BODY_Z0 + 0.2, SK_BODY_Z1 - 0.2)
    flange = box(SK_X0, SK_X1, SK_TAB_Y, SK_TAB_Y + 2.0, SK_Z0, SK_Z1)
    c = plug.union(flange)
    tools = [cyly(SK_TAB_Y - 1, SK_TAB_Y + 3, SK_SHAFT_X, SK_BODY_C + sz * MG90_HOLE_DX / 2, 1.2) for sz in (-1, 1)]
    return cut_all(c, tools)


def build_arm_horn():
    """Printed horn in its own frame: shaft along +Z (print flat, disc down), arm along +X.
    The 2 mm armature wire slides into the boss and is pinched by an M2 grub/self-tapping screw."""
    disc = cylz(0, 0, 0, ARM_HORN_T, 10.0)
    boss = box(0.0, HORN_BOSS_L, -HORN_BOSS_T / 2, HORN_BOSS_T / 2, 0, HORN_BOSS_T)
    h = disc.union(boss)
    zw = HORN_BOSS_T / 2
    tools = [cyl_x_local(5.0, HORN_BOSS_L + 1, zw, (ARM_WIRE_D + 0.3) / 2)]       # wire bore, 19 mm deep
    tools.append(cylz(15.0, 0, zw, HORN_BOSS_T + 1, 0.8))                         # M2 pinch screw from above, meets the bore
    tools.append(cylz(0, 0, -1, ARM_HORN_T + 1, 1.25))                             # centre screw (M2) through the servo spline
    for k in range(4):                                                             # screws into the stock cross horn
        a = math.radians(45 + 90 * k)
        tools.append(cylz(6.5 * math.cos(a), 6.5 * math.sin(a), -1, ARM_HORN_T + 1, 0.6))
    return cut_all(h, tools)


def cyl_x_local(x0, x1, cz, r):
    return cq.Workplane("YZ").workplane(offset=x0).center(0, cz).circle(r).extrude(x1 - x0)


# =====================================================================================
# 8  CHARACTER SHELLS: hollow, 1.5 mm wall, in two halves (split on x = 0 like the head) with the standard
#    magnet ring on the underside. Used for the example cloud former here and for the other shells in build_shells.py
# =====================================================================================
SHELL_WALL = 1.5
SHELL_CAV_R = HEAD_R + BEAD_H + 0.8           # cavity around the head sphere (clears the equator bead)
SHELL_FLOOR_Z = -COLLAR_T                     # underside of the mating ring (collar plane is z = 0)


def spheroid(cx, cy, cz, rxy, rz):
    if abs(rxy - rz) < 1e-6:
        return cq.Workplane("XY").sphere(rxy).translate((cx, cy, cz))
    prof = cq.Workplane("XZ").ellipseArc(rxy, rz, -90, 90, startAtCurrent=False).close()
    return prof.revolve(360, (0, 0, 0), (0, 1, 0)).translate((cx, cy, cz))


def blob_shell_full(blobs, wall=SHELL_WALL, extra_cav=(), extra_cuts=(), extra_add=()):
    """blobs = [(cx, cy, cz, r_xy, r_z)] in the head frame (collar plane z = 0, head centre z = HEAD_CUT_DZ).
    The first blob should be big enough to swallow the head (r >= SHELL_CAV_R + wall)."""
    zc, zf = HEAD_CUT_DZ, SHELL_FLOOR_Z
    outer = union_all([spheroid(*b) for b in blobs] + list(extra_add))
    cav = union_all([spheroid(b[0], b[1], b[2], b[3] - wall, b[4] - wall) for b in blobs]
                    + [cq.Workplane("XY").sphere(SHELL_CAV_R).translate((0, 0, zc))] + list(extra_cav))
    shell = outer.cut(cav).intersect(box(-300, 300, -300, 300, zf, 400))
    # mating ring: a solid 3.2 mm plate = the whole outer shape between z = zf and 0, minus the Ø96 neck hole.
    # (taking it from the outer solid closes the floor of any shape, however wide the belly is)
    plate = outer.intersect(box(-300, 300, -300, 300, zf, 0.0)).cut(cylz(0, 0, zf - 1, 1, COLLAR_ID / 2))
    shell = shell.union(plate)
    tools = magnet_pockets(zf, MAG_POCKET_DEPTH, -1)
    yo = plate.val().BoundingBox().ymax                                    # outer edge of the plate at the front/back seam
    for sy in (-1, 1):                                                     # screw lugs at the front and back seam
        low = box(-8.0, 8.0, min(sy * (yo - 3.0), sy * (yo + 7.0)), max(sy * (yo - 3.0), sy * (yo + 7.0)), zf, 0.0)
        up = box(-8.0, 8.0, min(sy * (yo + 3.0), sy * (yo + 7.0)), max(sy * (yo + 3.0), sy * (yo + 7.0)), 0.0 - 0.01, 8.0)
        shell = shell.union(low).union(up)
    tools += list(extra_cuts)
    SHELL_LUG_Y[0] = yo + 5.0
    return cut_all(shell, tools)


SHELL_LUG_Y = [0.0]


def blob_shell_halves(blobs, **kw):
    """Left half = x <= 0 of the symmetric shell; right half = its mirror image (a straight x>=0 cut of a union of
    spheres upsets the CAD kernel, the mirror is exact). Lug screw holes are cut last: clearance left, pilot right."""
    full = blob_shell_full(blobs, **kw)
    left0 = half(full, -1)
    right0 = left0.mirror("YZ")
    yl = SHELL_LUG_Y[0]
    left = cut_all(left0, [cylx(-9.0, 0.5, sy * yl, 4.0, 1.7) for sy in (-1, 1)])
    right = cut_all(right0, [cylx(-0.5, 9.0, sy * yl, 4.0, 1.35) for sy in (-1, 1)])
    return left, right


def cloud_blobs():
    zc = HEAD_CUT_DZ
    main_r = SHELL_CAV_R + SHELL_WALL
    return [
        (0, 0, zc, main_r, main_r),
        (-46.0, 0, zc - 2.0, 21.0, 21.0),   # left puff
        (46.0, 0, zc - 2.0, 21.0, 21.0),    # right puff
        (-34.0, 0, zc + 40.0, 24.0, 24.0),  # upper left puff
        (34.0, 0, zc + 40.0, 24.0, 24.0),   # upper right puff
        (0.0, 0, zc + 54.0, 22.0, 22.0),    # top puff
    ]


def build_cloud_former_halves():
    return blob_shell_halves(cloud_blobs())


# =====================================================================================
# 8b DUMMY CORE: a light stand that holds a resting skin on the shelf (one for each skin that is off the base)
# =====================================================================================
CORE_WALL = 1.2                 # 3 perimeters at 0.4 mm
CORE_TUBE_R = 30.0              # passes down through the skin's Ø96 neck hole
CORE_TUBE_Z0 = -30.0            # the tube runs down to here, then a 45 degree cone flares out to the foot
CORE_FOOT_R = COLLAR_D / 2      # foot as wide as the collar
CORE_SPOKES = 6


def build_dummy_core():
    """Head frame (collar plane z = 0): a copy of the head's magnet collar on six spokes, a thin tube down through the skin's
    neck hole and a 45 degree cone foot. Everything above the collar plane sits inside the head's own outline, so any skin
    that fits the head fits the core. Prints collar-down with no supports."""
    ro, w = CORE_TUBE_R, CORE_WALL
    ri, wh = ro - w, w * math.sqrt(2)               # wh = horizontal thickness of a 45 degree wall
    z_foot = CORE_TUBE_Z0 - (CORE_FOOT_R - ro)
    prof = [(ri, COLLAR_T), (ro, COLLAR_T), (ro, CORE_TUBE_Z0), (CORE_FOOT_R, z_foot), (CORE_FOOT_R - wh, z_foot),
            (ri, CORE_TUBE_Z0 - (wh - w))]
    core = cq.Workplane("XZ").polyline(prof).close().revolve(360, (0, 0, 0), (0, 1, 0))
    core = core.union(cylz(0, 0, 0, COLLAR_T, COLLAR_D / 2).cut(cylz(0, 0, -1, COLLAR_T + 1, COLLAR_ID / 2)))
    for k in range(CORE_SPOKES):                    # spokes sit between the magnets
        core = core.union(rot_z(box(ri, COLLAR_ID / 2 + 0.5, -3.0, 3.0, 0.0, COLLAR_T), 30 + 60 * k))
    return cut_all(core, magnet_pockets(COLLAR_T, MAG_POCKET_DEPTH, +1))


# =====================================================================================
# 9  ASSEMBLY PLACEMENT, POSES, PRINT ORIENTATION AND EXPORT
# =====================================================================================
HEAD_Z0_ABS = STEM_TOP_Z + NECK_TOP - WEB_Z0              # collar plane height with the carriage fully down
HEAD_TOP_ABS = HEAD_Z0_ABS + HEAD_CUT_DZ + HEAD_R
NOD_AXIS_Z = STEM_TOP_Z + G_ZN
TILT_AXIS_Z = STEM_TOP_Z + G_ZT
WIRE_LEN = 110.0
O = (0, 0, 0)
AX, AY, AZ = (1, 0, 0), (0, 1, 0), (0, 0, 1)


def build_all():
    P = {}
    P["base"] = build_base_one()
    P["turntable"] = build_turntable()
    P["turntable_hub"] = build_turntable_hub()
    P["column_L"], P["column_R"] = build_column_halves()
    P["carriage"] = build_carriage()
    P["yoke"] = build_yoke()
    P["lever"] = build_lever()                       # local frame
    P["neck_A"] = build_neck_base()                  # local frame: flange underside z = 0
    P["neck_B"] = build_neck_rocker()
    P["neck_C"] = build_neck_head_plate()
    P["head_L"], P["head_R"] = build_head_halves()   # head frame: collar plane z = 0
    P["socket_R"] = build_socket_right()
    P["socket_cap"] = build_socket_cap()
    P["horn"] = build_arm_horn()                     # local frame
    P["wire"] = cyl_x_local(5.0, 5.0 + WIRE_LEN, HORN_BOSS_T / 2, ARM_WIRE_D / 2)
    P["cloud_L"], P["cloud_R"] = build_cloud_former_halves()
    P["dummy_core"] = build_dummy_core()             # head frame; a shelf part, not in the assembly
    return P


def _place_lever(P, beta):
    return P["lever"].rotate(O, AZ, -beta).rotate(O, AX, -90).translate((LIFT_SHAFT_X, LEVER_Y0, LIFT_ZC))


def _place_horn(wp, beta):
    return wp.rotate(O, AZ, -beta).rotate(O, AX, -90).translate((SK_SHAFT_X, SK_HORN_Y0, SK_ZC))


def assemble(P, bob=0.0, nod=0.0, tilt=0.0, arm_deg=-90.0, with_cloud=False):
    """Return {name: solid} in the assembly frame. bob = carriage rise in mm (0..BOB_THROW);
    nod about X (+ = head leans forward/+Y... see note), tilt about Y; arm_deg = arm direction in the X-Z plane for the
    right arm (0 = out sideways, -90 = hanging down, +90 = straight up)."""
    A = {}
    for k in ("base", "turntable", "turntable_hub", "column_L", "column_R"):
        A[k] = P[k]
    # lever angle follows the bob: -45 deg (carriage down) .. +45 deg (carriage up)
    beta = -LIFT_SWING + (2 * LIFT_SWING) * (bob / BOB_THROW)
    A["lever"] = _place_lever(P, beta)
    up = (0, 0, bob)
    A["carriage"] = P["carriage"].translate(up)
    A["yoke"] = P["yoke"].translate(up)
    A["socket_R"] = P["socket_R"].translate(up)
    A["socket_L"] = P["socket_R"].mirror("YZ").translate(up)
    horn_R = _place_horn(P["horn"], arm_deg)
    wire_R = _place_horn(P["wire"], arm_deg)
    A["horn_R"], A["wire_R"] = horn_R.translate(up), wire_R.translate(up)
    A["horn_L"], A["wire_L"] = horn_R.mirror("YZ").translate(up), wire_R.mirror("YZ").translate(up)
    z_a = STEM_TOP_Z + bob
    nod_pt = (0, 0, NOD_AXIS_Z + bob)
    tilt_pt = (0, 0, TILT_AXIS_Z + bob)

    def nod_it(wp):
        return wp.rotate(nod_pt, (1, 0, NOD_AXIS_Z + bob), nod)

    def tilt_it(wp):
        return wp.rotate(tilt_pt, (0, 1, TILT_AXIS_Z + bob), tilt)

    A["neck_A"] = P["neck_A"].translate((0, 0, z_a))
    A["neck_B"] = nod_it(P["neck_B"].translate((0, 0, z_a)))
    A["neck_C"] = nod_it(tilt_it(P["neck_C"].translate((0, 0, z_a))))
    hz = HEAD_Z0_ABS + bob
    A["head_L"] = nod_it(tilt_it(P["head_L"].translate((0, 0, hz))))
    A["head_R"] = nod_it(tilt_it(P["head_R"].translate((0, 0, hz))))
    if with_cloud:
        A["cloud_L"] = nod_it(tilt_it(P["cloud_L"].translate((0, 0, hz))))
        A["cloud_R"] = nod_it(tilt_it(P["cloud_R"].translate((0, 0, hz))))
    return A


def overlap_mm3(a, b):
    try:
        c = a.intersect(b)
        vs = c.solids().vals()
        return sum(v.Volume() for v in vs) if vs else 0.0
    except Exception:
        return 0.0


def gimbal_interference(P):
    """Pose the neck at every nod/tilt extreme (and the bob extremes) and report any solid-on-solid overlap."""
    rows, worst = [], 0.0
    for bob in (0.0, BOB_THROW):
        for nod in (-NOD_LIMIT, 0.0, NOD_LIMIT):
            for tilt in (-TILT_LIMIT, 0.0, TILT_LIMIT):
                A = assemble(P, bob=bob, nod=nod, tilt=tilt)
                head = A["head_L"].union(A["head_R"])
                pairs = [("B/A", A["neck_B"], A["neck_A"]), ("C/A", A["neck_C"], A["neck_A"]),
                         ("C/B", A["neck_C"], A["neck_B"]), ("head/A", head, A["neck_A"]),
                         ("head/B", head, A["neck_B"]), ("head/carriage", head, A["carriage"]),
                         ("head/column", head, A["column_L"].union(A["column_R"]))]
                bad = {n: overlap_mm3(a, b) for (n, a, b) in pairs}
                bad = {n: v for n, v in bad.items() if v > 1.0}
                worst = max([worst] + list(bad.values()))
                rows.append((bob, nod, tilt, bad))
    return rows, worst


# print orientation: (file name, copies, part key, rotations, supports note, thin-wall?)
PRINT_LIST = [
    ("base_plate", 1, "base", [], "none (one piece; pockets open on top; speaker/jack holes bridge by a few mm)", False),
    ("turntable", 1, "turntable", [], "none (plate down, cradle up; servo slot open at the top)", False),
    ("turntable_hub", 1, "turntable_hub", [(AX, 180)], "none (floor down)", False),
    ("column_left", 1, "column_L", [], "none (stands on its foot ring, lugs have 45 deg undersides)", True),
    ("column_right", 1, "column_R", [], "none (stands on its foot ring, lugs have 45 deg undersides)", True),
    ("bob_carriage", 1, "carriage", [], "none (frame down, stem up, 45 deg fillet)", False),
    ("lift_yoke", 1, "yoke", [(AX, 180)], "none (flange down, blade up)", False),
    ("lift_lever", 1, "lever", [], "none (flat)", False),
    ("neck_base_A", 1, "neck_A", [], "none (plug down; 45 deg sleeve under the flange and uprights)", False),
    ("neck_rocker_B", 1, "neck_B", [], "none (pivot boss is a short 4.5 mm radius stub)", False),
    ("neck_head_plate_C", 1, "neck_C", [(AX, 180)], "none (plate down, legs up)", False),
    ("head_half_left", 1, "head_L", [(AY, 90)], "YES: crown of the dome (top ~30%) and the collar flange", True),
    ("head_half_right", 1, "head_R", [(AY, -90)], "YES: crown of the dome (top ~30%) and the collar flange", True),
    ("shoulder_socket_right", 1, "socket_R", [(AX, 90)], "none (pocket opens upward)", False),
    ("shoulder_socket_left", 1, "socket_L", [(AX, 90)], "none (pocket opens upward)", False),
    ("shoulder_cap", 0, "socket_cap", [(AX, -90)], "none (flange down); not needed on the shared base: both shoulder servos stay fitted", True),
    ("arm_horn", 2, "horn", [], "none (disc down)", False),
    ("cloud_former_left", 1, "cloud_L", [(AY, 90)], "YES: puffs and crown; tree supports", True),
    ("cloud_former_right", 1, "cloud_R", [(AY, -90)], "YES: puffs and crown; tree supports", True),
    ("dummy_core", 5, "dummy_core", [(AX, 180)], "none (collar down, 45 deg cone)", True),
]


def settle(wp, rots):
    for ax, ang in rots:
        wp = wp.rotate(O, ax, ang)
    bb = wp.val().BoundingBox()
    return wp.translate((-(bb.xmin + bb.xmax) / 2, -(bb.ymin + bb.ymax) / 2, -bb.zmin))


def clean_stl(path):
    """The CAD mesher leaves one to four zero-area triangles at sphere seams in some dome parts (head halves, shells).
    Dropping them makes the mesh watertight with an identical volume. Never fatal: a failure just leaves the file as exported."""
    try:
        import trimesh
        m = trimesh.load(path, force="mesh", process=False)
        m.merge_vertices()
        n0 = len(m.faces)
        m.update_faces(m.nondegenerate_faces(height=1e-9))
        m.remove_unreferenced_vertices()
        if len(m.faces) != n0:
            m.export(path)
    except Exception as e:
        print("  (mesh clean skipped:", repr(e)[:80], ")", flush=True)


def export_stl(wp, path, tol=0.02, ang=0.12):
    cq.exporters.export(wp, path, tolerance=tol, angularTolerance=ang)
    if tol <= 0.05:                      # print-quality files only; the coarse assembly poses are left alone
        clean_stl(path)


def main(skip_check=False):
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(ASM_DIR, exist_ok=True)
    P = build_all()
    P["socket_L"] = P["socket_R"].mirror("YZ")
    for tag in (1, 2, 3, 4):
        P[f"skin_ring_{tag}"] = build_skin_ring(tag)
    plist = list(PRINT_LIST) + [(f"skin_ring_{t}", 1, f"skin_ring_{t}", [], "none (flat)", True) for t in (1, 2, 3, 4)]
    rows = []
    for (fname, copies, key, rots, sup, thin) in plist:
        pw = settle(P[key], rots)
        path = os.path.join(OUT_DIR, fname + ".stl")
        export_stl(pw, path)
        bb = pw.val().BoundingBox()
        v = vol_cm3(P[key])
        rows.append((fname, copies, v, bb.xlen, bb.ylen, bb.zlen, v * 1.24 * 0.25, v * 1.24, sup, thin, os.path.getsize(path)))
        print(f"{fname:24s} x{copies}  {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:6.1f} mm  {v:7.1f} cm3  "
              f"{v * 1.24 * 0.25:6.1f} g (25%)  {v * 1.24:6.1f} g (solid)  {os.path.getsize(path) / 1e6:5.2f} MB  supports: {sup}", flush=True)
    with open(os.path.join(OUT_DIR, "parts_report.csv"), "w", encoding="utf-8") as f:
        f.write("file,copies,volume_cm3,x_mm,y_mm,z_mm,grams_25pct_infill,grams_if_solid,supports,thin_wall,stl_bytes\n")
        for r in rows:
            f.write(",".join([r[0], str(r[1]), f"{r[2]:.1f}", f"{r[3]:.1f}", f"{r[4]:.1f}", f"{r[5]:.1f}", f"{r[6]:.1f}", f"{r[7]:.1f}",
                              '"' + r[8] + '"', str(r[9]), str(r[10])]) + "\n")
    need = pocket_break_even()
    with open(os.path.join(OUT_DIR, "base_pockets.csv"), "w", encoding="utf-8") as f:
        f.write(f"# infill {PS.INFILL:.0%}, skin {PS.skin_mm():.1f} mm: a pocket is cut when volume / new wall area >= {need:.1f} mm\n")
        f.write("pocket,volume_cm3,ratio_mm,grams_saved,cut\n")
        for (n, v, ratio, saved, kept) in BASE_POCKETS_REPORT:
            f.write(f"{n},{v:.1f},{ratio:.1f},{saved:.1f},{'yes' if kept else 'no'}\n")
    cut = [r for r in BASE_POCKETS_REPORT if r[4]]
    print(f"base hollowing: {len(cut)} of {len(BASE_POCKETS_REPORT)} pockets cut (break-even {need:.1f} mm), "
          f"{sum(r[1] for r in cut):.0f} cm3 removed, about {sum(r[3] for r in cut):.0f} g saved at {PS.INFILL:.0%} infill")
    # assembly STLs (rest pose, coarse mesh) for the preview renders
    A = assemble(P, with_cloud=True)
    for k, wp in A.items():
        export_stl(wp, os.path.join(ASM_DIR, k + ".stl"), tol=0.1, ang=0.35)
    print(f"assembly pose STLs written: {len(A)}")
    print(f"overall height, head top (rest pose): {HEAD_TOP_ABS:.1f} mm; bob throw {BOB_THROW:.1f} mm; head collar z {HEAD_Z0_ABS:.1f}")
    if not skip_check:
        irows, worst = gimbal_interference(P)
        print("gimbal / head interference check over bob {0, max} x nod {-30,0,+30} x tilt {-25,0,+25}:")
        for (bob, nod, tilt, bad) in irows:
            if bad:
                print(f"  bob {bob:4.1f} nod {nod:+5.1f} tilt {tilt:+5.1f}: OVERLAP {bad}")
        print("  worst overlap mm3:", round(worst, 1))


if __name__ == "__main__":
    main(skip_check="--no-check" in sys.argv)
