# Universal motorised puppet base - printable CAD

A parametric, all-printed puppet body: a turntable that spins the whole puppet, a torso column that bobs up and down,
a two-axis neck (nod and tilt), a 120 mm head sphere, and a family of clip-on character shells (cloud, pear, frog, heart,
hooded Jolly, boxy Clawd (Claude)) plus small clip-ons (beret, round glasses, sunglasses). Everything is designed for a home FDM printer in
PLA or PETG. One shared base, built to Jolly's spec with the full set of servos (2 x MG996R and 4 x MG90S), carries all
six toys: every skin swaps onto that one base. All the hidden parts print without supports; only the head halves, the
shells, the Cloud formers and the clip-ons (beret, glasses, sunglasses) still need them. The source of truth is the Python
file at the top of the project; change a number in its PARAMETERS block and re-run to get new STLs.

The build spec (what the six toys are, what moves, electronics, voice, and what we would like printed) is in
[docs/SPEC.md](docs/SPEC.md). The print-ready zip and the print-quantities sheet are on the Releases page.

Status: designed and checked on screen only. Nothing has been printed or test-fitted yet (there is no printer to hand),
so every fit number marked (CHECK) is a best guess for common hobby servos and bearings. Measure yours first (see
"Check before you print").

Built with CadQuery 2.8.0 (a Python wrapper around the OpenCASCADE CAD kernel) on Python 3.14, in the project's `.venv`.

## What is in this folder

| File | What it is |
|---|---|
| `build_puppet_base.py` | Main source. PARAMETERS block at the top (all dimensions), then every base part, the assembly poses and the STL export. |
| `build_shells.py` | The character shells and clip-ons. Its own PARAMETERS block at the top; it imports the base file for the shared dimensions. |
| `check_shell_clearance.py` | Exact (CadQuery distance) clearance of a two-half shell against the base parts over the full nod and tilt range. |
| `render_preview.py` | Makes the assembly preview pictures (`render_preview.py claude` makes only the Claude one). |
| `print_settings.py` | The print settings in one place (bed, nozzle, layers, walls, infill, filament density and price, shrink). They are Andy's printer settings (Bambu Lab H2D, Bambu PLA Basic); only the shrink figure is still to be agreed. |
| `print_cost.py` | Works out plastic, time and cost for one base plus six skins plus five dummy cores from `print_settings.py`; writes `out/print_cost.txt`. |
| `out/*.stl` | One STL per part, already turned to its print orientation (lowest point at z = 0). Import and slice as-is. |
| `out/parts_report.csv`, `out/shells_report.csv` | Size, volume, grams and support notes for every part. |
| `out/shell_clearance.csv` | Smallest gap between a shell and the base parts, per pose (written by `check_shell_clearance.py`). |
| `out/print_cost.txt` | Plastic, printer time and filament cost per part, per skin and in total (model estimate; the slicer on the real printer wins). |
| `out/base_pockets.csv` | Which hollow pockets in the base plate are cut at the current infill, and the grams each one saves. |
| `out/preview_*.png` | The pictures (see below). |
| `out/_assembly/` | Coarse posed copies used only for the pictures. Do not print these. |
| `out/_build_log.txt` | Console output of the last full base build. |

## Preview pictures

Method: each pose is assembled in CadQuery (parts moved and rotated into place), written out as a coarse mesh, and
rendered by VTK off-screen (proper depth-sorted 3D rendering with lighting). Render engine used: VTK off-screen.
A matplotlib fallback is coded into `render_preview.py` but was not needed.

- `out/preview_rest.png` - body at rest: carriage down, head level, arms down, no character shell.
- `out/preview_bobbed_tilted.png` - bobbed up 33.9 mm, head nodded 20 degrees and tilted 20 degrees, arms raised 35 degrees.
- `out/preview_with_cloud.png` - the example cloud shell on the head, at rest.
- `out/preview_shells.png` - the six shells and three clip-ons side by side (front view).
- `out/preview_claude.png` - the Clawd (Claude) shell on the full base, seen from the front, two poses side by side: at rest, and bobbed up 33.9 mm with the head nodded 20 and tilted 20 degrees (no arms fitted). Clawd's four legs are soft fleece, not printed, so they are drawn see-through.

## Key numbers

