"""
Spooling Guide Geometry Calculations - SIMPLIFIED IMPLEMENTATION

This module contains simplified geometric functions for calculating vertices,
coordinates, and geometric properties of the Spooling Guide component.

SIMPLIFIED DESIGN IMPLEMENTATION:
- Removed complex concave arc calculations for robustness
- Simplified arm termination to straight-line boundary at r=505mm
- Trapezoidal arm shape with clean geometric relationships
- Maintained mathematical precision for basic geometric elements

Mathematical Foundation:
- Simple trapezoidal arm geometry
- Exact linear taper calculations
- Straightforward coordinate calculations
- No complex curve intersections
"""

import numpy as np
import math
from . import specifications as spec


# ============================================================================
# MATHEMATICAL HELPER FUNCTIONS (RETAINED FOR UTILITY)
# ============================================================================

def _solve_quadratic_equation(a, b, c):
    """
    Solve quadratic equation ax² + bx + c = 0 using exact mathematical formula.
    
    Args:
        a, b, c (float): Quadratic coefficients
        
    Returns:
        list: Solutions [x1, x2] or empty list if no real solutions
    """
    if abs(a) < 1e-12:  # Handle linear case
        if abs(b) < 1e-12:
            return []  # No solution or infinite solutions
        return [-c / b]
    
    discriminant = b**2 - 4*a*c
    
    if discriminant < 0:
        return []  # No real solutions
    elif discriminant == 0:
        return [-b / (2*a)]  # One solution
    else:
        sqrt_discriminant = math.sqrt(discriminant)
        x1 = (-b - sqrt_discriminant) / (2*a)
        x2 = (-b + sqrt_discriminant) / (2*a)
        return [x1, x2]


def _calculate_line_equation_from_points(point1, point2):
    """
    Calculate standard form line equation Ax + By + C = 0 from two points.
    
    Args:
        point1, point2 (tuple): (x, y) coordinates
        
    Returns:
        tuple: (A, B, C) coefficients for standard form equation
    """
    x1, y1 = point1
    x2, y2 = point2
    
    # Calculate slope
    if abs(x2 - x1) < 1e-12:  # Vertical line
        return (1.0, 0.0, -x1)
    
    slope = (y2 - y1) / (x2 - x1)
    
    # Convert to standard form: y - y1 = slope(x - x1)
    # Rearrange to: slope*x - y + (y1 - slope*x1) = 0
    A = slope
    B = -1.0
    C = y1 - slope * x1
    
    return (A, B, C)


def _distance_point_to_line_standard_form(point, line_coeffs):
    """
    Calculate distance from point to line using standard form equation.
    
    Args:
        point (tuple): (x, y) coordinates
        line_coeffs (tuple): (A, B, C) for line equation Ax + By + C = 0
        
    Returns:
        float: Distance from point to line
    """
    x, y = point
    A, B, C = line_coeffs
    
    return abs(A*x + B*y + C) / math.sqrt(A**2 + B**2)


# ============================================================================
# ARM GEOMETRY CALCULATIONS - SIMPLIFIED IMPLEMENTATION
# ============================================================================

def arm_width_at_radius(radius):
    """
    Calculate arm width at a given radius using the linear taper.
    
    Formula: W(r) = 50 + 50 * (r - 250) / 255
    
    Args:
        radius (float): Radial distance from origin
        
    Returns:
        float: Arm width at the specified radius
    """
    r_inner = spec.ARM_INNER_RADIUS  # 250mm
    r_outer = spec.ARM_OUTER_RADIUS  # 505mm
    
    if radius < r_inner:
        return spec.ARM_WIDTH_INNER
    elif radius > r_outer:
        return spec.ARM_WIDTH_OUTER
    else:
        # Linear interpolation: W(r) = 50 + 50 * (r - 250) / 255
        width = spec.ARM_WIDTH_INNER + (spec.ARM_WIDTH_OUTER - spec.ARM_WIDTH_INNER) * (radius - r_inner) / (r_outer - r_inner)
        return width


