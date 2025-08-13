"""
Spooling Guide Professional Annotations - Simplified Version

This module provides basic annotation functions for the Spooling Guide,
using standard matplotlib functionality for reliable rendering.
"""

import matplotlib.pyplot as plt
import numpy as np
import sys
import os

from . import specifications as spec
from . import geometry as geom


def add_basic_dimensions(ax):
    """
    Add basic dimensional annotations.
    
    Args:
        ax: Matplotlib axes object
    """
    # Central opening radius dimension
    ax.annotate(f'R{spec.CENTRAL_OPENING_RADIUS}', 
                xy=(spec.CENTRAL_OPENING_RADIUS/2, 0),
                xytext=(spec.CENTRAL_OPENING_RADIUS/2 + 100, 50),
                arrowprops=dict(arrowstyle='->', color='black'),
                fontsize=10, fontweight='bold')
    
    # Overall diameter notation
    overall_dims = geom.calculate_overall_dimensions()
    ax.annotate(f'⌀{overall_dims["overall_diameter"]:.0f} OVERALL', 
                xy=(0, overall_dims['overall_radius']),
                xytext=(100, overall_dims['overall_radius'] + 100),
                arrowprops=dict(arrowstyle='->', color='black'),
                fontsize=12, fontweight='bold')


def add_hole_annotations(ax):
    """
    Add hole pattern annotations.
    
    Args:
        ax: Matplotlib axes object
    """
    hole_coords = geom.calculate_hole_coordinates()
    
    # Central hole annotation
    central_coord = hole_coords['central'][0]
    ax.annotate(f'⌀{spec.CENTRAL_HOLE_DIAMETER} PILOT HOLE', 
                xy=(central_coord[0], central_coord[1]),
                xytext=(80, 80),
                arrowprops=dict(arrowstyle='->', color='red'),
                fontsize=9, color='red')
    
    # Inner holes annotation (show one example)
    inner_coord = hole_coords['inner'][0]
    ax.annotate(f'{spec.INNER_HOLE_COUNT}× ⌀{spec.INNER_HOLE_DIAMETER} ON ⌀{spec.INNER_HOLE_PCD} PCD', 
                xy=(inner_coord[0], inner_coord[1]),
                xytext=(200, 200),
                arrowprops=dict(arrowstyle='->', color='blue'),
                fontsize=9, color='blue')
    
    # Outer holes annotation
    outer_coord = hole_coords['outer'][0]
    ax.annotate(f'{spec.OUTER_HOLE_COUNT}× ⌀{spec.OUTER_HOLE_DIAMETER} ON ⌀{spec.OUTER_HOLE_PCD} PCD', 
                xy=(outer_coord[0], outer_coord[1]),
                xytext=(300, 300),
                arrowprops=dict(arrowstyle='->', color='green'),
                fontsize=9, color='green')


def add_arm_annotations(ax):
    """
    Add arm geometry annotations.
    
    Args:
        ax: Matplotlib axes object
    """
    # Arm width annotations
    y_pos = spec.CENTRAL_OPENING_RADIUS + 50
    ax.annotate(f'{spec.ARM_WIDTH_INNER}mm', 
                xy=(0, y_pos),
                fontsize=9, ha='center')
    
    # Concave arc radius annotation
    ax.annotate(f'R{spec.ARM_END_ARC_RADIUS} CONCAVE ARC', 
                xy=(400, 400),
                fontsize=9, fontweight='bold', color='purple')


def add_material_notes(ax):
    """
    Add material and manufacturing notes.
    
    Args:
        ax: Matplotlib axes object
    """
    overall_dims = geom.calculate_overall_dimensions()
    note_x = -overall_dims['overall_radius'] * 0.9
    note_y = overall_dims['overall_radius'] * 0.8
    
    notes = [
        f"MATERIAL: {spec.MAIN_PLATE_MATERIAL}",
        f"OUTER RING: {spec.OUTER_RING_MATERIAL}",
        f"EDGE FINISH: {spec.EDGE_FINISH}",
        f"CORNER FILLETS: R{spec.CORNER_FILLET_RADIUS} ({spec.CORNER_FILLET_COUNT} PLACES)",
        f"CONCAVE ARC RADIUS: R{spec.ARM_END_ARC_RADIUS}",
        f"TOTAL HOLES: {1 + spec.INNER_HOLE_COUNT + spec.OUTER_HOLE_COUNT}"
    ]
    
    notes_text = '\n'.join(notes)
    ax.text(note_x, note_y, f"MANUFACTURING NOTES:\n{notes_text}",
            fontsize=8,
            bbox=dict(boxstyle="round,pad=0.5", 
                     facecolor='lightblue', 
                     edgecolor='black',
                     alpha=0.9),
            verticalalignment='top')


def add_title_block(ax):
    """
    Add title block with drawing information.
    
    Args:
        ax: Matplotlib axes object
    """
    overall_dims = geom.calculate_overall_dimensions()
    title_x = -overall_dims['overall_radius'] * 0.9
    title_y = -overall_dims['overall_radius'] * 0.9
    
    ax.text(title_x, title_y, 
            f"{spec.DRAWING_TITLE}\n{spec.DRAWING_VIEW_NAME}\nScale: {spec.DRAWING_SCALE}",
            fontsize=14, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.5", 
                     facecolor='white', 
                     edgecolor='black'))


def create_simple_legend(ax):
    """
    Create a simple legend for the drawing.
    
    Args:
        ax: Matplotlib axes object
    """
    legend_elements = [
        plt.Line2D([0], [0], color='black', linewidth=2, label='Main Plate'),
        plt.Line2D([0], [0], color='red', marker='o', linewidth=0, markersize=8, label='Holes'),
        plt.Line2D([0], [0], color='blue', linewidth=2, linestyle='--', label='Outer Ring'),
        plt.Line2D([0], [0], color='green', linewidth=1, linestyle=':', label='PCD References'),
        plt.Line2D([0], [0], color='gray', linewidth=1, linestyle='-.', label='Centerlines')
    ]
    
    ax.legend(handles=legend_elements, 
              loc='upper left',
              fontsize=9,
              title='COMPONENTS',
              title_fontsize=10)


def add_all_annotations(ax, style_config):
    """
    Add all annotations to the spooling guide drawing.
    
    Args:
        ax: Matplotlib axes object
        style_config: Dictionary containing styling parameters (not used in simplified version)
    """
    add_basic_dimensions(ax)
    add_hole_annotations(ax)
    add_arm_annotations(ax)
    add_material_notes(ax)
    add_title_block(ax)
    create_simple_legend(ax)