- Overall height at rest, to the top of the head sphere: 311 mm. Head collar plane sits 227 mm above the floor.
- Bob throw: 33.9 mm (lever 24 mm, swings plus and minus 45 degrees; target was 30-40 mm).
- Neck range: nod plus and minus 30 degrees, tilt plus and minus 25 degrees.
- Shoulder arms swing plus and minus 80 degrees.
- Collision check (head sphere and neck gimbal against the column, carriage and neck parts) over bob {0, max} x nod {-30, 0, +30} x tilt {-25, 0, +25}: worst overlap 0.0 mm3, method: boolean intersection volume in CadQuery.
- Closest approaches in the neck gimbal (tight for a printer): rocker B to base A 0.50 mm, head plate C to rocker B 0.40 mm, head plate C to base A at least 3.2 mm.
- Skin clearance (`check_shell_clearance.py`) was re-run on 23 Oct for Pear, Frog, Heart, Jolly and Clawd against the new base and is unchanged: Jolly's worst case is still 4.24 mm to the column at the nod and tilt extremes; the others are 10.56 mm to neck base A.
- Mesh check: all 39 STLs in `out/` are watertight with a consistent winding (checked with trimesh on 23 Oct) and rest on z = 0. Two of the 39, `base_plate_left` and `base_plate_right`, are superseded by the one-piece `base_plate` and are not printed. Twelve dome-shaped parts (head halves, shells) first came out of the CAD mesher with one to four zero-area triangles each; `clean_stl()` in `build_puppet_base.py` now removes them on export (volume unchanged).

## How it moves

- Yaw (spin): an MG996R sits in a pocket in the base plate with its shaft up. Its horn is fixed to the turntable hub (`turntable_hub`, a small separate disc under the turntable plate) with 4 M2 screws, about 8 mm, that go up through the horn and the hub into the turntable plate. The turntable rides on the 72 mm bearing. The turntable therefore carries the bearing recess, the column and the cradle for the second MG996R, and prints plate-down without supports because the hub is its own part.
- Bob (up and down): that second MG996R lies in the cradle wall on the turntable. A 24 mm lever with an M5 pin pushes a slot in the yoke under the carriage; the carriage slides in two vertical guide channels (the bob rails) inside the column, and an extension spring pulls it back down.
- Neck: a three-part gimbal (base A on the carriage stem, rocker B, head plate C) with one MG90S for nod and one for tilt.
- Head: a 120 mm sphere split down the middle, with the 110 mm magnet collar at the bottom. Skin rings and character shells snap on with six 5 x 2 mm magnets.
- Shoulders: an MG90S socket bolted to each side of the carriage (so the arms bob with the body); the printed horn grips a 2 mm aluminium wire. Both shoulder servos stay fitted on the shared base, so the shoulder caps are no longer printed (`shoulder_cap` is still in the code, at 0 copies). Jolly's two arm horns are part of the base set; take them off when an armless skin goes on.

## Part list, print orientation, grams

All STLs in `out/` are already in the orientation below. Sizes are the printed bounding box (X x Y x Z, mm).

Grams: two estimates, because the two kinds of part behave differently.
- Assumption stated: volume x 1.24 g/cm3 (PLA) x 0.25 infill factor. This is the "25% rule" and is right for chunky parts.
- "Near-solid" is volume x 1.24 with no infill factor. Thin-walled parts (walls 1.5 to 2.4 mm) print almost entirely
  as perimeters, so the 25% rule underestimates them; use the near-solid number for the parts marked thin.

These two columns are rough per-part bounds from `out/parts_report.csv`. For plastic, time and cost of the whole plan use
`out/print_cost.txt` (see "Plastic, time and cost" below): it applies the settings in `print_settings.py` (3 walls, 5
top and bottom layers, 25% infill, supports allowance) part by part.

