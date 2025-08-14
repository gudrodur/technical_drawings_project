# SPOOLING GUIDE PLATE
## Technical Specifications & Dimensional Documentation

**Drawing Scale**: 1:10  
**View**: 2D Technical Drawing - Side View  
**Drawing File**: `spooling_guide_plate.svg`  
**Generated**: August 2025

---

## OVERVIEW

The Spooling Guide Plate is a precision-engineered component featuring a simplified tapered arm design with comprehensive hole patterns for versatile mounting and assembly applications. The design incorporates a central opening with four symmetric arms extending outward to an outer ring assembly.

---

## MATERIAL SPECIFICATIONS

| Component | Material | Dimensions |
|-----------|----------|------------|
| **Main Plate** | 4mm Stainless Steel | Thickness: 4.0mm |
| **Outer Ring** | 10mm diameter Stainless Steel rod | Rod diameter: 10.0mm |
| **Finish** | Sharp as-cut | All edges |

---

## OVERALL DIMENSIONS

| Parameter | Dimension |
|-----------|-----------|
| **Overall Diameter** | ⌀1030mm |
| **Central Opening** | ⌀500mm (R250mm) |
| **Plate Thickness** | 4.0mm |
| **Outer Ring Position** | ⌀1020mm PCD |

---

## ARM GEOMETRY

### Basic Configuration
- **Arm Count**: 4 arms
- **Angular Spacing**: 90° (positioned at 0°, 90°, 180°, 270°)
- **Design**: Simplified tapered geometry with straight-line terminations

### Dimensional Specifications
| Parameter | Inner Radius | Outer Radius |
|-----------|--------------|--------------|
| **Arm Boundaries** | R250mm | R505mm |
| **Arm Width** | 50mm | 100mm |
| **Taper Type** | Linear progression from inner to outer |

### Arm Width Formula
```
W(r) = 50 + 50 × (r - 250) / 255
```
Where:
- W(r) = Width at radius r
- r = Distance from center (250mm ≤ r ≤ 505mm)

---

## HOLE PATTERNS & SPECIFICATIONS

### Central Pilot Hole
- **Quantity**: 1
- **Diameter**: ⌀30mm
- **Position**: Center (0, 0)
- **Purpose**: Central pilot/alignment hole

### Inner Hole Pattern
- **Quantity**: 8 holes
- **Diameter**: ⌀8mm each
- **Pattern**: Circular array on ⌀90mm PCD
- **Angular Spacing**: 45° intervals
- **Starting Position**: 0° (positive X-axis)
- **Purpose**: Primary mounting pattern

#### Inner Hole Coordinates (mm)
| Hole # | Angle | X-Coordinate | Y-Coordinate |
|--------|-------|--------------|--------------|
| 1 | 0° | 45.0 | 0.0 |
| 2 | 45° | 31.8 | 31.8 |
| 3 | 90° | 0.0 | 45.0 |
| 4 | 135° | -31.8 | 31.8 |
| 5 | 180° | -45.0 | 0.0 |
| 6 | 225° | -31.8 | -31.8 |
| 7 | 270° | 0.0 | -45.0 |
| 8 | 315° | 31.8 | -31.8 |

### Arm Centerline Holes
- **Quantity**: 4 holes
- **Diameter**: ⌀8mm each
- **Position**: R480mm from center
- **Alignment**: One hole per arm centerline
- **Offset**: 30mm inward from outer ring center
- **Purpose**: Secondary mounting/fastening points

#### Arm Centerline Hole Coordinates (mm)
| Hole # | Arm Angle | X-Coordinate | Y-Coordinate |
|--------|-----------|--------------|--------------|
| 1 | 0° | 480.0 | 0.0 |
| 2 | 90° | 0.0 | 480.0 |
| 3 | 180° | -480.0 | 0.0 |
| 4 | 270° | 0.0 | -480.0 |

