# Universal motorised puppet base - printable CAD

A parametric, all-printed puppet body: a turntable that spins the whole puppet, a torso column that bobs up and down,
a two-axis neck (nod and tilt), a 120 mm head sphere, and a family of clip-on character shells (cloud, pear, frog, heart,
hooded Jolly, starburst Claude) plus small clip-ons (beret, round glasses, sunglasses). Everything is designed for a home FDM printer in
PLA or PETG, with no supports wherever that was possible. The source of truth is the Python file at the top of the
project; change a number in its PARAMETERS block and re-run to get new STLs.

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
| `out/*.stl` | One STL per part, already turned to its print orientation (lowest point at z = 0). Import and slice as-is. |
| `out/parts_report.csv`, `out/shells_report.csv` | Size, volume, grams and support notes for every part. |
| `out/shell_clearance.csv` | Smallest gap between a shell and the base parts, per pose (written by `check_shell_clearance.py`). |
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
- `out/preview_claude.png` - the Claude shell on the full base, seen from the front, two poses side by side: at rest, and bobbed up 33.9 mm with the head nodded 20 and tilted 20 degrees (no arms fitted).

## Key numbers

- Overall height at rest, to the top of the head sphere: 311 mm. Head collar plane sits 227 mm above the floor.
- Bob throw: 33.9 mm (lever 24 mm, swings plus and minus 45 degrees; target was 30-40 mm).
- Neck range: nod plus and minus 30 degrees, tilt plus and minus 25 degrees.
- Shoulder arms swing plus and minus 80 degrees.
- Collision check (head sphere and neck gimbal against the column, carriage and neck parts) over bob {0, max} x nod {-30, 0, +30} x tilt {-25, 0, +25}: worst overlap 0.0 mm3, method: boolean intersection volume in CadQuery.
- Closest approaches in the neck gimbal (tight for a printer): rocker B to base A 0.50 mm, head plate C to rocker B 0.40 mm, head plate C to base A at least 3.2 mm.
- Mesh check: all 36 STLs in `out/` are watertight with a consistent winding (checked with trimesh) and rest on z = 0. Twelve dome-shaped parts (head halves, shells) first came out of the CAD mesher with one to four zero-area triangles each; `clean_stl()` in `build_puppet_base.py` now removes them on export (volume unchanged).

## How it moves

- Yaw (spin): an MG996R sits in a pocket in the base plate with its shaft up. Its horn is fixed in the hub under the turntable, and the turntable rides on the 70 mm bearing. The turntable therefore carries the bearing recess, the column and the cradle for the second MG996R.
- Bob (up and down): that second MG996R lies in the cradle wall on the turntable. A 24 mm lever with an M5 pin pushes a slot in the yoke under the carriage; the carriage slides in two vertical guide channels (the bob rails) inside the column, and an extension spring pulls it back down.
- Neck: a three-part gimbal (base A on the carriage stem, rocker B, head plate C) with one MG90D for nod and one for tilt.
- Head: a 120 mm sphere split down the middle, with the 110 mm magnet collar at the bottom. Skin rings and character shells snap on with six 5 x 2 mm magnets.
- Shoulders: an MG90D socket bolted to each side of the carriage (so the arms bob with the body); the printed horn grips a 2 mm aluminium wire. A blanking cap fills a socket that has no servo.

## Part list, print orientation, grams

All STLs in `out/` are already in the orientation below. Sizes are the printed bounding box (X x Y x Z, mm).

Grams: two estimates, because the two kinds of part behave differently.
- Assumption stated: volume x 1.24 g/cm3 (PLA) x 0.25 infill factor. This is the "25% rule" and is right for chunky parts.
- "Near-solid" is volume x 1.24 with no infill factor. Thin-walled parts (walls 1.5 to 2.4 mm) print almost entirely
  as perimeters, so the 25% rule underestimates them; use the near-solid number for the parts marked thin.

