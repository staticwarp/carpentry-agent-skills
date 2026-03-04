"""Roof Pitch Calculator Skill

Calculate roof pitch and rafter lengths:
- Pitch ratio (e.g., 4:12)
- Roof angle
- Rafter length
- Slope percentage

Based on myCarpentry.com formulas.
"""

import math
from dataclasses import dataclass


PI = 3.1416


@dataclass
class RoofPitchResult:
    """Results from roof pitch calculation."""
    pitch_ratio: str  # e.g., "4:12"
    rise_per_foot: float
    angle_degrees: float
    slope_percent: float
    rafter_length: float


def calculate(run_feet: float, rise_feet: float) -> RoofPitchResult:
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


def calculate_from_pitch(pitch: int, run_feet: float) -> RoofPitchResult:
    """Calculate roof pitch from pitch ratio (e.g., 4:12)."""
    rise_feet = (pitch / 12) * run_feet
    return calculate(run_feet, rise_feet)


def format_length(feet: float) -> str:
    """Format feet as feet-inches."""
    whole_feet = int(feet)
    inches = (feet - whole_feet) * 12
    
    if whole_feet > 0:
        return f"{whole_feet}' {inches:.1f}\""
    return f"{inches:.1f}\""


def solve(question: str) -> str:
    """Solve a roof pitch question from natural language."""
    import re
    
    rise_feet = 0.0
    run_feet = 0.0
    
    # Try "6 foot run and 2 foot rise"
    match = re.search(r'(\d+(?:\.\d+)?)\s*(?:foot|feet|ft|\')\s*(?:run|rise).*?(\d+(?:\.\d+)?)\s*(?:foot|feet|ft|\')', question)
    if match:
        run_feet = float(match.group(1))
        rise_feet = float(match.group(2))
    
    # Try "rise of X feet" and "run of Y feet"
    if rise_feet == 0 or run_feet == 0:
        rise_m = re.search(r'rise[:\s]+(\d+(?:\.\d+)?)\s*(?:foot|feet|ft|\')', question)
        run_m = re.search(r'run[:\s]+(\d+(?:\.\d+)?)\s*(?:foot|feet|ft|\')', question)
        
        if rise_m:
            rise_feet = float(rise_m.group(1))
        if run_m:
            run_feet = float(run_m.group(1))
    
    # Try X:12 format
    pitch_match = re.search(r'(\d+):12', question)
    if pitch_match and run_feet == 0:
        pitch = float(pitch_match.group(1))
        # Assume 12 foot run if not specified
        run_feet = 12
        rise_feet = (pitch / 12) * run_feet
    
    # Try just "4:12 pitch"
    if rise_feet == 0 or run_feet == 0:
        match = re.search(r'(\d+):12.*?(\d+(?:\.\d+)?)\s*(?:foot|feet|ft)', question)
        if match:
            pitch = float(match.group(1))
            run_feet = float(match.group(2))
            rise_feet = (pitch / 12) * run_feet
    
    if rise_feet == 0 or run_feet == 0:
        return "I need both rise and run. Try: 'roof pitch with 6 foot run and 2 foot rise'"
    
    result = calculate(run_feet, rise_feet)
    
    output = f"Roof Pitch Calculation:\n\n"
    output += f"Pitch: {result.pitch_ratio}\n"
    output += f"Angle: {result.angle_degrees:.1f}°\n"
    output += f"Slope: {result.slope_percent:.1f}%\n"
    output += f"Rafter length: {result.rafter_length:.2f} feet ({format_length(result.rafter_length)})\n"
    
    return output


# Common roof pitches for reference
COMMON_PITCHES = {
    "1:12": {"angle": 4.8, "use": "Low slope, shed roofs"},
    "2:12": {"angle": 9.5, "use": "Low slope"},
    "3:12": {"angle": 14.0, "use": "Minimum for shingles"},
    "4:12": {"angle": 18.4, "use": "Standard pitch"},
    "5:12": {"angle": 22.6, "use": "Good for snow/rain"},
    "6:12": {"angle": 26.6, "use": "Common in snow areas"},
    "7:12": {"angle": 30.3, "use": "Steep"},
    "8:12": {"angle": 33.7, "use": "Steep"},
    "9:12": {"angle": 36.9, "use": "Very steep"},
    "10:12": {"angle": 39.8, "use": "Very steep"},
    "12:12": {"angle": 45.0, "use": "45° - maximum walkable"},
}


if __name__ == "__main__":
    print(solve("What's the roof pitch with 6 feet of run and 2 feet of rise?"))
