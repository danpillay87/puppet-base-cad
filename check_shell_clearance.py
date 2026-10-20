r"""
Clearance of a character shell against the fixed base parts, over the neck's whole range (CadQuery exact distance, no meshes).

Run:  .venv\Scripts\python.exe check_shell_clearance.py claude          # one shell (names as in build_shells.JOBS: pear frog heart jolly claude)
      .venv\Scripts\python.exe check_shell_clearance.py claude jolly    # several
      add --bob to also test the four nod/tilt corners with the carriage fully up.

For each pose the shell halves are moved with the head (build_shells.pose_head_frame = the same transform B.assemble uses for
the head) and the smallest distance to every other assembled part is taken: base plate, turntable, column halves, carriage,
yoke, lever, neck base A, rocker B and the shoulder sockets. Left out on purpose: the head halves and head plate C (they move
with the shell, so they are never a clearance question: overlap with the head is checked in build_shells.py) and the arm horns /
wires (arms exist on the Jolly only; the round characters have the sockets blanked off). A distance of 0.0 means touching.
Poses: nod {-30, 0, +30} x tilt {-25, 0, +25} at rest (bob 0), which includes all four combined corners.
Writes/updates out/shell_clearance.csv (one row per shell x pose). All units mm.
"""
import csv
import os
import sys
import time

import build_puppet_base as B
import build_shells as S

SKIP = ("head_L", "head_R", "neck_C", "horn_L", "horn_R", "wire_L", "wire_R")   # see the docstring
NODS = (-B.NOD_LIMIT, 0.0, B.NOD_LIMIT)
TILTS = (-B.TILT_LIMIT, 0.0, B.TILT_LIMIT)
CORNERS = [(n, t) for n in (-B.NOD_LIMIT, B.NOD_LIMIT) for t in (-B.TILT_LIMIT, B.TILT_LIMIT)]


def bbox_gap(a, b):
    """Lower bound on the distance between two solids from their bounding boxes (0 when the boxes overlap)."""
    ba, bb = a.val().BoundingBox(), b.val().BoundingBox()
    dx = max(ba.xmin - bb.xmax, bb.xmin - ba.xmax, 0.0)
    dy = max(ba.ymin - bb.ymax, bb.ymin - ba.ymax, 0.0)
    dz = max(ba.zmin - bb.zmax, bb.zmin - ba.zmax, 0.0)
    return (dx * dx + dy * dy + dz * dz) ** 0.5


def min_distance(shell_parts, parts):
    """(smallest distance, name of the nearest part) between any shell half and any part. Parts whose bounding box is already
    farther than the best distance found so far are skipped (exact distance is only computed for candidates)."""
    cands = []
    for name, wp in parts.items():
        gap = min(bbox_gap(s, wp) for s in shell_parts)
        cands.append((gap, name, wp))
    cands.sort(key=lambda c: c[0])
    best, best_name = 1e9, ""
    for gap, name, wp in cands:
        if gap >= best:
            break
        for s in shell_parts:
            d = s.val().distance(wp.val())
            if d < best:
                best, best_name = d, name
    return best, best_name


def run(keys, with_bob=False):
    t0 = time.time()
    P = B.build_all()
    print(f"base parts built in {time.time() - t0:.0f} s", flush=True)
    rep = os.path.join(B.OUT_DIR, "shell_clearance.csv")
    rows = {}
    if os.path.exists(rep):
        with open(rep, encoding="utf-8") as f:
            for r in csv.reader(f):
                if r and r[0] != "shell":
                    rows[(r[0], r[1], r[2], r[3])] = r
    for key in keys:
        fn, kind = S.JOBS[key]
        L, R = fn()
        poses = [(0.0, n, t) for n in NODS for t in TILTS]
        if with_bob:
            poses += [(B.BOB_THROW, n, t) for n, t in CORNERS]
        worst = (1e9, None)
        for bob, nod, tilt in poses:
            A = B.assemble(P, bob=bob, nod=nod, tilt=tilt, arm_deg=-90.0)
            parts = {k: v for k, v in A.items() if k not in SKIP}
            shell = [S.pose_head_frame(L, bob, nod, tilt), S.pose_head_frame(R, bob, nod, tilt)]
            d, who = min_distance(shell, parts)
            print(f"{key:7s} bob {bob:5.1f} nod {nod:6.1f} tilt {tilt:6.1f}   min distance {d:6.2f} mm   nearest: {who}", flush=True)
            rows[(key, f"{bob:.1f}", f"{nod:.0f}", f"{tilt:.0f}")] = [key, f"{bob:.1f}", f"{nod:.0f}", f"{tilt:.0f}", f"{d:.2f}", who]
            if d < worst[0]:
                worst = (d, (bob, nod, tilt, who))
        print(f"  -> {key}: worst case {worst[0]:.2f} mm at bob/nod/tilt/part {worst[1]}", flush=True)
    with open(rep, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["shell", "bob_mm", "nod_deg", "tilt_deg", "min_distance_mm", "nearest_part"])
        for k in sorted(rows):
            w.writerow(rows[k])
    print("wrote", rep)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    bad = [a for a in args if a not in S.JOBS or S.JOBS[a][1] != "halves"]
    if bad or not args:
        raise SystemExit(f"give one or more shell names (two-half shells only) from {[k for k, v in S.JOBS.items() if v[1] == 'halves']}")
    run(args, with_bob="--bob" in sys.argv)