def calculate_arm_vertices(arm_angle_deg):
    """
    Calculate the four corner vertices for a single trapezoidal arm.
    
    SIMPLIFIED DESIGN: Arms terminate in straight lines at r=505mm.
    No complex concave arcs - just clean trapezoidal geometry.
    
    Args:
        arm_angle_deg (float): Arm centerline angle in degrees (0° = +X axis)
        
    Returns:
        tuple: (arm_outline_points, concave_arc_points, fillet_data)
               - arm_outline_points: numpy array of 4 corner coordinates
               - concave_arc_points: empty array (no arcs in simplified design)
               - fillet_data: simplified fillet data structure
    """
    angle_rad = math.radians(arm_angle_deg)
    
    # Calculate the four corner points of the trapezoidal arm
    r_inner = spec.ARM_INNER_RADIUS     # 250mm
    r_outer = spec.ARM_OUTER_RADIUS     # 505mm
    
    # Calculate half-widths at inner and outer radii
    half_width_inner = spec.ARM_WIDTH_INNER / 2.0  # 25mm
    half_width_outer = spec.ARM_WIDTH_OUTER / 2.0  # 50mm
    
    # Arm centerline direction
    arm_direction = np.array([math.cos(angle_rad), math.sin(angle_rad)])
    # Perpendicular direction (left side positive)
    perp_direction = np.array([-math.sin(angle_rad), math.cos(angle_rad)])
    
    # Calculate the four corner points
    inner_left = r_inner * arm_direction + half_width_inner * perp_direction
    inner_right = r_inner * arm_direction - half_width_inner * perp_direction
    outer_left = r_outer * arm_direction + half_width_outer * perp_direction
    outer_right = r_outer * arm_direction - half_width_outer * perp_direction
    
    # Create closed trapezoid outline (5 points to close the shape)
    arm_outline_points = np.array([
        inner_left,
        outer_left,
        outer_right,
        inner_right,
        inner_left  # Close the shape
    ])
    
    # No concave arc in simplified design
    concave_arc_points = np.array([])
    
    # Simplified fillet data (corners where fillets would be applied)
    fillet_data = {
        'centers': [inner_left, inner_right, outer_left, outer_right],
        'arcs': [],
        'radius': spec.CORNER_FILLET_RADIUS
    }
    
    return arm_outline_points, concave_arc_points, fillet_data


def calculate_arm_corner_coordinates(arm_angle_deg):
    """
    Calculate the exact corner coordinates for a trapezoidal arm.
    
    Args:
        arm_angle_deg (float): Arm centerline angle in degrees
        
    Returns:
        dict: Dictionary containing all four corner coordinates
    """
    angle_rad = math.radians(arm_angle_deg)
    
    r_inner = spec.ARM_INNER_RADIUS     # 250mm
    r_outer = spec.ARM_OUTER_RADIUS     # 505mm
    
    # Calculate half-widths at inner and outer radii
    half_width_inner = spec.ARM_WIDTH_INNER / 2.0  # 25mm
    half_width_outer = spec.ARM_WIDTH_OUTER / 2.0  # 50mm
    
    # Arm centerline direction
    arm_direction = np.array([math.cos(angle_rad), math.sin(angle_rad)])
    # Perpendicular direction (left side positive)
    perp_direction = np.array([-math.sin(angle_rad), math.cos(angle_rad)])
    
    # Calculate the four corner points
    inner_left = r_inner * arm_direction + half_width_inner * perp_direction
    inner_right = r_inner * arm_direction - half_width_inner * perp_direction
    outer_left = r_outer * arm_direction + half_width_outer * perp_direction
    outer_right = r_outer * arm_direction - half_width_outer * perp_direction
    
    return {
        'inner_left': (inner_left[0], inner_left[1]),
        'inner_right': (inner_right[0], inner_right[1]),
        'outer_left': (outer_left[0], outer_left[1]),
        'outer_right': (outer_right[0], outer_right[1])
    }


def assemble_arm_outline_with_fillets(inner_left, inner_right, outer_left, outer_right, 
                                     concave_arc_points, fillet_data):
    """
    Assemble a simple trapezoidal arm outline.
    
    SIMPLIFIED IMPLEMENTATION: Creates a basic closed trapezoid.
    Fillet implementation will be added in a later step.
    
    Args:
        inner_left, inner_right: Inner corner coordinates
        outer_left, outer_right: Outer corner coordinates  
        concave_arc_points: Ignored (no arcs in simplified design)
        fillet_data: Ignored for now (basic shape first)
        
    Returns:
        numpy.ndarray: Simple trapezoidal outline points
    """
    # Create simple closed trapezoid
    outline_points = np.array([
        inner_left,
        outer_left,
        outer_right, 
        inner_right,
        inner_left  # Close the shape
    ])
    
    return outline_points


def calculate_simplified_fillet_data(arm_angle_rad, inner_left, inner_right, outer_left, outer_right):
    """
    Calculate simplified fillet data for the trapezoidal arm corners.
    
    Args:
        arm_angle_rad: Arm centerline angle
        inner_left, inner_right: Inner corner coordinates
        outer_left, outer_right: Outer corner coordinates
        
    Returns:
        dict: Simplified fillet data structure
    """
    fillet_radius = spec.CORNER_FILLET_RADIUS
    
    return {
        'centers': [inner_left, inner_right, outer_left, outer_right],
        'arcs': [],  # No arc calculations in simplified version
        'radius': fillet_radius
    }


# ============================================================================
# VALIDATION AND UTILITY FUNCTIONS
# ============================================================================

