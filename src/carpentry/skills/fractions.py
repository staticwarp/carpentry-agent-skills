"""Fraction Calculator Skill

Convert decimal measurements to fractions (like on a tape measure).

This is one of the most useful carpentry math skills. Converts decimals
to the nearest 1/32" (or other precision) for easy reading on a tape measure.

Example problems:
- "What is 0.375 as a fraction?"
- "Convert 2.843 inches to fractions"
- "What is 3/16 + 1/8?"
"""

import math
from typing import Tuple, Optional
from dataclasses import dataclass


# Common denominators used on tape measures
TAPE_MEASURE_DENOMINATORS = [2, 4, 8, 16, 32, 64]


@dataclass
class FractionResult:
    """Result of decimal to fraction conversion."""
    decimal: float
    fraction: str
    nearest_32: str
    nearest_16: str
    nearest_8: str
    nearest_4: str
    nearest_2: str


def decimal_to_fraction(decimal: float, denominator: int = 32) -> Tuple[int, int]:
    """
    Convert decimal to fraction with given denominator.
    
    Args:
        decimal: Decimal value (e.g., 0.375)
        denominator: Target denominator (e.g., 32)
    
    Returns:
        Tuple of (numerator, denominator)
    """
    if denominator == 0:
        raise ValueError("Denominator cannot be zero")
    
    # Handle negative decimals
    sign = -1 if decimal < 0 else 1
    decimal = abs(decimal)
    
    # Separate whole and fractional parts
    whole = int(decimal)
    frac = decimal - whole
    
    # Calculate numerator
    numerator = round(frac * denominator)
    
    # Simplify if possible
    while numerator > 0 and numerator % 2 == 0 and denominator % 2 == 0:
        numerator //= 2
        denominator //= 2
    
    return sign * numerator, denominator


def format_fraction(numerator: int, denominator: int) -> str:
    """Format fraction as a string."""
    if denominator == 1:
        return str(numerator)
    if numerator == 0:
        return "0"
    if numerator == denominator:
        return "1"
    return f"{numerator}/{denominator}"


