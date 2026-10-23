r"""
Plastic, print time and filament cost for the shared-base plan: one Jolly-spec base, six skins, five dummy cores.

Reads the print STLs in out/ and the numbers in print_settings.py, so re-run it after changing either:
    .venv\Scripts\python.exe print_cost.py          # prints the table and writes out/print_cost.txt

Weight model (the same one the 23 Oct cost-down plan used, so the before/after numbers compare):
  every surface carries a solid skin of print_settings.skin_mm() (the thicker of the walls and the top/bottom layers),
  the rest is infill at print_settings.INFILL; parts that need supports get SUPPORT_FRACTION extra. Time is plastic divided
  by a throughput range in g/h, plus a set-up per plate (plates estimated from the parts' footprints), so it is only a
  guide: the slicer's own estimate on Andy's printer wins.
"""
import math
import os

import trimesh

import print_settings as PS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")

# (file in out/, copies). One shared base keeps both shoulder servos, so Jolly's two arm horns are part of it and no
# shoulder caps are printed; the horns come off when an armless skin goes on.
BASE_SET = [("base_plate", 1), ("turntable", 1), ("turntable_hub", 1), ("column_left", 1), ("column_right", 1),
            ("bob_carriage", 1), ("lift_yoke", 1), ("lift_lever", 1), ("shoulder_socket_left", 1),
            ("shoulder_socket_right", 1), ("neck_base_A", 1), ("neck_rocker_B", 1), ("neck_head_plate_C", 1),
            ("head_half_left", 1), ("head_half_right", 1), ("arm_horn", 2)]
SKINS = {
    "Jolly": [("shell_jolly_left", 1), ("shell_jolly_right", 1)],
    "Clawd": [("shell_claude_left", 1), ("shell_claude_right", 1)],
    "Cloud": [("cloud_former_left", 1), ("cloud_former_right", 1), ("clip_beret", 1)],
    "Pear": [("shell_pear_left", 1), ("shell_pear_right", 1), ("clip_glasses_round", 1)],
    "Frog": [("shell_frog_left", 1), ("shell_frog_right", 1)],
    "Heart": [("shell_heart_left", 1), ("shell_heart_right", 1), ("clip_sunglasses", 1)],
}
CORES = [("dummy_core", 5)]                      # one for each skin that is off the base
OPTIONAL = [("skin_ring_1", 1), ("skin_ring_2", 1), ("skin_ring_3", 1), ("skin_ring_4", 1)]   # spare face rings, not counted

NEEDS_SUPPORTS = ("head_half_", "shell_", "cloud_former_", "clip_")

# The old design (two base plates, supported turntable and neck A, two shoulder caps per armless toy), same model and
# settings, measured from the out/ STLs on 23 Oct 2026 before this change. Six-base figures are the all-six-toys route.
BASELINE = {"base_set_g": 721.0, "shared_total_g": 1481.0, "six_bases_total_g": 5100.0, "infill": 0.15}


def grams(name):
    m = trimesh.load(os.path.join(OUT, name + ".stl"), force="mesh")
    s = 1.0 + PS.SHRINK_PCT / 100.0
    v, a = abs(m.volume) / 1000.0 * s ** 3, m.area / 100.0 * s ** 2          # cm3, cm2
    skin = min(v, a * PS.skin_mm() / 10.0)
    g = (skin + PS.INFILL * (v - skin)) * PS.DENSITY
    if name.startswith(NEEDS_SUPPORTS):
        g *= 1.0 + PS.SUPPORT_FRACTION
    ext = (m.bounds[1] - m.bounds[0]) * s
    fits = ext[0] <= PS.BED_X and ext[1] <= PS.BED_Y and ext[2] <= PS.BED_Z
    return g, ext, fits


def plates(footprint_mm2):
    return max(1, math.ceil(footprint_mm2 / (PS.BED_X * PS.BED_Y * PS.PLATE_FILL)))


def hours(g, n_plates):
    setup = n_plates * PS.PLATE_SETUP_MIN / 60.0
    return [g / r + setup for r in reversed(PS.GRAMS_PER_HOUR)]      # fast end first


