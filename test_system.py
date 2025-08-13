#!/usr/bin/env python3
"""
Test Script for Technical Drawing Generation System
==================================================

This script tests the system by generating mounting bracket drawings
without interactive input.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from src.drawing_engine import DrawingEngine
    print("✓ Successfully imported DrawingEngine")
    
    from specifications import mounting_bracket as mb_specs
    print("✓ Successfully imported mounting bracket specifications")
    
    # Test a few key specifications
    print(f"✓ Base plate size: {mb_specs.BASE_PLATE_WIDTH}x{mb_specs.BASE_PLATE_HEIGHT}mm")
    print(f"✓ U-arm height: {mb_specs.U_ARM_OVERALL_HEIGHT}mm")
    print(f"✓ Material: {mb_specs.MATERIAL}")
    
    # Initialize drawing engine
    engine = DrawingEngine()
    print("✓ Drawing engine initialized")
    
    # Generate mounting bracket drawings
    print("\nGenerating mounting bracket drawings...")
    engine.draw_mounting_bracket()
    print("✓ Mounting bracket drawings completed!")
    
    print("\n" + "="*60)
    print("SYSTEM TEST COMPLETED SUCCESSFULLY")
    print("="*60)
    print("All components are working correctly.")
    print("The technical drawing generation system is ready for use.")
    
except Exception as e:
    print(f"✗ Error during testing: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
