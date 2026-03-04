"""Concrete & Volume Calculator Skill

Calculate cubic yards for concrete, mulch, fill:
- Cubic feet/yards
- Concrete bag quantities
- Slabs, footings, columns

Example problems:
- "How many cubic yards for a 12x12 slab at 4 inches?"
- "Concrete for 6 footings 18 inches diameter, 24 inches deep"
"""

import math
from dataclasses import dataclass


PI = 3.1416


@dataclass
class ConcreteResult:
    """Results from concrete calculation."""
    cubic_feet: float
    cubic_yards: float
    square_feet: float
    depth_inches: float
    bags_80lb: int
    bags_60lb: int


def calculate_cubic_yards(
    length_feet: float,
    width_feet: float,
    depth_inches: float
) -> ConcreteResult:
    """
    Calculate cubic yards for a rectangular pour.
    
    Args:
        length_feet: Length in feet
        width_feet: Width in feet
        depth_inches: Depth in inches
    
    Returns:
        ConcreteResult with volume and bag quantities
    """
    depth_feet = depth_inches / 12
    cubic_feet = length_feet * width_feet * depth_feet
    cubic_yards = cubic_feet / 27
    
    bags_80lb = round(cubic_feet / 0.6)  # 80lb bag = 0.6 cu ft
    bags_60lb = round(cubic_feet / 0.45)  # 60lb bag = 0.45 cu ft
    
    return ConcreteResult(
        cubic_feet=round(cubic_feet, 2),
        cubic_yards=round(cubic_yards, 2),
        square_feet=length_feet * width_feet,
        depth_inches=depth_inches,
        bags_80lb=bags_80lb,
        bags_60lb=bags_60lb
    )


def calculate_cylinder(
    diameter_inches: float,
    depth_inches: float,
    quantity: int = 1
) -> ConcreteResult:
    """
    Calculate concrete for cylindrical forms (footings, columns).
    
    Args:
        diameter_inches: Diameter in inches
        depth_inches: Depth in inches
        quantity: Number of cylinders
    
    Returns:
        ConcreteResult
    """
    radius_feet = (diameter_inches / 2) / 12
    depth_feet = depth_inches / 12
    
    cubic_feet = PI * (radius_feet ** 2) * depth_feet * quantity
    cubic_yards = cubic_feet / 27
    
    bags_80lb = round(cubic_feet / 0.6)
    bags_60lb = round(cubic_feet / 0.45)
    
    return ConcreteResult(
        cubic_feet=round(cubic_feet, 2),
        cubic_yards=round(cubic_yards, 2),
        square_feet=0,  # N/A for cylinders
        depth_inches=depth_inches,
        bags_80lb=bags_80lb,
        bags_60lb=bags_60lb
    )


def solve(question: str) -> str:
    """Solve a concrete question from natural language."""
    import re
    
    # Check for footings/cylinders
    is_cylinder = 'footing' in question or 'column' in question or 'cylinder' in question
    
    if is_cylinder:
        return solve_cylinder(question)
    
    # Rectangular slab
    length = 0.0
    width = 0.0
    depth = 4.0  # default 4 inches
    
    # Try "12x12", "12 by 12"
    dims = re.findall(r'(\d+(?:\.\d+)?)\s*(?:x|by)\s*(\d+(?:\.\d+)?)', question)
    if dims:
        length = float(dims[0][0])
        width = float(dims[0][1])
    
    # Try feet first
    if length == 0:
        match = re.search(r'(\d+)\s*(?:foot|feet|ft)\s*(?:x|by)?\s*(\d+)\s*(?:foot|feet|ft)?', question)
        if match:
            length = float(match.group(1))
            width = float(match.group(2))
    
    # Look for depth
    depth_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:inch|inches|in|")\s*deep', question)
    if depth_match:
        depth = float(depth_match.group(1))
    else:
        # Check for common phrases
        if 'slab' in question:
            depth = 4  # default for slabs
        elif 'pad' in question or 'footer' in question:
            depth = 8  # default for footers
    
    if length == 0:
        return "I need dimensions. Try: 'cubic yards for a 12x12 slab at 4 inches deep'"
    
    result = calculate_cubic_yards(length, width, depth)
    
    output = f"Volume for {length}' x {width}' at {depth}\" deep:\n\n"
    output += f"Square footage: {result.square_feet} sq ft\n"
    output += f"Cubic feet: {result.cubic_feet}\n"
    output += f"Cubic yards: {result.cubic_yards}\n\n"
    output += "Concrete bags needed:\n"
    output += f"  80 lb bags: ~{result.bags_80lb}\n"
    output += f"  60 lb bags: ~{result.bags_60lb}\n"
    
    return output


def solve_cylinder(question: str) -> str:
    """Solve cylinder/footing concrete question."""
    import re
    
    # Extract diameter
    diameter = 0.0
    match = re.search(r'(\d+)\s*(?:inch|inches|in|")\s*(?:diameter|dia|wide)', question)
    if match:
        diameter = float(match.group(1))
    
    if diameter == 0:
        match = re.search(r'(\d+)\s*-?\s*inch', question)
        if match:
            diameter = float(match.group(1))
    
    # Extract depth
    depth = 24.0  # default
    match = re.search(r'(\d+)\s*(?:inch|inches|in|")\s*(?:deep|depth|deep)', question)
    if match:
        depth = float(match.group(1))
    
    # Extract quantity
    quantity = 1
    match = re.search(r'(\d+)\s*(?:footing|footings|column|columns)', question)
    if match:
        quantity = int(match.group(1))
    
    if diameter == 0:
        return "I need the diameter. Try: 'concrete for 6 footings 18 inches diameter'"
    
    result = calculate_cylinder(diameter, depth, quantity)
    
    output = f"Volume for {quantity} footing(s), {diameter}\" diameter x {depth}\" deep:\n\n"
    output += f"Cubic feet: {result.cubic_feet}\n"
    output += f"Cubic yards: {result.cubic_yards}\n\n"
    output += "Concrete bags needed:\n"
    output += f"  80 lb bags: ~{result.bags_80lb}\n"
    output += f"  60 lb bags: ~{result.bags_60lb}\n"
    
    # Per footing breakdown
    if quantity > 1:
        single = calculate_cylinder(diameter, depth, 1)
        output += f"\nPer footing: {single.cubic_feet} cu ft (~{single.bags_80lb} 80lb bags)"
    
    return output


# Common concrete thicknesses
COMMON_DEPTHS = {
    "4": "Standard slab, walkway",
    "5": "Heavy duty slab",
    "6": "Driveway, garage floor",
    "8": "Footer, thick slab",
    "12": "Heavy footer, pad",
}


if __name__ == "__main__":
    print(solve("How many cubic yards for a 12x12 slab at 4 inches deep?"))
