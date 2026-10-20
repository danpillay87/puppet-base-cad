DESK ANIMATRONICS - PRINT PACK (20 Oct 2026)
===========================================

What this is
------------
Six small desk animatronics (one yeti with arms, five round characters) that all
sit on the same 3D-printed base. The base turns, bobs up and down, and the head
nods and tilts. A magnet ring at the neck lets the character shells click on and off.
What they look like (this picture shows the first five; the sixth, Claude, is the
coral starburst with seven soft rays, see docs/images/06-six-toys-concept.png in the repo):
https://d8j0ntlcm91z4.cloudfront.net/user_3ElkytIwAZasEJ6yWmCzklZkS3B/hf_20261017_140641_e573edb6-a83d-4693-99ff-e605dbf3bbe1.png

36 STL files. All are watertight and already in their print orientation, so load
them as they are. Everything fits a 180 mm bed. Nothing has been printed yet, so
the servo and bearing pockets are from datasheets: please print neck_base_A and
one shoulder_socket first and I will check the fit before the rest goes on.

Settings
--------
Layers 0.2 mm, 3 walls, 15-20% infill on the structural parts.
Character shells are hollow with a 1.5 mm wall: 3 walls, 0-5% infill.
PLA for everything except the three neck gimbal parts, which want PETG:
neck_base_A, neck_rocker_B, neck_head_plate_C.
A brim helps on the tall thin parts (column halves, head halves, shells).

GROUP 1 - BASE SET (print one set per toy; 23 files, 25 pieces, roughly 450-520 g
with supports, about 16-20 printer hours)
---------------------------------------------------------------------------------
File                      Qty  Size (mm)        Supports
base_plate_left           1    80 x 160 x 48    none
base_plate_right          1    80 x 160 x 48    none
turntable                 1    150 x 150 x 48   YES, small supports under the plate and cradle window
column_left               1    58 x 116 x 100   none
column_right              1    58 x 116 x 100   none
bob_carriage              1    112 x 77 x 63    none
lift_yoke                 1    22 x 7 x 39      none
lift_lever                1    41 x 20 x 5      none
neck_base_A      (PETG)   1    62 x 62 x 54     YES, small supports under the flange rim
neck_rocker_B    (PETG)   1    51 x 44 x 36     none
neck_head_plate_C (PETG)  1    88 x 88 x 36     none
head_half_left            1    84 x 122 x 61    YES, crown of the dome and the collar flange
head_half_right           1    84 x 122 x 61    YES, crown of the dome and the collar flange
shoulder_socket_left      1    20 x 36 x 23     none
shoulder_socket_right     1    20 x 36 x 23     none
shoulder_cap              2    20 x 36 x 10     none  (blanks the shoulder on the five round characters)
arm_horn                  2    34 x 20 x 9      none  (only needed for the yeti)
skin_ring_1 to _4         1 each  110 x 110 x 3  none  (four flat rings, one per spare shell)
cloud_former_left/right   1 each 103 x 131 x 67 YES, puffs and crown, tree supports
                                                (the cloud character's shell, listed here because it
                                                 was drawn with the base; print it once, not per toy)

GROUP 2 - CHARACTER SHELLS (one pair per character, each pair 85-110 g)
----------------------------------------------------------------------
Each shell is two halves that lie on their split face. Tree supports.
shell_frog_left / right     100 x 132 x 71   supports on eye domes and cheeks
shell_heart_left / right    107 x 132 x 67   supports on both lobes
shell_pear_left / right     127 x 146 x 70   supports on the crown and the stalk
shell_jolly_left / right    126 x 144 x 72   supports on the hood peak, flank slots and hem rim
shell_claude_left / right   130 x 132 x 93   supports on the two 38-degree rays, the arch over the top ray
                                             and the dome crown (pair about 109 g; the 75 and 108 degree
                                             rays stand up nearly vertical when printed)
(cloud shell = cloud_former_left / right in Group 1)

GROUP 3 - CLIP-ONS (one each, small)
------------------------------------
clip_beret            119 x 115 x 51   YES, under the saucer (or crown-down on the stalk with tree supports)
clip_glasses_round    122 x 36 x 90    none, front face down
clip_sunglasses       122 x 32 x 90    none, front face down

Totals
------
One toy = one base set + one shell pair, roughly 550-630 g.
All six = six base sets + six shells + clip-ons, roughly 3.5-4 kg and 95-120 printer hours
(the four skin rings, the arm horns and the clip-ons are printed once, not per toy;
10 shoulder caps in all, 2 for each of the five round characters).
Suggested first print to prove it moves: one base set + the frog shell.

Dan Pillay
