# Carpentry Agent Skills

**Because most AI tools are terrible at carpentry math.**

If you ask a typical AI "How do I center these 4 lights in a 73" space?", you're as likely to get a wrong answer or a joke as you are to get the correct solution. This skill fixes that.

This is an OpenClaw agent skill that provides accurate carpentry calculations based on [myCarpentry.com](https://www.mycarpentry.com/).

## Skills

| Skill | What It Does | Example |
|-------|-------------|---------|
| `stairs` | Stair rise, run, stringer | "stairs for 8 foot rise" |
| `spacing` | Center items evenly | "center 4 lights in 73 inches" |
| `roof` | Roof pitch, rafter length | "roof pitch with 6ft run" |
| `concrete` | Cubic yards, bags needed | "concrete for 12x12 slab" |
| `geometry` | Area, volume, diagonal | "diagonal of 10x12 room" |

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
```

## Project Structure

```
carpentry-agent-skills/
├── src/carpentry/
│   ├── __init__.py          # Main interface + solve()
│   ├── skills/
│   │   ├── __init__.py
│   │   ├── stairs.py        # Stair calculations
│   │   ├── spacing.py       # Center items evenly
│   │   ├── roof.py          # Roof pitch calculations
│   │   ├── concrete.py      # Concrete/volume
│   │   └── geometry.py      # Area, volume, diagonal
│   └── calculators.py       # (legacy, moving to skills/)
├── examples/
│   └── problems.md          # Example problems
└── README.md
```

## Features

- **Precise calculations** - Uses actual formulas, not AI guessing
- **Fractional output** - Shows 1/16" precision (e.g., "9 1/8")
- **Natural language** - Parses "6 feet", "6'", "73 inches" automatically
- **Multiple skills** - Import only what you need, or use the main `solve()`

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
     Light 3: 2' 6 9/16" on center
     Light 4: 3' 5 3/16" on center
```

### Stairs

```
Q: Build stairs for a 10-foot rise

A: Stair Calculation for 10' 0" total rise:

   Number of steps: 17
   Rise per step: 7 1/16"
   Run per step: 11"
   Total run: 15' 7"
   Stringer length: 18' 5 13/16"
   Angle: 32.7° (4:12)
```

### Roof Pitch

```
Q: What's the roof pitch with 6' run and 2' rise?

A: Roof Pitch Calculation:

   Pitch: 4:12
   Angle: 18.4°
   Slope: 33.3%
   Rafter length: 6.32 feet (6' 3.9")
```

## License

MIT
