r"""
Print settings in one place. These are Andy's (his reply of 23 Oct 2026): Bambu Lab H2D, Bambu PLA Basic,
0.4 mm nozzle, 0.2 mm layers, 3 walls, 25% infill.

Change a number here, then re-run:
  .venv\Scripts\python.exe build_puppet_base.py --no-check   (the infill decides which hollow pockets in the base pay)
  .venv\Scripts\python.exe print_cost.py                     (plastic, time and cost for one base + six skins + five cores)
"""
PRINTER = "Bambu Lab H2D"
BED_X, BED_Y, BED_Z = 325.0, 320.0, 325.0     # mm, H2D single-nozzle build area (300 x 320 when both nozzles print)
NOZZLE = 0.4                                  # mm
LAYER = 0.2                                   # mm
WALLS = 3                                     # perimeters
TOP_BOTTOM_LAYERS = 5                         # solid layers top and bottom
INFILL = 0.25                                 # 0..1
FILAMENT = "Bambu PLA Basic"
GBP_PER_KG = 20.0                             # full list price (Andy buys in sales nearer 15, but he is being paid properly)
GRAMS_PER_HOUR = (25.0, 40.0)                 # H2D on its standard 0.20 mm PLA profile: small or supported parts at the
                                              # low end, big plates of plain parts at the high end
PLATE_SETUP_MIN = 6.0                         # heat-up, bed levelling and nozzle wipe before each plate
PLATE_FILL = 0.55                             # share of the bed that parts' footprints fill on a typical plate
DENSITY = 1.24                                # g/cm3, PLA
SUPPORT_FRACTION = 0.15                       # extra plastic on a part that needs supports
SHRINK_PCT = 0.0                              # slicer scale-up for shrink. Andy quoted 4%, but PLA shrinks well under 1%
                                              # and a 4% scale-up would print the servo and bearing seats loose, so the
                                              # CAD is drawn true size and this stays 0 until that is settled


def skin_mm():
    """Solid skin the weight model assumes on every surface: the thicker of the side walls and the top/bottom layers."""
    return max(WALLS * NOZZLE, TOP_BOTTOM_LAYERS * LAYER)