| Part (STL) | Qty | Size mm | Print orientation | g (25% rule) | g (near-solid) | Supports |
|---|---|---|---|---|---|---|
| `base_plate` | 1 | 160.1 x 160.1 x 48.1 | As assembled: underside down, pockets and bays open upward | 205.2 | 820.7 | none (one piece; speaker and jack holes bridge a few mm) |
| `turntable` | 1 | 150.0 x 150.1 x 43.2 | Plate down, cradle wall up | 30.7 | 122.9 | none (the servo slot is open at the top) |
| `turntable_hub` | 1 | 34.0 x 34.0 x 5.2 | Floor down (upside down compared with how it sits in the turntable) | 0.8 | 3.4 | none |
| `column_left` | 1 | 58.1 x 116.1 x 100.1 | Standing on its foot ring (half-pipe upright, cut face to the side). Use a brim. | 14.5 | 58.0 (thin) | none (lugs have 45 degree undersides) |
| `column_right` | 1 | 58.1 x 116.1 x 100.1 | Same | 14.6 | 58.3 (thin) | none |
| `bob_carriage` | 1 | 112.0 x 77.0 x 63.0 | Frame down, stem up | 14.6 | 58.3 | none (45 degree fillet at the stem foot) |
| `lift_yoke` | 1 | 21.5 x 7.0 x 38.5 | Flange down, blade up | 0.8 | 3.1 | none |
| `lift_lever` | 1 | 41.0 x 20.0 x 5.0 | Flat | 0.7 | 2.8 | none |
| `neck_base_A` | 1 | 62.3 x 62.0 x 58.1 | Plug down, flange above | 14.9 | 59.7 | none (45 degree sleeve and skirt under the flange and uprights; the two cross screws are M3 x 10 in counterbores) |
| `neck_rocker_B` | 1 | 50.5 x 44.0 x 35.5 | As assembled | 8.2 | 33.0 | none |
| `neck_head_plate_C` | 1 | 88.0 x 88.0 x 36.0 | Plate down, legs up | 8.9 | 35.6 | none |
| `head_half_left` | 1 | 84.2 x 122.1 x 61.1 | Lying on its split face | 10.8 | 43.3 (thin) | YES: top ~30% of the dome and the collar flange (tree supports) |
| `head_half_right` | 1 | 84.2 x 122.1 x 61.1 | Lying on its split face | 10.8 | 43.4 (thin) | YES: same |
| `shoulder_socket_right` | 1 | 19.8 x 36.0 x 23.1 | Pocket opening upward | 3.0 | 12.1 | none |
| `shoulder_socket_left` | 1 | 19.8 x 36.0 x 23.1 | Pocket opening upward | 3.0 | 12.1 | none |
| `shoulder_cap` | 0 | 19.8 x 36.0 x 10.0 | Flange down | 1.1 each | 4.5 each (thin) | none (not printed on the shared base: both shoulder servos stay fitted; the part is still in the code at 0 copies) |
| `arm_horn` | 2 | 34.0 x 20.0 x 9.0 | Disc down | 0.8 each | 3.4 each | none (grips the 2 mm armature wire; part of the base set, take them off when an armless skin goes on) |
| `cloud_former_left` | 1 | 103.3 x 131.2 x 67.1 | Lying on its split face | 10.4 | 41.5 (thin) | YES: puffs and crown (tree supports) |
| `cloud_former_right` | 1 | 103.3 x 131.2 x 67.1 | Lying on its split face | 10.4 | 41.5 (thin) | YES: same |
| `skin_ring_1` to `skin_ring_4` | 4 (optional spares) | 110.0 x 110.0 x 3.2 | Flat | 2.1 each | 8.5 each (thin) | none (notches on the edge: 1 to 4, to tell them apart; not in the totals) |
| `dummy_core` | 5 | 110.4 x 110.4 x 58.4 | Collar down | 8.5 each | 34.1 each (thin) | none (45 degree cone) |

`base_plate_left` and `base_plate_right` are superseded by the one-piece `base_plate`. The two files stay in `out/` but are not listed as parts to print.

### Plastic, time and cost