def main():
    lines = []

    def say(s=""):
        print(s)
        lines.append(s)

    say(f"Settings (print_settings.py): {PS.PRINTER}, {PS.NOZZLE} mm nozzle, {PS.LAYER} mm layers, {PS.WALLS} walls, "
        f"{PS.TOP_BOTTOM_LAYERS} top/bottom layers, {PS.INFILL:.0%} infill, {PS.FILAMENT} {PS.DENSITY} g/cm3 at GBP {PS.GBP_PER_KG:.2f}/kg, "
        f"bed {PS.BED_X:.0f} x {PS.BED_Y:.0f} x {PS.BED_Z:.0f} mm, shrink {PS.SHRINK_PCT}%")
    say(f"Supports add {PS.SUPPORT_FRACTION:.0%} to: head halves, shells, cloud formers and clip-ons. Every other part prints without.")
    say()
    groups = [("Shared base (Jolly spec, all servos)", BASE_SET)] + [(f"{k} skin", v) for k, v in SKINS.items()] + \
             [("Dummy cores", CORES), ("Optional: spare skin rings (not in the totals)", OPTIONAL)]
    totals, too_big, foot = {}, [], {}
    for title, items in groups:
        say(title)
        gsum = 0.0
        foot[title] = 0.0
        for name, n in items:
            g, ext, fits = grams(name)
            gsum += g * n
            foot[title] += ext[0] * ext[1] * n
            sup = "supports" if name.startswith(NEEDS_SUPPORTS) else ""
            if not fits:
                too_big.append(name)
            say(f"  {name:24s} x{n}  {g:6.1f} g each  {ext[0]:5.0f} x {ext[1]:5.0f} x {ext[2]:5.0f} mm  "
                f"{'' if fits else 'DOES NOT FIT THE BED  '}{sup}")
        say(f"  {'':24s}     {gsum:6.1f} g  GBP {gsum / 1000 * PS.GBP_PER_KG:5.2f}")
        totals[title] = gsum
    base = totals["Shared base (Jolly spec, all servos)"]
    skins = sum(v for k, v in totals.items() if k.endswith(" skin"))
    cores = totals["Dummy cores"]
    total = base + skins + cores
    n_pl = plates(sum(v for k, v in foot.items() if not k.startswith("Optional")))
    h_fast, h_slow = hours(total, n_pl)
    lo, hi = PS.GRAMS_PER_HOUR
    say()
    say(f"One base + six skins + five dummy cores: {total:6.0f} g, GBP {total / 1000 * PS.GBP_PER_KG:5.2f}, "
        f"about {h_fast:.0f}-{h_slow:.0f} h on the {PS.PRINTER} ({lo:.0f}-{hi:.0f} g/h, about {n_pl} plates "
        f"at {PS.PLATE_SETUP_MIN:.0f} min set-up each)")
    skins_fp = sum(v for k, v in foot.items() if k.endswith(" skin"))
    for title, g, fp in (("base set", base, foot["Shared base (Jolly spec, all servos)"]), ("six skins", skins, skins_fp),
                         ("five cores", cores, foot["Dummy cores"])):
        f_, s_ = hours(g, plates(fp))
        say(f"  {title:10s} {g:6.0f} g  GBP {g / 1000 * PS.GBP_PER_KG:5.2f}  about {f_:.0f}-{s_:.0f} h")
    b = BASELINE
    same = abs(PS.INFILL - b["infill"]) < 1e-9
    say(f"Before the shared base ({b['infill']:.0%} infill{'' if same else ', so not comparable with these settings'}): "
        f"base set {b['base_set_g']:.0f} g; one shared base + six skins {b['shared_total_g']:.0f} g; "
        f"six full toys {b['six_bases_total_g']:.0f} g")
    if same:
        say(f"  base set now {base:.0f} g ({base - b['base_set_g']:+.0f} g)")
    say("Bed: every part fits." if not too_big else f"Bed: TOO BIG for {PS.BED_X:.0f} x {PS.BED_Y:.0f}: {', '.join(too_big)}")
    with open(os.path.join(OUT, "print_cost.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
