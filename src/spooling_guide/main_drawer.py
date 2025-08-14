"""
Spooling Guide Main Drawing Generator

This is the primary orchestration script that coordinates all modules to generate
the complete professional technical drawing of the Spooling Guide Plate.

This script:
1. Initializes matplotlib figure and axes with professional settings
2. Defines comprehensive styling configuration
3. Calls drawing component functions in logical sequence
4. Applies professional annotations and documentation
5. Exports high-quality output files (PNG and SVG)

The resulting drawing meets gold standard requirements with:
- Professional multi-level dimensioning
- Comprehensive legends and technical notes  
- Manufacturing documentation with material callouts
- Consistent visual styling and non-overlapping annotations
"""

import matplotlib.pyplot as plt
import sys
import os

# Import spooling guide modules
from . import specifications as spec
from . import geometry as geom
from . import drawing_components as components
from . import annotations


def save_drawing_files(fig, base_filename, output_directory):
    """
    Save drawing files in PNG and SVG formats.
    
    Args:
        fig: Matplotlib figure object
        base_filename: Base name for output files
        output_directory: Directory to save files
    """
    import os
    
    # Create output directories if they don't exist
    png_dir = os.path.join(output_directory, 'png')
    svg_dir = os.path.join(output_directory, 'svg')
    
    os.makedirs(png_dir, exist_ok=True)
    os.makedirs(svg_dir, exist_ok=True)
    
    # Save PNG (high resolution)
    png_path = os.path.join(png_dir, f"{base_filename}.png")
    fig.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved PNG: {png_path}")
    
    # Save SVG (vector format)
    svg_path = os.path.join(svg_dir, f"{base_filename}.svg")
    fig.savefig(svg_path, format='svg', bbox_inches='tight', facecolor='white')
    print(f"Saved SVG: {svg_path}")


def create_style_configuration():
    """
    Define comprehensive styling configuration for gold standard appearance.
    
    Returns:
        dict: Complete styling parameters for all drawing elements
    """
    return {
        # Primary drawing elements
        'primary_color': '#000000',        # Black for main outlines
        'primary_linewidth': 2.0,
        
        # Holes and features
        'hole_color': '#FF0000',           # Red for holes
        'hole_linewidth': 1.5,
        
        # Outer ring
        'ring_color': '#0066CC',           # Blue for outer ring
        'ring_linewidth': 2.0,
        
        # Reference elements
        'pcd_color': '#00AA00',            # Green for PCD circles
        'pcd_linewidth': 1.0,
        'centerline_color': '#666666',     # Gray for centerlines  
        'centerline_linewidth': 1.0,
        
        # Dimensions and annotations
        'dimension_color': '#000000',      # Black for dimensions
        'dimension_linewidth': 1.0,
        'notes_color': '#000080',          # Dark blue for notes
        'title_color': '#000000',          # Black for titles
        
        # Font sizes (professional hierarchy)
        'title_font_size': 16,
        'subtitle_font_size': 12,
        'primary_font_size': 10,
        'secondary_font_size': 8,
        'notes_font_size': 8,
        
        # Legend and layout
        'legend_font_size': 9,
        'background_color': '#FFFFFF',     # White background
        'grid_alpha': 0.3,
        
        # Arm line labeling
        'show_arm_line_labels': True,      # Enable arm line identification
    }


def setup_figure_and_axes():
    """
    Initialize matplotlib figure and axes with professional settings.
    
    Returns:
        tuple: (figure, axes) objects configured for technical drawing
    """
    # Create figure with appropriate size for complex drawing
    fig, ax = plt.subplots(1, 1, figsize=(16, 16))  # Large square format
    
    # Apply professional styling
    components.apply_professional_styling(ax)
    
    return fig, ax


def generate_spooling_guide_drawing(save_files=True, output_directory=None):
    """
    Generate the complete professional technical drawing of the Spooling Guide.
    
    Args:
        save_files (bool): Whether to save output files
        output_directory (str): Directory for output files (optional)
        
    Returns:
        tuple: (figure, axes) objects with complete drawing
    """
    print("Generating Spooling Guide technical drawing...")
    
    # Validate geometry before drawing
    validation = geom.validate_geometry()
    if validation['warnings']:
        print("GEOMETRY WARNINGS:")
        for warning in validation['warnings']:
            print(f"  - {warning}")
    
    if not validation['geometry_valid']:
        print("GEOMETRY ERRORS:")
        for error in validation['errors']:
            print(f"  - {error}")
        return None, None
    
    # Initialize drawing
    fig, ax = setup_figure_and_axes()
    style_config = create_style_configuration()
    
    print("Drawing geometric components...")
    
    # Draw main geometric components in logical order
    components.draw_central_opening(ax, style_config)
    components.draw_all_arms(ax, style_config)
    components.draw_all_holes(ax, style_config)
    components.draw_outer_ring(ax, style_config)
    components.draw_all_pcds(ax, style_config)
    components.draw_centerlines(ax, style_config)
    components.draw_corner_fillets(ax, style_config)
    
    print("Adding professional annotations...")
    
    # Add comprehensive professional annotations
    annotations.add_all_annotations(ax, style_config)
    
    # Final layout adjustments
    plt.tight_layout()
    
    # Save files if requested
    if save_files:
        base_filename = "spooling_guide_plate"
        if output_directory is None:
            # Default to project drawings directory
            output_directory = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                'drawings'
            )
        
        print(f"Saving drawing files to {output_directory}...")
        save_drawing_files(fig, base_filename, output_directory)
        print("Drawing generation complete!")
    
    return fig, ax


def generate_multiple_views():
    """
    Generate multiple orthographic views of the spooling guide.
    Future enhancement for complete documentation.
    
    Returns:
        dict: Dictionary of (figure, axes) pairs for each view
    """
    views = {}
    
    # Top view (primary view)
    print("Generating TOP VIEW...")
    fig_top, ax_top = generate_spooling_guide_drawing(save_files=False)
    views['top'] = (fig_top, ax_top)
    
    # TODO: Add side view showing plate thickness and ring profile
    # TODO: Add detail views of arm termination and fillets
    # TODO: Add assembly view showing welding details
    
    return views


def main():
    """
    Main entry point for spooling guide drawing generation.
    Can be called directly or from the top-level drawing_engine.py
    """
    try:
        # Generate the primary drawing
        fig, ax = generate_spooling_guide_drawing(save_files=True)
        
        if fig is not None:
            # Display the drawing
            plt.show()
        else:
            print("ERROR: Drawing generation failed due to geometry errors.")
            
    except Exception as e:
        print(f"ERROR generating spooling guide drawing: {str(e)}")
        raise


if __name__ == "__main__":
    main()
