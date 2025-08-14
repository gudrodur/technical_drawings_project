#!/usr/bin/env python3
"""
Debug script to test annotation calculations
"""
import sys
import os
sys.path.append('src')

from spooling_guide import specifications as spec
from spooling_guide import geometry as geom

print("=== DEEP SCAN DEBUG REPORT ===")
print()

print("1. SPECIFICATIONS VALUES:")
print(f"   OUTER_HOLE_PCD = {spec.OUTER_HOLE_PCD}")
print(f"   OUTER_HOLE_COUNT = {spec.OUTER_HOLE_COUNT}")
print(f"   OUTER_HOLE_DIAMETER = {spec.OUTER_HOLE_DIAMETER}")
print(f"   OUTER_RING_DIAMETER = {spec.OUTER_RING_DIAMETER}")
print()

print("2. OVERALL DIMENSIONS CALCULATION:")
overall_dims = geom.calculate_overall_dimensions()
print(f"   overall_diameter = {overall_dims['overall_diameter']}")
print(f"   overall_radius = {overall_dims['overall_radius']}")
print(f"   outer_ring_center_radius = {overall_dims['outer_ring_center_radius']}")
print()

print("3. ANNOTATION TEXT GENERATION:")
# Simulate the annotation text generation
outer_annotation = f'{spec.OUTER_HOLE_COUNT}× ⌀{spec.OUTER_HOLE_DIAMETER} ON ⌀{spec.OUTER_HOLE_PCD} PCD'
overall_annotation = f'⌀{overall_dims["overall_diameter"]:.0f} OVERALL'

print(f"   Outer holes: '{outer_annotation}'")
print(f"   Overall: '{overall_annotation}'")
print()

print("4. HOLE COORDINATES:")
hole_coords = geom.calculate_hole_coordinates()
if len(hole_coords['outer']) > 0:
    print(f"   First outer hole: {hole_coords['outer'][0]}")
else:
    print("   Outer holes: NONE (removed)")
print(f"   Outer hole radius: {spec.OUTER_HOLE_PCD / 2.0}")
print()

print("5. CALCULATION BREAKDOWN:")
outer_ring_center_radius = spec.OUTER_HOLE_PCD / 2.0
ring_radius = spec.OUTER_RING_DIAMETER / 2.0
overall_radius = outer_ring_center_radius + ring_radius
overall_diameter = 2.0 * overall_radius

print(f"   outer_ring_center_radius = {spec.OUTER_HOLE_PCD}/2 = {outer_ring_center_radius}")
print(f"   ring_radius = {spec.OUTER_RING_DIAMETER}/2 = {ring_radius}")
print(f"   overall_radius = {outer_ring_center_radius} + {ring_radius} = {overall_radius}")
print(f"   overall_diameter = 2 * {overall_radius} = {overall_diameter}")
