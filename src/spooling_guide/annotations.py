"""
Spooling Guide Professional Annotations

This module provides professional annotation functions specific to the Spooling Guide,
building upon the shared utilities in the top-level drawing_utils.py module.

Features:
- Multi-level dimensioning (primary and secondary)
- Coordinate labeling for hole positions
- Material callouts with leader lines
- Manufacturing notes and assembly details
- Professional legends and technical documentation
"""

import matplotlib.pyplot as plt
import numpy as np
import sys
import os

# Import shared utilities from top-level drawing_utils.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from drawing_utils import (
    add_primary_dimension, add_secondary_dimension, add_coordinate_label,
    add_material_callout, add_manufacturing_detail, create_professional_legend,
    add_leader_line, save_drawing_files
)

from . import specifications as spec
from . import geometry as geom


def add_radial_dimensions(ax, style_config):
    """
    Add primary radial dimensions for key features.
    
    Args:
        ax: Matplotlib axes object
        style_config: Dictionary containing styling parameters
    """
    # Central opening radius dimension
    add_primary_dimension(ax, 
                         start_point=(0, 0),
                         end_point=(spec.CENTRAL_OPENING_RADIUS, 0),
                         dimension_text=f"R{spec.CENTRAL_OPENING_RADIUS}",
                         offset_distance=50,
                         style_config=style_config)
    
    # Outer ring center radius
    outer_radius = spec.OUTER_HOLE_PCD / 2.0
    add_primary_dimension(ax,
                         start_point=(0, 0), 
                         end_point=(outer_radius, 0),
                         dimension_text=f"R{outer_radius}",
                         offset_distance=-80,
                         style_config=style_config)


def add_arm_dimensions(ax, style_config):
    """
    Add dimensions specific to arm geometry.
    
    Args:
        ax: Matplotlib axes object
        style_config: Dictionary containing styling parameters
    """
    # Arm width at inner edge
    y_pos = spec.CENTRAL_OPENING_RADIUS + 30
    add_secondary_dimension(ax,
                           start_point=(-spec.ARM_WIDTH_INNER/2, y_pos),
                           end_point=(spec.ARM_WIDTH_INNER/2, y_pos),
                           dimension_text=f"{spec.ARM_WIDTH_INNER}",
                           offset_distance=20,
                           style_config=style_config)
    
    # Arm width at outer edge (approximate position)
    outer_y = spec.OUTER_HOLE_PCD / 2.0
    add_secondary_dimension(ax,
                           start_point=(-spec.ARM_WIDTH_OUTER/2, outer_y),
                           end_point=(spec.ARM_WIDTH_OUTER/2, outer_y),
                           dimension_text=f"{spec.ARM_WIDTH_OUTER}",
                           offset_distance=30,
                           style_config=style_config)


def add_hole_coordinates(ax, style_config):
    """
    Add coordinate labels for all hole positions.
    
    Args:
        ax: Matplotlib axes object
        style_config: Dictionary containing styling parameters
    """
    hole_coords = geom.calculate_hole_coordinates()
    
    # Central hole coordinate
    central_coord = hole_coords['central'][0]
    add_coordinate_label(ax, central_coord[0], central_coord[1], 
                        f"({central_coord[0]:.0f}, {central_coord[1]:.0f})",
                        style_config)
    
    # Inner hole coordinates (show first 4 to avoid clutter)
    for i, coord in enumerate(hole_coords['inner'][:4]):
        add_coordinate_label(ax, coord[0], coord[1],
                           f"({coord[0]:.0f}, {coord[1]:.0f})",
                           style_config)
    
    # Outer hole coordinates
    for coord in hole_coords['outer']:
        add_coordinate_label(ax, coord[0], coord[1],
                           f"({coord[0]:.0f}, {coord[1]:.0f})",
                           style_config)


