"""
Mounting Bracket Specifications
===============================

Single Source of Truth (SSOT) for all mounting bracket dimensions.
All measurements are in millimeters (mm).

Component: Mounting Bracket (for gunwale/roof attachment)
Material: 4mm thick Stainless Steel
"""

# === GENERAL SPECIFICATIONS ===
MATERIAL = "4mm Stainless Steel"
MATERIAL_THICKNESS = 4  # mm

# === BASE PLATE SPECIFICATIONS ===
BASE_PLATE_WIDTH = 120  # mm
BASE_PLATE_HEIGHT = 120  # mm
BASE_PLATE_THICKNESS = 4  # mm

# Base plate hole pattern
BASE_PLATE_HOLE_COUNT = 6
BASE_PLATE_HOLE_DIAMETER = 8  # mm

# Hole coordinates (X, Y) - Origin at center of base plate
BASE_PLATE_HOLE_POSITIONS = [
    (-40, 30),   # Top row, left
    (0, 30),     # Top row, center
    (40, 30),    # Top row, right
    (-40, -30),  # Bottom row, left
    (0, -30),    # Bottom row, center
    (40, -30)    # Bottom row, right
]

# === U-SHAPED ARM SPECIFICATIONS ===
U_ARM_OVERALL_HEIGHT = 200  # mm
U_ARM_OVERALL_WIDTH = 120   # mm
U_ARM_WALL_THICKNESS = 4    # mm

# U-arm positioning
U_ARM_BACK_EDGE_Y = -60  # mm (flush with back edge of base plate)

# Semicircular top section
U_ARM_SEMICIRCLE_RADIUS = 60  # mm
U_ARM_STRAIGHT_HEIGHT = U_ARM_OVERALL_HEIGHT - U_ARM_SEMICIRCLE_RADIUS  # 140mm

# === U-ARM HOLE PATTERN (8 holes on PCD) ===
U_ARM_HOLE_COUNT = 8
U_ARM_HOLE_DIAMETER = 8  # mm
U_ARM_PCD_DIAMETER = 90  # mm (Pitch Circle Diameter)
U_ARM_PCD_RADIUS = U_ARM_PCD_DIAMETER / 2  # 45mm

# Hole angular positions (degrees)
U_ARM_HOLE_ANGLES = [0, 45, 90, 135, 180, 225, 270, 315]

# PCD center position
U_ARM_PCD_CENTER_X = 0  # mm (centered)
U_ARM_PCD_CENTER_Z = U_ARM_STRAIGHT_HEIGHT  # 140mm (at semicircle center)

# === CENTER MILLED SLOT SPECIFICATIONS ===
CENTER_SLOT_OVERALL_DIAMETER = 25  # mm (overall height)
CENTER_SLOT_FLAT_WIDTH = 20         # mm (distance between parallel flats)
CENTER_SLOT_FLAT_HALF_WIDTH = CENTER_SLOT_FLAT_WIDTH / 2  # 10mm
CENTER_SLOT_END_RADIUS = CENTER_SLOT_FLAT_HALF_WIDTH      # 10mm
CENTER_SLOT_STRAIGHT_HEIGHT = CENTER_SLOT_OVERALL_DIAMETER - (2 * CENTER_SLOT_END_RADIUS)  # 5mm

# Center slot position
CENTER_SLOT_CENTER_X = U_ARM_PCD_CENTER_X  # 0mm
CENTER_SLOT_CENTER_Z = U_ARM_PCD_CENTER_Z  # 140mm

# === COORDINATE SYSTEM ===
# Origin (0,0) is at the geometric center of the base plate
# X-axis: Left (-) to Right (+)
# Y-axis: Front (-) to Back (+)
# Z-axis: Down (-) to Up (+)

# === WELDING SPECIFICATIONS ===
WELD_TYPE = "Continuous fillet weld"
WELD_LOCATION = "Inside corner where U-arm meets base plate"

# === DERIVED CALCULATIONS ===
# Base plate boundaries
BASE_PLATE_LEFT = -BASE_PLATE_WIDTH / 2    # -60mm
BASE_PLATE_RIGHT = BASE_PLATE_WIDTH / 2    # +60mm
BASE_PLATE_FRONT = -BASE_PLATE_HEIGHT / 2  # -60mm
BASE_PLATE_BACK = BASE_PLATE_HEIGHT / 2    # +60mm

# U-arm inner dimensions
U_ARM_INNER_WIDTH = U_ARM_OVERALL_WIDTH - (2 * U_ARM_WALL_THICKNESS)  # 112mm
U_ARM_INNER_RADIUS = U_ARM_SEMICIRCLE_RADIUS - U_ARM_WALL_THICKNESS    # 56mm

# U-arm side positions
U_ARM_LEFT_OUTER = -U_ARM_OVERALL_WIDTH / 2                           # -60mm
U_ARM_RIGHT_OUTER = U_ARM_OVERALL_WIDTH / 2                           # +60mm
U_ARM_LEFT_INNER = U_ARM_LEFT_OUTER + U_ARM_WALL_THICKNESS            # -56mm
U_ARM_RIGHT_INNER = U_ARM_RIGHT_OUTER - U_ARM_WALL_THICKNESS          # +56mm
