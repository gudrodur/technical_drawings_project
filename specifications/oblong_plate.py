"""
Stadium Plate Specifications - Single Source of Truth (SSOT)
=============================================================

All dimensional specifications for the stadium-shaped mounting plate.
All measurements are in millimeters (mm).

Component: Stadium Mounting Plate
Material: 4mm thick Stainless Steel
Application: Interface mounting plate for U-shaped mounting bracket
Manufacturing: Sharp as-cut edges (no chamfers or fillets)
"""

import numpy as np

# === MATERIAL SPECIFICATION ===
MATERIAL = "4mm Stainless Steel"
MATERIAL_THICKNESS = 4  # mm

# === OVERALL GEOMETRY ===
OVERALL_LENGTH = 330  # mm - Total stadium length
OVERALL_WIDTH = 120   # mm - Constant width throughout
PLATE_THICKNESS = 4   # mm - Same as mounting bracket

# === STADIUM SHAPE GEOMETRY ===
END_RADIUS = OVERALL_WIDTH / 2  # 60mm - Semicircular end radius
CENTRAL_RECTANGLE_LENGTH = OVERALL_LENGTH - (2 * END_RADIUS)  # 210mm
CENTRAL_RECTANGLE_WIDTH = OVERALL_WIDTH  # 120mm

# === COORDINATE SYSTEM ===
# Origin at geometric center of stadium plate
PLATE_LEFT = -OVERALL_LENGTH / 2     # -165mm
PLATE_RIGHT = OVERALL_LENGTH / 2     # +165mm  
PLATE_TOP = OVERALL_WIDTH / 2        # +60mm
PLATE_BOTTOM = -OVERALL_WIDTH / 2    # -60mm

# === SEMICIRCULAR ENDS ===
LEFT_SEMICIRCLE_CENTER_X = PLATE_LEFT + END_RADIUS    # -105mm
RIGHT_SEMICIRCLE_CENTER_X = PLATE_RIGHT - END_RADIUS  # +105mm
SEMICIRCLE_CENTER_Y = 0  # mm - Both ends centered on X-axis

# === HOLE GROUP SPECIFICATIONS ===
HOLE_GROUP_SPACING = 190  # mm - Center-to-center distance between groups
HOLE_GROUP_LEFT_X = -HOLE_GROUP_SPACING / 2   # -95mm
HOLE_GROUP_RIGHT_X = HOLE_GROUP_SPACING / 2   # +95mm

# === CIRCULAR HOLES (8 per group) ===
CIRCULAR_HOLE_DIAMETER = 8     # mm
CIRCULAR_HOLE_PCD = 90         # mm - Pitch Circle Diameter
CIRCULAR_HOLE_PCD_RADIUS = CIRCULAR_HOLE_PCD / 2  # 45mm

# 8 holes evenly spaced on PCD (45° intervals)
CIRCULAR_HOLE_ANGLES = [0, 45, 90, 135, 180, 225, 270, 315]  # degrees

# === CENTER HOLES (1 per group) ===
CENTER_HOLE_DIAMETER = 25  # mm - Simple circular holes
# Legacy Double-D compatibility names (now just circular)
DOUBLE_D_OVERALL_DIAMETER = CENTER_HOLE_DIAMETER  # 25mm
DOUBLE_D_FLAT_TO_FLAT = 20      # mm - No longer used (legacy compatibility)
DOUBLE_D_FLAT_WIDTH = DOUBLE_D_FLAT_TO_FLAT  # Compatibility alias
DOUBLE_D_FLAT_HEIGHT = (DOUBLE_D_OVERALL_DIAMETER**2 - (DOUBLE_D_FLAT_TO_FLAT/2)**2)**0.5 * 2  # Calculated height

# === HOLE GROUP POSITIONS ===
# Left hole group centered at (-95, 0)
LEFT_GROUP_CENTER = (HOLE_GROUP_LEFT_X, 0)

# Right hole group centered at (+95, 0) 
RIGHT_GROUP_CENTER = (HOLE_GROUP_RIGHT_X, 0)

# === MANUFACTURING SPECIFICATIONS ===
EDGE_FINISH = "Sharp as-cut edges"
SURFACE_FINISH = "Standard mill finish"

# === FUNCTIONAL SPECIFICATIONS ===
APPLICATION = "Interface mounting plate for U-shaped mounting bracket"
HOLE_PATTERN_PURPOSE = "Perfect alignment with mounting bracket hole pattern"
ASSEMBLY_METHOD = "Bolted connection through circular holes"

# === COMPATIBILITY SPECIFICATIONS (for existing drawing code) ===
CENTRAL_RECT_LEFT = LEFT_SEMICIRCLE_CENTER_X   # -105mm
CENTRAL_RECT_RIGHT = RIGHT_SEMICIRCLE_CENTER_X  # +105mm
STADIUM_TOP_EDGE = PLATE_TOP      # +60mm
STADIUM_BOTTOM_EDGE = PLATE_BOTTOM # -60mm
STADIUM_LEFT_END = PLATE_LEFT     # -165mm
STADIUM_RIGHT_END = PLATE_RIGHT   # +165mm

# === HOLE POSITION CALCULATIONS ===
# Left group circular holes (8 holes on PCD)
LEFT_GROUP_HOLES = []
for angle in CIRCULAR_HOLE_ANGLES:
    angle_rad = np.radians(angle)
    x = HOLE_GROUP_LEFT_X + CIRCULAR_HOLE_PCD_RADIUS * np.cos(angle_rad)
    y = 0 + CIRCULAR_HOLE_PCD_RADIUS * np.sin(angle_rad)
    LEFT_GROUP_HOLES.append((x, y))

# Right group circular holes (8 holes on PCD)
RIGHT_GROUP_HOLES = []
for angle in CIRCULAR_HOLE_ANGLES:
    angle_rad = np.radians(angle)
    x = HOLE_GROUP_RIGHT_X + CIRCULAR_HOLE_PCD_RADIUS * np.cos(angle_rad)
    y = 0 + CIRCULAR_HOLE_PCD_RADIUS * np.sin(angle_rad)
    RIGHT_GROUP_HOLES.append((x, y))

# === CENTER HOLE CENTERS ===
LEFT_CENTER_HOLE_CENTER = (HOLE_GROUP_LEFT_X, 0)   # (-95, 0)
RIGHT_CENTER_HOLE_CENTER = (HOLE_GROUP_RIGHT_X, 0)  # (+95, 0)
# Legacy Double-D compatibility aliases
LEFT_DOUBLE_D_CENTER = LEFT_CENTER_HOLE_CENTER
RIGHT_DOUBLE_D_CENTER = RIGHT_CENTER_HOLE_CENTER
