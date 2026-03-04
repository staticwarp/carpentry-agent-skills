"""
Carpentry Agent Skill

This skill provides accurate carpentry calculations. Unlike general AI tools
that often give wrong answers or joke about carpentry math, this skill uses
precise formulas based on myCarpentry.com.

Usage:
    from carpentry import solve
    
    result = solve("How do I center 4 lights in a 73 inch space?")
    print(result)
"""

from .calculators import (
    calculate_stairs,
    calculate_roof_pitch,
    center_items_in_space,
    calculate_cubic_yards,
    solve_lighting_spacing,
    pythagorean,
    calculate_diagonal,
    decimal_to_fraction,
    format_measurement,
    # Basic shapes
    calculate_area_rectangle,
    calculate_area_triangle,
    calculate_area_circle,
    calculate_circumference,
    calculate_volume_cylinder,
    calculate_volume_cube,
    calculate_area_trapezoid,
)

# For backwards compatibility
from .calculators import (
    calculate_stairs as stairs,
    calculate_roof_pitch as roof_pitch,
    center_items_in_space as center_items,
    calculate_cubic_yards as cubic_yards,
)


def parse_measurement(text: str) -> float:
    """
    Parse common measurement formats to inches.
    
    Examples:
        - "73 inches" -> 73.0
        - "6 feet" -> 72.0
        - "6'" -> 72.0
        - "6' 3\"" -> 75.0
        - "10 foot" -> 120.0
    """
    import re
    
    text = text.lower().strip()
    total_inches = 0.0
    
    # Pattern for feet and inches: 6' 3" or 6 feet 3 inches
    feet_match = re.search(r"(\d+)\s*(?:foot|feet|ft|')", text)
    inches_match = re.search(r"(\d+)\s*(?:inch|inches|in|\")", text)
    
    # Just a number (assume inches)
    just_number = re.search(r"^(\d+(?:\.\d+)?)\s*$", text)
    
    if feet_match:
        total_inches += float(feet_match.group(1)) * 12
    
    if inches_match:
        total_inches += float(inches_match.group(1))
    
    if not feet_match and not inches_match and just_number:
        return float(just_number.group(1))
    
    if feet_match or inches_match:
        return total_inches
    
    # Try parsing as decimal inches
    try:
        return float(text.strip('"\''))
    except ValueError:
        return 0.0


def parse_number(text: str) -> float:
    """Parse a number from text."""
    import re
    text = text.lower()
    
    # Handle fractions like "1/4", "3/8"
    if '/' in text:
        parts = text.split('/')
        if len(parts) == 2:
            try:
                num, denom = float(parts[0]), float(parts[1])
                return num / denom
            except:
                pass
    
    # Handle "4:12" style ratios (for roof pitch)
    if ':' in text:
        parts = text.split(':')
        try:
            return float(parts[0].strip())
        except:
            pass
    
    # Try direct conversion
    try:
        return float(text)
    except ValueError:
        return 0.0


def solve(question: str) -> str:
    """
    Solve a carpentry question.
    
    Args:
        question: Natural language question about carpentry
    
    Returns:
        Answer with calculations and measurements
    """
    question = question.lower()
    
    # Centering items (lights, outlets, etc.)
    if 'center' in question or 'space evenly' in question or 'space equally' in question:
        return solve_centering(question)
    
    # Stairs
    if 'stair' in question or 'steps' in question:
        return solve_stairs(question)
    
    # Roof pitch
    if 'roof pitch' in question or 'rafter' in question:
        return solve_roof_pitch(question)
    
    # Cubic yards / concrete
    if 'cubic' in question or 'concrete' in question or 'yard' in question:
        return solve_cubic(question)
    
    # Diagonal / square
    if 'diagonal' in question or 'square' in question:
        return solve_diagonal(question)
    
    # Area
    if 'area' in question:
        return solve_area(question)
    
    # Volume
    if 'volume' in question or 'how much' in question:
        return solve_volume(question)
    
    return "I didn't understand that question. Try asking about:\n- Centering items (e.g., 'center 4 lights in 73 inches')\n- Stairs (e.g., 'stairs for 8 foot rise')\n- Roof pitch (e.g., 'roof pitch with 6 foot run')\n- Concrete (e.g., 'cubic yards for 12x12 slab')"


