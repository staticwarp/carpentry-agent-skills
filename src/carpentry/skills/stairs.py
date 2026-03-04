"""Stair Calculator Skill

Calculate stair dimensions including:
- Number of steps
- Rise per step
- Run per step
- Stringer length
- Stair angle

Based on myCarpentry.com formulas.
"""

import math
from dataclasses import dataclass
from typing import Optional


# Standard constants
STANDARD_RISER = 7.0  # inches
STANDARD_TREAD = 11.0  # inches
MAX_RISER = 7.75  # inches (IRC code)
MIN_TREAD = 10.0  # inches


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
    angle_ratio: str  # e.g., "4:12"


def calculate(total_rise_inches: float, target_rise: Optional[float] = None) -> StairResult:
    """
    Calculate stair measurements.
    
    Args:
        total_rise_inches: Total height from bottom to top
        target_rise: Desired rise per step (optional)
    
    Returns:
        StairResult with all calculations
    """
    if target_rise:
        num_steps = round(total_rise_inches / target_rise)
        if num_steps < 1:
            num_steps = 1
        rise_per_step = total_rise_inches / num_steps
        run_per_step = STANDARD_TREAD
    else:
        # Use standard proportions
        num_steps = round(total_rise_inches / STANDARD_RISER)
        if num_steps < 1:
            num_steps = 1
        rise_per_step = total_rise_inches / num_steps
        run_per_step = STANDARD_TREAD
    
    total_run = num_steps * run_per_step
    stringer_length = math.sqrt(total_rise_inches ** 2 + total_run ** 2)
    angle_degrees = math.degrees(math.atan(total_rise_inches / total_run))
    
    # Ratio style (like roof pitch)
    rise_per_12 = (rise_per_step / run_per_step) * 12
    angle_ratio = f"{rise_per_12:.1f}:12"
    
    return StairResult(
        total_rise=total_rise_inches,
        total_run=total_run,
        num_steps=num_steps,
        rise_per_step=rise_per_step,
        run_per_step=run_per_step,
        stringer_length=stringer_length,
        angle_degrees=angle_degrees,
        angle_ratio=angle_ratio
    )


def format_inches(inches: float) -> str:
    """Format inches as feet-inches-fraction."""
    feet = int(inches // 12)
    remaining = inches % 12
    frac = _to_fraction(remaining / 12)
    
    if feet > 0:
        return f"{feet}' {frac}\""
    return f"{frac}\""


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


def solve(question: str) -> str:
    """Solve a stair question from natural language."""
    import re
    
    # Extract rise measurement
    rise_inches = 0.0
    
    # Try "8 foot rise", "8 feet", "8'"
    match = re.search(r'(\d+(?:\.\d+)?)\s*(?:foot|feet|ft|\')', question)
    if match:
        rise_inches = float(match.group(1)) * 12
    
    # Try "96 inches", "96\""
    if rise_inches == 0:
        match = re.search(r'(\d+)\s*(?:inch|inches|in|")', question)
        if match:
            rise_inches = float(match.group(1))
    
    if rise_inches == 0:
        return "I need the total rise. Try: 'stairs for 8 foot rise'"
    
    # Check for custom rise
    target_rise = None
    match = re.search(r'(\d+(?:\.\d+)?)\s*(?:inch|inches|in|")\s+(?:rise|riser)', question)
    if match:
        target_rise = float(match.group(1))
    
    result = calculate(rise_inches, target_rise)
    
    output = f"Stair Calculation for {format_inches(rise_inches)} total rise:\n\n"
    output += f"Number of steps: {result.num_steps}\n"
    output += f"Rise per step: {format_inches(result.rise_per_step)}\n"
    output += f"Run per step: {format_inches(result.run_per_step)}\n"
    output += f"Total run: {format_inches(result.total_run)}\n"
    output += f"Stringer length: {format_inches(result.stringer_length)}\n"
    output += f"Angle: {result.angle_degrees:.1f}° ({result.angle_ratio})\n"
    
    return output


if __name__ == "__main__":
    # Demo
    print(solve("stairs for 8 foot rise"))
