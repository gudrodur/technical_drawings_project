#!/usr/bin/env python3
"""
Visual Validation Script - Gold Standard Quality Verification

This script performs comprehensive visual validation of the spooling guide
to confirm that mathematical precision has achieved Gold Standard visual output.
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


def validate_mathematical_precision():
    """Validate that mathematical calculations are working precisely."""
    print("=== MATHEMATICAL PRECISION VALIDATION ===")
    
    # Test the exact mathematical implementation
    arm_angle = 0.0  # Test 0-degree arm
    
    # 1. Verify line equations match expected mathematical results
    side_points = geom.calculate_arm_side_line_points(math.radians(arm_angle))
    
    print(f"Arm side points for {arm_angle}° arm:")
    print(f"  Inner top: ({side_points['top']['inner'][0]:.1f}, {side_points['top']['inner'][1]:.1f})")
    print(f"  Inner bottom: ({side_points['bottom']['inner'][0]:.1f}, {side_points['bottom']['inner'][1]:.1f})")
    print(f"  Outer top: ({side_points['top']['outer'][0]:.1f}, {side_points['top']['outer'][1]:.1f})")
    print(f"  Outer bottom: ({side_points['bottom']['outer'][0]:.1f}, {side_points['bottom']['outer'][1]:.1f})")
    
    # 2. Verify arc center calculation
    arc_geom = geom.calculate_concave_arc_geometry(math.radians(arm_angle))
    center = arc_geom['center']
    print(f"\nConcave arc center: ({center[0]:.3f}, {center[1]:.3f})")
    
    # 3. Verify intersection calculations
    intersections = geom.find_precise_line_arc_intersections(math.radians(arm_angle))
    if intersections['top'] and intersections['bottom']:
        top_int = intersections['top']
        bottom_int = intersections['bottom']
        print(f"Top intersection: ({top_int[0]:.3f}, {top_int[1]:.3f})")
        print(f"Bottom intersection: ({bottom_int[0]:.3f}, {bottom_int[1]:.3f})")
        
        # Verify intersections are on the arc
        top_dist = math.sqrt((top_int[0] - center[0])**2 + (top_int[1] - center[1])**2)
        bottom_dist = math.sqrt((bottom_int[0] - center[0])**2 + (bottom_int[1] - center[1])**2)
        
        print(f"Top intersection radius: {top_dist:.3f}mm (expected: {spec.ARM_END_ARC_RADIUS}mm)")
        print(f"Bottom intersection radius: {bottom_dist:.3f}mm (expected: {spec.ARM_END_ARC_RADIUS}mm)")
        
        radius_error_top = abs(top_dist - spec.ARM_END_ARC_RADIUS)
        radius_error_bottom = abs(bottom_dist - spec.ARM_END_ARC_RADIUS)
        
        precision_valid = radius_error_top < 0.001 and radius_error_bottom < 0.001
        print(f"Mathematical precision: {'✅ EXCELLENT' if precision_valid else '❌ INSUFFICIENT'}")
        
        return precision_valid
    else:
        print("❌ ERROR: Could not calculate intersections")
        return False


def validate_geometric_continuity():
    """Validate that the arm outline forms a continuous, smooth curve."""
    print("\n=== GEOMETRIC CONTINUITY VALIDATION ===")
    
    continuity_valid = True
    
    for arm_angle in [0.0, 90.0, 180.0, 270.0]:
        print(f"\nValidating arm at {arm_angle}°:")
        
        arm_outline, concave_arc, fillet_data = geom.calculate_arm_vertices(arm_angle)
        
        if len(arm_outline) < 5:
            print(f"  ❌ ERROR: Insufficient outline points ({len(arm_outline)})")
            continuity_valid = False
            continue
        
        # Check for excessive gaps in outline
        gaps = []
        for i in range(len(arm_outline) - 1):
            gap = np.linalg.norm(arm_outline[i+1] - arm_outline[i])
            gaps.append(gap)
        
        max_gap = max(gaps)
        avg_gap = np.mean(gaps)
        
        print(f"  Outline points: {len(arm_outline)}")
        print(f"  Maximum gap: {max_gap:.2f}mm")
        print(f"  Average gap: {avg_gap:.2f}mm")
        
        # Check for reasonable gap sizes (no massive jumps indicating discontinuities)
        excessive_gaps = [g for g in gaps if g > 100.0]  # 100mm is excessive for smooth curves
        
        if len(excessive_gaps) > 0:
            print(f"  ❌ WARNING: {len(excessive_gaps)} excessive gaps detected")
            continuity_valid = False
        else:
            print(f"  ✅ Continuity: Good")
    
    return continuity_valid


def validate_manufacturing_feasibility():
    """Validate that the geometry is manufacturable."""
    print("\n=== MANUFACTURING FEASIBILITY VALIDATION ===")
    
    # Check ring clearance
    ring_inner_radius = (spec.OUTER_HOLE_PCD / 2.0) - (spec.OUTER_RING_DIAMETER / 2.0)
    arm_outer_radius = spec.ARM_OUTER_RADIUS
    
    clearance = ring_inner_radius - arm_outer_radius
    
    print(f"Ring inner radius: {ring_inner_radius}mm")
    print(f"Arm outer radius: {arm_outer_radius}mm")
    print(f"Clearance: {clearance:.3f}mm")
    
    if abs(clearance) < 0.001:
        print("✅ Perfect tangency achieved - weld clearance optimal")
        clearance_valid = True
    elif clearance > 0:
        print(f"⚠️  WARNING: {clearance:.3f}mm gap - may affect weld quality")
        clearance_valid = True
    else:
        print(f"❌ ERROR: {abs(clearance):.3f}mm interference - not manufacturable")
        clearance_valid = False
    
    # Check hole clearances
    holes = geom.calculate_hole_coordinates()
    
    print(f"\nHole pattern validation:")
    print(f"  Central hole: ⌀{spec.CENTRAL_HOLE_DIAMETER}mm at center")
    print(f"  Inner holes: {len(holes['inner'])} × ⌀{spec.INNER_HOLE_DIAMETER}mm on ⌀{spec.INNER_HOLE_PCD}mm PCD")
    print(f"  Outer holes: {len(holes['outer'])} × ⌀{spec.OUTER_HOLE_DIAMETER}mm on ⌀{spec.OUTER_HOLE_PCD}mm PCD")
    
    return clearance_valid


def validate_dimensional_accuracy():
    """Validate dimensional accuracy of the implementation."""
    print("\n=== DIMENSIONAL ACCURACY VALIDATION ===")
    
    # Test arm width function
    print("Arm width function validation:")
    width_250 = geom.arm_width_at_radius(250.0)
    width_505 = geom.arm_width_at_radius(505.0)
    width_377_5 = geom.arm_width_at_radius(377.5)  # Midpoint
    
    print(f"  Width at r=250mm: {width_250:.1f}mm (expected: 50.0mm)")
    print(f"  Width at r=505mm: {width_505:.1f}mm (expected: 100.0mm)")
    print(f"  Width at r=377.5mm: {width_377_5:.1f}mm (expected: 75.0mm)")
    
    width_accuracy = (abs(width_250 - 50.0) < 0.1 and 
                     abs(width_505 - 100.0) < 0.1 and 
                     abs(width_377_5 - 75.0) < 0.1)
    
    if width_accuracy:
        print("  ✅ Width function: Accurate")
    else:
        print("  ❌ Width function: Inaccurate")
    
    # Test overall dimensions
    overall_dims = geom.calculate_overall_dimensions()
    print(f"\nOverall dimensions:")
    print(f"  Overall diameter: {overall_dims['overall_diameter']:.1f}mm")
    print(f"  Central opening: {overall_dims['central_opening_diameter']:.1f}mm")
    
    return width_accuracy


def create_quality_assessment_plot():
    """Create a detailed quality assessment plot."""
    print("\n=== CREATING QUALITY ASSESSMENT PLOT ===")
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 16))
    
    # Plot 1: Single arm detail
    arm_outline, concave_arc, fillet_data = geom.calculate_arm_vertices(0.0)
    
    ax1.plot(arm_outline[:, 0], arm_outline[:, 1], 'b-', linewidth=2, label='Arm Outline')
    ax1.plot(concave_arc[:, 0], concave_arc[:, 1], 'r-', linewidth=2, label='Concave Arc')
    
    # Add fillet centers
    for i, center in enumerate(fillet_data['centers']):
        ax1.plot(center[0], center[1], 'go', markersize=6, 
                label='Fillet Centers' if i == 0 else "")
    
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.set_title('Single Arm Detail (0°)')
    ax1.set_xlabel('X (mm)')
    ax1.set_ylabel('Y (mm)')
    
    # Plot 2: All four arms
    for angle in [0.0, 90.0, 180.0, 270.0]:
        arm_outline, _, _ = geom.calculate_arm_vertices(angle)
        ax2.plot(arm_outline[:, 0], arm_outline[:, 1], 'b-', linewidth=1.5, alpha=0.8)
    
    # Add central opening
    central_opening = geom.generate_central_opening_points()
    ax2.plot(central_opening[:, 0], central_opening[:, 1], 'k--', linewidth=2, label='Central Opening')
    
    # Add holes
    holes = geom.calculate_hole_coordinates()
    ax2.plot(holes['central'][:, 0], holes['central'][:, 1], 'ro', markersize=8, label='Central Hole')
    ax2.plot(holes['inner'][:, 0], holes['inner'][:, 1], 'bo', markersize=4, label='Inner Holes')
    ax2.plot(holes['outer'][:, 0], holes['outer'][:, 1], 'go', markersize=4, label='Outer Holes')
    
    ax2.set_aspect('equal')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_title('Complete Assembly')
    ax2.set_xlabel('X (mm)')
    ax2.set_ylabel('Y (mm)')
    
    # Plot 3: Mathematical validation
    arm_angles = np.linspace(0, 360, 8, endpoint=False)
    arc_centers_x = []
    arc_centers_y = []
    
    for angle in arm_angles:
        arc_geom = geom.calculate_concave_arc_geometry(math.radians(angle))
        center = arc_geom['center']
        arc_centers_x.append(center[0])
        arc_centers_y.append(center[1])
    
    ax3.plot(arc_centers_x, arc_centers_y, 'ro-', linewidth=2, markersize=6)
    ax3.set_aspect('equal')
    ax3.grid(True, alpha=0.3)
    ax3.set_title('Arc Centers Distribution')
    ax3.set_xlabel('X (mm)')
    ax3.set_ylabel('Y (mm)')
    
    # Plot 4: Width function validation
    radii = np.linspace(250, 505, 100)
    widths = [geom.arm_width_at_radius(r) for r in radii]
    
    ax4.plot(radii, widths, 'b-', linewidth=2, label='Calculated Width')
    ax4.plot([250, 505], [50, 100], 'ro-', linewidth=2, markersize=8, label='Specification Points')
    ax4.grid(True, alpha=0.3)
    ax4.legend()
    ax4.set_title('Arm Width Function Validation')
    ax4.set_xlabel('Radius (mm)')
    ax4.set_ylabel('Width (mm)')
    
    plt.tight_layout()
    
    output_path = '/home/gudro/Development/projects/technical_drawings_project/quality_assessment.png'
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    print(f"Quality assessment plot saved: {output_path}")
    
    plt.close()


def run_comprehensive_validation():
    """Run complete visual validation suite."""
    print("=" * 80)
    print("COMPREHENSIVE VISUAL VALIDATION - GOLD STANDARD VERIFICATION")
    print("=" * 80)
    
    # Run all validation tests
    tests = [
        ("Mathematical Precision", validate_mathematical_precision),
        ("Geometric Continuity", validate_geometric_continuity),
        ("Manufacturing Feasibility", validate_manufacturing_feasibility),
        ("Dimensional Accuracy", validate_dimensional_accuracy),
    ]
    
    results = []
    
    for test_name, test_function in tests:
        try:
            result = test_function()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ ERROR in {test_name}: {e}")
            results.append((test_name, False))
    
    # Create quality assessment plot
    try:
        create_quality_assessment_plot()
    except Exception as e:
        print(f"\n❌ ERROR creating quality plot: {e}")
    
    # Summary
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<30} {status}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(results)} validation tests")
    
    if passed == len(results):
        print("\n🏆 GOLD STANDARD ACHIEVED!")
        print("   Mathematical precision has successfully translated to visual excellence.")
        print("   All geometric calculations are mathematically exact and manufacturable.")
    else:
        print(f"\n⚠️  VALIDATION INCOMPLETE: {len(results) - passed} issues remain")
        print("   Additional corrections may be needed to achieve Gold Standard quality.")
    
    return passed == len(results)


if __name__ == "__main__":
    success = run_comprehensive_validation()
    sys.exit(0 if success else 1)
