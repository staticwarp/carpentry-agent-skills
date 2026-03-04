"""Arch Calculator Skill

Calculate arch/elliptical arch layouts for building archways.

The Arch Calculator calculates the position of the focus points of an ellipse,
based on the height and length of an ellipse, to determine the curve of an arch.

Example problems:
- "Calculate arch for 8 foot wide and 4 foot tall opening"
- "What's the arch focal points for a 6x3 arch?"
"""

import math
from dataclasses import dataclass
from typing import Optional


@dataclass
class ArchResult:
    """Results from arch calculation."""
    width: float  # Major axis (2a)
    height: float  # Minor axis (b)
    semi_major: float  # a
    semi_minor: float  # b
    focal_distance: float  # c = sqrt(a² - b²)
    focal_points: tuple  # Distance from center to each focus
    eccentricity: float  # e = c/a


def calculate(width_feet: float, height_feet: float) -> ArchResult:
    """
    Calculate arch/ellipse parameters.
    
    Args:
        width_feet: Total width of arch opening (major axis)
        height_feet: Height of arch (minor axis)
    
    Returns:
        ArchResult with calculations
    """
    # Semi-axes
    semi_major = width_feet / 2  # a
    semi_minor = height_feet  # b (from center to top)
    
    # Focal distance: c = sqrt(a² - b²)
    # This only works if a > b (ellipse, not circle)
    if semi_major > semi_minor:
        focal_distance = math.sqrt(semi_major**2 - semi_minor**2)
    else:
        # For tall/narrow arches, swap axes for calculation
        focal_distance = math.sqrt(semi_minor**2 - semi_major**2)
    
    # Focal points are at +/- c from center along major axis
    focal_points = (-focal_distance, focal_distance)
    
    # Eccentricity: e = c/a (how "stretched" the ellipse is)
    eccentricity = focal_distance / semi_major if semi_major > 0 else 0
    
    return ArchResult(
        width=width_feet,
        height=height_feet,
        semi_major=semi_major,
        semi_minor=semi_minor,
        focal_distance=focal_distance,
        focal_points=focal_points,
        eccentricity=eccentricity
    )


def layout_points(
    width_feet: float,
    height_feet: float,
    num_points: int = 16
) -> list:
    """
    Calculate points along the arch for layout.
    
    Returns a list of (x, y) coordinates for marking the arch curve.
    
    Args:
        width_feet: Total width
        height_feet: Height
        num_points: Number of points to calculate
    
    Returns:
        List of (distance from left, height) tuples in inches
    """
    result = calculate(width_feet, height_feet)
    a = result.semi_major
    b = result.semi_minor
    
    points = []
    
    for i in range(num_points + 1):
        # x goes from -a to +a (in feet)
        x = -a + (2 * a * i / num_points)
        
        # y = b * sqrt(1 - x²/a²) for upper half of ellipse
        if abs(x) < a:
            y = b * math.sqrt(1 - (x**2 / a**2))
        else:
            y = 0
        
        # Convert to inches from left edge
        x_inches = (x + a) * 12
        y_inches = y * 12
        
        points.append((round(x_inches, 2), round(y_inches, 2)))
    
    return points


def format_measurement(feet: float) -> str:
    """Format feet as feet-inches."""
    whole_feet = int(feet)
    inches = (feet - whole_feet) * 12
    
    if whole_feet > 0:
        return f"{whole_feet}' {inches:.1f}\""
    return f"{inches:.1f}\""


def solve(question: str) -> str:
    """Solve an arch calculation question."""
    import re
    
    width = 0.0
    height = 0.0
    
    # Try pattern like "8 foot wide and 4 foot tall"
    match = re.search(r'(\d+(?:\.\d+)?)\s*(?:foot|feet|ft)\s*(?:wide|width).*?(\d+(?:\.\d+)?)\s*(?:foot|feet|ft)\s*(?:tall|height)', question)
    if match:
        width = float(match.group(1))
        height = float(match.group(2))
    
    # Try "6x3" or "6 x 3"
    if width == 0:
        match = re.search(r'(\d+(?:\.\d+)?)\s*x\s*(\d+(?:\.\d+)?)', question)
        if match:
            width = float(match.group(1))
            height = float(match.group(2))
    
    # Try just widths and heights mentioned separately
    if width == 0:
        match = re.search(r'(\d+(?:\.\d+)?)\s*(?:foot|feet|ft).*?(?:width|wide)', question)
        if match:
            width = float(match.group(1))
    
    if height == 0:
        match = re.search(r'(\d+(?:\.\d+)?)\s*(?:foot|feet|ft).*?(?:height|tall)', question)
        if match:
            height = float(match.group(1))
    
    if width == 0 or height == 0:
        return "I need both width and height. Try: 'arch for 8 foot wide and 4 foot tall'"
    
    result = calculate(width, height)
    
    output = f"Arch Calculation for {width}' wide x {height}' tall opening:\n\n"
    output += f"Semi-major axis (half width): {format_measurement(result.semi_major)}\n"
    output += f"Semi-minor axis (height): {format_measurement(result.semi_minor)}\n"
    output += f"Focal distance: {format_measurement(result.focal_distance)}\n"
    output += f"Focal points from center: ±{format_measurement(result.focal_distance)}\n"
    output += f"Eccentricity: {result.eccentricity:.3f}\n\n"
    
    output += "Layout points (from left edge, at 12\" intervals):\n"
    points = layout_points(width, height, num_points=int(width))
    for x, y in points:
        output += f"  {x:5.1f}\" from left, {y:5.1f}\" up\n"
    
    output += "\nTo lay out the arch:\n"
    output += f"1. Mark focal points at {format_measurement(result.focal_distance)} on either side of center\n"
    output += "2. Drive nails at focal points\n"
    output += "3. Tie a string from one focal point to the edge, then to the other focal point\n"
    output += "4. The string length equals the major axis\n"
    output += "5. Trace the curve with the string pulled taut\n"
    
    return output


if __name__ == "__main__":
    print(solve("Calculate arch for 8 foot wide and 4 foot tall opening"))