def format_inches(decimal_inches: float) -> str:
    """Format decimal inches as feet-inches-fraction."""
    sign = "-" if decimal_inches < 0 else ""
    decimal_inches = abs(decimal_inches)
    
    feet = int(decimal_inches // 12)
    inches = decimal_inches % 12
    
    whole_inches = int(inches)
    frac_inches = inches - whole_inches
    
    # Get fraction
    num, den = decimal_to_fraction(frac_inches, 32)
    
    # Build string
    parts = []
    if feet > 0:
        parts.append(f"{feet}'")
    if whole_inches > 0 or num == 0:
        parts.append(f"{whole_inches}")
    if num > 0:
        parts.append(f"{num}/{den}")
    if num > 0 and feet > 0:
        # Add the fraction part after inches
        return f"{sign}{feet}' {whole_inches} {num}/{den}\""
    elif whole_inches > 0:
        return f"{sign}{whole_inches} {num}/{den}\""
    elif num > 0:
        return f"{sign}{num}/{den}\""
    else:
        return f"{sign}0\""


def convert(decimal: float, precision: int = 32) -> FractionResult:
    """
    Convert decimal to fractions at multiple precisions.
    
    Args:
        decimal: Decimal value to convert
        precision: Target denominator (default 32)
    
    Returns:
        FractionResult with fractions at various precisions
    """
    # Calculate at different denominators
    results = {}
    for den in TAPE_MEASURE_DENOMINATORS:
        num, simplified_den = decimal_to_fraction(decimal, den)
        key = f"nearest_{den}"
        if den == 2:
            key = "nearest_2"
        elif den == 4:
            key = "nearest_4"
        elif den == 8:
            key = "nearest_8"
        elif den == 16:
            key = "nearest_16"
        elif den == 32:
            key = "nearest_32"
        
        if num == 0:
            results[key] = "0"
        elif simplified_den == 1:
            results[key] = str(num)
        else:
            results[key] = f"{num}/{simplified_den}"
    
    # At requested precision
    num, den = decimal_to_fraction(decimal, precision)
    if num == 0:
        fraction = "0"
    elif den == 1:
        fraction = str(num)
    else:
        fraction = f"{num}/{den}"
    
    return FractionResult(
        decimal=decimal,
        fraction=fraction,
        **results
    )


def solve(question: str) -> str:
    """Solve a fraction conversion question."""
    import re
    
    # Extract decimal number
    decimal = None
    
    # Try "0.375", "2.843"
    match = re.search(r'(\d+\.?\d*)', question)
    if match:
        decimal = float(match.group(1))
    
    if decimal is None:
        return "I need a decimal number. Try: 'What is 0.375 as a fraction?'"
    
    result = convert(decimal)
    
    output = f"Decimal: {result.decimal}\n\n"
    output += f"At 1/32\" precision: {result.nearest_32}\" (your tape measure)\n"
    output += f"At 1/16\" precision: {result.nearest_16}\"\n"
    output += f"At 1/8\" precision: {result.nearest_8}\"\n"
    output += f"At 1/4\" precision: {result.nearest_4}\"\n"
    output += f"At 1/2\" precision: {result.nearest_2}\"\n"
    
    # Also show as feet-inches
    if decimal > 12:
        output += f"\nAs feet-inches: {format_inches(decimal)}"
    
    return output


# === FRACTION MATH ===

def add_fractions(frac1: str, frac2: str) -> str:
    """Add two fractions. Examples: "1/4 + 3/8" or "1 1/4 + 2 3/8"."""
    n1, d1 = parse_fraction(frac1)
    n2, d2 = parse_fraction(frac2)
    
    # Common denominator
    lcm = math.lcm(d1, d2)
    n1 = n1 * (lcm // d1)
    n2 = n2 * (lcm // d2)
    
    result = n1 + n2
    return format_fraction_result(result, lcm)


def subtract_fractions(frac1: str, frac2: str) -> str:
    """Subtract fractions."""
    n1, d1 = parse_fraction(frac1)
    n2, d2 = parse_fraction(frac2)
    
    lcm = math.lcm(d1, d2)
    n1 = n1 * (lcm // d1)
    n2 = n2 * (lcm // d2)
    
    result = n1 - n2
    return format_fraction_result(result, lcm)


def multiply_fractions(frac1: str, frac2: str) -> str:
    """Multiply fractions."""
    n1, d1 = parse_fraction(frac1)
    n2, d2 = parse_fraction(frac2)
    
    result_num = n1 * n2
    result_den = d1 * d2
    
    return format_fraction_result(result_num, result_den)


def divide_fractions(frac1: str, frac2: str) -> str:
    """Divide fractions."""
    n1, d1 = parse_fraction(frac1)
    n2, d2 = parse_fraction(frac2)
    
    # Multiply by reciprocal
    result_num = n1 * d2
    result_den = d1 * n2
    
    return format_fraction_result(result_num, result_den)


def parse_fraction(frac_str: str) -> Tuple[int, int]:
    """Parse a fraction string like '1/4' or '1 1/4' into numerator/denominator."""
    frac_str = frac_str.strip()
    
    # Handle mixed numbers like "1 1/4"
    if ' ' in frac_str and '/' in frac_str:
        parts = frac_str.split()
        whole = int(parts[0])
        frac = parts[1]
        num, den = map(int, frac.split('/'))
        return whole * den + num, den
    
    # Handle simple fractions like "1/4"
    if '/' in frac_str:
        num, den = map(int, frac_str.split('/'))
        return num, den
    
    # Handle whole numbers
    return int(frac_str), 1


def format_fraction_result(numerator: int, denominator: int) -> str:
    """Format fraction result, converting improper to mixed."""
    if denominator == 0:
        return "undefined"
    
    # Simplify
    g = math.gcd(abs(numerator), abs(denominator))
    numerator //= g
    denominator //= g
    
    # Handle negative
    sign = "-" if (numerator < 0) != (denominator < 0) else ""
    numerator = abs(numerator)
    denominator = abs(denominator)
    
    whole = numerator // denominator
    remainder = numerator % denominator
    
    if whole == 0:
        if remainder == 0:
            return "0"
        return f"{sign}{remainder}/{denominator}"
    elif remainder == 0:
        return f"{sign}{whole}"
    else:
        return f"{sign}{whole} {remainder}/{denominator}"


def solve_math(question: str) -> str:
    """Solve a fraction math problem."""
    import re
    
    question = question.lower()
    
    # Addition
    match = re.search(r'(.+?)\s*\+\s*(.+)', question)
    if match:
        result = add_fractions(match.group(1).strip(), match.group(2).strip())
        return f"{match.group(1)} + {match.group(2)} = {result}"
    
    # Subtraction
    match = re.search(r'(.+?)\s*-\s*(.+)', question)
    if match:
        result = subtract_fractions(match.group(1).strip(), match.group(2).strip())
        return f"{match.group(1)} - {match.group(2)} = {result}"
    
    # Multiplication
    match = re.search(r'(.+?)\s*\*\s*(.+)', question)
    if match:
        result = multiply_fractions(match.group(1).strip(), match.group(2).strip())
        return f"{match.group(1)} × {match.group(2)} = {result}"
    
    # Division
    match = re.search(r'(.+?)\s*/\s*(.+)', question)
    if match:
        result = divide_fractions(match.group(1).strip(), match.group(2).strip())
        return f"{match.group(1)} ÷ {match.group(2)} = {result}"
    
    return "I didn't understand. Try formats like '1/4 + 3/8' or '1 1/2 * 2 3/4'"


# Quick reference table
QUICK_REFERENCE = {
    0.0625: "1/16",
    0.125: "1/8",
    0.1875: "3/16",
    0.25: "1/4",
    0.3125: "5/16",
    0.375: "3/8",
    0.4375: "7/16",
    0.5: "1/2",
    0.5625: "9/16",
    0.625: "5/8",
    0.6875: "11/16",
    0.75: "3/4",
    0.8125: "13/16",
    0.875: "7/8",
    0.9375: "15/16",
}


if __name__ == "__main__":
    print(solve("What is 0.375 as a fraction?"))
    print()
    print(solve_math("1/4 + 3/8"))
