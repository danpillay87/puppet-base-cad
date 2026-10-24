DESK ANIMATRONICS - PRINT PACK (20 Oct 2026, updated 24 Oct 2026)
==================================================================

PRINT THE SKELETON FIRST
------------------------
24 Oct fix: base_plate.stl is new. The turntable servo's slot has moved about 10 mm
so its shaft sits on the turning axis. Do not use the 23 Oct base_plate.stl.

Print at 100% scale: no shrink compensation (in Bambu Studio, leave the filament's
Shrinkage (XY) at 100%). All 14 files below print without supports.

File                        Qty
base_plate.stl              1
turntable.stl               1
turntable_hub.stl           1
column_left.stl             1
column_right.stl            1
bob_carriage.stl            1
lift_yoke.stl               1
lift_lever.stl              1
neck_base_A.stl             1   (PETG if you have it, PLA is fine)
neck_rocker_B.stl           1   (PETG if you have it, PLA is fine)
neck_head_plate_C.stl       1   (PETG if you have it, PLA is fine)
shoulder_socket_left.stl    1
shoulder_socket_right.stl   1
arm_horn.stl                2
Total: 15 pieces, about 658 g, roughly 17-26 hours on the H2D (about 2 plates).

Later: head_half_left and head_half_right (these need supports), then the skins
and the five dummy cores (groups 2 and 3 below). Do not print anything in
out/superseded/: those are the old two-piece base halves.

What this is
------------
Six small desk animatronics (one yeti with arms, five round characters) that all
swap onto ONE shared 3D-printed base, built to the yeti's spec with the full set of
servos (2 x MG996R and 4 x MG90S). The base turns, bobs up and down, and the head
nods and tilts. A magnet ring at the neck lets the character shells click on and off.
Both shoulder servos stay fitted; the yeti's two arm horns are part of the base set
and come off when an armless skin goes on. The five skins that are not on the base
sit on a printed dummy core on the shelf.
What they look like (this picture shows the first five; the sixth, Claude, is Clawd, the
Claude Code mascot: a boxy terracotta body with two stub arms (no legs and no fabric in the first build),
see docs/images/06-six-toys-concept.png in the repo):
https://d8j0ntlcm91z4.cloudfront.net/user_3ElkytIwAZasEJ6yWmCzklZkS3B/hf_20261017_140641_e573edb6-a83d-4693-99ff-e605dbf3bbe1.png

37 STL files in out/. All are watertight and already in their print orientation, so
load them as they are. shoulder_cap is not printed. The old base halves
(base_plate_left and base_plate_right) have moved to out/superseded/ and are NOT
printed. Every part fits the H2D bed (and a 220 x 220 mm bed too). The servo slots
in neck_base_A and the shoulder sockets are exactly the same size as in Andy's
first test prints, so a servo fit check on those prints holds for these files.
The bearing seat (in base_plate and turntable) is new: it is now 72 mm, to match
the bearing in the basket.
The design uses the 72 mm lazy-susan bearing (Amazon B0FBLK3JLH) and MG90S servos
(same body and tabs as the MG90D, a bit less torque).

Settings
--------
Andy's printer settings (they live in print_settings.py, so they are easy to change):
Bambu Lab H2D, bed 325 x 320 x 325 mm (single-nozzle build area), 0.4 mm nozzle,
0.2 mm layers, 3 walls, 5 top and bottom layers, 25% infill, Bambu PLA Basic at
1.24 g/cm3, GBP 20/kg (full price), shrink 0%.
Print at 100% scale. The parts are drawn true size with the fit clearances built in.
Andy quoted 4% shrink; PLA usually shrinks well under 1%, and a 4% scale-up would
leave the servo seats about 1-2 mm loose and the bearing seat about 3 mm loose.
Dan is test-fitting real servos in Andy's first prints to settle it.
Character shells are hollow with a 1.5 mm wall: 3 walls, 0-5% infill.
PLA for everything except the three neck gimbal parts, which want PETG:
neck_base_A, neck_rocker_B, neck_head_plate_C (the cost figures below assume PLA).
A brim helps on the tall thin parts (column halves, head halves, shells).
Supports: only the head halves, the shells, the cloud formers and the clip-ons
(beret, glasses, sunglasses) need them. Everything else prints without supports;
the only bridges left are short ones (12 mm jack hole, 6 mm channels, magnet
pocket roofs).
Base hollowing: at 25% infill 5 of the 10 open-top pockets in the base plate pay and
are cut (the two big wells plus the voids under the ESP32, the PCA9685 and the buck
converter, about 38 g saved in total); the other 5 stay solid. At the old 15% infill
only 2 paid (about 3 g). The report is out/base_pockets.csv.
After changing a setting, run .venv\Scripts\python.exe print_cost.py; it writes
out/print_cost.txt.

