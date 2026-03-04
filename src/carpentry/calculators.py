"""Carpentry calculators based on myCarpentry.com formulas."""

import math
from typing import Dict, Tuple, Optional
from dataclasses import dataclass


# Standard constants
PI = 3.1416
STANDARD_RISER_HEIGHT = 7.0  # inches
STANDARD_TREAD_DEPTH = 11.0  # inches
MAX_RISER_HEIGHT = 7.75  # inches (IRC code)
MIN_TREAD_DEPTH = 10.0  # inches


@dataclass
class StairResult:
    """Results from stair calculation."""
    total_rise: float
    total_run: float
    num_steps: int
    rise_per_step: float
    run_per_step: float
    stringer_length: float
    angle_degrees: float
    angle_inches: str  # e.g., "4:12"


@dataclass
class RoofPitchResult:
    """Results from roof pitch calculation."""
    pitch_ratio: str  # e.g., "4:12"
    rise_per_foot: float
    angle_degrees: float
    slope_percent: float
    rafter_length: float


def calculate_stairs(
    total_rise_inches: float,
    target_rise: Optional[float] = None,
    target_run: Optional[float] = None,
    use_standard: bool = True
) -> StairResult:
    """
    Calculate stair measurements.
    
    Args:
        total_rise_inches: Total height from bottom to top
        target_rise: Desired rise per step (if not using standard)
        target_run: Desired run per step (if not using standard)
        use_standard: Use standard 7" rise, 11" run
    
    Returns:
        StairResult with all calculations
    """
    if use_standard:
        # Calculate number of steps for standard rise
        num_steps = round(total_rise_inches / STANDARD_RISER_HEIGHT)
        if num_steps < 1:
            num_steps = 1
        rise_per_step = total_rise_inches / num_steps
        run_per_step = STANDARD_TREAD_DEPTH
    else:
        num_steps = round(total_rise_inches / target_rise)
        if num_steps < 1:
            num_steps = 1
        rise_per_step = total_rise_inches / num_steps
        run_per_step = target_run or STANDARD_TREAD_DEPTH
    
    total_run = num_steps * run_per_step
    stringer_length = math.sqrt(total_rise_inches ** 2 + total_run ** 2)
    angle_degrees = math.degrees(math.atan(total_rise_inches / total_run))
    
    # Convert to roof-pitch style ratio (rise per 12" run)
    rise_per_12_run = (rise_per_step / run_per_step) * 12
    angle_inches = f"{rise_per_12_run:.1f}:12"
    
    return StairResult(
        total_rise=total_rise_inches,
        total_run=total_run,
        num_steps=num_steps,
        rise_per_step=rise_per_step,
        run_per_step=run_per_step,
        stringer_length=stringer_length,
        angle_degrees=angle_degrees,
        angle_inches=angle_inches
    )


def calculate_roof_pitch(run_feet: float, rise_feet: float) -> RoofPitchResult:
    """
    Calculate roof pitch from rise and run.
    
    Args:
        run_feet: Horizontal run of rafter (in feet)
        rise_feet: Vertical rise of rafter (in feet)
    
    Returns:
        RoofPitchResult with pitch calculations
    """
    # Rise per 12" of run
    rise_per_12 = (rise_feet / run_feet) * 12
    pitch_ratio = f"{round(rise_per_12)}:12"
    
    # Angle in degrees
    angle_degrees = math.degrees(math.atan(rise_feet / run_feet))
    
    # Slope as percentage
    slope_percent = (rise_feet / run_feet) * 100
    
    # Rafter length (hypotenuse)
    rafter_length = math.sqrt(run_feet ** 2 + rise_feet ** 2)
    
    return RoofPitchResult(
        pitch_ratio=pitch_ratio,
        rise_per_foot=rise_per_12,
        angle_degrees=angle_degrees,
        slope_percent=slope_percent,
        rafter_length=rafter_length
    )


def center_items_in_space(
    num_items: int,
    total_width_inches: float,
    item_width_inches: Optional[float] = None
) -> Dict:
    """
    Calculate spacing to center items evenly in a space.
    
    Args:
        num_items: Number of items to center
        total_width_inches: Total available width
        item_width_inches: Width of each item (if fixed)
    
    Returns:
        Dictionary with spacing measurements
    """
    if item_width_inches:
        # Calculate gap between items
        total_item_width = item_width_inches * num_items
        remaining_space = total_width_inches - total_item_width
        gap = remaining_space / (num_items + 1)
        
        positions = []
        for i in range(num_items):
            pos = gap + (i * (item_width_inches + gap))
            positions.append({
                "item": i + 1,
                "start": pos,
                "center": pos + item_width_inches / 2,
                "end": pos + item_width_inches
            })
        
        return {
            "num_items": num_items,
            "total_space": total_width_inches,
            "item_width": item_width_inches,
            "gap_between_items": gap,
            "edge_to_first": gap,
            "positions": positions
        }
    else:
        # Just center points, no item width
        spacing = total_width_inches / (num_items + 1)
        
        positions = []
        for i in range(num_items):
            pos = spacing * (i + 1)
            positions.append({
                "item": i + 1,
                "center": pos
            })
        
        return {
            "num_items": num_items,
            "total_space": total_width_inches,
            "spacing_center_to_center": spacing,
            "edge_to_first": spacing / 2,
            "edge_to_last": spacing / 2,
            "positions": positions
        }