def solve_centering(question: str) -> str:
    """Solve centering/spacing problems."""
    import re
    
    # Extract number of items
    num_match = re.search(r'(\d+)\s+(?:lights?|outlets?|items?|recessed|sconces?|can)', question)
    if not num_match:
        num_match = re.search(r'(?:center|space)\s+(\d+)', question)
    if not num_match:
        num_match = re.search(r'(\d+)\s+in\s+a', question)
    
    if not num_match:
        return "I couldn't determine how many items you're trying to center. Please specify the number."
    
    num_items = int(num_match.group(1))
    
    # Extract width
    width_inches = parse_measurement(question)
    if width_inches == 0:
        # Try to find measurement
        numbers = re.findall(r'(\d+(?:\.\d+)?)\s*(?:inch|in|")', question)
        if numbers:
            width_inches = float(numbers[0])
        else:
            return "I couldn't determine the total width. Please specify (e.g., 'in a 73 inch space')."
    
    # Extract item width if mentioned
    item_width = None
    item_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:inch|in|")\s+(?:wide|diameter|size)', question)
    if item_match:
        item_width = float(item_match.group(1))
    
    result = center_items_in_space(num_items, width_inches, item_width)
    
    output = f"To center {num_items} item(s) in a {width_inches}\" space:\n\n"
    
    if item_width:
        output += f"Item width: {item_width}\"\n"
        output += f"Gap between items: {decimal_to_fraction(result['gap_between_items']/12)}\"\n"
        output += f"Edge to first item: {decimal_to_fraction(result['edge_to_first']/12)}\"\n\n"
        output += "Measure from left edge:\n"
        for pos in result['positions']:
            center = format_measurement(pos['center'])
            output += f"  Item {pos['item']}: {center} on center\n"
    else:
        output += f"Spacing (center to center): {decimal_to_fraction(result['spacing_center_to_center']/12)}\"\n"
        output += f"Edge to first: {decimal_to_fraction(result['edge_to_first']/12)}\"\n\n"
        output += "Mark positions from left edge:\n"
        for pos in result['positions']:
            center = format_measurement(pos['center'])
            output += f"  Item {pos['item']}: {center} on center\n"
    
    return output


def solve_stairs(question: str) -> str:
    """Solve stair calculations."""
    import re
    
    # Extract total rise
    rise = parse_measurement(question)
    if rise == 0:
        # Try other patterns
        match = re.search(r'(\d+(?:\.\d+)?)\s*(?:foot|feet|ft)', question)
        if match:
            rise = float(match.group(1)) * 12
    
    if rise == 0:
        return "I couldn't determine the total rise. Please specify (e.g., 'stairs for 8 foot rise')."
    
    result = calculate_stairs(rise)
    
    output = f"Stair Calculation for {format_measurement(rise)} total rise:\n\n"
    output += f"Number of steps: {result.num_steps}\n"
    output += f"Rise per step: {format_measurement(result.rise_per_step)}\n"
    output += f"Run per step: {format_measurement(result.run_per_step)}\n"
    output += f"Total run: {format_measurement(result.total_run)}\n"
    output += f"Stringer length: {format_measurement(result.stringer_length)}\n"
    output += f"Angle: {result.angle_degrees:.1f}° ({result.angle_inches})\n"
    
    return output


def solve_roof_pitch(question: str) -> str:
    """Solve roof pitch calculations."""
    import re
    
    # Extract rise and run
    rise_feet = 0.0
    run_feet = 0.0
    
    # Try various patterns
    rise_match = re.search(r'(\d+)\s*[\'f]oot.*?(\d+)\s*[\'f]oot', question)
    if rise_match:
        rise_feet = float(rise_match.group(1))
        run_feet = float(rise_match.group(2))
    else:
        # Try "rise of X feet" and "run of Y feet"
        rise_m = re.search(r'rise[:\s]+(\d+(?:\.\d+)?)\s*(?:foot|feet|ft|\')', question)
        run_m = re.search(r'run[:\s]+(\d+(?:\.\d+)?)\s*(?:foot|feet|ft|\')', question)
        
        if rise_m:
            rise_feet = float(rise_m.group(1))
        if run_m:
            run_feet = float(run_m.group(1))
    
    # Also check for X:12 format
    pitch_match = re.search(r'(\d+):12', question)
    if pitch_match and rise_feet == 0:
        # Convert pitch to rise/run
        pitch = float(pitch_match.group(1))
        # Ask for run if not provided
        if run_feet == 0:
            # Assume standard run and calculate rise
            run_feet = 12  # per foot
            rise_feet = pitch
    
    if rise_feet == 0 or run_feet == 0:
        return "I need both rise and run values. Try: 'roof pitch with 6 foot run and 2 foot rise'"
    
    result = calculate_roof_pitch(run_feet, rise_feet)
    
    output = f"Roof Pitch Calculation:\n\n"
    output += f"Pitch: {result.pitch_ratio}\n"
    output += f"Angle: {result.angle_degrees:.1f}°\n"
    output += f"Slope: {result.slope_percent:.1f}%\n"
    output += f"Rafter length: {result.rafter_length:.2f} feet\n"
    
    return output