def validate_simplified_geometry():
    """
    Validate the simplified geometric implementation.
    
    Returns:
        dict: Validation results
    """
    warnings = []
    errors = []
    
    # Test arm calculation for all angles
    test_angles = [0.0, 90.0, 180.0, 270.0]
    
    for angle in test_angles:
        try:
            arm_outline, _, fillet_data = calculate_arm_vertices(angle)
            
            if len(arm_outline) != 5:  # Should be 5 points (4 corners + closing point)
                errors.append(f"Arm at {angle}°: Expected 5 outline points, got {len(arm_outline)}")
            
            if len(fillet_data['centers']) != 4:  # Should be 4 corner points
                errors.append(f"Arm at {angle}°: Expected 4 fillet centers, got {len(fillet_data['centers'])}")
                
        except Exception as e:
            errors.append(f"Arm at {angle}°: Calculation failed - {e}")
    
    # Check arm width function
    width_250 = arm_width_at_radius(250.0)
    width_505 = arm_width_at_radius(505.0)
    
    if abs(width_250 - 50.0) > 0.1:
        errors.append(f"Width at r=250mm: {width_250:.1f}mm (expected: 50.0mm)")
    
    if abs(width_505 - 100.0) > 0.1:
        errors.append(f"Width at r=505mm: {width_505:.1f}mm (expected: 100.0mm)")
    
    # Check manufacturing clearance
    ring_inner = (spec.OUTER_HOLE_PCD / 2.0) - (spec.OUTER_RING_DIAMETER / 2.0)
    arm_outer = spec.ARM_OUTER_RADIUS
    clearance = ring_inner - arm_outer
    
    if abs(clearance) > 0.001:
        warnings.append(f"Ring clearance: {clearance:.3f}mm (expected: 0.000mm)")
    
    return {
        'warnings': warnings,
        'errors': errors,
        'geometry_valid': len(errors) == 0
    }


# ============================================================================
# EXISTING UTILITY FUNCTIONS (MAINTAINED FOR COMPATIBILITY)
# ============================================================================

def calculate_hole_coordinates():
    """
    Calculate coordinates for all hole patterns.
    
    Returns:
        dict: Dictionary containing coordinates for each hole pattern
    """
    holes = {}
    
    # Central pilot hole
    holes['central'] = np.array([[spec.CENTRAL_HOLE_X, spec.CENTRAL_HOLE_Y]])
    
    # Inner hole pattern (8 holes on 360mm PCD)
    inner_coords = []
    for angle_deg in spec.INNER_HOLE_ANGLES:
        angle_rad = math.radians(angle_deg)
        x = (spec.INNER_HOLE_PCD / 2.0) * math.cos(angle_rad)
        y = (spec.INNER_HOLE_PCD / 2.0) * math.sin(angle_rad)
        inner_coords.append([x, y])
    holes['inner'] = np.array(inner_coords)
    
    # Outer hole pattern (4 holes on 1020mm PCD, aligned with arms)
    outer_coords = []
    for angle_deg in spec.OUTER_HOLE_ANGLES:
        angle_rad = math.radians(angle_deg)
        x = (spec.OUTER_HOLE_PCD / 2.0) * math.cos(angle_rad)
        y = (spec.OUTER_HOLE_PCD / 2.0) * math.sin(angle_rad)
        outer_coords.append([x, y])
    holes['outer'] = np.array(outer_coords)
    
    return holes


def calculate_overall_dimensions():
    """
    Calculate overall bounding dimensions of the complete assembly.
    
    Returns:
        dict: Dictionary with overall width, height, and key radial dimensions
    """
    outer_ring_center_radius = spec.OUTER_HOLE_PCD / 2.0
    ring_radius = spec.OUTER_RING_DIAMETER / 2.0
    
    overall_radius = outer_ring_center_radius + ring_radius
    overall_diameter = 2.0 * overall_radius
    
    return {
        'overall_diameter': overall_diameter,
        'overall_radius': overall_radius,
        'outer_ring_center_radius': outer_ring_center_radius,
        'central_opening_diameter': 2.0 * spec.CENTRAL_OPENING_RADIUS
    }


def generate_central_opening_points(num_points=100):
    """
    Generate points for the central circular opening.
    
    Args:
        num_points (int): Number of points around the circle
        
    Returns:
        numpy.ndarray: Array of (x, y) coordinates around central opening
    """
    angles = np.linspace(0, 2*np.pi, num_points)
    radius = spec.CENTRAL_OPENING_RADIUS
    
    x_coords = radius * np.cos(angles)
    y_coords = radius * np.sin(angles) 
    
    return np.column_stack((x_coords, y_coords))


def validate_geometry():
    """
    Perform geometric validation checks on calculated dimensions.
    
    Returns:
        dict: Validation results with any warnings or errors
    """
    # Use the simplified validation function
    return validate_simplified_geometry()
