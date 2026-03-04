# Carpentry Agent Skills

**Because most AI tools are terrible at carpentry math.**

If you ask a typical AI "How do I center these 4 lights in a 73" space?", you're as likely to get a wrong answer or a joke as you are to get the correct solution. This skill fixes that.

This is an OpenClaw agent skill that provides accurate carpentry calculations based on [myCarpentry.com](https://www.mycarpentry.com/).

## Skills

| Skill | File | What It Does | Example |
|-------|------|-------------|---------|
| `stairs` | `stairs.py` | Stair rise, run, stringer | "stairs for 8 foot rise" |
| `spacing` | `spacing.py` | Center items evenly | "center 4 lights in 73 inches" |
| `roof` | `roof.py` | Roof pitch, rafter length | "roof pitch with 6ft run" |
| `concrete` | `concrete.py` | Cubic yards, bags needed | "concrete for 12x12 slab" |
| `geometry` | `geometry.py` | Area, volume, diagonal | "diagonal of 10x12 room" |
| `fractions` | `fractions.py` | Decimal ↔ fraction conversion | "What is 0.375 as a fraction?" |
| `arch` | `arch.py` | Arch/ellipse layout | "arch for 8x4 opening" |
| `land_area` | `land_area.py` | Acre/sq mile conversions | "How many acres is 5 sq miles?" |
| `span_tables` | `span_tables.py` | Joist/rafter max spans10 floor joist | "2x span" |

## Installation

```bash
pip install -r requirements.txt
```

Or use as an OpenClaw skill.

## Usage

```python
from carpentry import solve

# Center items
print(solve("How do I center 4 lights in a 73 inch space?"))

# Stair calculations
print(solve("Build stairs for a 10 foot deck"))

# Roof pitch
print(solve("What's the roof pitch with 6 feet of run and 2 feet of rise?"))

# Concrete
print(solve("How many cubic yards for a 12x12 slab at 4 inches deep?"))

# Diagonal
print(solve("What's the diagonal of a 12x16 room?"))

# Fractions - convert decimals to tape measure fractions
print(solve("What is 0.375 as a fraction?"))
print(solve("1/4 + 3/8"))  # Fraction math!

# Arch layout
print(solve("Calculate arch for 8 foot wide and 4 foot tall"))

# Land area conversion
print(solve("How many acres is 5 square miles?"))

# Span tables
print(solve("How far can a 2x10 floor joist span at 16 inch spacing?"))
```

## Project Structure

```
carpentry-agent-skills/
├── src/carpentry/
│   ├── __init__.py          # Main interface + solve()
│   └── skills/
│       ├── __init__.py
│       ├── stairs.py        # Stair calculations
│       ├── spacing.py       # Center items evenly
│       ├── roof.py          # Roof pitch calculations
│       ├── concrete.py      # Concrete/volume
│       ├── geometry.py      # Area, volume, diagonal
│       ├── fractions.py     # Decimal ↔ fractions + math
│       ├── arch.py          # Arch/ellipse layout
│       ├── land_area.py     # Area conversions
│       └── span_tables.py   # Joist/rafter spans
├── examples/
│   └── problems.md          # Example problems
└── README.md
```

## Features

- **Precise calculations** - Uses actual formulas, not AI guessing
- **Fractional output** - Shows 1/32" precision (e.g., "9 1/8")
- **Natural language** - Parses "6 feet", "6'", "73 inches" automatically
- **Multiple skills** - Import only what you need, or use the main `solve()`
- **Fraction math** - Add, subtract, multiply, divide fractions

## Examples

### Centering Items

```
Q: How do I center 4 lights in a 73-inch space?

A: To center 4 item(s) in a 73.0" space:

   Spacing (center to center): 14.625" (14 5/8")
   Edge to first: 7.3125" (7 5/16")

   Mark positions from left edge:
     Light 1: 7 5/16" on center
     Light 2: 1' 7 15/16" on center
```

### Fractions (Tape Measure)

```
Q: What is 0.375 as a fraction?

A: Decimal: 0.375

   At 1/32" precision: 12/32" (3/8")
   At 1/16" precision: 6/16" (3/8")
   At 1/8" precision: 3/8"
   At 1/4" precision: 4/12" (1/4")
   At 1/2" precision: 4/8" (1/2")
```

### Fraction Math

```
Q: 1/4 + 3/8

A: 1/4 + 3/8 = 5/8
```

### Span Tables

```
Q: How far can a 2x10 floor joist span at 16 inch spacing?

A: Maximum Span for 2x10 Floor Joist
   at 16" on center (OC)

   Max Span: 18 feet

   All spacing options for 2x10:
     12" OC: 20 feet
     16" OC: 18 feet
     24" OC: 14.5 feet
```

## License

MIT
