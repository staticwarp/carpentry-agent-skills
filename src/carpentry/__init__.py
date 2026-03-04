"""
Carpentry Agent Skills

Accurate carpentry calculations based on myCarpentry.com.

This package provides multiple skills for solving carpentry problems:

- stairs    : Stair rise, run, stringer calculations
- spacing   : Center items evenly (lights, outlets, cabinets)
- roof      : Roof pitch, rafter length calculations  
- concrete  : Cubic yards, bag quantities
- geometry  : Area, volume, diagonal, squaring
- fractions : Decimal to fraction conversions
- arch      : Arch/elliptical layout calculations
- land_area : Convert acres, sq miles, sq meters, etc.
- span_tables : Joist and rafter span references

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
    fractions,
    arch,
    land_area,
    span_tables,
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
    
    # Fractions (must check before general math)
    if any(kw in q for kw in ['fraction', 'decimal to fraction', 'convert']):
        return fractions.solve(question)
    
    # Fraction math (add, subtract, multiply, divide fractions)
    if any(kw in q for kw in ['/ + - *', '1/4 +', '3/8 -', '1/2 *']) or \
       ('+' in q and '/' in q) or ('-' in q and '/' in q) or \
       ('×' in q) or ('÷' in q):
        return fractions.solve_math(question)
    
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
    
    # Arch
    if any(kw in q for kw in ['arch', 'ellipse', 'archway', 'arches']):
        return arch.solve(question)
    
    # Land area conversion
    if any(kw in q for kw in ['acre', 'hectare', 'sq mile', 'square meter', 'convert']):
        return land_area.solve(question)
    
    # Span tables
    if any(kw in q for kw in ['span', 'joist', 'rafter']):
        return span_tables.solve(question)
    
    # Default
    return """I didn't understand that question. Try asking about:

• Centering: "center 4 lights in 73 inches"
• Stairs: "stairs for 8 foot rise"  
• Roof: "roof pitch with 6 foot run"
• Concrete: "cubic yards for 12x12 slab"
• Geometry: "diagonal of 10x12 room"
• Fractions: "What is 0.375 as a fraction?"
• Arch: "arch for 8 foot wide and 4 foot tall"
• Land area: "How many acres is 5 square miles?"
• Spans: "How far can a 2x10 floor joist span?"
"""


__all__ = [
    'solve',
    'stairs',
    'spacing', 
    'roof',
    'concrete',
    'geometry',
    'fractions',
    'arch',
    'land_area',
    'span_tables',
]
