"""Spacing Skill - Center items evenly

Calculate measurements for evenly spacing items:
- Recessed lights
- Outlets
- Cabinets
- Any evenly-spaced fixtures

Example problems this solves:
- "How do I center 4 lights in a 73-inch space?"
- "Space 5 outlets on a 30-foot wall"
- "Center 3 cabinets (18\" wide) in a 72-inch opening"
"""

import math
from typing import Optional, Dict, List
from dataclasses import dataclass


@dataclass
class SpacingResult:
    """Results from spacing calculation."""
    num_items: int
    total_space: float
    spacing: float
    edge_to_first: float
    positions: List[Dict]


def center_items(
    num_items: int,
    total_space_inches: float,
    item_width_inches: Optional[float] = None
) -> SpacingResult:
    """
    Calculate spacing to center items evenly.
    
    Args:
        num_items: Number of items to center
        total_space_inches: Total available width
        item_width_inches: Width of each item (if fixed)
    
    Returns:
        SpacingResult with measurements
    """
    if item_width_inches:
        # Fixed-width items: calculate gaps
        total_item_width = item_width_inches * num_items
        remaining_space = total_space_inches - total_item_width
        gap = remaining_space / (num_items + 1)
        
        positions = []
        for i in range(num_items):
            start = gap + (i * (item_width_inches + gap))
            positions.append({
                "item": i + 1,
                "start": start,
                "center": start + item_width_inches / 2,
                "end": start + item_width_inches
            })
        
        return SpacingResult(
            num_items=num_items,
            total_space=total_space_inches,
            spacing=gap,
            edge_to_first=gap,
            positions=positions
        )
    else:
        # Just center points
        spacing = total_space_inches / (num_items + 1)
        
        positions = []
        for i in range(num_items):
            center = spacing * (i + 1)
            positions.append({
                "item": i + 1,
                "center": center
            })
        
        return SpacingResult(
            num_items=num_items,
            total_space=total_space_inches,
            spacing=spacing,
            edge_to_first=spacing / 2,
            positions=positions
        )


def _to_fraction(decimal: float) -> str:
    """Convert decimal to 1/32 fraction."""
    denominators = [2, 4, 8, 16, 32]
    closest = min(denominators, key=lambda d: abs((round(decimal * d) / d) - decimal))
    numerator = round(decimal * closest)
    
    if numerator == 0:
        return "0"
    if closest == 1:
        return str(numerator)
    return f"{numerator}/{closest}"


def format_measurement(inches: float) -> str:
    """Format inches with fraction."""
    feet = int(inches // 12)
    remaining = inches % 12
    frac = _to_fraction(remaining / 12)
    
    if feet > 0:
        return f"{feet}' {frac}\""
    return f"{frac}\""


def solve(question: str) -> str:
    """Solve a spacing question from natural language."""
    import re
    
    # Extract number of items
    num_match = re.search(r'(\d+)\s+(?:lights?|outlets?|items?|recessed|sconces?|can|cabinets?|posts?|plants?)', question)
    if not num_match:
        num_match = re.search(r'(?:center|space)\s+(\d+)', question)
    if not num_match:
        num_match = re.search(r'^(\d+)\s+in\s+a', question)
    
    if not num_match:
        return "I couldn't determine how many items. Try: 'center 4 lights in 73 inches'"
    
    num_items = int(num_match.group(1))
    
    # Extract total width
    total_space = 0.0
    
    # Try "73 inches", "73\""
    match = re.search(r'(\d+(?:\.\d+)?)\s*(?:inch|inches|in|")', question)
    if match:
        total_space = float(match.group(1))
    
    # Try "30-foot", "30 feet", "30'"
    if total_space == 0:
        match = re.search(r'(\d+(?:\.\d+)?)\s*(?:foot|feet|ft|\')', question)
        if match:
            total_space = float(match.group(1)) * 12
    
    if total_space == 0:
        return "I need the total space. Try: 'center 4 lights in 73 inches'"
    
    # Extract item width if mentioned
    item_width = None
    item_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:inch|inches|in|")\s*(?:wide|diameter)', question)
    if item_match:
        item_width = float(item_match.group(1))
    
    result = center_items(num_items, total_space, item_width)
    
    output = f"To center {num_items} item(s) in a {total_space}\" space:\n\n"
    
    if item_width:
        output += f"Item width: {item_width}\"\n"
        output += f"Gap between items: {format_measurement(result.spacing)}\n"
        output += f"Edge to first: {format_measurement(result.edge_to_first)}\n\n"
        output += "Measure from left edge:\n"
        for pos in result.positions:
            output += f"  Item {pos['item']}: {format_measurement(pos['center'])} on center\n"
    else:
        output += f"Spacing (center to center): {format_measurement(result.spacing)}\n"
        output += f"Edge to first: {format_measurement(result.edge_to_first)}\n\n"
        output += "Mark positions from left edge:\n"
        for pos in result.positions:
            output += f"  Item {pos['item']}: {format_measurement(pos['center'])} on center\n"
    
    return output


if __name__ == "__main__":
    print(solve("How do I center 4 lights in a 73-inch space?"))
