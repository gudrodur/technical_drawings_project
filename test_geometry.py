#!/usr/bin/env python3
"""
Geometric Validation Test Script

This script validates the corrected geometric calculations for the Spooling Guide
to ensure mathematical precision and identify any remaining issues.
"""

import sys
import os
import numpy as np
import math

# Add the src directory to the path to import modules
sys.path.append('/home/gudro/Development/projects/technical_drawings_project/src')

from spooling_guide import geometry as geom
from spooling_guide import specifications as spec


def test_arm_width_function():
    """Test the arm width calculation function."""
    print("Testing arm width function...")
    
    # Test at known points
    width_inner = geom.arm_width_at_radius(spec.CENTRAL_OPENING_RADIUS)
    width_outer = geom.arm_width_at_radius(spec.OUTER_HOLE_PCD / 2.0)
    
    print(f"  Width at r=250mm: {width_inner:.1f}mm (expected: 50.0mm)")
    print(f"  Width at r=510mm: {width_outer:.1f}mm (expected: 100.0mm)")
    
    # Test intermediate point
    width_mid = geom.arm_width_at_radius(380.0)  # Midpoint
    expected_mid = 50.0 + 50.0 * (380.0 - 250.0) / (510.0 - 250.0)
    print(f"  Width at r=380mm: {width_mid:.1f}mm (expected: {expected_mid:.1f}mm)")
    
    return abs(width_inner - 50.0) < 0.1 and abs(width_outer - 100.0) < 0.1


def test_line_circle_intersection():
    """Test the analytical line-circle intersection function."""
    print("Testing line-circle intersection...")
    
    # Test simple case: horizontal line through circle center
    line_start = np.array([-10.0, 0.0])
    line_direction = np.array([1.0, 0.0])  # Horizontal
    circle_center = np.array([0.0, 0.0])
    circle_radius = 5.0
    
    intersections = geom.line_circle_intersection(line_start, line_direction, circle_center, circle_radius)
    
    print(f"  Found {len(intersections)} intersections")
    if len(intersections) == 2:
        print(f"  Intersection 1: ({intersections[0][0]:.1f}, {intersections[0][1]:.1f})")
        print(f"  Intersection 2: ({intersections[1][0]:.1f}, {intersections[1][1]:.1f})")
        
        # Should be at (-5, 0) and (5, 0)
        expected_valid = (abs(intersections[0][0] + 5.0) < 0.1 or abs(intersections[0][0] - 5.0) < 0.1)
        return expected_valid
    
    return False


def test_arm_calculation():
    """Test the main arm calculation function."""
    print("Testing arm calculation...")
    
    try:
        # Test calculation for arm at 0 degrees
        arm_outline, concave_arc, fillet_data = geom.calculate_arm_vertices(0.0)
        
        print(f"  Arm outline points: {len(arm_outline)}")
        print(f"  Concave arc points: {len(concave_arc)}")
        print(f"  Fillet centers: {len(fillet_data['centers'])}")
        
        # Check that we have reasonable point counts
        valid_outline = len(arm_outline) >= 5
        valid_arc = len(concave_arc) >= 10
        valid_fillets = len(fillet_data['centers']) >= 4
        
        return valid_outline and valid_arc and valid_fillets
        
    except Exception as e:
        print(f"  Error in arm calculation: {e}")
        return False


def test_concave_arc_center():
    """Test the concave arc center calculation."""
    print("Testing concave arc center calculation...")
    
    try:
        arc_center = geom.calculate_concave_arc_center_precise(0.0)  # 0 degree arm
        
        print(f"  Arc center: ({arc_center[0]:.1f}, {arc_center[1]:.1f})")
        
        # Arc center should be on the positive X axis for 0-degree arm
        on_x_axis = abs(arc_center[1]) < 0.1
        reasonable_distance = arc_center[0] > 500.0  # Should be beyond outer radius
        
        return on_x_axis and reasonable_distance
        
    except Exception as e:
        print(f"  Error in arc center calculation: {e}")
        return False


def test_side_line_equations():
    """Test the arm side line equation calculation."""
    print("Testing side line equations...")
    
    try:
        # Test for 0-degree arm
        left_start, left_direction = geom.calculate_arm_side_line_equation(0.0, 'left')
        right_start, right_direction = geom.calculate_arm_side_line_equation(0.0, 'right')
        
        print(f"  Left line start: ({left_start[0]:.1f}, {left_start[1]:.1f})")
        print(f"  Right line start: ({right_start[0]:.1f}, {right_start[1]:.1f})")
        
        # For 0-degree arm, left should have positive Y, right should have negative Y
        left_positive_y = left_start[1] > 0
        right_negative_y = right_start[1] < 0
        
        # Both should start near the inner radius
        left_reasonable = abs(np.linalg.norm(left_start) - 250.0) < 10.0
        right_reasonable = abs(np.linalg.norm(right_start) - 250.0) < 10.0
        
        return left_positive_y and right_negative_y and left_reasonable and right_reasonable
        
    except Exception as e:
        print(f"  Error in side line calculation: {e}")
        return False


def run_all_tests():
    """Run all validation tests."""
    print("=" * 60)
    print("SPOOLING GUIDE GEOMETRY VALIDATION TESTS")
    print("=" * 60)
    
    tests = [
        ("Arm Width Function", test_arm_width_function),
        ("Line-Circle Intersection", test_line_circle_intersection),
        ("Side Line Equations", test_side_line_equations),
        ("Concave Arc Center", test_concave_arc_center),
        ("Main Arm Calculation", test_arm_calculation),
    ]
    
    results = []
    
    for test_name, test_function in tests:
        print(f"\n{test_name}:")
        print("-" * 40)
        
        try:
            result = test_function()
            results.append((test_name, result))
            print(f"  Result: {'PASS' if result else 'FAIL'}")
        except Exception as e:
            print(f"  EXCEPTION: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name:<30} {status}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(results)} tests")
    
    if passed == len(results):
        print("\n✅ ALL TESTS PASSED - Geometric calculations are functioning correctly!")
    else:
        print(f"\n❌ {len(results) - passed} TESTS FAILED - Further corrections needed")
    
    return passed == len(results)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
