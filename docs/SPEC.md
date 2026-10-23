# Six controllable toys: build spec

17 Oct 2026, Dan. Rev 15, exported 18 Oct 2026 as a backup of the working spec. Rev 16, 20 Oct: Claude added as a sixth toy, with a six-toy parts and materials costing. Rev 17, 20 Oct evening: Claude redrawn as Clawd, the Claude Code mascot. Rev 18, 23 Oct: one shared base for all six toys, costed and printed as one base plus six skins plus five dummy cores. Rev 19, 23 Oct: Andy prints the parts on a Bambu Lab H2D, so the print figures are redone at 25% infill and £20/kg, and the voice and software sections are rewritten for the one base. Images are in docs/images.

Six Wi-Fi animatronic toys as skins on one shared servo base: Jolly (Meta's plush yeti, a body with arms), four OpenAI dots (fuzzy blobs, built as motorised bobblehead bodies with no arms) and Claude (Clawd). The base is built to Jolly's spec with the full set of servos, so every skin swaps onto it. Everything is printed, base and character shells alike, with fur or fleece glued over for the fuzzy look. The base carries the ESP32; one MCP server we write drives it, so an AI agent can turn, nod, bounce or wave whichever skin is on. Budget: about £192 for the one base and all six skins (shopping list below, 20 Oct prices, nothing bought). This page is for Andy, who prints the parts: what the toys are, what moves, and what we would like printed.

![The five toys as they should read on the desk: Jolly plus the four dots. Concept render, 17 Oct.](images/01-five-toys-concept.png)

*The five toys as they should read on the desk: Jolly plus the four dots. Concept render, 17 Oct.*

## The six units

All six share one printed base, built to Jolly's spec with all six servos. Jolly's two arm horns are part of the base set and go on only for Jolly; the dots and Claude are bobblehead bodies with the horns off, so the head does the acting. The five skins not on the base sit on a printed dummy core on the shelf.

| # | Toy | Look | Body | Arms | How it expresses itself |
| --- | --- | --- | --- | --- | --- |
| 1 | Jolly | Cream long-pile yeti, hooded head and torso, mitten hands, flat oval face, dot eyes, smile line, no mouth opening | Full base: turn, bob, nod, tilt | Yes, one servo per shoulder | Waves, body bob, nod, head tilt |
| 2 | Dot: cloud | Blue fuzzy cloud with a beret | Bobblehead body | No | Eyes, bounce and squash, lean |
| 3 | Dot: pear | Yellow pear or rounded triangle with glasses | Bobblehead body | No | Eyes, bounce and squash, lean |
| 4 | Dot: frog | Green rounded frog blob | Bobblehead body | No | Eyes, bounce and squash, lean |
| 5 | Dot: heart | Pink heart with sunglasses | Bobblehead body | No | Eyes, bounce and squash, lean |
| 6 | Claude (added 20 Oct) | Clawd, the Claude Code mascot, as a terracotta fleece plush: boxy body, two stub arms out to the sides, four stubby legs, dot eyes, no mouth | Bobblehead body | No (stub arms are fixed) | Eyes, bounce and squash, lean |

Target size: 30 to 35 cm tall for Jolly, about 25 cm tall and wide for each dot. Neither character has a mouth, so there is no jaw mechanism. Jolly and the dots are Meta and OpenAI characters, and Claude is Anthropic's, so these are for personal and demo use only.

## Sixth toy: Claude (added 20 Oct)

Claude joins as a sixth toy, built like the four dots: the same shared base, arm horns off (both shoulder servos stay fitted), no moving arms. Only the shell and the fleece are new.

![Claude as Clawd, concept render, 20 Oct](images/05-claude-character-concept.png)

*Claude as Clawd, concept render, 20 Oct*

The character is Clawd, the Claude Code mascot, made plush (changed on the evening of 20 Oct from an earlier starburst design based on Claude's spark logo). It has a chunky rounded box body, two short stub arms sticking straight out at the sides, and four stubby legs underneath. It has two black bead eyes, no mouth and no accessory, because the outline is the identity. The arms are fixed, part of the printed shell. The skin is short terracotta anti-pill fleece (about #C96A4A) glued over the shell, not long-pile fur, so the boxy edges stay crisp.

![All six on the desk, concept render, 20 Oct](images/06-six-toys-concept.png)

*All six on the desk, concept render, 20 Oct*

In software it is the sixth character: the same moves as a dot, with its own voice and personality profile.

![CAD preview: Clawd's shell on the base, at rest, then bobbed up 34 mm with 20 degrees of nod and tilt; the see-through legs are soft fleece](images/07-claude-cad-preview.png)

*CAD preview: Clawd's shell on the base, at rest, then bobbed up 34 mm with 20 degrees of nod and tilt; the see-through legs are soft fleece*

**CAD (20 Oct, redrawn as Clawd):** the Claude shell is exported as two STL halves, `shell_claude_left` and `shell_claude_right` (39 STLs in the set now, counting the two superseded `base_plate_left` and `base_plate_right` files). It is a rounded box over the head with a hollow stub arm on each side. The four legs are soft sewn fleece on the skin, not printed.

- Size: 196 mm wide across the arms, 130 mm deep and 110 mm tall. The body is 126 × 130 × 110 mm with rounded edges. Each arm sticks out 35 mm and is 37 mm tall. The four legs are 22 × 30 mm and hang 28 mm below. Each half prints at 110 × 130 × 98 mm, so it fits the A1 mini.
- Wall: 1.0 mm, not the usual 1.5 mm. A box round the 120 mm head has much more surface than a sphere, so 1.5 mm walls take the head to about 277 g, over the 250 g budget. At 1.0 mm the pair is about 109 g near-solid, 27 g at normal shell settings, and the head is about 231 g, just under Jolly's 233 g. Use a brim and expect the first print to be fragile.
- Why soft legs: printed legs ended within 0 to 7 mm of the neck at full nod and tilt, and they would add about 18 g.
- Fit: the shell clears the base by at least 10.6 mm at full nod and full tilt, bobbed up or down. Re-run on 23 Oct against the new base and unchanged (10.56 mm to neck base A).
- Leg check: the soft legs can still brush the neck gimbal. The outer pair is 5 mm clear at rest and touches at full nod and tilt. The inner pair sits over the neck at full length. Stuff them lightly, or make the inner two short flat pads, and test with real fleece.
- Printing: tree supports, about 15% of the surface overhangs (Jolly 15.8%). The roof, the arm ends and the rounded edges need them.

Not test-printed yet; the clearances are CAD distances with no allowance for print tolerance.

## What moves

The one shared base carries six servos: 2 × MG996R (turn and bounce) and 4 × MG90S (nod, tilt and the two shoulders). Every skin gets turn, bounce, nod and tilt; both shoulder servos stay fitted, and the arms (printed horns and wire) go on only for Jolly. Nothing else moves; eyes are printed, embroidered or LED matrices behind the fabric.

| Motion | Mechanism | Servo | Range | On which toys |
| --- | --- | --- | --- | --- |
| Turn (yaw) | Printed turntable on a 72 mm lazy-susan bearing, servo at the base; the turntable hub is a separate printed disc fixed with 4 M2 screws up through the servo horn | MG996R | ±90° | All six |
| Bounce / squash | Torso column on two printed rails, lifted by a servo lever with a return spring | MG996R | 30 to 40 mm lift | All six |
| Nod | Two-axis printed neck gimbal, first axis | MG90S | ±30° | All six |
| Tilt | Same gimbal, second axis | MG90S | ±25° | All six |
| Arm swing (left, right) | Shoulder socket on the torso, printed horn, 2 mm aluminium armature wire sheathed in foam | 2 × MG90S | ±80° | Servos always fitted; arms (horns and wire) on for Jolly only |

The MG90S has the same body and tabs as the MG90D the CAD was first drawn for, but a bit less torque (about 1.8 against 2.2 kg.cm), so check the nod and tilt once a head is on.

![Exploded view of one unit, bottom to top: base plate with the board, speaker, mic and power jack; bearing and turntable over the yaw servo; lift column with servo, lever and spring; two-axis neck gimbal; head sphere in two halves with the magnet collar; character shell lifting off. Concept render, not CAD.](images/02-exploded-view-concept.png)

*Exploded view of one unit, bottom to top: base plate with the board, speaker, mic and power jack; bearing and turntable over the yaw servo; lift column with servo, lever and spring; two-axis neck gimbal; head sphere in two halves with the magnet collar; character shell lifting off. Concept render, not CAD.*

![CAD preview: the base bobbed up 34 mm, head nodded and tilted 20 degrees, arms raised](images/03-cad-preview-pose.png)

*CAD preview: the base bobbed up 34 mm, head nodded and tilted 20 degrees, arms raised*

**CAD status (17 Oct, evening; updated 23 Oct):** the whole base is drawn in CadQuery and exported as 39 print-ready STL files: a one-piece base plate (160 × 160 × 48 mm; the old `base_plate_left` and `base_plate_right` files are superseded and not printed), turntable with the 72 mm bearing seat and a separate 34 × 34 × 5 mm turntable hub (`turntable_hub`, 3.4 g, so the turntable prints without supports), torso column with the bob carriage and lift lever, three-part neck gimbal (neck base A redesigned to print without supports, with a 45 degree sleeve and skirt and M3 × 10 cross screws in counterbores), head sphere halves with the 110 mm collar and six magnet pockets, four optional skin rings, shoulder sockets and arm horns (the shoulder caps are no longer printed; `shoulder_cap` stays in the code at 0 copies), a dummy core, plus the six character shells (cloud, pear, frog, heart, Jolly, Claude) and the beret, round glasses and sunglasses clip-ons. Height 311 mm, bob throw 34 mm. One shared base set is about 755 g of filament (model estimate, 25% infill), each skin 98 to 133 g. All the hidden parts print without supports; only the head halves, the shells, the Cloud formers and the clip-ons need them. One thing to check before any real print: servo and bearing pocket sizes are from datasheets, not measured, so print one shoulder socket and the neck base first. **Jolly hood fixed (21:10):** the hood's open lower edge was raised from 58 mm below the head centre to 26 mm, so it is now a 126 mm hood over the head and top of the neck rather than a full-depth shell. It clears the torso column by at least 4.2 mm at rest even with full nod and full tilt together (14 to 16 mm with one axis alone), and the Jolly head drops to about 233 g, inside the 250 g neck-servo budget. About 38 mm of neck flange shows below the hood; the fur covers it. The character shells are placeholders in shape: a better route is to generate them from the render with an image-to-3D tool (Hi3D or similar), then hollow them to a 1.5 mm wall and cut the collar ring in. The base stays hand-drawn CAD.

![The six printed character shells (Claude added 20 Oct) and three clip-ons from the CAD, Jolly hood at its final height](images/04-shells-and-clip-ons.png)

*The six printed character shells (Claude added 20 Oct) and three clip-ons from the CAD, Jolly hood at its final height*

Head mass budget is 250 g including the skin, or the small gimbal servos stall. The head former is a hollow Ø120 mm printed sphere in two halves. Every skin attaches at a Ø110 mm collar carrying six 5 mm magnets at 60° spacing, the same arrangement Reachy Mini uses, so skins swap in seconds.

## Skins: all printed, fur or fleece over the top

Every character is a hollow printed shell that clips over the head sphere and torso and carries the magnet collar, so skins still swap in seconds. The fuzzy look comes from fabric glued over the shell: long-pile faux fur for Jolly, fleece or flock for the dots. Custom plush is parked; the base would take one later without changes.

| Toy | Shell | Finish | Filament |
| --- | --- | --- | --- |
| Jolly | Hooded head-and-torso shell in two halves, mitten hands printed on the arm wires, stubby feet on the base plate | Cream faux fur glued over; felt oval face patch; dot eyes and smile line in felt or stitching | 127.0 g |
| Cloud | Cloud silhouette over the head sphere, beret printed on | Blue fleece wrap or flock | 133.2 g (formers plus beret) |
| Pear | Pear or rounded-triangle shell, glasses printed as a clip-on | Yellow fleece or flock | 122.4 g (with the round glasses) |
| Frog | Rounded frog shell with eye bumps | Green fleece or flock | 98.0 g |
| Heart | Heart shell, sunglasses printed as a clip-on | Pink fleece or flock | 114.7 g (with the sunglasses) |
| Claude (Clawd) | Rounded box shell in two halves with two hollow stub arms, 1.0 mm wall; four soft sewn fleece legs | Short terracotta anti-pill fleece, black bead eyes | 124.9 g |

The six skins come to 720 g, about £14.40 at £20/kg (model estimate from `out/print_cost.txt`, supports allowance included; the slicer on the real printer wins).

Shell rules: 1.5 mm walls, 0 to 5% infill. The shells and clip-ons need supports; the hidden base parts do not. A hollow 1.5 mm wall prints almost all as perimeters, so a finished skin comes out at about 98 to 133 g before fabric. The head budget above still applies: Jolly is the heaviest at about 233 g against 250 g. Eyes are printed white discs with black pupils glued on; the same pockets take LED matrices later.

## Electronics on the one base: the lean build

The one shared base is self-contained: one ESP32 on Wi-Fi, servos driven straight from its pins, one 5 V supply. No servo board, no speaker or mic, no LED eyes in the first build; all three bolt on later. The base plate is already shaped for the servo board, the speaker and the mic, so the full build is still one of each, never one per skin. Prices are in the shopping list below (20 Oct 2026 UK prices, nothing bought).

| Part | On the one base | Notes |
| --- | --- | --- |
| ESP32 WROOM devkit | 1 (plus 1 spare) | Runs the motion library and a small web API |
| MG996R | 2 | Turn and bounce, the heavy axes |
| MG90S | 4 | Nod, tilt and the two shoulders |
| 5 V 4 A supply with barrel socket | 1 | Never power servos from USB; common ground |
| 72 mm lazy-susan bearing | 1 | The one in the basket (Amazon B0FBLK3JLH); or a printed bearing |
| 5 × 2 mm magnets | 42 | Head 6 + 6 per skin × 6; 72 if every dummy core gets magnets, 96 with the four spare rings |
| Springs, M2 and M3 screws, 2 mm armature wire, leads | 1 set | The screw kit covers the 4 M2 × 8 hub screws and the 2 M3 × 10 neck screws |
| Filament, 2 kg | 1.65 kg of parts, leaving about 0.35 kg for failed prints | Base, six skins and five dummy cores; we supply the spools |
| Faux fur, fleece or flock, glue | 1 set | Covers all six skins |
| Total |  | about £192.31 (shopping list below), spares not included beyond those listed |

### MVP costing (added 17 Oct, revised 23 Oct for one base)

The earlier five-toy figures (£243 for five, £245 in two steps) are superseded. With one shared base there is nothing to multiply: the whole spend is the one-base shopping list below, about £192.31, which includes the filament for all six skins and five dummy cores and the fur and fleece for all six skins. If you want to spend it in two steps, buy the base electronics, servos, bearing and filament first and prove the base with one skin on it; the fur and fleece can wait. Andy printing is assumed throughout (the filament line above is for the parts Andy prints); if that falls through, the printer in the backup plan below is the one line that would add to the total.

Voice, first build: the spare Home Assistant Voice puck, £0.

Later add-ons for the base: PCA9685 servo board £14, I2S amp and 40 mm speaker £10, mic £5, two 8×8 RGB eye matrices £16. Servo-care rules still apply: per-servo min and max in software, a mechanical stop on the bounce lift.

### Shopping list for the one shared base, priced 20 Oct

Same UK prices as the 20 Oct 2026 six-toy basket. The pack sizes below are derived from that old basket and were not re-checked at checkout. Nothing has been bought. The counts include a few spares: one extra ESP32, two extra MG996R, two extra MG90S. For buying, this replaces the six-toy basket. Links: A = amazon.co.uk/dp/, E = ebay.co.uk/itm/.

| Part | Buy | Cost | Where |
| --- | --- | --- | --- |
| ESP32 WROOM-32 devkit, USB-C | 2 (1 + 1 spare) | £10.58 | E386194572609 |
| MG996R servo (turn, bounce) | one 4-pack (2 needed) | £13.99 | E800790539208 |
| MG90S metal-gear servo (nod, tilt, the two shoulders) | one 6-pack (4 needed) | £17.99 | A B0DGD55Q71 or A B0C1N8VZ1S (the old basket bought a 10-pack and a 6-pack from these two; which link is the 6-pack was not recorded) |
| 5 V 4 A supply, 5.5 × 2.1 mm plug | 1 | £10.69 | E156521193797 |
| Barrel sockets with screw terminals | 10-pack | £3.98 | A B07GJ43VKS |
| Turntable bearing, 72 mm | 1 needed | £12.58 (upper bound) | A B0FBLK3JLH |
| 5 × 2 mm magnets | 100-pack (42 needed) | £4.99 | A B0DQTVNWG2 |
| M2 to M5 screw and nut kit, spring assortment (covers the 4 M2 × 8 hub screws and the 2 M3 × 10 neck screws) | 1 each | £10.79 | A B0GKGWVQNF, A B07WFPPXXX |
| Jumper wires, servo extension leads | 1 kit, 1 pack | £12.98 | A B0BZ7PYYLB, A B08727XZBQ |
| PLA filament, 2 kg at £18/kg (1.65 kg of parts, leaving about 0.35 kg for failed prints) | 2 kg | £36.00 | A B0GTLQ31W1 (the 20 Oct listing was £31.44 for 4.4 kg; this line keeps the old £18/kg price, not re-checked, while the print cost figures now use £20/kg) |
| Long-pile faux fur, five colours at 50 × 180 cm (£8.99 each); terracotta anti-pill fleece for Clawd, 1 m × 150 cm; glue gun (unchanged, covers all six skins) | 5 + 1 + 1 | £57.74 | A B0FB9CNYR7, A B0CVLJB56L, A B0DDKG29ND |
| **Total** |  | **about £192.31** | one base, six skins |

The bearing line is the old basket's price for its 8-bearing pack (£12.58). The smallest pack size was not checked, so treat £12.58 as an upper bound.

Before: the six-toy basket, with a full rig for each toy, was £342.60 (about £57 a toy).

Not in the total: print labour, PETG for the gimbal and lift arm, a speaker and mic, steel washers for ballast, rubber feet, 2 mm armature wire and the 5 V buck converter. No dowel pins are needed now that the base plate is one piece.

Optional: one PCA9685 servo board (A B0D7RQ5JXY). The 17 Oct estimate was £14 a board; the old six-toy basket listed £25.62 for its set, and that listing's pack size is not recorded here, so £25.62 is the upper bound. That makes about £206 to £218 in all. The lean build drives the servos straight from the ESP32, so the board is only for tidier wiring.

Checks before ordering:

- Fur: Clawd takes short terracotta fleece, not the long-pile fur. The listing is called "Terracotta" but shows no true swatch, so check it against #C96A4A (Neotrims "Rust Brick", A B07HWYN213, £8.25, is the fallback). The other five long-pile colours exist: cream, sky blue, yellow, light green and pink. The fur arrives last, on 29 Oct.
- Magnets: the 100-pack does not state its grade. Confirmed N35 costs £19.98 for 2 × 50 (A B00TACMMP0). The 100-pack covers the 42 magnets needed, and also the 72 or 96 if the dummy cores and spare rings get magnets.
- Supply: one 5 V 4 A supply for the one base. The old warning against sharing one supply across six toys no longer applies, because there is only one base.
- Genuine TowerPro MG996R are £9 each at The Pi Hut, so £18 for the two needed. The cheap servos and ESP32s are unbranded clones, which is normal for this kind of build.
- Filament: 2 kg covers the 1.65 kg of parts (base 755 g, six skins 720 g, five dummy cores 170 g), leaving about 0.35 kg for failed prints. The print cost figures use £20/kg.
- Servo torque: the MG90S has a bit less torque than the MG90D the CAD was first drawn for (about 1.8 against 2.2 kg.cm). Check the nod and tilt once a head is on.

## Voice and speech (added 17 Oct, rewritten 23 Oct for the one base)

The base needs to listen and talk, not just move. It is one base with one set of electronics: one ESP32, one speaker and one PCA9685 servo board driving all six servos (2 × MG996R and 4 × MG90S); the lean first build leaves the speaker and servo board off (see the electronics section). Whichever of the six skins is on the base, it is the same speaker, so there is one voice path to build, not six. What changes with the skin is the voice and personality the software uses. Three ways to do the listening and talking; we are going with the hybrid.

| Route | What it is | Cost for the one base | Verdict |
| --- | --- | --- | --- |
| A. Shared voice puck | One Home Assistant Voice Preview Edition (we have a spare) sits on the desk and does the wake word, hearing and speaking. Home Assistant's OpenAI integration answers (a text pipeline: speech to text, model, text to speech) and fires the base's moves over the network. The voice comes from the puck; the base moves. The pipeline is told which character is on the base, so it answers in that character's persona and voice. | £0 | Day-one route. No extra parts. |
| B. Voice on the base | A small I2S mic (INMP441) plus amp and 40 mm speaker (MAX98357A) on the one base. The ESP32 streams audio to a small Python bridge that talks to OpenAI's live speech models (gpt-realtime-2.1, about $32 per million audio tokens in and $64 out; or gpt-live-1 at $0.05 a minute) and streams the reply back. The speak-bob follows the audio, so whichever skin is on the base talks from the one speaker, in that character's voice. | about £7 at multipack prices (mic £2.50, amp £2.50, 40 mm speaker £1.50); the later add-ons line in the costing section prices the same parts at £15 from single listings. A later upgrade, not needed for the first build. | v2 upgrade, the fun version. |
| C. Hybrid (chosen) | Start with A. Print the base with the speaker pocket, grille and mic port already in it, so B becomes a parts drop-in rather than a re-print. | £0 now, about £7 to £15 later | What we are doing. |

Two board facts shape this. On-device wake word (ESPHome microWakeWord) wants an ESP32-S3 with PSRAM, while Bottango only documents the classic ESP32-WROOM. So v1 keeps motion on one classic ESP32 on the base and lets the puck or the bridge PC do the listening; nothing on the base has to hear a wake word. If we ever want the base to hear on its own, it gets an ESP32-S3 and we drop Bottango for it.

What this means for the printed base plate: a Ø40 mm speaker pocket with a grille under it, a 3 mm mic port on the rim, and the barrel jack as drawn. Empty in v1, filled in v2.

## Software: one base on Wi-Fi, one MCP server, six characters

We write the software ourselves. It follows the pattern already running on Dan's Walkie robot: the base exposes a small HTTP API over Wi-Fi, and one Python MCP server on the home network wraps it so any AI agent (Claude, or whatever is driving the demo) can call it as tools.

There is one base, so there is one of each board: one ESP32 on Wi-Fi, one speaker, one PCA9685 servo board and the six servos it drives (2 × MG996R and 4 × MG90S); the lean first build leaves the servo board and speaker off (see the electronics section above). The six characters are not six devices. They are six skins that swap onto the one base, and the software on that base switches between the six characters' voices and personalities when a different skin goes on.

1. On the ESP32: Bottango exports the motion library (idle breathe, listen, think, speak-bob, celebrate, wave, nod-yes, tilt-curious) to run standalone. A thin REST layer adds `/pose`, `/play/<clip>`, `/say` and `/status`. The motion library is the same for every character; a character only changes how it is used.
2. On the network: one MCP server with tools such as `toy.list` (the six characters and which one is active), `toy.set_mood(mood)`, `toy.react(clip)` and `toy.say(text)`, each acting as the active character, plus a way to say which character is active. Speech drives the bounce and arm gestures from the audio loudness.
3. One profile per character (JSON), six in all: which modules are fitted (the shoulder servos are used only for Jolly, whose arm horns and wire are on; the other five leave them still), servo limits, eye style, idle style, voice and personality (the persona the model is given). Putting a different skin on means the base's software loads that character's profile; the agent code never changes.

The active character is chosen in software: the agent, or whoever is driving the base, names the character and the base loads that profile (how the base knows which skin is on is still to be decided).

Voice: see the Voice and speech section above. First build: the spare voice puck on the desk does the listening and talking, and the base's bounce and arm gestures follow the audio loudness. Later: a mic and speaker on the base, streaming to OpenAI's live speech models. The one base answers to one server, so one agent can run a conversation as whichever character is on the base; a new skin means a new voice and personality, not a new device. The software proof of concept in `sim/` (see `sim/README.md`) already gives Jolly, Clawd and Cloud their own brain, voice and persona, and shows the toys as separate figures on a desk; on the real build only one skin is on the base at a time and the other five rest on dummy cores.

## What we would like from Andy

Printing, in two batches: the one shared base set plus one skin first so we can prove the mechanism and the magnet swap, then the other five skins and the five dummy cores once it moves. That is about 1.65 kg of filament (1,645 g: base 755 g, six skins 720 g, five dummy cores 170 g), about £32.91 at £20/kg, and roughly 42 to 67 hours of printer time on the H2D (25 to 40 g/h, about 7 plates at 6 minutes set-up each, a guide only), spread over a few weeks. These are model estimates from `print_cost.py` (written to `out/print_cost.txt`); the slicer on the real printer wins. We supply the spools, or pay for them. Parametric CAD (CadQuery) and STLs come from Dan, sized for FDM. The hidden parts print without supports; only the head halves, the shells, the Cloud formers and the clip-ons need them. The print settings are Andy's: Bambu Lab H2D (325 × 320 × 325 mm single-nozzle build area), 0.4 mm nozzle, 0.2 mm layers, 3 walls, 5 top and bottom layers, 25% infill, Bambu PLA Basic at 1.24 g/cm³ and £20/kg (full price), shrink 0%; they live in `print_settings.py`. Shrink compensation is still to be agreed with Andy. Andy quoted 4%; PLA usually shrinks well under 1%, and a 4% scale-up would leave the servo seats about 1-2 mm loose and the bearing seat about 3 mm loose. The parts are drawn true size. Every part fits the H2D bed (it also still fits a 220 × 220 mm bed).

| Part | Qty | Material | Notes |
| --- | --- | --- | --- |
| Base plate, one piece (160 × 160 × 48 mm) | 1 | PLA | Pocket for steel washers as ballast; electronics bay; at 25% infill 5 of the 10 open-top pockets are cut (the two big wells plus the voids under the ESP32, PCA9685 and buck-converter bays; about 40 g saved); no supports |
| Turntable (72 mm bearing seat) | 1 | PLA | Plate down, no supports |
| Turntable hub, 34 × 34 × 5 mm (3.4 g) | 1 | PLA | Split off the turntable so it prints without supports; fixed with 4 M2 screws, about 8 mm, up through the yaw servo horn and the hub into the turntable plate |
| Torso column, two halves with rails | 2 | PLA | 30 to 40 mm bounce travel |
| Bob carriage, lift yoke | 1 each | PLA | No supports |
| Bounce lift lever | 1 | PETG | Takes the lift load (the cost model assumes PLA) |
| Servo mounts: yaw pocket in the base plate, lift cradle on the turntable, MG90S pockets in neck base A, rocker B and the two shoulder sockets | built into those parts | PLA | M2 and M3 tabs; 4 × MG90S, 2 × MG996R |
| Neck gimbal, three parts | 3 | PETG | The only parts under real stress; neck base A prints without supports (45 degree sleeve and skirt), cross screws M3 × 10 in counterbores |
| Head sphere, two halves (Ø120 mm) | 2 | PLA | Hollow, thin wall; needs supports |
| Shoulder sockets and arm horns | 2 + 2 | PLA | Both shoulder servos stay fitted; the arm horns are part of the base set and come off for armless skins; the shoulder caps are not printed |
| Skin rings, spare (optional) | 4 | PLA | 8.5 g each, not in the totals; six 5 mm magnet pockets at 60° |
| Character shells (cloud, pear, frog, heart, Jolly, Claude) | 6 skins | PLA | Hollow, 1.5 mm wall, 0 to 5% infill; need supports |
| Clip-ons: beret, glasses, sunglasses | 3 | PLA | Small; need supports |
| Dummy core, 110 × 110 × 58 mm (34 g, about £0.68 each) | 5 | PLA | A cheap light former so the five skins not on the base hold their shape on the shelf; prints collar down without supports; six magnet pockets like the head (magnets optional); checked for zero overlap with all six skins |

Filament: 755 g for the base set (£15.11), 98 to 133 g per skin (720 g for six, £14.40), 34 g per dummy core (170 g for five, £3.40), 1,645 g in all, about £32.91 at £20/kg. Option 1, one test toy (the shared base set plus the Frog skin), is 18 pieces, about 853 g and £17.07, roughly 22 to 34 printer hours; option 2, the full run, is 41 pieces. The base set is 16 files (17 pieces); each skin is 2 to 3 pieces. Hardware we buy separately: servos, bearing, magnets, screws, wire, springs.

## If the print job is too much: backup plan

Nobody should be lumbered with 42 to 67 printer hours. Options, cheapest credible first (prices checked 17 Oct 2026, UK, except where marked as recalculated):

- Buy a Bambu Lab A1 mini (£169 on the UK store; 180 mm cube, so the Ø160 plate and the Ø120 sphere halves fit, the taller shells are tight). Printer plus 1.65 kg of filament (about £33 at £20/kg) is about £202 (recalculated 23 Oct), which beats every service we found for this much plastic, and the project owns a printer afterwards. The full-size A1 (256 mm cube, roughly £280 to £300) is the safer size for the shells.
- Online services: Craftcloud, JLC3DP and Protolabs Network all quote instantly from an STL upload but publish no per-gram rate. Rough expectation: £150 to £400 from JLC3DP (shipped from China, plus VAT) up to £450 to £900 from UK partners via Craftcloud; those ranges were guessed for the earlier, larger job and not redone for the one-base job. The one published UK rate (Reprap Ltd, £0.40 per cm³) comes to about £530 for the lot (recalculated 23 Oct: 1,645 g at 1.24 g/cm³ is about 1,327 cm³). Unverified until we upload the STLs.
- A peer maker on Fiverr at about £3.50 per printer hour comes to about £147 to £235 for the run (42 to 67 hours, recalculated 23 Oct), filament unclear.

So: the base set and one skin from Andy proves the design; if the full run is too much printer time, the A1 mini is the backup.

## Build order and open questions

1. Bench: ESP32 + two servos on external 5 V, first Bottango clip. One evening.
2. First base printed and assembled: turn, bounce, nod, tilt. First idle loop. One weekend.
3. First dot shell on, fleece over it. Prove the magnet swap.
4. The other skins and the five dummy cores printed; the skins dressed.
5. Jolly shell, fur wrap, arms (the arm horns and wire on the base's shoulder servos).
6. REST on the base, the MCP server, the six character profiles (voice and personality), speech-driven bounce.
7. Later: LED eyes, speaker and mic on the base, live AI mode.

Open questions

- [ ] Andy: is PETG fine for the gimbal and lift arm, or all PLA? (The bed size is settled: the Bambu Lab H2D, and every part fits it.)
- [ ] Andy: can the printer take 42 to 67 hours over two to three weeks without it being a pain?
- [ ] Andy: spools from us, or we pay for yours?
- [ ] Fuzzy finish on the dots: fleece wrap or flock? Flock is DIY, no UK service found.
- [ ] Bottango on the spare ESP32-C3 boards is unverified; a classic ESP32 WROOM is the safe buy.