### Hole Summary
| Pattern | Quantity | Diameter | Purpose |
|---------|----------|----------|---------|
| Central | 1 | ⌀30mm | Pilot/Alignment |
| Inner Ring | 8 | ⌀8mm | Primary Mounting |
| Arm Centerline | 4 | ⌀8mm | Secondary Mounting |
| **TOTAL** | **13** | **Mixed** | **Multi-purpose** |

---

## OUTER RING ASSEMBLY

### Ring Specifications
- **Material**: 10mm diameter Stainless Steel rod
- **Position**: Centered on ⌀1020mm PCD
- **Clearance**: Tangent to arm outer boundary (R505mm)
- **Weld Type**: Continuous fillet weld

### Ring Geometry
- **Ring Center Radius**: 510mm from plate center
- **Rod Diameter**: 10mm
- **Inner Edge**: R505mm (tangent to arms)
- **Outer Edge**: R515mm
- **Overall Assembly Diameter**: ⌀1030mm

---

## MANUFACTURING NOTES

### Fabrication Requirements
1. **Material**: 4mm Stainless Steel main plate
2. **Outer Ring**: 10mm diameter Stainless Steel rod
3. **Finish**: Sharp as-cut on all edges
4. **Welding**: Continuous fillet weld at outer ring
5. **Arm Geometry**: Simplified tapered design (no complex curves)

### Quality Control Points
- **Hole Alignment**: ±0.1mm positional tolerance
- **Hole Diameter**: +0.1/-0.0mm tolerance
- **Central Opening**: ⌀500mm ±0.5mm
- **Overall Diameter**: ⌀1030mm ±1.0mm
- **Plate Flatness**: ±0.5mm across diameter

### Assembly Notes
- Ring positioning critical for arm clearance
- Verify tangency at R505mm before welding
- All holes deburred and chamfered
- Final inspection of weld penetration

---

## DIMENSIONAL VERIFICATION

### Critical Measurements
| Dimension | Specification | Tolerance |
|-----------|---------------|-----------|
| Central Opening | ⌀500mm | ±0.5mm |
| Inner Hole PCD | ⌀90mm | ±0.1mm |
| Arm Centerline Holes | R480mm | ±0.2mm |
| Outer Ring PCD | ⌀1020mm | ±1.0mm |
| Overall Diameter | ⌀1030mm | ±1.0mm |
| Plate Thickness | 4.0mm | ±0.1mm |

---

## COORDINATE SYSTEM

**Reference**: Center of plate (0, 0)
- **X-Axis**: Horizontal, positive to the right
- **Y-Axis**: Vertical, positive upward
- **Angular Reference**: 0° = positive X-axis, increasing counter-clockwise
- **Units**: All dimensions in millimeters (mm)

---

## FILE INFORMATION

### Drawing Files
- **Vector**: `spooling_guide_plate.svg` (scalable vector graphics)
- **Raster**: `spooling_guide_plate.png` (300 DPI bitmap)
- **Documentation**: `SPOOLING_GUIDE_PLATE_README.md` (this file)

### Version Control
- **Repository**: technical_drawings_project
- **Component**: Spooling Guide Plate
- **Status**: Production Ready
- **Last Updated**: August 2025

---

## COMPATIBILITY NOTES

### Component Integration
- **Inner Hole Pattern**: Compatible with ⌀90mm PCD mounting systems
- **Arm Centerline Holes**: Suitable for secondary fastening applications
- **Central Opening**: Accommodates ⌀500mm maximum clearance requirement
- **Overall Assembly**: Designed for integration with larger spooling systems

### Assembly Sequence
1. Position main plate in assembly fixture
2. Verify hole alignment with mating components
3. Install fasteners through inner hole pattern
4. Secure arm centerline connections if required
5. Final torque verification per assembly specifications

---

*This documentation provides complete dimensional and manufacturing specifications for the Spooling Guide Plate component. All dimensions are derived from the mathematically precise technical drawing system and verified for manufacturing feasibility.*
