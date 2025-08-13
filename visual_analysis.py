#!/usr/bin/env python3
"""
Visual Quality Analysis Script

This script analyzes the generated spooling guide drawing to verify that
the geometric corrections have resolved the visual defects identified
in the root cause analysis.
"""

import sys
import os
import numpy as np
import math
import matplotlib.pyplot as plt

# Add the src directory to the path
sys.path.append('/home/gudro/Development/projects/technical_drawings_project/src')

from spooling_guide import geometry as geom
from spooling_guide import specifications as spec


def analyze_arm_geometry():
    """Analyze the geometric quality of a single arm."""
    print("Analyzing arm geometric quality...")
    
    # Calculate arm for 0 degrees
    arm_outline, concave_arc, fillet_data = geom.calculate_arm_vertices(0.0)
    
    print(f"  Generated {len(arm_outline)} outline points")
    print(f"  Generated {len(concave_arc)} concave arc points")
    print(f"  Generated {len(fillet_data['centers'])} fillet centers")
    
    # Check continuity of outline
    outline_lengths = []
    for i in range(len(arm_outline) - 1):
        segment_length = np.linalg.norm(arm_outline[i+1] - arm_outline[i])
        outline_lengths.append(segment_length)
    
    max_gap = max(outline_lengths)
    min_gap = min(outline_lengths)
    avg_gap = np.mean(outline_lengths)
    
    print(f"  Outline segment analysis:")
    print(f"    Maximum gap: {max_gap:.2f}mm")
    print(f"    Minimum gap: {min_gap:.2f}mm")
    print(f"    Average gap: {avg_gap:.2f}mm")
    
    # Check for excessive gaps (indicating discontinuities)
    excessive_gaps = [gap for gap in outline_lengths if gap > 50.0]
    print(f"    Gaps > 50mm: {len(excessive_gaps)}")
    
    return len(excessive_gaps) == 0


def analyze_concave_arc_quality():
    """Analyze the quality of concave arc terminations."""
    print("Analyzing concave arc quality...")
    
    # Test all four arms
    arc_quality_good = True
    
    for arm_angle in [0.0, 90.0, 180.0, 270.0]:
        arm_outline, concave_arc, fillet_data = geom.calculate_arm_vertices(arm_angle)
        
        if len(concave_arc) < 10:
            print(f"  Warning: Arm at {arm_angle}° has only {len(concave_arc)} arc points")
            arc_quality_good = False
        
        # Check arc radius consistency
        arc_center = geom.calculate_concave_arc_center_precise(math.radians(arm_angle))
        
        radii = []
        for point in concave_arc:
            radius = np.linalg.norm(point - arc_center)
            radii.append(radius)
        
        radius_variation = max(radii) - min(radii)
        print(f"  Arm {arm_angle:3.0f}°: Arc radius variation = {radius_variation:.2f}mm")
        
        if radius_variation > 5.0:  # More than 5mm variation indicates problems
            arc_quality_good = False
    
    return arc_quality_good


def analyze_intersection_precision():
    """Analyze the precision of line-arc intersections."""
    print("Analyzing intersection precision...")
    
    precision_good = True
    
    for arm_angle in [0.0, 90.0]:  # Test two arms
        angle_rad = math.radians(arm_angle)
        
        # Get intersection points
        left_intersection = geom.find_precise_line_arc_intersection(angle_rad, 'left')
        right_intersection = geom.find_precise_line_arc_intersection(angle_rad, 'right')
        
        # Get arc center
        arc_center = geom.calculate_concave_arc_center_precise(angle_rad)
        
        # Check that intersections are actually on the arc
        left_radius = np.linalg.norm(left_intersection - arc_center)
        right_radius = np.linalg.norm(right_intersection - arc_center)
        
        expected_radius = spec.ARM_END_ARC_RADIUS
        
        left_error = abs(left_radius - expected_radius)
        right_error = abs(right_radius - expected_radius)
        
        print(f"  Arm {arm_angle:3.0f}°:")
        print(f"    Left intersection radius error: {left_error:.2f}mm")
        print(f"    Right intersection radius error: {right_error:.2f}mm")
        
        if left_error > 1.0 or right_error > 1.0:  # More than 1mm error
            precision_good = False
    
    return precision_good