def solve_cubic(question: str) -> str:
    """Solve cubic yard / concrete calculations."""
    import re
    
    # Extract dimensions
    length = 0.0
    width = 0.0
    depth = 4.0  # default 4 inches
    
    # Look for dimensions
    dims = re.findall(r'(\d+(?:\.\d+)?)\s*(?:x|by)\s*(\d+(?:\.\d+)?)', question)
    
    if dims:
        length = float(dims[0][0])
        width = float(dims[0][1])
    
    # Look for depth
    depth_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:inch|in|")', question)
    if depth_match:
        depth = float(depth_match.group(1))
    
    if length == 0:
        return "I need dimensions. Try: 'cubic yards for a 12x12 slab' or 'concrete for 10x10 at 4 inches deep'"
    
    result = calculate_cubic_yards(length, width, depth)
    
    output = f"Volume Calculation for {length}' x {width}' at {depth}\" deep:\n\n"
    output += f"Cubic feet: {result['cubic_feet']}\n"
    output += f"Cubic yards: {result['cubic_yards']}\n"
    output += f"\nConcrete bags needed:\n"
    output += f"  80 lb bags: ~{result['bags_80lb']}\n"
    output += f"  60 lb bags: ~{result['bags_60lb']}\n"
    
    return output


def solve_diagonal(question: str) -> str:
    """Solve diagonal/squaring problems."""
    import re
    
    length = 0.0
    width = 0.0
    
    dims = re.findall(r'(\d+(?:\.\d+)?)\s*(?:x|by)\s*(\d+(?:\.\d+)?)', question)
    if dims:
        length = float(dims[0][0])
        width = float(dims[0][1])
    
    if length == 0 or width == 0:
        return "I need both length and width. Try: 'diagonal of 10x12 room'"
    
    diagonal = calculate_diagonal(length, width)
    
    output = f"Diagonal for {length}' x {width}' space:\n\n"
    output += f"Diagonal: {diagonal:.3f}' ({format_measurement(diagonal * 12)})\n\n"
    output += "This is how far apart your marks should be when squaring corners.\n"
    output += "Use 3-4-5 multiples: e.g., 6-8-10, 9-12-15, 12-16-20"
    
    return output


def solve_area(question: str) -> str:
    """Solve area calculations."""
    import re
    
    length = 0.0
    width = 0.0
    
    dims = re.findall(r'(\d+(?:\.\d+)?)\s*(?:x|by)\s*(\d+(?:\.\d+)?)', question)
    if dims:
        length = float(dims[0][0])
        width = float(dims[0][1])
    
    if length == 0 or width == 0:
        return "I need dimensions. Try: 'area of 10x12 room'"
    
    area = calculate_area_rectangle(length, width)
    
    return f"Area: {area} square feet"


def solve_volume(question: str) -> str:
    """Solve volume calculations."""
    import re
    
    length = 0.0
    width = 0.0
    height = 0.0
    
    dims = re.findall(r'(\d+(?:\.\d+)?)\s*(?:x|by)\s*(\d+(?:\.\d+)?)', question)
    if dims:
        length = float(dims[0][0])
        width = float(dims[0][1])
    
    height_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:x|by)\s*(\d+(?:\.\d+)?)\s*(?:x|by)\s*(\d+(?:\.\d+)?)', question)
    if height_match:
        length = float(height_match.group(1))
        width = float(height_match.group(2))
        height = float(height_match.group(3))
    
    if height == 0:
        height = 1  # Assume 1 foot if not specified, treat as area
    
    if length == 0 or width == 0:
        return "I need dimensions. Try: 'volume of 10x10x8 space'"
    
    volume = calculate_volume_cube(length, width, height)
    
    return f"Volume: {volume} cubic feet"


__all__ = [
    'solve',
    'calculate_stairs',
    'calculate_roof_pitch',
    'center_items_in_space',
    'calculate_cubic_yards',
    'solve_lighting_spacing',
    'pythagorean',
    'calculate_diagonal',
    'decimal_to_fraction',
    'format_measurement',
]
