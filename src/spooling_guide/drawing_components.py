"""
Spooling Guide Drawing Components

This module contains discrete matplotlib rendering functions for each major 
component of the Spooling Guide. Each function handles the visual rendering
of specific geometric elements with professional styling.

Components:
- Main plate outline with central opening
- Individual arms with taper and concave terminations
- Hole patterns (central, inner, outer)
- Outer ring assembly
- Corner fillets and finishing details
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from . import specifications as spec
from . import geometry as geom


def draw_central_opening(ax, style_config):
    """
    Draw the central circular opening (250mm radius).
    
    Args:
        ax: Matplotlib axes object
        style_config: Dictionary containing styling parameters
    """
    opening_points = geom.generate_central_opening_points()
    
    ax.plot(opening_points[:, 0], opening_points[:, 1], 
            color=style_config['primary_color'],
            linewidth=style_config['primary_linewidth'],
            label='Central Opening')


def draw_single_arm(ax, arm_angle_deg, style_config):
    """
    Draw a single arm with simplified trapezoidal geometry.
    
    SIMPLIFIED DESIGN: Arms are now simple trapezoids with straight-line terminations.
    No complex concave arcs - clean geometric shapes for robust manufacturing.
    
    Args:
        ax: Matplotlib axes object  
        arm_angle_deg: Arm centerline angle in degrees
        style_config: Dictionary containing styling parameters
    """
    # Get simplified arm geometry
    arm_outline_points, concave_arc_points, fillet_data = geom.calculate_arm_vertices(arm_angle_deg)
    
    # Draw main arm outline (simple trapezoid)
    ax.plot(arm_outline_points[:, 0], arm_outline_points[:, 1],
            color=style_config['primary_color'],
            linewidth=style_config['primary_linewidth'],
            solid_capstyle='round')
    
    # Draw concave arc termination only if points exist (for backward compatibility)
    if len(concave_arc_points) > 0 and concave_arc_points.ndim == 2:
        ax.plot(concave_arc_points[:, 0], concave_arc_points[:, 1],
                color=style_config['primary_color'],
                linewidth=style_config['primary_linewidth'] * 1.2,
                linestyle='-',
                alpha=0.8)
    
    # Draw R5 corner fillets (simplified - will be enhanced later)
    draw_arm_fillets(ax, fillet_data, style_config)
    
    # Optional: Draw construction lines for visualization
    if style_config.get('show_construction_lines', False):
        draw_arm_construction_lines(ax, arm_angle_deg, style_config)


def draw_all_arms(ax, style_config):
    """
    Draw all 4 arms positioned at 90° intervals.
    
    Args:
        ax: Matplotlib axes object
        style_config: Dictionary containing styling parameters  
    """
    for arm_angle in spec.ARM_ANGLES:
        draw_single_arm(ax, arm_angle, style_config)


def draw_hole_pattern(ax, hole_type, style_config):
    """
    Draw a specific hole pattern (central, inner, or outer).
    
    Args:
        ax: Matplotlib axes object
        hole_type: String - 'central', 'inner', or 'outer'
        style_config: Dictionary containing styling parameters
    """
    hole_coords = geom.calculate_hole_coordinates()
    
    if hole_type == 'central':
        coords = hole_coords['central']
        diameter = spec.CENTRAL_HOLE_DIAMETER
        color = '#FFFF00'  # Yellow for central pilot hole
        label = f'Central Hole ⌀{diameter}mm'
        
    elif hole_type == 'inner':
        coords = hole_coords['inner'] 
        diameter = spec.INNER_HOLE_DIAMETER
        color = style_config['hole_color']
        label = f'Inner Holes ⌀{diameter}mm'
        
    elif hole_type == 'outer':
        if spec.OUTER_HOLE_COUNT == 0:
            return  # No outer holes to draw
        coords = hole_coords['outer']
        diameter = spec.OUTER_HOLE_DIAMETER  
        color = style_config['hole_color']
        label = f'Outer Holes ⌀{diameter}mm'
    
    else:
        raise ValueError(f"Unknown hole type: {hole_type}")
    
    # Draw each hole as a circle
    radius = diameter / 2.0
    for coord in coords:
        circle = patches.Circle((coord[0], coord[1]), radius, 
                               fill=False, 
                               edgecolor=color,
                               linewidth=style_config['hole_linewidth'])
        ax.add_patch(circle)
    
    # Add label to first hole only
    if len(coords) > 0:
        ax.plot(coords[0, 0], coords[0, 1], 'o', 
                color=color, markersize=2, label=label)


def draw_all_holes(ax, style_config):
    """
    Draw all hole patterns on the component.
    
    Args:
        ax: Matplotlib axes object
        style_config: Dictionary containing styling parameters
    """
    draw_hole_pattern(ax, 'central', style_config)
    draw_hole_pattern(ax, 'inner', style_config) 
    draw_hole_pattern(ax, 'outer', style_config)


def draw_outer_ring(ax, style_config):
    """
    Draw the outer stainless steel ring (10mm diameter rod).
    
    Args:
        ax: Matplotlib axes object
        style_config: Dictionary containing styling parameters
    """
    # Ring is positioned at the outer hole PCD
    ring_center_radius = spec.OUTER_HOLE_PCD / 2.0
    ring_radius = spec.OUTER_RING_DIAMETER / 2.0
    
    # Draw outer edge of ring
    outer_circle = patches.Circle((0, 0), ring_center_radius + ring_radius,
                                 fill=False,
                                 edgecolor=style_config['ring_color'],
                                 linewidth=style_config['ring_linewidth'],
                                 linestyle='--',
                                 label='Outer Ring (10mm ⌀)')
    ax.add_patch(outer_circle)
    
    # Draw inner edge of ring  
    inner_circle = patches.Circle((0, 0), ring_center_radius - ring_radius,
                                 fill=False,
                                 edgecolor=style_config['ring_color'], 
                                 linewidth=style_config['ring_linewidth'],
                                 linestyle='--')
    ax.add_patch(inner_circle)


def draw_pitch_circle_diameter(ax, pcd_radius, pcd_label, style_config):
    """
    Draw a pitch circle diameter (PCD) reference line.
    
    Args:
        ax: Matplotlib axes object
        pcd_radius: Radius of the PCD circle
        pcd_label: Label for the PCD
        style_config: Dictionary containing styling parameters
    """
    pcd_circle = patches.Circle((0, 0), pcd_radius,
                               fill=False,
                               edgecolor=style_config['pcd_color'],
                               linewidth=style_config['pcd_linewidth'],
                               linestyle=':',
                               alpha=0.6,
                               label=pcd_label)
    ax.add_patch(pcd_circle)


def draw_all_pcds(ax, style_config):
    """
    Draw all pitch circle diameters for reference.
    
    Args:
        ax: Matplotlib axes object
        style_config: Dictionary containing styling parameters
    """
    # Inner hole PCD
    draw_pitch_circle_diameter(ax, spec.INNER_HOLE_PCD / 2.0, 
                              f'Inner PCD {spec.INNER_HOLE_PCD}mm', style_config)
    
    # Outer hole PCD  
    draw_pitch_circle_diameter(ax, spec.OUTER_HOLE_PCD / 2.0,
                              f'Outer PCD {spec.OUTER_HOLE_PCD}mm', style_config)


def draw_corner_fillets(ax, style_config):
    """
    Draw R5 corner fillets at all 16 arm junction points.
    
    Args:
        ax: Matplotlib axes object
        style_config: Dictionary containing styling parameters
    """
    # Draw fillets for all arms
    for arm_angle in spec.ARM_ANGLES:
        # Get fillet data for this arm
        _, _, fillet_data = geom.calculate_arm_vertices(arm_angle)
        draw_arm_fillets(ax, fillet_data, style_config)


def draw_arm_fillets(ax, fillet_data, style_config):
    """
    Draw the R5 fillets for a single arm.
    
    Args:
        ax: Matplotlib axes object
        fillet_data: Dictionary containing fillet centers and arc data
        style_config: Dictionary containing styling parameters
    """
    # Draw each fillet arc
    for arc_points in fillet_data['arcs']:
        if len(arc_points) > 0:
            ax.plot(arc_points[:, 0], arc_points[:, 1],
                    color=style_config['primary_color'],
                    linewidth=style_config['primary_linewidth'] * 0.8,
                    linestyle='-',
                    alpha=0.9)
    
    # Draw fillet center points (optional, for construction reference)
    if style_config.get('show_fillet_centers', False):
        for center in fillet_data['centers']:
            ax.plot(center[0], center[1], 'o',
                    color=style_config['centerline_color'],
                    markersize=2,
                    alpha=0.6)


def draw_arm_construction_lines(ax, arm_angle_deg, style_config):
    """
    Draw construction lines for arm geometry visualization.
    
    Args:
        ax: Matplotlib axes object
        arm_angle_deg: Arm centerline angle in degrees
        style_config: Dictionary containing styling parameters
    """
    angle_rad = np.radians(arm_angle_deg)
    
    # Draw arm centerline
    max_radius = spec.OUTER_HOLE_PCD / 2.0 * 1.1
    centerline_end = np.array([
        max_radius * np.cos(angle_rad),
        max_radius * np.sin(angle_rad)
    ])
    
    ax.plot([0, centerline_end[0]], [0, centerline_end[1]],
            color=style_config['centerline_color'],
            linewidth=style_config['centerline_linewidth'],
            linestyle='--',
            alpha=0.4)


def draw_centerlines(ax, style_config):
    """
    Draw construction centerlines for arms and major axes.
    
    Args:
        ax: Matplotlib axes object
        style_config: Dictionary containing styling parameters
    """
    overall_dims = geom.calculate_overall_dimensions()
    max_radius = overall_dims['overall_radius']
    
    # Main X centerline only (Y centerline removed per user request)
    ax.axhline(y=0, color=style_config['centerline_color'], 
               linewidth=style_config['centerline_linewidth'],
               linestyle='-.', alpha=0.5, 
               xmin=0.1, xmax=0.9)  # Don't extend to edges
    
    # Arm centerlines (exclude 90° and 270° to prevent vertical centerline)
    for angle_deg in spec.ARM_ANGLES:
        # Skip 90° and 270° angles to eliminate vertical centerline
        if angle_deg in [90, 270]:
            continue
            
        angle_rad = np.radians(angle_deg)
        x_end = max_radius * 0.8 * np.cos(angle_rad)  # 80% of max radius
        y_end = max_radius * 0.8 * np.sin(angle_rad)
        
        ax.plot([0, x_end], [0, y_end],
                color=style_config['centerline_color'],
                linewidth=style_config['centerline_linewidth'],
                linestyle='-.', alpha=0.5)


def apply_professional_styling(ax):
    """
    Apply professional gold standard styling to the axes.
    
    Args:
        ax: Matplotlib axes object
    """
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3, linewidth=0.5)
    ax.set_axisbelow(True)
    
    # Set reasonable axis limits based on overall dimensions
    overall_dims = geom.calculate_overall_dimensions()
    limit = overall_dims['overall_radius'] * 1.1  # 10% margin
    
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
