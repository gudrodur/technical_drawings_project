"""
Drawing Engine - Gold Standard Implementation
============================================

Enhanced high-level drawing functions for generating professional technical drawing sets.
Each function corresponds to one component and generates all required views with
gold standard quality and comprehensive annotations.

All dimensional data is imported from the specifications package to maintain
the Single Source of Truth (SSOT) principle.
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from specifications import mounting_bracket as mb_specs
from src.drawing_utils import DrawingUtils


class DrawingEngine:
    """Enhanced drawing engine for generating professional technical drawings."""
    
    def __init__(self):
        """Initialize the drawing engine with professional utilities."""
        self.utils = DrawingUtils()
        self.output_base_path = project_root / "drawings"
        self.dpi = 300  # High DPI for technical drawings
    
    def draw_mounting_bracket(self):
        """
        Generate complete professional drawing set for mounting bracket.
        Creates: Side View, Top View, and Front View with gold standard quality.
        """
        print("Generating professional mounting bracket drawings...")
        
        # Generate all three views with enhanced features
        self._draw_mounting_bracket_side_view()
        self._draw_mounting_bracket_top_view()
        self._draw_mounting_bracket_front_view()
        
        print("✓ All mounting bracket views generated with professional quality")
    
    def _draw_mounting_bracket_side_view(self):
        """Generate enhanced side view of mounting bracket (U-arm profile)."""
        fig, ax = plt.subplots(1, 1, figsize=(14, 12), dpi=100)
        
        # === DRAW BASE PLATE EDGE ===
        ax.plot([-mb_specs.BASE_PLATE_WIDTH/2, mb_specs.BASE_PLATE_WIDTH/2], [0, 0], 
                color=self.utils.style.COLORS['primary_lines'], 
                linewidth=self.utils.style.LINE_WEIGHTS['main_outline'], 
                label='Base Plate Edge')
        
        # === DRAW BASE PLATE HOLES (projected) ===
        for x_pos, y_pos in mb_specs.BASE_PLATE_HOLE_POSITIONS:
            circle = plt.Circle((x_pos, 2), mb_specs.BASE_PLATE_HOLE_DIAMETER/2, 
                              fill=False, color=self.utils.style.COLORS['holes_base'], 
                              linewidth=self.utils.style.LINE_WEIGHTS['hole_outlines'])
            ax.add_patch(circle)
        
        # === DRAW U-ARM PROFILE ===
        # Outer vertical sides
        ax.plot([mb_specs.U_ARM_LEFT_OUTER, mb_specs.U_ARM_LEFT_OUTER], 
                [0, mb_specs.U_ARM_STRAIGHT_HEIGHT], 
                color=self.utils.style.COLORS['primary_lines'], 
                linewidth=self.utils.style.LINE_WEIGHTS['feature_lines'])
        ax.plot([mb_specs.U_ARM_RIGHT_OUTER, mb_specs.U_ARM_RIGHT_OUTER], 
                [0, mb_specs.U_ARM_STRAIGHT_HEIGHT], 
                color=self.utils.style.COLORS['primary_lines'], 
                linewidth=self.utils.style.LINE_WEIGHTS['feature_lines'])
        
        # Inner vertical sides
        ax.plot([mb_specs.U_ARM_LEFT_INNER, mb_specs.U_ARM_LEFT_INNER], 
                [0, mb_specs.U_ARM_STRAIGHT_HEIGHT], 
                color=self.utils.style.COLORS['primary_lines'], 
                linewidth=self.utils.style.LINE_WEIGHTS['feature_lines'])
        ax.plot([mb_specs.U_ARM_RIGHT_INNER, mb_specs.U_ARM_RIGHT_INNER], 
                [0, mb_specs.U_ARM_STRAIGHT_HEIGHT], 
                color=self.utils.style.COLORS['primary_lines'], 
                linewidth=self.utils.style.LINE_WEIGHTS['feature_lines'])
        
        # Bottom connections
        ax.plot([mb_specs.U_ARM_LEFT_OUTER, mb_specs.U_ARM_LEFT_INNER], [0, 0], 
                color=self.utils.style.COLORS['primary_lines'], 
                linewidth=self.utils.style.LINE_WEIGHTS['feature_lines'])
        ax.plot([mb_specs.U_ARM_RIGHT_INNER, mb_specs.U_ARM_RIGHT_OUTER], [0, 0], 
                color=self.utils.style.COLORS['primary_lines'], 
                linewidth=self.utils.style.LINE_WEIGHTS['feature_lines'])
        
        # === DRAW SEMICIRCULAR TOP ===
        theta = np.linspace(0, np.pi, 100)
        
        # Outer semicircle
        outer_x = mb_specs.U_ARM_PCD_CENTER_X + mb_specs.U_ARM_SEMICIRCLE_RADIUS * np.cos(theta)
        outer_z = mb_specs.U_ARM_PCD_CENTER_Z + mb_specs.U_ARM_SEMICIRCLE_RADIUS * np.sin(theta)
        ax.plot(outer_x, outer_z, color=self.utils.style.COLORS['primary_lines'], 
                linewidth=self.utils.style.LINE_WEIGHTS['feature_lines'])
        
        # Inner semicircle
        inner_x = mb_specs.U_ARM_PCD_CENTER_X + mb_specs.U_ARM_INNER_RADIUS * np.cos(theta)
        inner_z = mb_specs.U_ARM_PCD_CENTER_Z + mb_specs.U_ARM_INNER_RADIUS * np.sin(theta)
        ax.plot(inner_x, inner_z, color=self.utils.style.COLORS['primary_lines'], 
                linewidth=self.utils.style.LINE_WEIGHTS['feature_lines'])
        
        # === DRAW 8 HOLES ON PCD WITH ENHANCED ANNOTATIONS ===
        for angle_deg in mb_specs.U_ARM_HOLE_ANGLES:
            angle_rad = np.radians(angle_deg)
            hole_x = mb_specs.U_ARM_PCD_CENTER_X + mb_specs.U_ARM_PCD_RADIUS * np.cos(angle_rad)
            hole_z = mb_specs.U_ARM_PCD_CENTER_Z + mb_specs.U_ARM_PCD_RADIUS * np.sin(angle_rad)
            
            circle = plt.Circle((hole_x, hole_z), mb_specs.U_ARM_HOLE_DIAMETER/2, 
                              fill=False, color=self.utils.style.COLORS['holes_pcd'], 
                              linewidth=self.utils.style.LINE_WEIGHTS['hole_outlines'])
            ax.add_patch(circle)
        
        # === ADD PCD VISUALIZATION ===
        self.utils.add_pcd_visualization(ax, mb_specs.U_ARM_PCD_CENTER_X, mb_specs.U_ARM_PCD_CENTER_Z, 
                                       mb_specs.U_ARM_PCD_RADIUS, 'PCD 90')
        
        # === DRAW CENTER MILLED SLOT ===
        self.utils.draw_milled_slot(ax, mb_specs.CENTER_SLOT_CENTER_X, mb_specs.CENTER_SLOT_CENTER_Z,
                                   mb_specs.CENTER_SLOT_OVERALL_DIAMETER, mb_specs.CENTER_SLOT_FLAT_WIDTH)
        
        # === PROFESSIONAL DIMENSIONS ===
        # Primary dimensions
        self.utils.add_primary_dimension(ax, (-75, 0), (-75, mb_specs.U_ARM_OVERALL_HEIGHT), '200', vertical=True)
        self.utils.add_primary_dimension(ax, (-60, -15), (60, -15), '120')
        
        # === PROFESSIONAL LEGEND ===
        legend_items = [
            {'type': 'line', 'color': self.utils.style.COLORS['primary_lines'], 
             'linewidth': self.utils.style.LINE_WEIGHTS['feature_lines'], 'label': 'U-Arm Profile'},
            {'type': 'line', 'color': self.utils.style.COLORS['primary_lines'], 
             'linewidth': self.utils.style.LINE_WEIGHTS['main_outline'], 'label': 'Base Plate Edge'},
            {'type': 'line', 'color': self.utils.style.COLORS['holes_pcd'], 
             'linewidth': self.utils.style.LINE_WEIGHTS['hole_outlines'], 'label': '⌀8 Holes (8x on PCD)'},
            {'type': 'line', 'color': self.utils.style.COLORS['holes_base'], 
             'linewidth': self.utils.style.LINE_WEIGHTS['hole_outlines'], 'label': '⌀8 Holes (6x Base)'},
            {'type': 'line', 'color': self.utils.style.COLORS['slot_lines'], 
             'linewidth': self.utils.style.LINE_WEIGHTS['feature_lines'], 'label': 'Center Slot'}
        ]
        self.utils.create_professional_legend(ax, legend_items)
        
        # === DRAWING SETUP ===
        title_with_scale = self.utils.add_scale_to_title('MOUNTING BRACKET - SIDE VIEW\n4mm Stainless Steel', '1:2')
        self.utils.format_professional_layout(ax, title_with_scale, (-90, 90), (-30, 220), 'X (mm)', 'Z (mm)')
        
        # === COMPREHENSIVE TECHNICAL NOTES ===
        manufacturing_details = [
            'U-arm welded to base plate',
            'Origin at plate center'
        ]
        self.utils.add_comprehensive_notes(ax, mb_specs.MATERIAL, (-75, 180), manufacturing_details)
        
        plt.tight_layout()
        self._save_drawing(fig, 'mounting_bracket_side_view')
        plt.close()
    
    def _draw_mounting_bracket_top_view(self):
        """Generate enhanced top view of mounting bracket (base plate)."""
        fig, ax = plt.subplots(1, 1, figsize=(12, 12), dpi=100)
        
        # === DRAW BASE PLATE OUTLINE ===
        base_corners = [
            (mb_specs.BASE_PLATE_LEFT, mb_specs.BASE_PLATE_FRONT),
            (mb_specs.BASE_PLATE_RIGHT, mb_specs.BASE_PLATE_FRONT),
            (mb_specs.BASE_PLATE_RIGHT, mb_specs.BASE_PLATE_BACK),
            (mb_specs.BASE_PLATE_LEFT, mb_specs.BASE_PLATE_BACK),
            (mb_specs.BASE_PLATE_LEFT, mb_specs.BASE_PLATE_FRONT)
        ]
        
        base_x = [corner[0] for corner in base_corners]
        base_y = [corner[1] for corner in base_corners]
        ax.plot(base_x, base_y, color=self.utils.style.COLORS['primary_lines'], 
                linewidth=self.utils.style.LINE_WEIGHTS['main_outline'], 
                label='Base Plate Edge')
        
        # === DRAW U-ARM ATTACHMENT AREA ===
        attach_corners = [
            (mb_specs.BASE_PLATE_LEFT, mb_specs.BASE_PLATE_BACK),
            (mb_specs.BASE_PLATE_RIGHT, mb_specs.BASE_PLATE_BACK),
            (mb_specs.BASE_PLATE_RIGHT, mb_specs.BASE_PLATE_BACK - mb_specs.U_ARM_WALL_THICKNESS),
            (mb_specs.BASE_PLATE_LEFT, mb_specs.BASE_PLATE_BACK - mb_specs.U_ARM_WALL_THICKNESS),
            (mb_specs.BASE_PLATE_LEFT, mb_specs.BASE_PLATE_BACK)
        ]
        
        attach_x = [corner[0] for corner in attach_corners]
        attach_y = [corner[1] for corner in attach_corners]
        ax.fill(attach_x, attach_y, color=self.utils.style.COLORS['attachment_zones'], 
                alpha=self.utils.style.ALPHA['attachment_zones'], label='U-Arm Attachment Zone')
        ax.plot(attach_x, attach_y, color=self.utils.style.COLORS['secondary_dims'], 
                linewidth=self.utils.style.LINE_WEIGHTS['feature_lines'])
        
        # === DRAW MOUNTING HOLES WITH COORDINATE LABELS ===
        for x_pos, y_pos in mb_specs.BASE_PLATE_HOLE_POSITIONS:
            circle = plt.Circle((x_pos, y_pos), mb_specs.BASE_PLATE_HOLE_DIAMETER/2, 
                              fill=False, color=self.utils.style.COLORS['holes_pcd'], 
                              linewidth=self.utils.style.LINE_WEIGHTS['feature_lines'])
            ax.add_patch(circle)
            
            # Add hole diameter label
            ax.text(x_pos, y_pos, f'⌀{mb_specs.BASE_PLATE_HOLE_DIAMETER}', 
                   ha='center', va='center', 
                   fontsize=self.utils.style.FONT_SIZES['coordinate_labels'], 
                   color=self.utils.style.COLORS['holes_pcd'], fontweight='bold')
            
            # Add coordinate label
            coord_label = f'({x_pos:+d}, {y_pos:+d})'
            self.utils.add_coordinate_label(ax, (x_pos, y_pos), coord_label)
        
        # === PRIMARY DIMENSIONS ===
        self.utils.add_primary_dimension(ax, (-60, 70), (60, 70), '120')
        self.utils.add_primary_dimension(ax, (70, -60), (70, 60), '120', vertical=True)
        
        # === SECONDARY DIMENSIONS (HOLE SPACING) ===
        # Row spacing
        self.utils.add_secondary_dimension(ax, (-50, -30), (-50, 30), '60', vertical=True)
        
        # Column spacing
        self.utils.add_secondary_dimension(ax, (-40, -45), (0, -45), '40')
        self.utils.add_secondary_dimension(ax, (0, -45), (40, -45), '40')
        
        # === ADD REFERENCE GRID ===
        x_positions = [-40, 0, 40]
        y_positions = [-30, 30]
        self.utils.add_reference_grid(ax, x_positions, y_positions, (-50, 50), (-40, 40))
        
        # === ADD PROFESSIONAL CENTERLINES ===
        self.utils.add_professional_centerlines(ax, 0, 0, 140)
        
        # === PROFESSIONAL LEGEND ===
        legend_items = [
            {'type': 'line', 'color': self.utils.style.COLORS['primary_lines'], 
             'linewidth': self.utils.style.LINE_WEIGHTS['main_outline'], 'label': 'Base Plate Edge'},
            {'type': 'line', 'color': self.utils.style.COLORS['secondary_dims'], 
             'linewidth': self.utils.style.LINE_WEIGHTS['feature_lines'], 'label': 'U-Arm Attachment'},
            {'type': 'line', 'color': self.utils.style.COLORS['holes_pcd'], 
             'linewidth': self.utils.style.LINE_WEIGHTS['feature_lines'], 'label': '⌀8 Mounting Holes (6x)'},
            {'type': 'line', 'color': self.utils.style.COLORS['centerlines'], 
             'linewidth': self.utils.style.LINE_WEIGHTS['centerlines'], 'linestyle': '--', 'label': 'Centerlines'},
            {'type': 'line', 'color': self.utils.style.COLORS['reference_grid'], 
             'linewidth': self.utils.style.LINE_WEIGHTS['reference_grid'], 'linestyle': '--', 'label': 'Reference Grid'}
        ]
        self.utils.create_professional_legend(ax, legend_items, position='upper left', bbox_to_anchor=(0, 1))
        
        # === DRAWING SETUP ===
        title_with_scale = self.utils.add_scale_to_title('MOUNTING BRACKET - TOP VIEW (BASE PLATE)\n4mm Stainless Steel', '1:1')
        self.utils.format_professional_layout(ax, title_with_scale, (-90, 90), (-90, 90))
        
        # === COMPREHENSIVE TECHNICAL NOTES ===
        manufacturing_details = [
            'Origin at plate center',
            '6x ⌀8mm mounting holes',
            'U-arm welded to back edge'
        ]
        self.utils.add_comprehensive_notes(ax, mb_specs.MATERIAL, (60, -75), manufacturing_details)
        
        plt.tight_layout()
        self._save_drawing(fig, 'mounting_bracket_top_view')
        plt.close()
    
    def _draw_mounting_bracket_front_view(self):
        """Generate enhanced front view of mounting bracket (L-profile)."""
        fig, ax = plt.subplots(1, 1, figsize=(12, 10), dpi=100)
        
        # === DRAW BASE PLATE PROFILE ===
        base_corners = [
            (mb_specs.BASE_PLATE_LEFT, -mb_specs.BASE_PLATE_THICKNESS),
            (mb_specs.BASE_PLATE_RIGHT, -mb_specs.BASE_PLATE_THICKNESS),
            (mb_specs.BASE_PLATE_RIGHT, 0),
            (mb_specs.BASE_PLATE_LEFT, 0),
            (mb_specs.BASE_PLATE_LEFT, -mb_specs.BASE_PLATE_THICKNESS)
        ]
        
        base_x = [corner[0] for corner in base_corners]
        base_y = [corner[1] for corner in base_corners]
        ax.fill(base_x, base_y, color=self.utils.style.COLORS['base_plate_fill'], 
                alpha=self.utils.style.ALPHA['fills'], label='Base Plate')
        ax.plot(base_x, base_y, color=self.utils.style.COLORS['primary_lines'], 
                linewidth=self.utils.style.LINE_WEIGHTS['feature_lines'])
        
        # === DRAW U-ARM PROFILE ===
        u_arm_corners = [
            (mb_specs.BASE_PLATE_RIGHT - mb_specs.U_ARM_WALL_THICKNESS, 0),
            (mb_specs.BASE_PLATE_RIGHT, 0),
            (mb_specs.BASE_PLATE_RIGHT, mb_specs.U_ARM_OVERALL_HEIGHT),
            (mb_specs.BASE_PLATE_RIGHT - mb_specs.U_ARM_WALL_THICKNESS, mb_specs.U_ARM_OVERALL_HEIGHT),
            (mb_specs.BASE_PLATE_RIGHT - mb_specs.U_ARM_WALL_THICKNESS, 0)
        ]
        
        u_arm_x = [corner[0] for corner in u_arm_corners]
        u_arm_y = [corner[1] for corner in u_arm_corners]
        ax.fill(u_arm_x, u_arm_y, color=self.utils.style.COLORS['u_arm_fill'], 
                alpha=self.utils.style.ALPHA['fills'], label='U-Arm')
        ax.plot(u_arm_x, u_arm_y, color=self.utils.style.COLORS['primary_lines'], 
                linewidth=self.utils.style.LINE_WEIGHTS['feature_lines'])
        
        # === ADD WELD INDICATION ===
        self.utils.draw_weld_symbol(ax, (mb_specs.BASE_PLATE_RIGHT - mb_specs.U_ARM_WALL_THICKNESS, 0))
        
        # === PRIMARY DIMENSIONS ===
        self.utils.add_primary_dimension(ax, (mb_specs.BASE_PLATE_LEFT, -15), (mb_specs.BASE_PLATE_RIGHT, -15), '120')
        self.utils.add_primary_dimension(ax, (-75, -mb_specs.BASE_PLATE_THICKNESS), (-75, mb_specs.U_ARM_OVERALL_HEIGHT), '200', vertical=True)
        
        # === SECONDARY DIMENSIONS (THICKNESS) ===
        self.utils.add_secondary_dimension(ax, (mb_specs.BASE_PLATE_RIGHT + 10, -mb_specs.BASE_PLATE_THICKNESS), 
                                         (mb_specs.BASE_PLATE_RIGHT + 10, 0), '4', vertical=True)
        self.utils.add_secondary_dimension(ax, (mb_specs.BASE_PLATE_RIGHT - mb_specs.U_ARM_WALL_THICKNESS, mb_specs.U_ARM_OVERALL_HEIGHT + 10), 
                                         (mb_specs.BASE_PLATE_RIGHT, mb_specs.U_ARM_OVERALL_HEIGHT + 10), '4')
        
        # === ADD CENTERLINES ===
        # Base plate centerline
        ax.plot([mb_specs.BASE_PLATE_LEFT - 10, mb_specs.BASE_PLATE_RIGHT + 10], [0, 0], 
                color=self.utils.style.COLORS['centerlines'], linestyle='--', 
                linewidth=self.utils.style.LINE_WEIGHTS['centerlines'], 
                alpha=self.utils.style.ALPHA['centerlines'], label='Centerlines')
        
        # U-arm centerline
        ax.plot([mb_specs.BASE_PLATE_RIGHT - mb_specs.U_ARM_WALL_THICKNESS - 10, mb_specs.BASE_PLATE_RIGHT + 10], 
                [mb_specs.U_ARM_OVERALL_HEIGHT/2, mb_specs.U_ARM_OVERALL_HEIGHT/2], 
                color=self.utils.style.COLORS['centerlines'], linestyle='--', 
                linewidth=self.utils.style.LINE_WEIGHTS['centerlines'], 
                alpha=self.utils.style.ALPHA['centerlines'])
        
        # === ADD SECTION INDICATORS ===
        self.utils.add_view_identifier(ax, (mb_specs.BASE_PLATE_LEFT - 5, 5), 'A')
        self.utils.add_view_identifier(ax, (mb_specs.BASE_PLATE_RIGHT + 15, mb_specs.U_ARM_OVERALL_HEIGHT - 5), 'A')
        
        # === MATERIAL CALLOUTS ===
        self.utils.add_material_callout(ax, (0, -mb_specs.BASE_PLATE_THICKNESS/2), 
                                      '4mm THICK\nSTAINLESS STEEL', (-30, -25), 'yellow')
        self.utils.add_material_callout(ax, (mb_specs.BASE_PLATE_RIGHT - 2, mb_specs.U_ARM_OVERALL_HEIGHT/2), 
                                      '4mm THICK\nSTAINLESS STEEL', (30, mb_specs.U_ARM_OVERALL_HEIGHT/2 + 30), 'yellow')
        
        # === ASSEMBLY DETAIL ===
        self.utils.add_manufacturing_detail(ax, (mb_specs.BASE_PLATE_RIGHT, 10), 
                                          'FLUSH WITH\nBACK EDGE', (mb_specs.BASE_PLATE_RIGHT + 25, 40), 'red')
        
        # === PROFESSIONAL LEGEND ===
        legend_items = [
            {'type': 'fill', 'color': self.utils.style.COLORS['base_plate_fill'], 
             'alpha': self.utils.style.ALPHA['fills'], 'edgecolor': 'black', 'label': 'Base Plate'},
            {'type': 'fill', 'color': self.utils.style.COLORS['u_arm_fill'], 
             'alpha': self.utils.style.ALPHA['fills'], 'edgecolor': 'black', 'label': 'U-Arm'},
            {'type': 'line', 'color': self.utils.style.COLORS['weld_symbols'], 
             'linewidth': self.utils.style.LINE_WEIGHTS['feature_lines'], 'label': 'Fillet Weld'},
            {'type': 'line', 'color': self.utils.style.COLORS['centerlines'], 
             'linewidth': self.utils.style.LINE_WEIGHTS['centerlines'], 'linestyle': '--', 'label': 'Centerlines'}
        ]
        self.utils.create_professional_legend(ax, legend_items, position='upper left', bbox_to_anchor=(0, 1))
        
        # === DRAWING SETUP ===
        title_with_scale = self.utils.add_scale_to_title('MOUNTING BRACKET - FRONT VIEW (L-PROFILE)\n4mm Stainless Steel', '1:2')
        self.utils.format_professional_layout(ax, title_with_scale, (-90, 80), (-35, 230), 'X (mm)', 'Z (mm)')
        
        # === COMPREHENSIVE TECHNICAL NOTES ===
        manufacturing_details = [
            'U-arm flush with back edge',
            'Profile view Section A-A'
        ]
        self.utils.add_comprehensive_notes(ax, mb_specs.MATERIAL, (-85, 220), manufacturing_details)
        
        plt.tight_layout()
        self._save_drawing(fig, 'mounting_bracket_front_view')
        plt.close()
    
    def _save_drawing(self, fig, filename):
        """Save drawing in both PNG and SVG formats with enhanced messaging."""
        png_path = self.output_base_path / "png" / f"{filename}.png"
        svg_path = self.output_base_path / "svg" / f"{filename}.svg"
        
        # Save PNG with high DPI
        fig.savefig(png_path, dpi=self.dpi, bbox_inches='tight', format='png')
        print(f"✓ Professional PNG: {png_path}")
        
        # Save SVG
        fig.savefig(svg_path, bbox_inches='tight', format='svg')
        print(f"✓ Professional SVG: {svg_path}")
