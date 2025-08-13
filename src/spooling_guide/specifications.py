"""
Spooling Guide Plate - Single Source of Truth (SSOT)
All dimensional specifications for the Spooling Guide component.

This file contains ONLY dimensional constants - no calculations or logic.
All measurements are in millimeters (mm) unless otherwise specified.
"""

# ============================================================================
# MATERIAL SPECIFICATIONS
# ============================================================================
MAIN_PLATE_MATERIAL = "4mm Stainless Steel"
OUTER_RING_MATERIAL = "10mm diameter Stainless Steel rod"
MAIN_PLATE_THICKNESS = 4.0  # mm
OUTER_RING_DIAMETER = 10.0  # mm

# ============================================================================
# PLATE GEOMETRY
# ============================================================================
CENTRAL_OPENING_RADIUS = 250.0  # mm
ARM_COUNT = 4
ARM_ANGULAR_SPACING = 90.0  # degrees (360° / 4 arms)

# ============================================================================
# ARM GEOMETRY  
# ============================================================================
# Linear taper from inner to outer edge
ARM_WIDTH_INNER = 50.0   # mm (width at central opening)
ARM_WIDTH_OUTER = 100.0  # mm (width at outer ring)

# Arm radial boundaries - CORRECTED FOR RING CLEARANCE
ARM_INNER_RADIUS = 250.0  # mm (inner boundary at central opening)
ARM_OUTER_RADIUS = 505.0  # mm (outer boundary - tangent to ring inner surface)

# Concave arc termination at outer edge
ARM_END_ARC_RADIUS = 532.5  # mm

# ============================================================================
# HOLE SPECIFICATIONS
# ============================================================================
# Central pilot hole
CENTRAL_HOLE_DIAMETER = 30.0  # mm - UPDATED FROM 25.0
CENTRAL_HOLE_X = 0.0  # mm
CENTRAL_HOLE_Y = 0.0  # mm

# Inner hole pattern (8 holes on circle) - UPDATED FOR COMPONENT COMPATIBILITY
INNER_HOLE_COUNT = 8
INNER_HOLE_DIAMETER = 8.0  # mm
INNER_HOLE_PCD = 90.0  # mm (Pitch Circle Diameter) - CHANGED FROM 360.0 TO MATCH MOUNTING_BRACKET/OBLONG_PLATE

# Outer mounting hole pattern (4 holes aligned with arms)
OUTER_HOLE_COUNT = 4
OUTER_HOLE_DIAMETER = 8.0  # mm
OUTER_HOLE_PCD = 1020.0  # mm (Pitch Circle Diameter)

# ============================================================================
# FINISHING SPECIFICATIONS
# ============================================================================
EDGE_FINISH = "Sharp as-cut"
CORNER_FILLET_RADIUS = 5.0  # mm (R5)
CORNER_FILLET_COUNT = 16  # 4 corners per arm × 4 arms

# ============================================================================
# WELDING & ASSEMBLY
# ============================================================================
OUTER_RING_WELD_TYPE = "Continuous fillet weld"
RING_CENTERING_NOTE = "Ring centered on 4mm plate thickness"

# ============================================================================
# ANGULAR POSITIONS (calculated from 0° = positive X-axis)
# ============================================================================
ARM_ANGLES = [0.0, 90.0, 180.0, 270.0]  # degrees
OUTER_HOLE_ANGLES = ARM_ANGLES  # Aligned with arm centerlines

# Inner holes evenly distributed
INNER_HOLE_ANGULAR_SPACING = 360.0 / INNER_HOLE_COUNT  # 45.0 degrees
INNER_HOLE_ANGLES = [i * INNER_HOLE_ANGULAR_SPACING for i in range(INNER_HOLE_COUNT)]

# ============================================================================
# DRAWING SPECIFICATIONS
# ============================================================================
DRAWING_SCALE = "1:10"  # Recommended scale for this large component
DRAWING_TITLE = "LÍNUSTÝRING (SPOOLING GUIDE PLATE)"
DRAWING_VIEW_NAME = "2D Technical Drawing - Side View"