def add_pcd_annotations(ax, style_config):
    """
    Add pitch circle diameter annotations.
    
    Args:
        ax: Matplotlib axes object
        style_config: Dictionary containing styling parameters
    """
    # Inner PCD annotation
    inner_pcd_radius = spec.INNER_HOLE_PCD / 2.0
    ax.annotate(f'PCD {spec.INNER_HOLE_PCD}', 
                xy=(inner_pcd_radius * 0.7, inner_pcd_radius * 0.7),
                xytext=(inner_pcd_radius * 0.7 + 50, inner_pcd_radius * 0.7 + 50),
                arrowprops=dict(arrowstyle='->', color=style_config['pcd_color']),
                fontsize=style_config['secondary_font_size'],
                color=style_config['pcd_color'])
    
    # Outer PCD annotation  
    outer_pcd_radius = spec.OUTER_HOLE_PCD / 2.0
    ax.annotate(f'PCD {spec.OUTER_HOLE_PCD}',
                xy=(outer_pcd_radius * 0.7, outer_pcd_radius * 0.7), 
                xytext=(outer_pcd_radius * 0.7 + 80, outer_pcd_radius * 0.7 + 80),
                arrowprops=dict(arrowstyle='->', color=style_config['pcd_color']),
                fontsize=style_config['secondary_font_size'],
                color=style_config['pcd_color'])


def add_material_callouts(ax, style_config):
    """
    Add material specification callouts with leader lines.
    
    Args:
        ax: Matplotlib axes object
        style_config: Dictionary containing styling parameters
    """
    # Main plate material callout
    add_material_callout(ax, 
                        position=(100, 100),
                        material_text=spec.MAIN_PLATE_MATERIAL,
                        leader_target=(0, 0),
                        style_config=style_config)
    
    # Outer ring material callout
    ring_position = (spec.OUTER_HOLE_PCD / 2.0, 0)
    add_material_callout(ax,
                        position=(ring_position[0] + 100, ring_position[1] + 100), 
                        material_text=spec.OUTER_RING_MATERIAL,
                        leader_target=ring_position,
                        style_config=style_config)


def add_manufacturing_notes(ax, style_config):
    """
    Add manufacturing and assembly notes.
    
    Args:
        ax: Matplotlib axes object
        style_config: Dictionary containing styling parameters
    """
    overall_dims = geom.calculate_overall_dimensions()
    note_x = -overall_dims['overall_radius'] * 0.9
    note_y = overall_dims['overall_radius'] * 0.7
    
    manufacturing_notes = [
        f"• {spec.EDGE_FINISH}",
        f"• Corner fillets: R{spec.CORNER_FILLET_RADIUS} ({spec.CORNER_FILLET_COUNT} places)",
        f"• {spec.OUTER_RING_WELD_TYPE}",
        f"• {spec.RING_CENTERING_NOTE}",
        f"• Material: {spec.MAIN_PLATE_MATERIAL}",
        f"• Ring: {spec.OUTER_RING_MATERIAL}"
    ]
    
    # Create manufacturing notes box
    notes_text = '\n'.join(manufacturing_notes)
    ax.text(note_x, note_y, "MANUFACTURING NOTES:\n" + notes_text,
            fontsize=style_config['notes_font_size'],
            bbox=dict(boxstyle="round,pad=0.5", 
                     facecolor='white', 
                     edgecolor=style_config['notes_color'],
                     alpha=0.9),
            verticalalignment='top')


def add_hole_pattern_details(ax, style_config):
    """
    Add detailed hole pattern specifications.
    
    Args:
        ax: Matplotlib axes object
        style_config: Dictionary containing styling parameters
    """
    overall_dims = geom.calculate_overall_dimensions()
    detail_x = overall_dims['overall_radius'] * 0.6
    detail_y = overall_dims['overall_radius'] * 0.8
    
    hole_details = [
        f"HOLE PATTERNS:",
        f"• Central: 1× ⌀{spec.CENTRAL_HOLE_DIAMETER}mm at center",
        f"• Inner: {spec.INNER_HOLE_COUNT}× ⌀{spec.INNER_HOLE_DIAMETER}mm on {spec.INNER_HOLE_PCD}mm PCD",
        f"• Outer: {spec.OUTER_HOLE_COUNT}× ⌀{spec.OUTER_HOLE_DIAMETER}mm on {spec.OUTER_HOLE_PCD}mm PCD",
        f"• Total holes: {1 + spec.INNER_HOLE_COUNT + spec.OUTER_HOLE_COUNT}"
    ]
    
    details_text = '\n'.join(hole_details)
    ax.text(detail_x, detail_y, details_text,
            fontsize=style_config['notes_font_size'],
            bbox=dict(boxstyle="round,pad=0.5",
                     facecolor='lightblue',
                     edgecolor=style_config['hole_color'], 
                     alpha=0.8),
            verticalalignment='top')


