"""Land Area Calculator Skill

Convert between different land area measurements:
- Acres
- Square miles
- Square feet
- Square yards
- Square meters
- Hectares

Example problems:
- "How many acres is 5 square miles?"
- "Convert 10000 square feet to acres"
- "What's 2 hectares in acres?"
"""

import math
from dataclasses import dataclass
from typing import Optional


# Conversion factors (to square feet)
TO_SQ_FEET = {
    "sq_ft": 1,
    "sq_yd": 9,  # 1 sq yard = 9 sq ft
    "acre": 43560,  # 1 acre = 43,560 sq ft
    "sq_mile": 27878400,  # 1 sq mile = 27,878,400 sq ft
    "sq_m": 10.7639,  # 1 sq meter = 10.7639 sq ft
    "hectare": 107639,  # 1 hectare = 107,639 sq ft
}


@dataclass
class ConversionResult:
    """Result of area conversion."""
    value: float
    from_unit: str
    to_acres: float
    to_sq_ft: float
    to_sq_yd: float
    to_sq_mile: float
    to_sq_m: float
    to_hectare: float


def convert(value: float, from_unit: str) -> ConversionResult:
    """
    Convert an area value to all other units.
    
    Args:
        value: Numeric value
        from_unit: Unit of the input (sq_ft, sq_yd, acre, sq_mile, sq_m, hectare)
    
    Returns:
        ConversionResult with all conversions
    """
    # Normalize unit
    unit = from_unit.lower().replace(" ", "").replace("-", "_")
    
    # Handle various unit names
    unit_map = {
        "sqft": "sq_ft",
        "squarefeet": "sq_ft",
        "squarefoot": "sq_ft",
        "sqyd": "sq_yd",
        "squareyards": "sq_yd",
        "squareyard": "sq_yd",
        "acres": "acre",
        "acre": "acre",
        "sqmi": "sq_mile",
        "sqmile": "sq_mile",
        "squaremiles": "sq_mile",
        "sqm": "sq_m",
        "sqmeter": "sq_m",
        "squaremeters": "sq_m",
        "squaremeter": "sq_m",
        "ha": "hectare",
        "hectares": "hectare",
        "hectare": "hectare",
    }
    
    unit = unit_map.get(unit, unit)
    
    if unit not in TO_SQ_FEET:
        raise ValueError(f"Unknown unit: {from_unit}. Use: sq_ft, sq_yd, acre, sq_mile, sq_m, hectare")
    
    # Convert to sq ft first
    sq_ft = value * TO_SQ_FEET[unit]
    
    # Convert to all units
    return ConversionResult(
        value=value,
        from_unit=from_unit,
        to_acres=sq_ft / TO_SQ_FEET["acre"],
        to_sq_ft=sq_ft,
        to_sq_yd=sq_ft / TO_SQ_FEET["sq_yd"],
        to_sq_mile=sq_ft / TO_SQ_FEET["sq_mile"],
        to_sq_m=sq_ft / TO_SQ_FEET["sq_m"],
        to_hectare=sq_ft / TO_SQ_FEET["hectare"],
    )


def solve(question: str) -> str:
    """Solve a land area conversion question."""
    import re
    
    # Extract the number
    value = None
    match = re.search(r'(\d+(?:\.\d+)?)', question)
    if match:
        value = float(match.group(1))
    
    if value is None:
        return "I need a number. Try: 'How many acres is 5 square miles?'"
    
    # Determine the "from" unit
    unit = None
    
    if 'acre' in question.lower():
        unit = 'acre'
    elif 'sq mile' in question.lower() or 'square mile' in question.lower():
        unit = 'sq_mile'
    elif 'sq ft' in question.lower() or 'square foot' in question.lower() or 'square feet' in question.lower():
        unit = 'sq_ft'
    elif 'sq yd' in question.lower() or 'square yard' in question.lower():
        unit = 'sq_yd'
    elif 'sq m' in question.lower() or 'square meter' in question.lower():
        unit = 'sq_m'
    elif 'hectare' in question.lower() or 'ha' in question.lower():
        unit = 'hectare'
    
    if unit is None:
        # Try to infer from context
        return "I couldn't determine the unit. Try: 'convert 10000 square feet to acres'"
    
    try:
        result = convert(value, unit)
    except ValueError as e:
        return str(e)
    
    output = f"Converting {value} {result.from_unit}:\n\n"
    output += f"  Acres: {result.to_acres:.4f}\n"
    output += f"  Square feet: {result.to_sq_ft:,.2f}\n"
    output += f"  Square yards: {result.to_sq_yd:,.2f}\n"
    output += f"  Square miles: {result.to_sq_mile:.6f}\n"
    output += f"  Square meters: {result.to_sq_m:,.2f}\n"
    output += f"  Hectares: {result.to_hectare:.4f}\n"
    
    return output


def quick_convert(value: float, from_unit: str, to_unit: str) -> float:
    """
    Quick conversion between two specific units.
    
    Args:
        value: Value to convert
        from_unit: Source unit
        to_unit: Target unit
    
    Returns:
        Converted value
    """
    result = convert(value, from_unit)
    
    unit_map = {
        "acre": "to_acres",
        "sq_ft": "to_sq_ft",
        "sq_yd": "to_sq_yd",
        "sq_mile": "to_sq_mile",
        "sq_m": "to_sq_m",
        "hectare": "to_hectare",
    }
    
    attr = unit_map.get(to_unit.lower())
    if attr:
        return getattr(result, attr)
    
    return result.to_sq_ft


# Common land area references
REFERENCE = {
    "football_field": 1.322,  # acres (including end zones)
    "football_field_no_endzones": 1.1,  # acres
    "baseball_diamond": 0.043,  # acres (approx)
    "tennis_court": 0.003,  # acres (doubles)
    "parking_space": 0.002,  # acres (approx 90x180 ft)
    "lot_1_acre": 1.0,  # acres
    "city_block": 2.5,  # acres (typical)
}


if __name__ == "__main__":
    print(solve("How many acres is 5 square miles?"))
    print()
    print(solve("Convert 10000 square feet to acres"))
