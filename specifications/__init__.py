"""
Specifications Package
=====================

This package contains the Single Source of Truth (SSOT) for all component 
specifications and dimensions. Each module defines the complete dimensional 
data for one mechanical component.

Available Components:
- mounting_bracket: Mounting bracket for gunwale/roof attachment
- spooling_guide: (Future implementation)
- oblong_plate: (Future implementation)
"""

__version__ = "1.0.0"
__author__ = "Technical Drawing Generation System"

# Import all specification modules for easy access
from . import mounting_bracket

# List of available components
AVAILABLE_COMPONENTS = [
    'mounting_bracket',
    'spooling_guide',    # Future
    'oblong_plate'       # Future
]
