"""
Drawing Utilities - Gold Standard Implementation
===============================================

Enhanced reusable helper functions for professional technical drawing generation.
Implements gold standard techniques for annotations, legends, and manufacturing details.

All functions designed for modularity and professional technical drawing standards.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
from matplotlib.lines import Line2D

# === PROFESSIONAL STYLING CONSTANTS ===
class DrawingStyle:
    """Professional styling constants for technical drawings."""
    
    # Color coding system
    COLORS = {
        'primary_lines': 'black',
        'secondary_dims': 'blue',
        'holes_pcd': 'red', 
        'holes_base': 'blue',
        'centerlines': 'gray',
        'reference_grid': 'green',
        'weld_symbols': 'red',
        'material_callouts': 'black',
        'attachment_zones': 'lightgray',
        'base_plate_fill': 'lightblue',
        'u_arm_fill': 'lightgreen',
        'slot_lines': 'green'
    }
    
    # Font size standards
    FONT_SIZES = {
        'title': 14,
        'primary_dims': 12,
        'secondary_dims': 10,
        'coordinate_labels': 8,
        'annotations': 9,
        'notes': 9,
        'legend': 10
    }
    
    # Line weight standards
    LINE_WEIGHTS = {
        'main_outline': 3,
        'feature_lines': 2,
        'dimension_lines': 1,
        'centerlines': 0.5,
        'reference_grid': 0.5,
        'hole_outlines': 1.5
    }
    
    # Alpha values for transparency
    ALPHA = {
        'fills': 0.3,
        'attachment_zones': 0.5,
        'centerlines': 0.7,
        'reference_grid': 0.5,
        'callout_background': 0.8
    }


class DrawingUtils:
    """Enhanced collection of utility functions for professional technical drawings."""
    
    def __init__(self):
        """Initialize drawing utilities with professional styling."""
        self.style = DrawingStyle()
    
    # === ENHANCED DIMENSION AND ANNOTATION FUNCTIONS ===
    
    def add_primary_dimension(self, ax, start_point, end_point, label, vertical=False, offset=0):
        """
        Add a primary dimension line (black, bold) for overall measurements.
        
        Args:
            ax: Matplotlib axis object
            start_point: (x, y) tuple for line start
            end_point: (x, y) tuple for line end
            label: Text label for the dimension
            vertical: If True, rotate text 90 degrees
            offset: Additional offset for text positioning
        """
        # Draw dimension line with arrows
        ax.annotate('', xy=end_point, xytext=start_point,
                   arrowprops=dict(arrowstyle='<->', color=self.style.COLORS['primary_lines'], 
                                 lw=self.style.LINE_WEIGHTS['dimension_lines']))
        
        # Calculate text position (midpoint)
        text_x = (start_point[0] + end_point[0]) / 2
        text_y = (start_point[1] + end_point[1]) / 2
        
        # Apply offset based on dimension orientation
        if vertical:
            text_x += offset  # For vertical dimensions, offset moves text horizontally
        else:
            text_y += offset  # For horizontal dimensions, offset moves text vertically
        
        # Add dimension text
        rotation = 90 if vertical else 0
        ax.text(text_x, text_y, label, ha='center', va='center', 
               fontsize=self.style.FONT_SIZES['primary_dims'], fontweight='bold', 
               rotation=rotation, color=self.style.COLORS['primary_lines'])
    
    def add_secondary_dimension(self, ax, start_point, end_point, label, vertical=False, offset=0):
        """
        Add a secondary dimension line (blue, standard) for spacing measurements.
        
        Args:
            ax: Matplotlib axis object
            start_point: (x, y) tuple for line start
            end_point: (x, y) tuple for line end
            label: Text label for the dimension
            vertical: If True, rotate text 90 degrees
            offset: Additional offset for text positioning
        """
        # Draw dimension line with arrows
        ax.annotate('', xy=end_point, xytext=start_point,
                   arrowprops=dict(arrowstyle='<->', color=self.style.COLORS['secondary_dims'], 
                                 lw=self.style.LINE_WEIGHTS['dimension_lines']))
        
        # Calculate text position (midpoint)
        text_x = (start_point[0] + end_point[0]) / 2
        text_y = (start_point[1] + end_point[1]) / 2
        
        # Apply offset based on dimension orientation
        if vertical:
            text_x += offset  # For vertical dimensions, offset moves text horizontally
        else:
            text_y += offset  # For horizontal dimensions, offset moves text vertically
        
        # Add dimension text
        rotation = 90 if vertical else 0
        ax.text(text_x, text_y, label, ha='center', va='center', 
               fontsize=self.style.FONT_SIZES['secondary_dims'], 
               rotation=rotation, color=self.style.COLORS['secondary_dims'])
    
    def add_coordinate_label(self, ax, position, label, background=True):
        """
        Add coordinate labels for hole positions with optional background.
        
        Args:
            ax: Matplotlib axis object
            position: (x, y) position for the label
            label: Coordinate text (e.g., "(-40, +30)")
            background: Whether to add white background box
        """
        x, y = position
        
        # Offset label position to avoid overlap
        label_x = x + 8
        label_y = y + 8
        
        bbox_props = None
        if background:
            bbox_props = dict(boxstyle="round,pad=0.2", facecolor="white", 
                            alpha=self.style.ALPHA['callout_background'], edgecolor='none')
        
        ax.text(label_x, label_y, label, fontsize=self.style.FONT_SIZES['coordinate_labels'], 
               color=self.style.COLORS['reference_grid'], bbox=bbox_props, ha='left', va='bottom')
    
    def add_pcd_visualization(self, ax, center_x, center_y, radius, label="PCD"):
        """
        Add pitch circle diameter visualization with dashed circle and label.
        
        Args:
            ax: Matplotlib axis object
            center_x: X coordinate of circle center
            center_y: Y coordinate of circle center
            radius: Radius of the pitch circle
            label: Label text (e.g., "PCD 90")
        """
        # Draw dashed circle
        circle_pcd = Circle((center_x, center_y), radius, fill=False, 
                          color=self.style.COLORS['centerlines'], 
                          linewidth=self.style.LINE_WEIGHTS['centerlines'], 
                          linestyle='--', alpha=self.style.ALPHA['centerlines'])
        ax.add_patch(circle_pcd)
        
        # Add PCD label - positioned where plus symbol appears for optimal placement
        ax.text(center_x + 30, center_y - 10, label, ha='left', va='center', 
               fontsize=self.style.FONT_SIZES['annotations'], fontweight='bold',
               color=self.style.COLORS['centerlines'])
    
    def add_material_callout(self, ax, point, text, leader_end, callout_style='yellow'):
        """
        Add material specification callout with leader line.
        
        Args:
            ax: Matplotlib axis object
            point: (x, y) point where arrow points
            text: Callout text
            leader_end: (x, y) end point of leader line
            callout_style: Background color for callout box
        """
        # Draw leader line with arrow
        ax.annotate('', xy=point, xytext=leader_end,
                   arrowprops=dict(arrowstyle='->', color=self.style.COLORS['material_callouts'], lw=1))
        
        # Add callout text with background
        ax.text(leader_end[0], leader_end[1], text, ha='center', va='center',
               fontsize=self.style.FONT_SIZES['annotations'],
               bbox=dict(boxstyle="round,pad=0.3", facecolor=callout_style, 
                        alpha=self.style.ALPHA['callout_background']))
    
    def add_manufacturing_detail(self, ax, feature_point, detail_text, leader_end, color='red'):
        """
        Add manufacturing detail annotation with colored leader line.
        
        Args:
            ax: Matplotlib axis object
            feature_point: (x, y) point where arrow points
            detail_text: Detail text
            leader_end: (x, y) end point of leader line
            color: Color for leader line and text
        """
        # Draw leader line with arrow
        ax.annotate('', xy=feature_point, xytext=leader_end,
                   arrowprops=dict(arrowstyle='->', color=color, lw=1))
        
        # Add detail text
        ax.text(leader_end[0], leader_end[1], detail_text, ha='center', va='center',
               fontsize=self.style.FONT_SIZES['annotations'], color=color,
               bbox=dict(boxstyle="round,pad=0.3", facecolor='pink' if color=='red' else 'lightblue', 
                        alpha=self.style.ALPHA['callout_background']))
    
    def add_reference_grid(self, ax, x_positions, y_positions, x_range, y_range):
        """
        Add reference grid lines for hole positioning.
        
        Args:
            ax: Matplotlib axis object
            x_positions: List of X coordinates for vertical lines
            y_positions: List of Y coordinates for horizontal lines
            x_range: (min, max) range for horizontal lines
            y_range: (min, max) range for vertical lines
        """
        # Draw vertical reference lines
        for x_pos in x_positions:
            ax.plot([x_pos, x_pos], y_range, 
                   color=self.style.COLORS['reference_grid'], 
                   linestyle='--', linewidth=self.style.LINE_WEIGHTS['reference_grid'], 
                   alpha=self.style.ALPHA['reference_grid'])
        
        # Draw horizontal reference lines
        for y_pos in y_positions:
            ax.plot(x_range, [y_pos, y_pos], 
                   color=self.style.COLORS['reference_grid'], 
                   linestyle='--', linewidth=self.style.LINE_WEIGHTS['reference_grid'], 
                   alpha=self.style.ALPHA['reference_grid'])
    
    # === ENHANCED CENTERLINES AND GRIDS ===
    
    def add_professional_centerlines(self, ax, center_x, center_y, length=140, 
                                   style='--', alpha=None):
        """
        Add professional centerlines with proper styling.
        
        Args:
            ax: Matplotlib axis object
            center_x: X coordinate of center
            center_y: Y coordinate of center
            length: Length of centerlines extending from center
            style: Line style
            alpha: Line transparency (uses default if None)
        """
        if alpha is None:
            alpha = self.style.ALPHA['centerlines']
            
        half_length = length / 2
        
        # Horizontal centerline
        ax.plot([center_x - half_length, center_x + half_length], [center_y, center_y], 
                color=self.style.COLORS['centerlines'], linestyle=style, 
                linewidth=self.style.LINE_WEIGHTS['centerlines'], alpha=alpha, 
                label='Centerlines')
        
        # Vertical centerline
        ax.plot([center_x, center_x], [center_y - half_length, center_y + half_length], 
                color=self.style.COLORS['centerlines'], linestyle=style, 
                linewidth=self.style.LINE_WEIGHTS['centerlines'], alpha=alpha)
    
    # === ENHANCED SHAPE DRAWING FUNCTIONS ===
    
    def draw_milled_slot(self, ax, center_x, center_z, overall_height, flat_width, 
                        color=None, linewidth=None):
        """
        Draw a milled slot with parallel flats and semicircular ends.
        Enhanced with professional styling.
        """
        if color is None:
            color = self.style.COLORS['slot_lines']
        if linewidth is None:
            linewidth = self.style.LINE_WEIGHTS['feature_lines']
            
        flat_half_width = flat_width / 2
        end_radius = flat_half_width
        straight_height = overall_height - 2 * end_radius
        
        # Draw vertical flat sides
        flat_bottom_z = center_z - straight_height / 2
        flat_top_z = center_z + straight_height / 2
        
        ax.plot([center_x - flat_half_width, center_x - flat_half_width], 
                [flat_bottom_z, flat_top_z], color=color, linewidth=linewidth)
        ax.plot([center_x + flat_half_width, center_x + flat_half_width], 
                [flat_bottom_z, flat_top_z], color=color, linewidth=linewidth)
        
        # Draw semicircular ends
        theta = np.linspace(0, np.pi, 50)
        
        # Top semicircle
        top_semi_x = center_x + end_radius * np.cos(theta)
        top_semi_z = flat_top_z + end_radius * np.sin(theta)
        ax.plot(top_semi_x, top_semi_z, color=color, linewidth=linewidth)
        
        # Bottom semicircle
        bottom_semi_x = center_x + end_radius * np.cos(theta + np.pi)
        bottom_semi_z = flat_bottom_z + end_radius * np.sin(theta + np.pi)
        ax.plot(bottom_semi_x, bottom_semi_z, color=color, linewidth=linewidth)
    
    def draw_weld_symbol(self, ax, position, weld_type='fillet'):
        """
        Enhanced weld symbol drawing with professional styling.
        
        Args:
            ax: Matplotlib axis object
            position: (x, y) position for weld symbol
            weld_type: Type of weld ('fillet', 'butt', etc.)
        """
        x, y = position
        
        if weld_type == 'fillet':
            # Draw fillet weld symbol line
            ax.plot([x, x + 3], [y, y + 3], color=self.style.COLORS['weld_symbols'], 
                   linewidth=self.style.LINE_WEIGHTS['feature_lines'], label='Fillet Weld')
    
    # === PROFESSIONAL LEGEND AND LAYOUT FUNCTIONS ===
    
    def create_professional_legend(self, ax, legend_items, position='upper right', 
                                 bbox_to_anchor=(1, 1)):
        """
        Create a professional technical drawing legend.
        
        Args:
            ax: Matplotlib axis object
            legend_items: List of legend item dictionaries
            position: Legend position
            bbox_to_anchor: Bounding box anchor point
        """
        legend_elements = []
        
        for item in legend_items:
            if item['type'] == 'line':
                element = Line2D([0], [0], color=item['color'], 
                               linewidth=item.get('linewidth', 2),
                               linestyle=item.get('linestyle', '-'),
                               label=item['label'])
            elif item['type'] == 'fill':
                element = Rectangle((0,0), 1, 1, facecolor=item['color'], 
                                  alpha=item.get('alpha', 0.3),
                                  edgecolor=item.get('edgecolor', 'black'),
                                  label=item['label'])
            legend_elements.append(element)
        
        ax.legend(handles=legend_elements, loc=position, bbox_to_anchor=bbox_to_anchor, 
                 fontsize=self.style.FONT_SIZES['legend'])
    
    def add_scale_to_title(self, title, scale):
        """
        Add scale information to drawing title.
        
        Args:
            title: Base title string
            scale: Scale string (e.g., "1:2", "1:1")
        
        Returns:
            Enhanced title with scale information
        """
        return f"{title} | Scale {scale}"
    
    def add_view_identifier(self, ax, position, view_letter, fontsize=12):
        """
        Add section view identifiers (A, B, etc.) to drawings.
        
        Args:
            ax: Matplotlib axis object
            position: (x, y) position for identifier
            view_letter: Letter identifier (e.g., 'A', 'B')
            fontsize: Font size for identifier
        """
        ax.text(position[0], position[1], view_letter, fontsize=fontsize, 
               fontweight='bold', ha='center', va='center',
               bbox=dict(boxstyle="circle,pad=0.2", facecolor="white", edgecolor="black"))
    
    def add_comprehensive_notes(self, ax, material, position, manufacturing_details=None):
        """
        Add comprehensive technical notes with manufacturing details.
        
        Args:
            ax: Matplotlib axis object
            material: Material specification string
            position: (x, y) position for notes box
            manufacturing_details: List of additional manufacturing details
        """
        base_notes = [
            'NOTES:',
            '• All dimensions in mm',
            f'• Material: {material}',
            '• Continuous fillet weld',
            '• Remove all burrs and sharp edges'
        ]
        
        if manufacturing_details:
            base_notes.extend([f'• {detail}' for detail in manufacturing_details])
        
        notes_text = '\n'.join(base_notes)
        
        ax.text(position[0], position[1], notes_text, 
               fontsize=self.style.FONT_SIZES['notes'], va='top', ha='left',
               bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", 
                        alpha=self.style.ALPHA['callout_background']))
    
    def format_professional_layout(self, ax, title_with_scale, xlim, ylim, 
                                 xlabel='X (mm)', ylabel='Y (mm)'):
        """
        Apply professional formatting to technical drawings.
        
        Args:
            ax: Matplotlib axis object
            title_with_scale: Complete title including scale
            xlim: (min, max) for X-axis limits
            ylim: (min, max) for Y-axis limits
            xlabel: X-axis label
            ylabel: Y-axis label
        """
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_aspect('equal')  # Critical for technical drawings
        ax.grid(True, alpha=0.3, linewidth=0.5)
        ax.set_xlabel(xlabel, fontsize=self.style.FONT_SIZES['annotations'])
        ax.set_ylabel(ylabel, fontsize=self.style.FONT_SIZES['annotations'])
        ax.set_title(title_with_scale, fontsize=self.style.FONT_SIZES['title'], 
                    fontweight='bold')
    
    def draw_double_d_hole(self, ax, center_x, center_y, overall_diameter, flat_width,
                          color=None, linewidth=None, fill=False):
        """
        Draw a Double-D hole (stadium-shaped hole with parallel flats).
        
        Args:
            ax: Matplotlib axis object
            center_x: X coordinate of hole center
            center_y: Y coordinate of hole center
            overall_diameter: Overall diameter of the hole
            flat_width: Width between parallel flats
            color: Line color (default from style)
            linewidth: Line weight (default from style)
            fill: Whether to fill the hole (default False)
        """
        if color is None:
            color = self.style.COLORS['holes_pcd']
        if linewidth is None:
            linewidth = self.style.LINE_WEIGHTS['hole_outlines']
            
        # Calculate geometry
        radius = overall_diameter / 2
        flat_half_width = flat_width / 2
        
        # Draw the Double-D shape
        if flat_half_width < radius:
            # Calculate the height of the curved portions
            curve_height = np.sqrt(radius**2 - flat_half_width**2)
            
            # Create the complete Double-D profile
            angles_right = np.linspace(-np.arcsin(flat_half_width/radius), 
                                     np.arcsin(flat_half_width/radius), 25)
            angles_left = np.linspace(np.pi - np.arcsin(flat_half_width/radius), 
                                    np.pi + np.arcsin(flat_half_width/radius), 25)
            
            # Right semicircle
            right_x = center_x + radius * np.cos(angles_right)
            right_y = center_y + radius * np.sin(angles_right)
            
            # Left semicircle  
            left_x = center_x + radius * np.cos(angles_left)
            left_y = center_y + radius * np.sin(angles_left)
            
            # Top and bottom flats
            flat_top_y = center_y + curve_height
            flat_bottom_y = center_y - curve_height
            
            # Combine into complete closed profile
            x_coords = np.concatenate([
                right_x,
                [center_x + flat_half_width, center_x + flat_half_width],
                left_x[::-1],
                [center_x - flat_half_width, center_x - flat_half_width]
            ])
            
            y_coords = np.concatenate([
                right_y,
                [flat_top_y, flat_bottom_y],
                left_y[::-1],
                [flat_bottom_y, flat_top_y]
            ])
            
            if fill:
                ax.fill(x_coords, y_coords, color=color, alpha=0.3)
            ax.plot(x_coords, y_coords, color=color, linewidth=linewidth)
        else:
            # If flat width >= radius, just draw a circle
            circle = plt.Circle((center_x, center_y), radius, 
                              fill=fill, color=color, linewidth=linewidth)
            ax.add_patch(circle)
    
    
    # === LEGACY COMPATIBILITY FUNCTIONS ===
    
    def add_dimension_line(self, ax, start_point, end_point, label, vertical=False, offset=0):
        """Legacy compatibility - redirects to primary dimension."""
        self.add_primary_dimension(ax, start_point, end_point, label, vertical, offset)
    
    def add_technical_notes(self, ax, material, position, additional_notes=None):
        """Legacy compatibility - redirects to comprehensive notes."""
        self.add_comprehensive_notes(ax, material, position, additional_notes)