def add_angular_dimensions(ax, style_config):
    """
    Add angular dimensions for arm positioning.
    
    Args:
        ax: Matplotlib axes object
        style_config: Dictionary containing styling parameters
    """
    # Show 90° spacing between arms
    radius_for_arc = spec.CENTRAL_OPENING_RADIUS * 1.3
    
    # Draw angular dimension arc
    arc_angles = np.linspace(0, np.pi/2, 20)  # 0° to 90°
    arc_x = radius_for_arc * np.cos(arc_angles)
    arc_y = radius_for_arc * np.sin(arc_angles)
    
    ax.plot(arc_x, arc_y, 
            color=style_config['dimension_color'],
            linewidth=style_config['dimension_linewidth'])
    
    # Add dimension text
    mid_angle = np.pi / 4  # 45°
    text_x = radius_for_arc * 1.1 * np.cos(mid_angle)
    text_y = radius_for_arc * 1.1 * np.sin(mid_angle)
    
    ax.text(text_x, text_y, "90°",
            fontsize=style_config['primary_font_size'],
            ha='center', va='center',
            color=style_config['dimension_color'],
            weight='bold')


def create_spooling_guide_legend(ax, style_config):
    """
    Create a comprehensive legend specific to the spooling guide.
    
    Args:
        ax: Matplotlib axes object
        style_config: Dictionary containing styling parameters
    """
    legend_elements = [
        ('Main Plate Outline', style_config['primary_color'], '-'),
        ('Central Opening', style_config['primary_color'], '-'), 
        ('Holes', style_config['hole_color'], 'o'),
        ('Outer Ring', style_config['ring_color'], '--'),
        ('PCD References', style_config['pcd_color'], ':'),
        ('Centerlines', style_config['centerline_color'], '-.'),
        ('Dimensions', style_config['dimension_color'], '-')
    ]
    
    create_professional_legend(ax, legend_elements, 
                              title="SPOOLING GUIDE COMPONENTS",
                              style_config=style_config)


def add_title_block(ax, style_config):
    """
    Add professional title block with drawing information.
    
    Args:
        ax: Matplotlib axes object
        style_config: Dictionary containing styling parameters
    """
    overall_dims = geom.calculate_overall_dimensions()
    title_x = -overall_dims['overall_radius'] * 0.9
    title_y = -overall_dims['overall_radius'] * 0.9
    
    title_info = [
        f"{spec.DRAWING_TITLE}",
        f"{spec.DRAWING_VIEW_NAME}",
        f"Scale: {spec.DRAWING_SCALE}",
        f"Material: {spec.MAIN_PLATE_MATERIAL}"
    ]
    
    for i, line in enumerate(title_info):
        font_size = style_config['title_font_size'] if i == 0 else style_config['subtitle_font_size']
        weight = 'bold' if i == 0 else 'normal'
        
        ax.text(title_x, title_y - (i * 25), line,
                fontsize=font_size,
                weight=weight,
                color=style_config['title_color'])


def add_all_annotations(ax, style_config):
    """
    Add all professional annotations to the spooling guide drawing.
    
    Args:
        ax: Matplotlib axes object
        style_config: Dictionary containing styling parameters
    """
    add_radial_dimensions(ax, style_config)
    add_arm_dimensions(ax, style_config)
    add_hole_coordinates(ax, style_config)
    add_pcd_annotations(ax, style_config)
    add_material_callouts(ax, style_config)
    add_manufacturing_notes(ax, style_config)
    add_hole_pattern_details(ax, style_config)
    add_angular_dimensions(ax, style_config)
    create_spooling_guide_legend(ax, style_config)
    add_title_block(ax, style_config)
