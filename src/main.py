#!/usr/bin/env python3
"""
Technical Drawing Generation System - Main Interface
====================================================

This is the primary user interface for generating technical drawings.
Users can select components and generate complete drawing sets.

Usage:
    python main.py

The script will present a menu of available components and generate
the requested drawings in both PNG and SVG formats.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.drawing_engine import DrawingEngine
from specifications import AVAILABLE_COMPONENTS


class TechnicalDrawingGenerator:
    """Main application class for the technical drawing generation system."""
    
    def __init__(self):
        """Initialize the drawing generator."""
        self.drawing_engine = DrawingEngine()
        self.output_base_path = project_root / "drawings"
    
    def display_menu(self):
        """Display the main menu of available components."""
        print("\n" + "="*60)
        print("TECHNICAL DRAWING GENERATION SYSTEM")
        print("="*60)
        print("\nAvailable Components:")
        
        # Filter only implemented components
        implemented_components = ['mounting_bracket']  # Add more as implemented
        
        for i, component in enumerate(implemented_components, 1):
            print(f"  {i}. {component.replace('_', ' ').title()}")
        
        print(f"  {len(implemented_components) + 1}. Exit")
        print("\n" + "-"*60)
    
    def get_user_choice(self):
        """Get and validate user's component selection."""
        implemented_components = ['mounting_bracket']  # Keep in sync with display_menu
        
        while True:
            try:
                choice = int(input("Select component (number): "))
                if 1 <= choice <= len(implemented_components):
                    return implemented_components[choice - 1]
                elif choice == len(implemented_components) + 1:
                    return 'exit'
                else:
                    print(f"Invalid choice. Please select 1-{len(implemented_components) + 1}")
            except ValueError:
                print("Invalid input. Please enter a number.")
            except KeyboardInterrupt:
                print("\nExiting...")
                return 'exit'
    
    def generate_drawings(self, component_name):
        """Generate complete drawing set for the specified component."""
        print(f"\nGenerating drawings for: {component_name.replace('_', ' ').title()}")
        print("-" * 50)
        
        try:
            # Call the appropriate drawing function
            if component_name == 'mounting_bracket':
                self.drawing_engine.draw_mounting_bracket()
                print("✓ Mounting bracket drawings generated successfully!")
            else:
                print(f"Error: Drawing function for '{component_name}' not yet implemented.")
                return False
            
            # Display output information
            png_path = self.output_base_path / "png"
            svg_path = self.output_base_path / "svg"
            print(f"\nOutput files saved to:")
            print(f"  PNG: {png_path}")
            print(f"  SVG: {svg_path}")
            
            return True
            
        except Exception as e:
            print(f"Error generating drawings: {e}")
            return False
    
    def run(self):
        """Main application loop."""
        print("Initializing Technical Drawing Generation System...")
        
        while True:
            self.display_menu()
            choice = self.get_user_choice()
            
            if choice == 'exit':
                print("\nThank you for using the Technical Drawing Generation System!")
                break
            
            success = self.generate_drawings(choice)
            
            if success:
                input("\nPress Enter to continue...")
            else:
                input("\nPress Enter to return to menu...")


def main():
    """Entry point for the application."""
    try:
        app = TechnicalDrawingGenerator()
        app.run()
    except KeyboardInterrupt:
        print("\n\nApplication terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
