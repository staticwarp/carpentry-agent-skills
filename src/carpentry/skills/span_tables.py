"""Span Tables Skill

Reference for maximum joist and rafter spans.

Based on standard building codes and common lumber sizes.
This provides quick reference values - for precise engineering,
use the AWC Span Calculator at awc.org

Example problems:
- "How far can a 2x10 floor joist span?"
- "What's the max span for a 2x6 ceiling joist?"
- "Rafter span for 2x8 at 24 inch spacing"
"""

from dataclasses import dataclass
from typing import Optional


# Simplified span table (Southern Pine / Douglas Fir, #2, 40 psf live load)
# Values in feet
# Format: {size: {spacing: max_span}}
FLOOR_JOIST_SPANS = {
    "2x6": {"12": 12, "16": 10.5, "24": 9},
    "2x8": {"12": 16, "16": 14, "24": 11.5},
    "2x10": {"12": 20, "16": 18, "24": 14.5},
    "2x12": {"12": 24, "16": 21, "24": 17},
}

CEILING_JOIST_SPANS = {
    "2x4": {"12": 13, "16": 12, "24": 10},
    "2x6": {"12": 18, "16": 16, "24": 13},
    "2x8": {"12": 24, "16": 21, "24": 17},
    "2x10": {"12": 28, "16": 25, "24": 20},
}

RAFTER_SPANS = {
    # 30 psf snow load, standard exposure
    "2x4": {"12": 10, "16": 9, "24": 7},
    "2x6": {"12": 15, "16": 13, "24": 11},
    "2x8": {"12": 19, "16": 17, "24": 14},
    "2x10": {"12": 24, "16": 21, "24": 17},
    "2x12": {"12": 29, "16": 25, "24": 21},
}


@dataclass
class SpanResult:
    """Result of span lookup."""
    size: str
    spacing: str
    max_span: float
    span_type: str


def lookup_span(size: str, spacing: str, span_type: str = "floor") -> Optional[SpanResult]:
    """
    Look up maximum span for a given joist/rafter size.
    
    Args:
        size: Lumber size (e.g., "2x8", "2x10")
        spacing: On-center spacing (e.g., "12", "16", "24")
        span_type: "floor", "ceiling", or "rafter"
    
    Returns:
        SpanResult or None if not found
    """
    size = size.lower().replace(" ", "")
    spacing = str(spacing).replace('"', '').replace("in", "").replace("oc", "")
    
    if span_type == "floor":
        table = FLOOR_JOIST_SPANS
    elif span_type == "ceiling":
        table = CEILING_JOIST_SPANS
    elif span_type == "rafter":
        table = RAFTER_SPANS
    else:
        return None
    
    if size in table and spacing in table[size]:
        return SpanResult(
            size=size,
            spacing=spacing,
            max_span=table[size][spacing],
            span_type=span_type
        )
    
    return None


def format_span(feet: float) -> str:
    """Format span in feet-inches."""
    whole_feet = int(feet)
    inches = (feet - whole_feet) * 12
    
    if whole_feet > 0 and inches > 0:
        return f"{whole_feet}' {inounds:.1f}\""
    elif whole_feet > 0:
        return f"{whole_feet}'"
    else:
        return f"{inches:.1f}\""


def solve(question: str) -> str:
    """Solve a span table question."""
    import re
    
    question = question.lower()
    
    # Determine span type
    span_type = None
    if 'floor' in question or 'joist' in question:
        span_type = "floor"
    elif 'ceiling' in question:
        span_type = "ceiling"
    elif 'rafter' in question or 'roof' in question:
        span_type = "rafter"
    
    # Extract size
    size = None
    match = re.search(r'(2x[4-12])', question)
    if match:
        size = match.group(1)
    
    # Extract spacing
    spacing = None
    match = re.search(r'(\d+)\s*(?:inch|in|")?\s*(?:oc|on.center|on centre|spacing)', question)
    if match:
        spacing = match.group(1)
    
    # Try just the number if no "oc" mentioned
    if spacing is None:
        match = re.search(r'(?:at\s+)?(\d+)\s*(?:inch|in|")', question)
        if match:
            spacing = match.group(1)
    
    # Use 16" as default spacing
    if spacing is None:
        if '24' in question:
            spacing = "24"
        elif '12' in question:
            spacing = "12"
        else:
            spacing = "16"  # default
    
    if size is None:
        return "I need a lumber size. Try: 'How far can a 2x10 floor joist span?'"
    
    if span_type is None:
        # Try to infer from size
        if 'floor' in question:
            span_type = "floor"
        elif 'ceiling' in question:
            span_type = "ceiling"
        elif 'rafter' in question:
            span_type = "rafter"
        else:
            # Default to floor
            span_type = "floor"
    
    # Look up span
    result = lookup_span(size, spacing, span_type)
    
    if result is None:
        return f"Could not find span for {size} at {spacing}\" OC. Try common sizes: 2x6, 2x8, 2x10, 2x12"
    
    # Format spacing for display
    spacing_display = f"{result.spacing}\" on center (OC)"
    
    output = f"Maximum Span for {result.size} {result.span_type.capitalize()} Joist\n"
    output += f"at {spacing_display}\n\n"
    output += f"  Max Span: {result.max_span} feet\n"
    
    # Show all spacing options
    output += f"\nAll spacing options for {result.size}:\n"
    
    if span_type == "floor":
        table = FLOOR_JOIST_SPANS
    elif span_type == "ceiling":
        table = CEILING_JOIST_SPANS
    else:
        table = RAFTER_SPANS
    
    if size in table:
        for sp, span in table[size].items():
            output += f"  {sp}\" OC: {span} feet\n"
    
    # Notes
    output += "\n📋 Notes:\n"
    output += "- Based on Southern Pine or Douglas Fir, #2 grade\n"
    output += "- 40 psf live load for floor, 30 psf for ceiling\n"
    output += "- For snow loads or heavier loads, reduce span\n"
    output += "- Check local building codes\n"
    output += "- For precise engineering, use awc.org Span Calculator\n"
    
    return output


# Reference for common scenarios
SCENARIOS = {
    "deck_joist_16oc": "2x8 @ 16\" OC = 10' span (typical)",
    "deck_joist_24oc": "2x8 @ 24\" OC = 8' span",
    "floor_16oc": "2x10 @ 16\" OC = 15' span (common)",
    "ceiling_16oc": "2x6 @ 16\" OC = 16' span",
    "rafter_24oc": "2x8 @ 24\" OC = 14' span",
}


if __name__ == "__main__":
    print(solve("How far can a 2x10 floor joist span at 16 inch spacing?"))
