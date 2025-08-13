"""
Spooling Guide Professional Annotations - Simplified Version

This module provides basic annotation functions for the Spooling Guide,
using standard matplotlib functionality for reliable rendering.
"""

import matplotlib.pyplot as plt
import numpy as np
import math
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
    # Central opening radius dimension - CORRECTED to point to actual edge
    ax.annotate(f'R{spec.CENTRAL_OPENING_RADIUS}', 
                xy=(spec.CENTRAL_OPENING_RADIUS, 0),  # FIXED: Point to (250, 0) actual edge
                xytext=(spec.CENTRAL_OPENING_RADIUS + 100, 50),
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
    
    # Central hole annotation - ARROW POINTS TO CROSSHAIR CENTER
    central_coord = hole_coords['central'][0]  # This is (0, 0)
    ax.annotate(f'⌀{spec.CENTRAL_HOLE_DIAMETER} PILOT HOLE', 
                xy=(0, 0),  # Point directly at the crosshair center
                xytext=(100, -45),  # Position text away from center for clarity (moved y -20)
                arrowprops=dict(arrowstyle='->', color='yellow', lw=1.5),
                fontsize=10, color='yellow', fontweight='bold',
                ha='left', va='bottom')
    
    # Inner holes annotation (show one example)
    inner_coord = hole_coords['inner'][0]
    ax.annotate(f'{spec.INNER_HOLE_COUNT}× ⌀{spec.INNER_HOLE_DIAMETER} ON ⌀{spec.INNER_HOLE_PCD} PCD', 
                xy=(inner_coord[0], inner_coord[1]),
                xytext=(80, 40),
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
    Add arm geometry annotations with proper dimensioning.
    
    Args:
        ax: Matplotlib axes object
    """
    # Inner arm width dimension at central opening (more specific)
    ax.annotate(f'{spec.ARM_WIDTH_INNER}mm WIDTH @ R{spec.ARM_INNER_RADIUS}', 
                xy=(spec.ARM_INNER_RADIUS, spec.ARM_WIDTH_INNER/4),  # Point to arm edge
                xytext=(spec.ARM_INNER_RADIUS + 80, spec.ARM_WIDTH_INNER + 50),
                arrowprops=dict(arrowstyle='->', color='black'),
                fontsize=9, ha='left')
    
    # Outer arm width at outer radius
    ax.annotate(f'{spec.ARM_WIDTH_OUTER}mm WIDTH @ R{spec.ARM_OUTER_RADIUS}', 
                xy=(spec.ARM_OUTER_RADIUS, spec.ARM_WIDTH_OUTER/4),  # Point to arm edge
                xytext=(spec.ARM_OUTER_RADIUS - 150, spec.ARM_WIDTH_OUTER + 30),
                arrowprops=dict(arrowstyle='->', color='black'),
                fontsize=9, ha='left')
    
    # Concave arc radius annotation (kept as reference)
    ax.annotate(f'R{spec.ARM_END_ARC_RADIUS} CONCAVE ARC (LEGACY)', 
                xy=(400, 400),
                fontsize=8, fontweight='bold', color='purple', alpha=0.6)


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
        f"EFNI (MATERIAL): {spec.MAIN_PLATE_MATERIAL}",
        f"YTRI HRINGUR (OUTER RING): {spec.OUTER_RING_MATERIAL}",
        f"FRÁGANGUR (FINISH): {spec.EDGE_FINISH}",
        f"HORNAFLETIR (CORNER FILLETS): R{spec.CORNER_FILLET_RADIUS} ({spec.CORNER_FILLET_COUNT} STAÐIR)",
        f"INNÍ BOGRÁDIUS (CONCAVE ARC): R{spec.ARM_END_ARC_RADIUS}",
        f"HEILDARFJÖLDI GATA (TOTAL HOLES): {1 + spec.INNER_HOLE_COUNT + spec.OUTER_HOLE_COUNT}"
    ]
    
    notes_text = '\n'.join(notes)
    ax.text(note_x, note_y, f"FRAMLEIÐSLUUPPLÝSINGAR (MANUFACTURING NOTES):\n{notes_text}",
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
        plt.Line2D([0], [0], color='black', linewidth=2, label='Aðalplata (Main Plate)'),
        plt.Line2D([0], [0], color='red', marker='o', linewidth=0, markersize=8, label='Göt (Holes)'),
        plt.Line2D([0], [0], color='blue', linewidth=2, linestyle='--', label='Ytri hringur (Outer Ring)'),
        plt.Line2D([0], [0], color='green', linewidth=1, linestyle=':', label='PCD tilvísanir'),
        plt.Line2D([0], [0], color='gray', linewidth=1, linestyle='-.', label='Miðlínur (Centerlines)')
    ]
    
    ax.legend(handles=legend_elements, 
              loc='upper left',
              fontsize=9,
              title='HLUÚTAR (COMPONENTS)',
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