From `out/print_cost.txt` (model estimate at the settings below; the slicer on Andy's printer wins):

- Shared base set: 756.9 g, GBP 15.14, about 19 to 30 printer hours. 16 files, 17 pieces: `base_plate` 296.4 g, `turntable` 78.3, `turntable_hub` 3.4, `column_left` 57.1, `column_right` 57.1, `bob_carriage` 45.2, `lift_yoke` 3.1, `lift_lever` 2.8, `shoulder_socket_left` 9.5, `shoulder_socket_right` 9.5, `neck_base_A` 39.2, `neck_rocker_B` 22.9, `neck_head_plate_C` 27.4, `head_half_left` 49.6, `head_half_right` 49.7, `arm_horn` 2 x 2.9.
- Skins: Jolly 127.0 g (GBP 2.54), Clawd 124.9 g (2.50), Cloud 133.2 g (2.66, formers plus beret), Pear 122.4 g (2.45, with the round glasses), Frog 98.0 g (1.96), Heart 114.7 g (2.29, with the sunglasses). The six skins come to 720 g, GBP 14.40, about 18 to 29 printer hours.
- Dummy cores: 5 x 34.0 g = 170.1 g, GBP 3.40 (GBP 0.68 each), about 4 to 7 printer hours.
- Optional spare skin rings 1 to 4: 8.5 g each, not in the totals.
- Total, one base plus six skins plus five dummy cores: about 1,647 g (1.65 kg), GBP 32.94 of filament at GBP 20/kg, and about 42 to 67 printer hours on the H2D (25 to 40 g/h, about 7 plates at 6 minutes set-up each; a guide only).
- Before the shared base, at the old 15% infill (so not comparable with the figures above): base set 721 g, one shared base plus six skins 1,481 g, and six full toys each with its own base 5,100 g.

Dummy core (`dummy_core`): a cheap, light printed former, 110 x 110 x 58 mm, 34 g, about GBP 0.68 each, printed collar down without supports. The five skins that are not on the base sit on a core on the shelf so they keep their shape. Print 5. Checked: zero overlap with all six skins. It has six magnet pockets like the head; magnets in the cores are optional.

Supports: the hidden parts print without supports (base plate, turntable, turntable hub, columns, carriage, yoke, lever, neck A, B and C, shoulder sockets, arm horns, dummy core). Only the head halves, the shells, the Cloud formers and the clip-ons (beret, glasses, sunglasses) still need supports. What remains in the hidden parts are short bridges only: the 12 mm jack hole, the 6 mm channels and the roofs of the magnet pockets. Neck base A prints without supports because its sleeve and skirt are at 45 degrees; the turntable prints without them because the hub is a separate part.

Base hollowing: the base plate has pocket logic that cuts a hollow pocket only where it saves enough plastic for the walls it adds. At the current 25% infill 5 of the 10 open-top pockets pay and are cut: the two big wells plus the voids under the ESP32, the PCA9685 and the buck converter, about 40 g saved in total; the other 5 stay solid. (At the old 15% infill only 2 paid, the voids under the ESP32 and the PCA9685, about 3 g in total.) The report is `out/base_pockets.csv`.

Print settings (all in `print_settings.py`, so they are easy to change): Andy's Bambu Lab H2D, bed 325 x 320 x 325 mm (single-nozzle build area), 0.4 mm nozzle, 0.2 mm layers, 3 walls, 5 top and bottom layers, 25% infill, Bambu PLA Basic at 1.24 g/cm3, GBP 20/kg (full price), shrink 0%. The shrink figure is still to be agreed with Andy (see `print/README-PRINT.txt`); the parts are drawn true size. After changing the settings, run `.venv\Scripts\python.exe print_cost.py`; it writes `out/print_cost.txt`. Every part fits the H2D bed (it also still fits a 220 x 220 mm bed). PETG would be better for the lever, yoke and gimbal (tougher, less creep); PLA is fine for everything else, and the cost model assumes PLA throughout.

## Hardware list

Mechanics
- 1 x lazy-susan turntable bearing, 72 mm outside diameter: the one in the shopping basket (Amazon B0FBLK3JLH), which the design now uses. Still CHECK against the real bearing: the model assumes about a 38 mm centre hole, 7 mm tall, and three M3 holes on a circle of about 58 mm.
- 2 x MG996R servos (yaw, and bob lift), 4 x MG90S servos (neck nod, neck tilt, two shoulders). The MG90S is what the basket buys and has the same body and tabs as the MG90D the CAD was first drawn for. Its torque is a bit lower (about 1.8 against 2.2 kg.cm), so check the nod and tilt once a head is on. Keep each servo's own horn and screws.
- 1 x extension spring for the bob return (needs to stretch from about 33 mm to about 67 mm without over-stretching; free length about 25 to 30 mm; CHECK the force once built).
- 1 x M5 bolt, about 20 mm, with a nut: it is the pin the lift lever uses to push the carriage (its smooth shank rides in the yoke slot).
- Steel M16 flat washers (30 mm outside diameter) as ballast: two wells, 40 mm deep each, about 13 washers per well, roughly 150 g per well (CHECK your washers' thickness).
- No dowel pins: the base plate is one piece.
- 4 x rubber feet, 12 mm diameter (recesses are 12.2 mm).
- 2 mm aluminium armature wire for the arms: two lengths, each as long as you want the arm plus 19 mm that goes into the horn.
- Electronics that the base is shaped for (one set for the one base; an ESP32 spare is sensible): ESP32 dev board (55 x 28 mm), PCA9685 servo driver (62 x 25 mm), 5 V buck converter (44 x 21 mm), 40 mm speaker, 12 mm barrel-jack panel socket, and a power supply sized for the servos (CHECK).

Magnets (5 mm diameter x 2 mm, N35)
- 6 in the head collar (loaded from inside the head, before the halves are closed).
- 6 per skin you fit, loaded from underneath, opposite polarity to the head ones. Mark the polarity with a pen on all of them before loading.
- One head plus the six skins (cloud, pear, frog, heart, Jolly, Claude): 42 magnets (6 + 6 x 6). If every dummy core gets magnets too (optional): 72. With the four optional spare skin rings as well: 96. The beret, glasses and sunglasses need none (they grip the head sphere).

Screws (counts come from the holes in the CAD; use self-tapping into the printed pilot holes or tap them)
- M3: 35 for the base set, in assorted lengths of 8 to 16 mm (a 200-piece M3 kit covers it), plus 6 M3 nuts for the column foot. Breakdown: bearing 6 (3 into the base, 3 into the turntable), column foot 6, column halves 6, yoke 2, spring anchor 1, stem cross-screws 2 (M3 x 10, in counterbores), shoulder sockets 4, neck pivots 2, head plate to head 4, head halves 2. There are no base-half screws now that the base plate is one piece. Add 2 M3 for every character shell you print.
- M4: 8 (4 per MG996R, self-tapping into 3.4 mm pilot holes), about 14 mm long.
- M2: 16 (servo ears on the four MG90S 8, arm-horn pinch screws 2, arm-horn centre screws 2, turntable hub 4 at about 8 mm), about 6 to 8 mm long. The small horn screws that come with the servos cover the remaining horn fixings (neck horns, lever horn, printed arm horns; the printed arm horn has four 1.2 mm pilot holes for these, CHECK against your horns).

## Assembly order

1. Print and test-fit one servo mount first (see "Check before you print"). Do not print the whole kit before this.
2. Base: the base plate is one piece, so there is nothing to join; stick on the rubber feet.
3. Yaw servo: drop the MG996R (shaft up) into the pocket from above and fix it with 4 M4 screws. Run its lead along the cable lane.
4. Ballast: drop the washers into the two round wells. Fit the ESP32, PCA9685 and buck converter in their bays, the speaker behind the front wall, the barrel jack in its hole. Wire up.
5. Bearing: seat it in the recess in the top of the base and fix with 3 M3 screws.
6. Turntable and hub: press the six M3 nuts into the hex traps on the turntable's underside (a dab of glue holds them). Seat the stock servo horn in the recess of the `turntable_hub`, lower the turntable onto the bearing and the yaw servo spline, fix the horn and hub to the turntable plate with the 4 M2 x 8 screws (up through the horn and the hub into the plate), then fasten the plate to the bearing's upper ring with 3 M3 screws and put the centre horn screw through the access hole.
7. Lift servo: fit the second MG996R lying down in the cradle wall with 4 M4 screws; put the lever on its horn, and fit the M5 pin bolt.
8. Torso: fix the yoke under the carriage with 2 M3 screws; close the two column halves around the carriage so the slider blocks run in the side slots, join the halves with 6 M3, and fix the column foot to the turntable with 6 M3 and the nuts. Then bolt a shoulder socket onto each slider block end that pokes through the slot (2 M3 each; the screws go in from the servo pocket). Hook the spring between the turntable lug and the screw on the carriage.
9. Neck: plug neck base A into the carriage stem (2 M3 x 10 cross-screws, heads in the counterbores). Fit the nod MG90S in A's right upright, rocker B onto its horn, the M3 pivot through A's left upright into B. Fit the tilt MG90S in B's front wall, head plate C onto its horn, and the M3 pivot through B's back wall into C.
10. Head: load 6 magnets into the collar pockets, close the head halves with 2 M3, then fix the head to plate C with 4 M3.
11. Faces and shells: load 6 magnets (opposite polarity) into a skin ring or character shell and press it onto the collar. Clip on the beret or glasses if wanted.
12. Arms: Jolly's two arm horns are part of the base set. Fit a printed arm horn on each shoulder servo, push in the armature wire and pinch it with the M2 screw. When an armless skin goes on, take the arm horns off; both shoulder servos stay fitted and no shoulder caps are printed.
13. Shelf: each of the five skins that is not on the base sits on a printed dummy core (magnets in the cores are optional) so it holds its shape.

## Character shells and clip-ons

Each shell is hollow with a 1.5 mm wall (set by `SHELL_WALL`), prints in two halves lying on the split face, and attaches
to the head through the 110 mm collar: a 3.2 mm mating plate with six magnet pockets, and two M3 lugs at the front and
back seam join the halves. Printed with 0 to 5% infill they weigh about as much as the near-solid column below, because
1.5 mm walls are almost all perimeter. Every shell is under the 200 g limit, valid (one solid per half) and has zero
overlap with the head sphere.

| Part (STL) | Size mm (W x D x H) | g (25% rule) | g (near-solid) | Supports |
|---|---|---|---|---|
| `cloud_former_left/right` | 103 x 131 x 67 per half | 20.8 | 83.0 | yes, tree supports |
| `shell_pear_left/right` | 127 x 146 x 70 per half | 25.8 | 103.1 | yes: dome crown and the stalk |
| `shell_frog_left/right` | 100 x 132 x 71 per half | 21.4 | 85.5 | yes: eye domes and cheeks |
| `shell_heart_left/right` | 107 x 132 x 67 per half | 23.4 | 93.7 | yes: both lobes |
| `shell_jolly_left/right` | 126 x 144 x 72 per half | 27.6 | 110.5 | yes: hood peak, flank slots, open hem rim |
| `shell_claude_left/right` | 110 x 130 x 98 per half | 27.2 | 108.6 | yes: the flat roof (the inside of the outer side wall) and the arm ends, about 15 percent overhang (tree supports); 1.0 mm wall |
| `clip_beret` | 119 x 115 x 51 | 8.3 | 33.2 | yes: underside of the saucer (print crown-down on the stalk, or rim-down with supports under the saucer) |
| `clip_glasses_round` | 109 x 82 x 26 | 0.9 | 3.4 | yes: light tree supports under the lower rims and the temple bands (print it the way Pear wears it) |
| `clip_sunglasses` | 138 x 89 x 21 | 1.6 | 6.2 | yes: light tree supports under the lens plates and the temple bands (print it the way Heart wears it) |

(The shell masses above are for the pair; sizes are per half. Rebuild them with
`.venv\Scripts\python.exe build_shells.py` or just some of them with `build_shells.py pear jolly`; names are
pear frog heart jolly claude beret glasses sunglasses.)

Jolly hem: raised to -26 mm below the collar plane (`JOLLY_HEM_Z` in `build_shells.py`, 17 Oct 2026; it was -58, then -40), so the shell is 126 mm tall instead of 158 mm (it was 158 x 144 x 72, 33.6 g and 134.4 g). At -58 the hem hit the column at rest beyond about 13 degrees of nod or 10 degrees of tilt; at -40 it still touched when full nod and full tilt were used together. -26 clears the full nod 30 plus tilt 25 corner at rest.

Head mass budget (spec: 250 g or the MG90S neck stalls; the MG90S has a bit less torque than the MG90D the CAD was first drawn for, about 1.8 against 2.2 kg.cm, so check the nod and tilt once a head is on). My estimate for what hangs above the neck, counting the two
head halves and head plate C near-solid (122 g) plus the shell, before magnets, screws and any fabric:

- Cloud 205 g, frog 208 g, heart 216 g, pear 225 g: inside the budget.
- Claude 231 g (122.3 g of head halves and plate C plus the 108.6 g shell pair): inside the budget by about 19 g, second heaviest, 2 g under the Jolly. This is with a 1.0 mm wall on Clawd; at the 1.5 mm wall of the other shells the pair would be 154.9 g and the head 277 g, over the budget (see the Claude note below).
- Jolly 233 g (122.3 g of head halves and plate C plus the 110.5 g shell pair; it was 257 g before the hem was raised to -26): inside the budget by about 17 g, but still the heaviest of the six. Magnets, screws and fabric add more, and the rocker B and tilt servo also ride on the nod servo. Test it with real weights, print the head halves and Jolly with a thinner wall (`HEAD_WALL` in the base file, `SHELL_WALL` here), or fit the Jolly only with a stronger neck servo.

Notes on specific shells and clip-ons
- Heart: the point is cut flat at the collar plane, because a shell that hangs lower would hit the neck gimbal. It reads as a heart from the top cleft and the two lobes, not from a pointed bottom.
- Jolly: 126 mm tall hooded head-and-torso shell with a hood ridge and a swept cut-out on each shoulder flank for the mitten arms (cleared up to 80 degrees of arm swing). The hem is at -26 mm below the collar (raised from -58, then -40, on 17 Oct 2026), which is well above the shoulder sockets (those sit about 119 mm below the collar), so it hides the head and the top of the neck, not the shoulders or torso, and about 38 mm of the neck flange shows under the hem. The arm cut-outs are swept clearance slots, not tailored to the neck at every nod and tilt. Its wide hem swings down toward the top of the column when the head moves (measured by distance in CadQuery, no printing involved). Body at rest, hem at -26, worst case over nod plus or minus 30 and tilt plus or minus 25 including all four full corners: 4.2 mm gap (at the full corner; re-run on 23 Oct against the new base and unchanged at 4.24 mm). Single extremes at rest: full nod alone 14.6 mm, full tilt alone 15.8 mm. Earlier hems for comparison: at -58 it touched beyond about 13 degrees of nod or 10 degrees of tilt; at -40 nod alone and tilt alone cleared (5.5 and 2.1 mm) but the combined corner touched (0.0 mm); at -30 the corner gap was 1.9 mm. The cloud, pear, frog, heart and Claude shells stop at the collar plane, so they cannot reach the column.
- Claude: drawn as Clawd, the Claude Code mascot, made plush. The printed shell is a chunky rounded cube with two stub arms; the four legs are soft fleece and are not printed (next paragraph). Body 126 mm wide, 130 mm deep and 110 mm tall (from the underside of the mating plate at -3.2 mm up to 106.8 mm above the collar plane), with a flat front, the four vertical edges rounded 18 mm, the top edges 16 mm and the bottom edges 8 mm (the six magnet pockets need a flat floor out to 56 mm). Arms: one rounded block on each side at mid height, 35 mm out of the flat side face, 40 mm deep and 37 mm tall (about a third of the body), every edge rounded 12 mm; they are hollow and open into the body. Whole shell 196 mm wide, 130 mm deep, 110 mm tall (z -3.2 to 106.8). That is 6 mm over the 170 to 190 mm width aim: the body cannot get narrower than about 126 mm because the head cavity (123.6 mm) has to fit inside it with a wall, and 35 mm is already the short end of the 35 to 45 mm arm range. Wall 1.0 mm, not the 1.5 mm of the other shells, on purpose: a cube round a 120 mm sphere has far more skin than a sphere, and the shell pair measured 154.9 g at 1.5 mm (head 277 g, over the 250 g budget), 127.5 g at 1.2 mm (head 250 g, no margin) and 108.6 g at 1.0 mm (head 231 g). The solid 3.2 mm mating plate is only a ring (96 mm hole out to 116 mm across) so a wide flat floor does not carry a 3.2 mm slab across its whole footprint; the six magnet pockets and the two M3 lugs are as on the other shells (the lug blocks are trimmed to the outer shape). Parameters: `CLAWD_*` in `build_shells.py`. Valid solid per half, 0.0 mm3 overlap with the head. Built by `shell_full_solid` / `shell_halves_solid`, a variant of the shell recipe that takes any outer and cavity solid, so the other shells' code was not touched. Eyes are beads sewn on the fleece, not CAD; there is no mouth.
  Legs: four short stubby legs, 22 mm wide, 30 mm deep and 28 mm long with rounded ends, in a row across the front-to-back centre, evenly spaced (centres at -47, -15.7, +15.7 and +47 mm, outer edges at plus and minus 58 mm), so all four show from the front. They are soft stuffed fleece tubes sewn to the skin, NOT printed; `clawd_soft_legs()` only draws them (see-through) in the preview pictures. Why not printed: printed legs cannot keep the 8 mm gap to the neck. Tried by adding printed leg blocks to the built halves and running the same nod and tilt sweep (worst gap to the neck base A at nod -30 / tilt -25 or the carriage-up corner): outer pair 28 mm long 0.0 mm (touching), 20 mm 2.8 mm, 14 mm 5.4 mm, even 8 mm only 7.2 mm. The inner pair cannot be printed at all: they sit under the 96 mm neck hole, so there is nothing to fix them to, and they overlap the neck rocker B even at rest. Printed legs would also add about 18 g and put the head at about 249 g on a 250 g budget. The soft legs need care too (same sweep, full 28 mm legs): the outer pair is 5.0 mm clear of the neck at rest and touches the neck base A at the nod -30 / tilt -25 corner, and the inner pair overlaps the neck rocker B at rest. Fleece squashes, so this is a sewing note, not a hard stop: stuff the legs lightly (or make the inner pair short flat pads of about 8 mm, 4.6 mm clear at rest, still touching at the corner) and test with the real fleece.
  Clearance (`check_shell_clearance.py`, exact CadQuery distance, shell moved with the head, arms not applicable on the round characters; the same method reproduces the Jolly's 4.2 mm corner gap above; the printed shell only, the soft legs are covered above). Smallest gap to any base part, body at rest, nod / tilt in degrees: -30 / -25 12.0 mm; -30 / 0 15.4; -30 / +25 12.0; 0 / -25 10.6; 0 / 0 17.5; 0 / +25 10.6; +30 / -25 17.2; +30 / 0 17.5; +30 / +25 17.2. With the carriage fully up (bob 33.9 mm) the four corners give 12.0 mm (nod -30) and 17.2 mm (nod +30). Worst case 10.6 mm (collar plate to neck base A at tilt plus or minus 25; re-run on 23 Oct against the new base and unchanged at 10.56 mm), well over the 8 mm aim; the figures are the same as for the old starburst shell because the nearest point is the mating plate, which has the same inner edge. The body and arms never come near the column or the turntable, because the shell ends at the collar plane. Shell to head plate C: 5.7 mm. These are CAD distances with no printing tolerance (CHECK on the printed parts).
  Printing: lies on its split face, each half 110 x 130 x 98 mm (fits the H2D bed in `print_settings.py`, and a 220 x 220 mm bed too). About 15.0 percent of the surface is overhang (faces facing down and steeper than 45 degrees, not counting the bed contact; the same method gives 15.8 percent for the Jolly and 15.3 for the pear, and gave 10.9 for the old starburst). It is mostly the flat roof, the inside of the outer side wall (it faces down when the half lies on its split face), plus the flat end of each arm and the rounded top and bottom edges, so use tree supports (CHECK in the slicer; not test-printed). Measured alternatives for the left half: standing on the mating plate 13.0 percent, on its front face 12.5 percent, upside down with the flat top on the bed 10.2 percent (about 4,800 mm2 on the bed), so upside down is worth trying first; the STLs are exported in the usual split-face-down orientation. Cautions: in the exported orientation only the 1.0 mm wall edge and the plate ring touch the bed (about 475 mm2), so use a brim, and 1.0 mm is only about two 0.4 mm lines.
- Glasses and sunglasses: they hold on with a springy temple hook, designed with about 0.5 to 1.1 mm of deliberate squeeze. This has not been tested on a printed head; if they are loose or crack, change the `G_*` and `SUN_*` numbers.
- Beret: a plain friction fit (0.15 mm clearance), so it may slide when the head nods. A small dab of Blu-Tack on the inside fixes that.

## Check before you print

1. Servo pocket fit. Calipers on your actual servos, then compare with the (CHECK) numbers in the PARAMETERS block: MG90S tab-top height 20.5 mm, ear hole spacing 27.8 mm, shaft offset 6.0 mm (same body and tabs as the MG90D); MG996R tab-top height 28.0 mm, ear holes 49.5 x 10 mm, shaft offset 10.5 mm. Print the small `shoulder_socket_right` and `neck_base_A` first; they test the MG90S pocket. An MG996R pocket test is the base plate (a long print, now one piece) or just the turntable, which holds the lift-servo cradle.
2. Magnet pocket tolerance. Pockets are 5.4 mm wide and 2.2 mm deep for a 5 x 2 mm magnet, leaving 0.8 mm of plastic skin on the mating face. Print one skin ring first and press a magnet in: it should seat firmly without splitting the skin. If tight or loose, change `CLEAR` or `MAG_D`.
3. Head mass. See the budget above; the Jolly is the heaviest of the six (233 g against 250 g; Claude is 231 g). Weigh the printed head halves and shell before choosing the final neck servo. The MG90S has a bit less torque than the MG90D (about 1.8 against 2.2 kg.cm), so check the nod and tilt once a head is on.
4. Gimbal hinge gaps. 0.4 to 0.5 mm in the CAD is tight for FDM. If the hinges fuse or bind, raise `CLEAR` or sand the faces.
5. Bearing numbers. The design uses the 72 mm lazy-susan bearing from the shopping basket (Amazon B0FBLK3JLH, `BEARING_OD`). The 38 mm centre hole, 7 mm height and three M3 screws on a 58 mm circle are still CHECK: measure yours and change `BEARING_ID`, `BEARING_H`, `BEARING_SCREW_R`.
6. Supports. Only the head halves, the shells, the Cloud formers and the clip-ons need supports. The hidden parts, including the turntable and neck base A, print without them and have short bridges only (the 12 mm jack hole, the 6 mm channels and the magnet pocket roofs).
7. Jolly shell and the column. With the hem at -26 it clears the column at rest across the full nod (plus or minus 30) and tilt (plus or minus 25) range, worst case 4.2 mm at the combined corners (see the shell notes). That is a CAD distance with no printing tolerance, so check it on the printed parts with the head at full nod plus tilt. The skin clearance was re-run on 23 Oct for Pear, Frog, Heart, Jolly and Clawd against the new base and is unchanged: Jolly's worst case is 4.24 mm to the column at the nod and tilt extremes, and the others are 10.56 mm to neck base A.

## Known limits and what was skipped

- Nothing has been physically printed or bench-tested. The collision check covers the head sphere, neck gimbal, column and carriage (the grid above) and, for the Jolly and Claude shells, a separate set of checks (below, and `check_shell_clearance.py`). It does not model servo bodies, wires or fabric.
- The shell and cloud right-hand halves are built as a mirror of the left, because cutting a union of spheres straight down the middle upset the CAD kernel (it returned an invalid, near-empty solid). The mirror is exact; the lug holes are cut afterwards so left and right differ correctly (clearance holes on one, pilot holes on the other).
- Magnet pockets are placed at 0, 60, 120... degrees so none lands on the split plane.
- Nothing requested was skipped. Every part in the brief exists: a one-piece base plate, turntable with a separate hub, torso column in two halves with the lift carriage, yoke and lever, three-part neck gimbal, head sphere in two halves with the 110 mm collar, four optional skin rings, two shoulder sockets and arm horns (the shoulder caps are no longer printed), the dummy core, the example cloud shell, the pear, frog, heart, Jolly and Claude shells, the beret, round glasses and sunglasses.

## Changing the design

Open `build_puppet_base.py` and edit the PARAMETERS block at the top (wall 2.4, clearance 0.2, magnet 5 x 2, sphere 120,
collar 110, the servo sizes, the bearing size, the bob lever). The print settings (bed, nozzle, layers, walls, infill, filament, shrink) are in `print_settings.py`. Then, from this folder in PowerShell:

    $env:PYTHONIOENCODING='utf-8'
    .\.venv\Scripts\python.exe build_puppet_base.py       # all base parts, parts_report.csv, collision check (several minutes)
    .\.venv\Scripts\python.exe render_preview.py          # the preview pictures
    .\.venv\Scripts\python.exe render_preview.py claude   # only out/preview_claude.png
    .\.venv\Scripts\python.exe build_shells.py            # all shells and clip-ons (or name some: pear frog heart jolly claude beret glasses sunglasses)
    .\.venv\Scripts\python.exe check_shell_clearance.py claude     # shell-to-base gaps over nod and tilt (add --bob for the carriage-up corners)
    .\.venv\Scripts\python.exe build_puppet_base.py --no-check     # after changing the infill in print_settings.py: the infill decides which base pockets are cut
    .\.venv\Scripts\python.exe print_cost.py                       # plastic, time and cost; writes out/print_cost.txt
