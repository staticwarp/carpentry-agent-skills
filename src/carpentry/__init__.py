"""
Carpentry Agent Skills

Accurate carpentry calculations based on myCarpentry.com.

This package provides multiple skills for solving carpentry problems:

- stairs    : Stair rise, run, stringer calculations
- spacing   : Center items evenly (lights, outlets, cabinets)
- roof      : Roof pitch, rafter length calculations  
- concrete  : Cubic yards, bag quantities
- geometry  : Area, volume, diagonal, squaring

Usage:
    from carpentry import solve
    
    result = solve("How do I center 4 lights in a 73 inch space?")
"""

from .skills import (
    stairs,
    spacing,
    roof,
    concrete,
    geometry,
)

# Main solve function - routes to appropriate skill
def solve(question: str) -> str:
    """
    Solve a carpentry question.
    
    Automatically detects the type of question and routes to the
    appropriate skill.
    
    Args:
        question: Natural language question about carpentry
    
    Returns:
        Answer with calculations and measurements
    """
    q = question.lower()
    
    # Centering/spacing
    if any(kw in q for kw in ['center', 'space evenly', 'space equally', 'lights', 'outlets', 'cabinets']):
        return spacing.solve(question)
    
    # Stairs
    if any(kw in q for kw in ['stair', 'stairs', 'step', 'steps', 'stringer']):
        return stairs.solve(question)
    
    # Roof
    if any(kw in q for kw in ['roof', 'rafter', 'pitch']):
        return roof.solve(question)
    
    # Concrete
    if any(kw in q for kw in ['concrete', 'cubic', 'yard', 'slab', 'footing']):
        return concrete.solve(question)
    
    # Geometry
    if any(kw in q for kw in ['area', 'volume', 'diagonal', 'square', 'squaring']):
        return geometry.solve(question)
    
    # Default
    return """I didn't understand that question. Try asking about:

• Centering: "center 4 lights in 73 inches"
• Stairs: "stairs for 8 foot rise"  
• Roof: "roof pitch with 6 foot run"
• Concrete: "cubic yards for 12x12 slab"
• Geometry: "diagonal of 10x12 room"
"""


__all__ = [
    'solve',
    'stairs',
    'spacing', 
    'roof',
    'concrete',
    'geometry',
]
