"""Geometry & Framing Skill

Basic carpentry geometry:
- Area calculations
- Volume calculations
- Diagonal/squaring
- Pythagorean theorem

Based on myCarpentry.com math formulas.
"""

import math


PI = 3.1416


# === AREA CALCULATIONS ===

def rectangle_area(length: float, width: float) -> float:
    """Area of rectangle: A = L × W"""
    return length * width


def triangle_area(base: float, height: float) -> float:
    """Area of triangle: A = 0.5 × B × H"""
    return 0.5 * base * height


def circle_area(radius: float) -> float:
    """Area of circle: A = π × R²"""
    return PI * (radius ** 2)


def trapezoid_area(length1: float, length2: float, height: float) -> float:
    """Area of trapezoid: A = 0.5 × (L1 + L2) × H"""
    return 0.5 * (length1 + length2) * height


# === VOLUME CALCULATIONS ===

def cube_volume(length: float, width: float, height: float) -> float:
    """Volume of rectangular prism: V = L × W × H"""
    return length * width * height


def cylinder_volume(radius: float, height: float) -> float:
    """Volume of cylinder: V = π × R² × H"""
    return PI * (radius ** 2) * height


def circumference(diameter: float) -> float:
    """Circumference of circle: C = π × D"""
    return PI * diameter


# === PYTHAGOREAN THEOREM ===

def pythagorean(a: float = None, b: float = None, c: float = None) -> float:
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
        return math.sqrt(c**2 - a**2)
    elif c is not None and b is not None:
        return math.sqrt(c**2 - b**2)
    elif a is not None and b is not None:
        return math.sqrt(a**2 + b**2)
    else:
        raise ValueError("Need at least two values")


def diagonal(length: float, width: float) -> float:
    """Calculate diagonal of rectangle (for squaring)."""
    return pythagorean(a=length, b=width)


# === FRAMING UTILITIES ===

# Standard stud spacing
STUD_SPACING = {
    "16": "16\" on center - standard interior/exterior",
    "24": "24\" on center - standard exterior, ceiling joists",
}

# Standard heights
STANDARD_HEIGHTS = {
    "wall": "8', 9', 10' (typical)",
    "door": "6'8\" (80\")",
    "window_sill": "36\" from floor (typical)",
}

# Plywood sizes
PLYWOOD = {
    "standard": "4' × 8' (32 sq ft)",
    "half": "4' × 4'",
    "full": "4' × 8'",
}


def format_measurement(inches: float) -> str:
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


# === SOLVE FUNCTIONS ===

def solve_area(question: str) -> str:
    """Solve area question."""
    import re
    
    dims = re.findall(r'(\d+(?:\.\d+)?)\s*(?:x|by)\s*(\d+(?:\.\d+)?)', question)
    if not dims:
        return "I need dimensions. Try: 'area of 10x12 room'"
    
    length = float(dims[0][0])
    width = float(dims[0][1])
    
    area = rectangle_area(length, width)
    return f"Area: {area} square feet"


def solve_volume(question: str) -> str:
    """Solve volume question."""
    import re
    
    # Try 3 dimensions
    match = re.search(r'(\d+(?:\.\d+)?)\s*x\s*(\d+(?:\.\d+)?)\s*x\s*(\d+(?:\.\d+)?)', question)
    if match:
        l, w, h = float(match.group(1)), float(match.group(2)), float(match.group(3))
        vol = cube_volume(l, w, h)
        return f"Volume: {vol} cubic feet"
    
    # Try 2 dimensions (assume 1 ft height)
    dims = re.findall(r'(\d+(?:\.\d+)?)\s*(?:x|by)\s*(\d+(?:\.\d+)?)', question)
    if dims:
        l, w = float(dims[0][0]), float(dims[0][1])
        vol = cube_volume(l, w, 1)
        return f"Volume: {vol} cubic feet (assuming 1' height)"
    
    return "I need dimensions. Try: 'volume of 10x10x8 space'"


def solve_diagonal(question: str) -> str:
    """Solve diagonal/squaring question."""
    import re
    
    dims = re.findall(r'(\d+(?:\.\d+)?)\s*(?:x|by)\s*(\d+(?:\.\d+)?)', question)
    if not dims:
        return "I need dimensions. Try: 'diagonal of 10x12 room'"
    
    length = float(dims[0][0])
    width = float(dims[0][1])
    
    diag = diagonal(length, width)
    
    output = f"Diagonal for {length}' x {width}' space:\n\n"
    output += f"Diagonal: {diag:.3f}' ({format_measurement(diag * 12)})\n\n"
    output += "For squaring corners, use 3-4-5 multiples:\n"
    output += f"  6-8-10, 9-12-15, 12-16-20, 15-20-25\n"
    output += f"\nYour measurement: {diag:.2f}' should match when perfectly square."
    
    return output


def solve(question: str) -> str:
    """Route to appropriate solver."""
    question = question.lower()
    
    if 'area' in question:
        return solve_area(question)
    elif 'volume' in question or 'cubic' in question:
        return solve_volume(question)
    elif 'diagonal' in question or 'square' in question:
        return solve_diagonal(question)
    else:
        return "Try asking about:\n- Area: 'area of 10x12 room'\n- Volume: 'volume of 10x10x8'\n- Diagonal: 'diagonal of 10x12 room'"


# 3-4-5 rule reference
THREE_FOUR_FIVE = [
    (3, 4, 5),
    (6, 8, 10),
    (9, 12, 15),
    (12, 16, 20),
    (15, 20, 25),
    (18, 24, 30),
]


if __name__ == "__main__":
    print(solve("What's the diagonal of a 10x12 room?"))