GROUP 1 - BASE SET (print ONE set, shared by all six toys; 16 files, 17 pieces,
about 757 g, GBP 15.14, roughly 19-30 printer hours at 25-40 g/h as a guide)
---------------------------------------------------------------------------------
File                      Qty  Size (mm)        Supports
base_plate                1    160 x 160 x 48   none  (one piece; replaces base_plate_left/right)
turntable                 1    150 x 150 x 43   none  (plate down, cradle up)
turntable_hub             1    34 x 34 x 5      none  (3.4 g; fixed with 4 x M2 x 8 screws up through
                                                       the yaw servo horn and the hub into the plate)
column_left               1    58 x 116 x 100   none
column_right              1    58 x 116 x 100   none
bob_carriage              1    112 x 77 x 63    none
lift_yoke                 1    22 x 7 x 39      none
lift_lever                1    41 x 20 x 5      none
neck_base_A      (PETG)   1    62 x 62 x 58     none  (45 degree sleeve and skirt; cross screws M3 x 10
                                                       in counterbores)
neck_rocker_B    (PETG)   1    51 x 44 x 36     none
neck_head_plate_C (PETG)  1    88 x 88 x 36     none
head_half_left            1    84 x 122 x 61    YES, crown of the dome and the collar flange
head_half_right           1    84 x 122 x 61    YES, crown of the dome and the collar flange
shoulder_socket_left      1    20 x 36 x 23     none
shoulder_socket_right     1    20 x 36 x 23     none
arm_horn                  2    34 x 20 x 9      none  (part of the base set; take them off when an
                                                       armless skin goes on)

Not printed: base_plate_left, base_plate_right (superseded by base_plate) and
shoulder_cap (both shoulder servos stay fitted, so no caps; the part is still in the
code at 0 copies).
Optional spare skin rings: skin_ring_1 to _4, 1 each, 110 x 110 x 3, none, 8.5 g each,
not in the totals.
(The cloud character's shell, cloud_former_left/right, is the Cloud skin and is listed
in Group 2.)

GROUP 2 - CHARACTER SHELLS (one skin per character, each skin 98-133 g with its clip-ons)
-----------------------------------------------------------------------------------------
Each shell is two halves that lie on their split face. Tree supports.
No fabric in the first build: print each shell in its colour, or paint it.
Skin totals: Jolly 127.0 g, Clawd 124.9 g, Cloud 133.2 g (formers + beret),
Pear 122.4 g (with round glasses), Frog 98.0 g, Heart 114.7 g (with sunglasses).
Six skins: 720 g, GBP 14.40, roughly 18-29 printer hours.
shell_frog_left / right     100 x 132 x 71   supports on eye domes and cheeks
shell_heart_left / right    107 x 132 x 67   supports on both lobes
shell_pear_left / right     127 x 146 x 70   supports on the crown and the stalk
shell_jolly_left / right    126 x 144 x 72   supports on the hood peak, flank slots and hem rim
shell_claude_left / right   110 x 130 x 98   supports on the flat roof (inside of the outer side wall)
                                             and the arm ends (pair about 125 g with the supports
                                             allowance; thin 1.0 mm wall, use a brim; Clawd's four
                                             legs are not printed; left off for now)
cloud_former_left / right   103 x 131 x 67   YES, puffs and crown, tree supports (the Cloud skin)

GROUP 3 - CLIP-ONS (one each, small)
------------------------------------
clip_beret            119 x 115 x 51   YES, under the saucer (or crown-down on the stalk with tree supports)
clip_glasses_round    109 x 82 x 26    YES, light tree supports under the lower rims and temple bands
                                       (print it the way Pear wears it)
clip_sunglasses       138 x 88 x 21    YES, light tree supports under the lens plates and temple bands
                                       (print it the way Heart wears it)

GROUP 4 - DUMMY CORES (print 5)
-------------------------------
dummy_core            5    110 x 110 x 58   none  (34 g each, about GBP 0.68 each, collar down)
A cheap light printed former so the five skins that are not on the base hold their
shape on the shelf. Checked: zero overlap with all six skins. It has 6 magnet pockets
like the head; magnets in the cores are optional.

Totals (model estimate from out/print_cost.txt; the slicer on the real printer wins)
------------------------------------------------------------------------------------
One base + six skins + five dummy cores = about 1,647 g (1.65 kg), GBP 32.94 of
filament at GBP 20/kg, and about 42-67 printer hours on the H2D (25-40 g/h, about
7 plates at 6 minutes set-up each; a guide only).
  Base set 757 g (GBP 15.14, about 19-30 h), six skins 720 g (GBP 14.40, about
  18-29 h), five dummy cores 170 g (GBP 3.40, about 4-7 h; 34 g, GBP 0.68 each).
Option 1 (one test toy: the shared base set + the Frog skin): 18 pieces, about 855 g,
GBP 17.10, about 22-34 h. Option 2 (the full run above): 41 pieces.
Before the shared base, at the old 15% infill (so not comparable with the figures
above): base set 721 g, one shared base + six skins 1,481 g, six full toys each with
its own base 5,100 g.
The spare skin rings, the arm horns and the clip-ons are printed once; no shoulder
caps are printed.
Suggested first print to prove it moves: the base set + the frog shell (98.0 g),
which is Option 1 above.

Dan Pillay