def check_mathematical_relationships():
    """Verify key mathematical relationships are maintained."""
    print("Checking mathematical relationships...")
    
    relationships_valid = True
    
    # Check arm taper linearity
    test_radii = [250, 300, 350, 400, 450, 500, 510]
    widths = [geom.arm_width_at_radius(r) for r in test_radii]
    
    # Check linearity by verifying constant rate of change
    rates = []
    for i in range(len(test_radii) - 1):
        dr = test_radii[i+1] - test_radii[i]
        dw = widths[i+1] - widths[i]
        rate = dw / dr if dr > 0 else 0
        rates.append(rate)
    
    rate_variation = max(rates) - min(rates)
    print(f"  Taper rate variation: {rate_variation:.4f} (should be ~0)")
    
    if rate_variation > 0.01:
        relationships_valid = False
    
    # Check arm angular spacing
    arm_angles = spec.ARM_ANGLES
    for i in range(len(arm_angles)):
        next_angle = arm_angles[(i + 1) % len(arm_angles)]
        spacing = (next_angle - arm_angles[i]) % 360
        if spacing == 0:
            spacing = 360
        print(f"  Spacing from {arm_angles[i]}° to {next_angle}°: {spacing}°")
        
        if abs(spacing - 90.0) > 0.1:
            relationships_valid = False
    
    return relationships_valid


def create_diagnostic_plot():
    """Create a diagnostic plot showing key geometric elements."""
    print("Creating diagnostic plot...")
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    ax.set_aspect('equal')
    
    # Plot one arm in detail
    arm_outline, concave_arc, fillet_data = geom.calculate_arm_vertices(0.0)
    
    # Plot arm outline
    ax.plot(arm_outline[:, 0], arm_outline[:, 1], 'b-', linewidth=2, label='Arm Outline')
    
    # Plot concave arc
    ax.plot(concave_arc[:, 0], concave_arc[:, 1], 'r-', linewidth=2, label='Concave Arc')
    
    # Plot fillet centers
    for center in fillet_data['centers']:
        ax.plot(center[0], center[1], 'go', markersize=8, label='Fillet Center' if center is fillet_data['centers'][0] else "")
    
    # Plot central opening
    central_opening = geom.generate_central_opening_points()
    ax.plot(central_opening[:, 0], central_opening[:, 1], 'k--', alpha=0.5, label='Central Opening')
    
    # Add grid and labels
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_title('Spooling Guide Geometric Analysis - Single Arm Detail')
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    
    # Save diagnostic plot
    output_path = '/home/gudro/Development/projects/technical_drawings_project/diagnostic_plot.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"  Diagnostic plot saved: {output_path}")
    
    plt.close()


def run_visual_analysis():
    """Run complete visual quality analysis."""
    print("=" * 60)
    print("SPOOLING GUIDE VISUAL QUALITY ANALYSIS")
    print("=" * 60)
    
    tests = [
        ("Arm Geometry Continuity", analyze_arm_geometry),
        ("Concave Arc Quality", analyze_concave_arc_quality),
        ("Intersection Precision", analyze_intersection_precision),
        ("Mathematical Relationships", check_mathematical_relationships),
    ]
    
    results = []
    
    for test_name, test_function in tests:
        print(f"\n{test_name}:")
        print("-" * 40)
        
        try:
            result = test_function()
            results.append((test_name, result))
            print(f"  Overall Result: {'PASS' if result else 'FAIL'}")
        except Exception as e:
            print(f"  EXCEPTION: {e}")
            results.append((test_name, False))
    
    # Create diagnostic plot
    print(f"\nDiagnostic Visualization:")
    print("-" * 40)
    create_diagnostic_plot()
    
    print("\n" + "=" * 60)
    print("VISUAL ANALYSIS SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name:<30} {status}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(results)} visual quality tests")
    
    if passed == len(results):
        print("\n✅ ALL VISUAL QUALITY TESTS PASSED!")
        print("   The geometric corrections have successfully resolved the visual defects.")
    else:
        print(f"\n❌ {len(results) - passed} VISUAL TESTS FAILED")
        print("   Additional geometric corrections may be needed.")
    
    return passed == len(results)


if __name__ == "__main__":
    success = run_visual_analysis()
    sys.exit(0 if success else 1)