| Part (STL) | Qty | Size mm | Print orientation | g (25% rule) | g (near-solid) | Supports |
|---|---|---|---|---|---|---|
| `base_plate_left` | 1 | 80.1 x 160.2 x 48.1 | As assembled: underside down, bays open upward | 113.7 | 454.7 | none (speaker and jack holes bridge a few mm) |
| `base_plate_right` | 1 | 80.1 x 160.1 x 48.1 | Same | 112.3 | 449.3 | none |
| `turntable` | 1 | 150.0 x 150.1 x 48.4 | Hub down, plate above, cradle wall up | 30.6 | 122.3 | YES: the 5 mm plate overhangs the 34 mm hub all round, so it needs support under the plate, plus the cradle window |
| `column_left` | 1 | 58.1 x 116.1 x 100.1 | Standing on its foot ring (half-pipe upright, cut face to the side). Use a brim. | 14.5 | 58.0 (thin) | none (lugs have 45 degree undersides) |
| `column_right` | 1 | 58.1 x 116.1 x 100.1 | Same | 14.6 | 58.3 (thin) | none |
| `bob_carriage` | 1 | 112.0 x 77.0 x 63.0 | Frame down, stem up | 14.6 | 58.3 | none (45 degree fillet at the stem foot) |
| `lift_yoke` | 1 | 21.5 x 7.0 x 38.5 | Flange down, blade up | 0.8 | 3.1 | none |
| `lift_lever` | 1 | 41.0 x 20.0 x 5.0 | Flat | 0.7 | 2.8 | none |
| `neck_base_A` | 1 | 62.0 x 62.0 x 54.0 | Plug down, flange above | 8.0 | 32.0 | YES: small supports under the flange rim |
| `neck_rocker_B` | 1 | 50.5 x 44.0 x 35.5 | As assembled | 8.2 | 33.0 | none |
| `neck_head_plate_C` | 1 | 88.0 x 88.0 x 36.0 | Plate down, legs up | 8.9 | 35.6 | none |
| `head_half_left` | 1 | 84.2 x 122.1 x 61.1 | Lying on its split face | 10.8 | 43.3 (thin) | YES: top ~30% of the dome and the collar flange (tree supports) |
| `head_half_right` | 1 | 84.2 x 122.1 x 61.1 | Lying on its split face | 10.8 | 43.4 (thin) | YES: same |
| `shoulder_socket_right` | 1 | 19.8 x 36.0 x 23.1 | Pocket opening upward | 3.0 | 12.2 | none |
| `shoulder_socket_left` | 1 | 19.8 x 36.0 x 23.1 | Pocket opening upward | 3.0 | 12.2 | none |
| `shoulder_cap` | 2 | 19.8 x 36.0 x 10.0 | Flange down | 1.1 each | 4.5 each (thin) | none (blanks off an empty socket; one STL fits both sides) |
| `arm_horn` | 2 | 34.0 x 20.0 x 9.0 | Disc down | 0.8 each | 3.4 each | none (grips the 2 mm armature wire) |
| `cloud_former_left` | 1 | 103.3 x 131.2 x 67.1 | Lying on its split face | 10.4 | 41.5 (thin) | YES: puffs and crown (tree supports) |
| `cloud_former_right` | 1 | 103.3 x 131.2 x 67.1 | Lying on its split face | 10.4 | 41.5 (thin) | YES: same |
| `skin_ring_1` to `skin_ring_4` | 4 | 110.0 x 110.0 x 3.2 | Flat | 2.1 each | 8.5 each (thin) | none (notches on the edge: 1 to 4, to tell them apart) |

Totals (base set):
- Core base without the cloud shell and rings: about 358 g by the 25% rule, about 1,434 g if everything printed solid.
- A more honest estimate (chunky parts at 25%, thin-walled parts near-solid): about 520 g, so one 1 kg spool is plenty.
- Skin rings x 4: 8 g (25% rule) or 34 g (near-solid). Cloud shell (pair): 21 g or 83 g.

Parts that still need supports: turntable, neck base A, both head halves, and every character shell half (see below).
Everything else prints support-free. The supports on the turntable are the largest job (all of the plate underside
around the hub); tree supports and a 0.2 mm support interface make them easy to remove.