def calculate_cubic_yards(
    length_feet: float,
    width_feet: float,
    depth_inches: float
) -> Dict:
    """
    Calculate cubic yards for concrete, mulch, etc.
    
    Args:
        length_feet: Length in feet
        width_feet: Width in feet  
        depth_inches: Depth in inches
    
    Returns:
        Dictionary with volume calculations
    """
    depth_feet = depth_inches / 12
    cubic_feet = length_feet * width_feet * depth_feet
    cubic_yards = cubic_feet / 27
    
    # Also calculate 80lb bags of concrete (0.6 cu ft each)
    bags_80lb = cubic_feet / 0.6
    
    # 60lb bags (0.45 cu ft each)
    bags_60lb = cubic_feet / 0.45
    
    return {
        "cubic_feet": round(cubic_feet, 2),
        "cubic_yards": round(cubic_yards, 2),
        "square_feet": length_feet * width_feet,
        "depth_inches": depth_inches,
        "bags_80lb": round(bags_80lb),
        "bags_60lb": round(bags_60lb)
    }


def calculate_area_rectangle(length: float, width: float) -> float:
    """Calculate area of rectangle: A = L × W"""
    return length * width


def calculate_area_triangle(base: float, height: float) -> float:
    """Calculate area of triangle: A = 0.5 × B × H"""
    return 0.5 * base * height


def calculate_area_circle(radius: float) -> float:
    """Calculate area of circle: A = π × R²"""
    return PI * (radius ** 2)


def calculate_circumference(diameter: float) -> float:
    """Calculate circumference: C = π × D"""
    return PI * diameter


def calculate_volume_cylinder(radius: float, height: float) -> float:
    """Calculate volume of cylinder: V = π × R² × H"""
    return PI * (radius ** 2) * height


def calculate_volume_cube(length: float, width: float, height: float) -> float:
    """Calculate volume of rectangular prism: V = L × W × H"""
    return length * width * height


def calculate_area_trapezoid(
    length1: float,
    length2: float,
    height: float
) -> float:
    """Calculate area of trapezoid: A = 0.5 × (L1 + L2) × H"""
    return 0.5 * (length1 + length2) * height


def pythagorean(a: Optional[float] = None, b: Optional[float] = None, c: Optional[float] = None) -> float:
    """
    Pythagorean theorem: A² + B² = C²
    
    Pass any two values, get the third.
    
    Args:
        a: One leg of right triangle
        b: Other leg of right triangle  
        c: Hypotenuse
    
    Returns:
        The missing value
    """
    if c is not None and a is not None:
        # Find b
        return math.sqrt(c**2 - a**2)
    elif c is not None and b is not None:
        # Find a
        return math.sqrt(c**2 - b**2)
    elif a is not None and b is not None:
        # Find c
        return math.sqrt(a**2 + b**2)
    else:
        raise ValueError("Need at least two values to calculate the third")


def calculate_diagonal(length: float, width: float) -> float:
    """Calculate diagonal of rectangle (e.g., for squaring walls)."""
    return pythagorean(a=length, b=width)


def decimal_to_fraction(decimal: float) -> str:
    """Convert decimal to nearest 1/32 fraction."""
    # Common denominators
    denominators = [2, 4, 8, 16, 32]
    whole = int(decimal)
    frac = decimal - whole
    
    closest = min(denominators, key=lambda d: abs((round(frac * d) / d) - frac))
    numerator = round(frac * closest)
    
    if numerator == 0:
        return str(whole)
    elif whole == 0:
        return f"{numerator}/{closest}"
    else:
        return f"{whole} {numerator}/{closest}"


def format_measurement(inches: float, precision: float = 0.0625) -> str:
    """Format inches as feet-inches and fraction."""
    feet = int(inches // 12)
    remaining_inches = inches % 12
    
    frac = decimal_to_fraction(remaining_inches / 12)
    
    if feet > 0:
        return f"{feet}' {frac}\""
    else:
        return f"{frac}\""


# Example usage functions for common scenarios
def solve_lighting_spacing(
    num_lights: int,
    space_width_inches: float,
    light_width_inches: Optional[float] = None
) -> str:
    """
    Solve lighting spacing problem.
    
    Example: "How do I center 4 lights in a 73-inch space?"
    """
    result = center_items_in_space(num_lights, space_width_inches, light_width_inches)
    
    output = f"To center {num_lights} light(s) in a {space_width_inches}\" space:\n\n"
    
    if light_width_inches:
        output += f"- Light width: {light_width_inches}\"\n"
        output += f"- Gap between lights: {result['gap_between_items']:.3f}\" ({decimal_to_fraction(result['gap_between_items']/12)})\n"
        output += f"- Edge to first light: {result['edge_to_first']:.3f}\"\n\n"
        
        output += "Measure from left edge:\n"
        for pos in result['positions']:
            output += f"  Light {pos['item']}: {format_measurement(pos['center'])} on center\n"
    else:
        output += f"- Spacing (center to center): {result['spacing_center_to_center']:.3f}\"\n"
        output += f"- Edge to first: {result['edge_to_first']:.3f}\"\n\n"
        
        output += "Measure from left edge:\n"
        for pos in result['positions']:
            output += f"  Light {pos['item']}: {format_measurement(pos['center'])} on center\n"
    
    return output