Suggested settings (my defaults, not tested): 0.4 mm nozzle, 0.2 mm layers, 3 to 4 perimeters on anything that carries
load (column, carriage, gimbal, lever, yoke, sockets), 25% gyroid for the base plates. PETG is better for the lever,
yoke and gimbal (tougher, less creep); PLA is fine for everything else.

## Hardware list

Mechanics
- 1 x lazy-susan turntable bearing, 70 mm outside diameter (CHECK: model assumes about 38 mm hole, 7 mm tall, three M3 holes on a circle of about 58 mm).
- 2 x MG996R servos (yaw, and bob lift), 4 x MG90D servos (neck nod, neck tilt, two shoulders). Keep each servo's own horn and screws.
- 1 x extension spring for the bob return (needs to stretch from about 33 mm to about 67 mm without over-stretching; free length about 25 to 30 mm; CHECK the force once built).
- 1 x M5 bolt, about 20 mm, with a nut: it is the pin the lift lever uses to push the carriage (its smooth shank rides in the yoke slot).
- Steel M16 flat washers (30 mm outside diameter) as ballast: two wells, 40 mm deep each, about 13 washers per well, roughly 150 g per well (CHECK your washers' thickness).
- 3 x 4 mm dowel pins, about 14 mm long (wood or steel), to align the two base halves.
- 4 x rubber feet, 12 mm diameter (recesses are 12.2 mm).
- 2 mm aluminium armature wire for the arms: two lengths, each as long as you want the arm plus 19 mm that goes into the horn.
- Electronics that the base is shaped for: ESP32 dev board (55 x 28 mm), PCA9685 servo driver (62 x 25 mm), 5 V buck converter (44 x 21 mm), 40 mm speaker, 12 mm barrel-jack panel socket, and a power supply sized for the servos (CHECK).

Magnets (5 mm diameter x 2 mm, N35)
- 6 in the head collar (loaded from inside the head, before the halves are closed).
- 6 per skin ring or shell you fit, loaded from underneath, opposite polarity to the head ones. Mark the polarity with a pen on all of them before loading.
- All four skin rings: 24. All six shells (cloud, pear, frog, heart, Jolly, Claude): 36. Printing everything needs 66 magnets; the head plus the rings alone is 30. The beret, glasses and sunglasses need none (they grip the head sphere).

Screws (counts come from the holes in the CAD; use self-tapping into the printed pilot holes or tap them)
- M3: 37 for the base set, in assorted lengths of 8 to 16 mm (a 200-piece M3 kit covers it), plus 6 M3 nuts for the column foot. Breakdown: base halves 2, bearing 6 (3 into the base, 3 into the turntable), column foot 6, column halves 6, yoke 2, spring anchor 1, stem cross-screws 2, shoulder sockets 4, neck pivots 2, head plate to head 4, head halves 2. Add 2 M3 for every character shell you print.
- M4: 8 (4 per MG996R, self-tapping into 3.4 mm pilot holes), about 14 mm long.
- M2: 12 (servo ears on the four MG90D 8, arm-horn pinch screws 2, arm-horn centre screws 2), about 6 to 8 mm long. The small horn screws that come with the servos cover the remaining horn fixings (neck horns, lever horn, printed arm horns; the printed arm horn has four 1.2 mm pilot holes for these, CHECK against your horns).

## Assembly order

1. Print and test-fit one servo mount first (see "Check before you print"). Do not print the whole kit before this.
2. Base: join the two halves with 2 M3 screws (down the two access wells) and the 3 dowels; stick on the rubber feet.
3. Yaw servo: drop the MG996R (shaft up) into the pocket from above and fix it with 4 M4 screws. Run its lead along the cable lane.
4. Ballast: drop the washers into the two round wells. Fit the ESP32, PCA9685 and buck converter in their bays, the speaker behind the front wall, the barrel jack in its hole. Wire up.
5. Bearing: seat it in the recess in the top of the base and fix with 3 M3 screws.
6. Turntable: press the six M3 nuts into the hex traps on its underside (a dab of glue holds them). Fix the stock servo horn into the hub recess, lower the turntable onto the bearing and the yaw servo spline, then fasten it to the bearing's upper ring with 3 M3 screws and the centre horn screw through the access hole.
7. Lift servo: fit the second MG996R lying down in the cradle wall with 4 M4 screws; put the lever on its horn, and fit the M5 pin bolt.
8. Torso: fix the yoke under the carriage with 2 M3 screws; close the two column halves around the carriage so the slider blocks run in the side slots, join the halves with 6 M3, and fix the column foot to the turntable with 6 M3 and the nuts. Then bolt a shoulder socket onto each slider block end that pokes through the slot (2 M3 each; the screws go in from the servo pocket). Hook the spring between the turntable lug and the screw on the carriage.
9. Neck: plug neck base A into the carriage stem (2 M3 cross-screws). Fit the nod MG90D in A's right upright, rocker B onto its horn, the M3 pivot through A's left upright into B. Fit the tilt MG90D in B's front wall, head plate C onto its horn, and the M3 pivot through B's back wall into C.
10. Head: load 6 magnets into the collar pockets, close the head halves with 2 M3, then fix the head to plate C with 4 M3.
11. Faces and shells: load 6 magnets (opposite polarity) into a skin ring or character shell and press it onto the collar. Clip on the beret or glasses if wanted.
12. Arms: fit a printed arm horn on each shoulder servo, push in the armature wire and pinch it with the M2 screw. If a shoulder is not used, fill its socket with a shoulder cap.

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
| `shell_claude_left/right` | 130 x 132 x 93 per half | 27.2 | 108.8 | yes: the two 38 degree rays, the arch over the top ray and the dome crown (tree supports); the 75 and 108 degree rays stand up nearly vertical |
| `clip_beret` | 119 x 115 x 51 | 8.3 | 33.2 | yes: underside of the saucer (print crown-down on the stalk, or rim-down with supports under the saucer) |
| `clip_glasses_round` | 122 x 36 x 90 | 1.8 | 7.3 | none: print front face down |
| `clip_sunglasses` | 122 x 32 x 90 | 3.8 | 15.1 | none: print front face down |

(The shell masses above are for the pair; sizes are per half. Rebuild them with
`.venv\Scripts\python.exe build_shells.py` or just some of them with `build_shells.py pear jolly`; names are
pear frog heart jolly claude beret glasses sunglasses.)

Jolly hem: raised to -26 mm below the collar plane (`JOLLY_HEM_Z` in `build_shells.py`, 17 Oct 2026; it was -58, then -40), so the shell is 126 mm tall instead of 158 mm (it was 158 x 144 x 72, 33.6 g and 134.4 g). At -58 the hem hit the column at rest beyond about 13 degrees of nod or 10 degrees of tilt; at -40 it still touched when full nod and full tilt were used together. -26 clears the full nod 30 plus tilt 25 corner at rest.

Head mass budget (spec: 250 g or the MG90D neck stalls). My estimate for what hangs above the neck, counting the two
head halves and head plate C near-solid (122 g) plus the shell, before magnets, screws and any fabric:

- Cloud 205 g, frog 208 g, heart 216 g, pear 225 g: inside the budget.
- Claude 231 g (122.3 g of head halves and plate C plus the 108.8 g shell pair): inside the budget by about 19 g, second heaviest, 2 g under the Jolly.
- Jolly 233 g (122.3 g of head halves and plate C plus the 110.5 g shell pair; it was 257 g before the hem was raised to -26): inside the budget by about 17 g, but still the heaviest of the six. Magnets, screws and fabric add more, and the rocker B and tilt servo also ride on the nod servo. Test it with real weights, print the head halves and Jolly with a thinner wall (`HEAD_WALL` in the base file, `SHELL_WALL` here), or fit the Jolly only with a stronger neck servo.

Notes on specific shells and clip-ons
- Heart: the point is cut flat at the collar plane, because a shell that hangs lower would hit the neck gimbal. It reads as a heart from the top cleft and the two lobes, not from a pointed bottom.
- Jolly: 126 mm tall hooded head-and-torso shell with a hood ridge and a swept cut-out on each shoulder flank for the mitten arms (cleared up to 80 degrees of arm swing). The hem is at -26 mm below the collar (raised from -58, then -40, on 17 Oct 2026), which is well above the shoulder sockets (those sit about 119 mm below the collar), so it hides the head and the top of the neck, not the shoulders or torso, and about 38 mm of the neck flange shows under the hem. The arm cut-outs are swept clearance slots, not tailored to the neck at every nod and tilt. Its wide hem swings down toward the top of the column when the head moves (measured by distance in CadQuery, no printing involved). Body at rest, hem at -26, worst case over nod plus or minus 30 and tilt plus or minus 25 including all four full corners: 4.2 mm gap (at the full corner). Single extremes at rest: full nod alone 14.6 mm, full tilt alone 15.8 mm. Earlier hems for comparison: at -58 it touched beyond about 13 degrees of nod or 10 degrees of tilt; at -40 nod alone and tilt alone cleared (5.5 and 2.1 mm) but the combined corner touched (0.0 mm); at -30 the corner gap was 1.9 mm. The cloud, pear, frog, heart and Claude shells stop at the collar plane, so they cannot reach the column.
- Claude: a puffy starburst after Claude's spark logo. The shell is the same head-swallowing sphere as the other round shells (R 63.3 mm about the head-sphere centre) plus seven soft rays in the front (X-Z) plane, all pointing out from that centre. Angles from vertical 0, plus and minus 38, plus and minus 75, plus and minus 108 degrees; the tip-sphere centres are 89, 84, 82 and 74 mm out (so the rays are uneven in length, like the logo). Each ray is a short, fat cone frustum capped with a full hemisphere, root radius 19 mm tapering to a tip radius of 14 mm, so they read as stubby plush fingers, not spikes; hollow with the same 1.5 mm wall (`CLAUDE_RAYS`, `CLAUDE_ROOT_R`, `CLAUDE_TIP_R` in `build_shells.py`). (First version: 13 to 8 mm rays reaching 95, 90, 88 and 80 mm, 99 g; it looked like a spiky sea mine, so the rays were thickened and the reaches pulled in by the tip-radius growth to keep the same overall size.) Everything below the mating plane is cut flat and the standard mating plate (3.2 mm, 96 mm hole, six magnet pockets, two M3 lugs) closes it, so it fits the same base as the others. Whole shell 186 mm wide, 132 mm deep, 127 mm above the collar plane (a little over the 120 mm aim; the height costs no clearance). Valid solid per half, 0.0 mm3 overlap with the head. Built by `shell_full_solid` / `shell_halves_solid`, a variant of the shell recipe that takes any outer and cavity solid, so the other shells' code was not touched. The fleece skin on top will soften it further. The radii were tried at 19 / 14 first and the mass fits (108.8 g, under the 120 g limit), so the 18 / 13, 17 / 12 and 16 / 11 fall-backs were not needed.
  Clearance (`check_shell_clearance.py`, exact CadQuery distance, shell moved with the head, arms not applicable on the round characters; the same method reproduces the Jolly's 4.2 mm corner gap above). Smallest gap to any base part, body at rest, nod / tilt in degrees: -30 / -25 12.0 mm; -30 / 0 15.4; -30 / +25 12.0; 0 / -25 10.6; 0 / 0 17.5; 0 / +25 10.6; +30 / -25 17.2; +30 / 0 17.5; +30 / +25 17.2. With the carriage fully up (bob 33.9 mm) the four corners give 12.0 mm (nod -30) and 17.2 mm (nod +30). Worst case 10.6 mm (collar plate to neck base A at tilt plus or minus 25), well over a 3 mm aim: the rays never come near the column or the turntable, because the shell ends at the collar plane. Shell to head plate C: 5.7 mm. These are CAD distances with no printing tolerance (CHECK on the printed parts).
  Printing: lies on its split face, each half 130 x 132 x 93 mm (fits a 180 mm bed). About 10.9 percent of the surface is steeper than 45 degrees, mostly the two 38 degree rays (about 50 degrees off vertical when printed) and the arch over the top ray, so use tree supports there (CHECK in the slicer; not test-printed).
- Glasses and sunglasses: they hold on with a springy temple hook, designed with about 0.5 to 1.1 mm of deliberate squeeze. This has not been tested on a printed head; if they are loose or crack, change the `G_*` and `SUN_*` numbers.
- Beret: a plain friction fit (0.15 mm clearance), so it may slide when the head nods. A small dab of Blu-Tack on the inside fixes that.

## Check before you print

1. Servo pocket fit. Calipers on your actual servos, then compare with the (CHECK) numbers in the PARAMETERS block: MG90D tab-top height 20.5 mm, ear hole spacing 27.8 mm, shaft offset 6.0 mm; MG996R tab-top height 28.0 mm, ear holes 49.5 x 10 mm, shaft offset 10.5 mm. Print the small `shoulder_socket_right` and `neck_base_A` first; they test the MG90D pocket. A MG996R pocket test is one half of the base plate (long print) or print only the turntable cradle.
2. Magnet pocket tolerance. Pockets are 5.4 mm wide and 2.2 mm deep for a 5 x 2 mm magnet, leaving 0.8 mm of plastic skin on the mating face. Print one skin ring first and press a magnet in: it should seat firmly without splitting the skin. If tight or loose, change `CLEAR` or `MAG_D`.
3. Head mass. See the budget above; the Jolly is the heaviest of the six (233 g against 250 g; Claude is 231 g). Weigh the printed head halves and shell before choosing the final neck servo.
4. Gimbal hinge gaps. 0.4 to 0.5 mm in the CAD is tight for FDM. If the hinges fuse or bind, raise `CLEAR` or sand the faces.
5. Bearing numbers. The model assumes 38 mm hole, 7 mm tall, three screws on a 58 mm circle. Measure yours and change `BEARING_ID`, `BEARING_H`, `BEARING_SCREW_R`.
6. Supports. The turntable plate needs supports under it; neck base A, head halves and all shell halves also do.
7. Jolly shell and the column. With the hem at -26 it clears the column at rest across the full nod (plus or minus 30) and tilt (plus or minus 25) range, worst case 4.2 mm at the combined corners (see the shell notes). That is a CAD distance with no printing tolerance, so check it on the printed parts with the head at full nod plus tilt.

## Known limits and what was skipped

- Nothing has been physically printed or bench-tested. The collision check covers the head sphere, neck gimbal, column and carriage (the grid above) and, for the Jolly and Claude shells, a separate set of checks (below, and `check_shell_clearance.py`). It does not model servo bodies, wires or fabric.
- The shell and cloud right-hand halves are built as a mirror of the left, because cutting a union of spheres straight down the middle upset the CAD kernel (it returned an invalid, near-empty solid). The mirror is exact; the lug holes are cut afterwards so left and right differ correctly (clearance holes on one, pilot holes on the other).
- Magnet pockets are placed at 0, 60, 120... degrees so none lands on the split plane.
- Nothing requested was skipped. Every part in the brief exists: base plate in two halves, turntable, torso column in two halves with the lift carriage, yoke and lever, three-part neck gimbal, head sphere in two halves with the 110 mm collar, four skin rings, two shoulder sockets with blanking caps and arm horns, the example cloud shell, the pear, frog, heart, Jolly and Claude shells, the beret, round glasses and sunglasses.

## Changing the design

Open `build_puppet_base.py` and edit the PARAMETERS block at the top (wall 2.4, clearance 0.2, magnet 5 x 2, sphere 120,
collar 110, the servo sizes, the bearing size, the bob lever). Then, from this folder in PowerShell:

    $env:PYTHONIOENCODING='utf-8'
    .\.venv\Scripts\python.exe build_puppet_base.py       # all base parts, parts_report.csv, collision check (several minutes)
    .\.venv\Scripts\python.exe render_preview.py          # the preview pictures
    .\.venv\Scripts\python.exe render_preview.py claude   # only out/preview_claude.png
    .\.venv\Scripts\python.exe build_shells.py            # all shells and clip-ons (or name some: pear frog heart jolly claude beret glasses sunglasses)
    .\.venv\Scripts\python.exe check_shell_clearance.py claude     # shell-to-base gaps over nod and tilt (add --bob for the carriage-up corners)
