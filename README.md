# Carpentry Agent Skills

**Because most AI tools are terrible at carpentry math.**

If you ask a typical AI "How do I center these 4 lights in a 73" space?", you're as likely to get a wrong answer or a joke as you are to get the correct solution. This skill fixes that.

This is an OpenClaw agent skill that provides accurate carpentry calculations based on [myCarpentry.com](https://www.mycarpentry.com/).

## What It Does

- **Stair Calculator** - Calculate rise, run, stringer length, angle, number of steps
- **Roof Pitch Calculator** - Calculate pitch, slope, rafter length
- **Span Tables** - Maximum spans for joists and rafters
- **Area/Volume Calculator** - Rectangles, triangles, circles, cylinders
- **Center Finding** - Accurately space items evenly in a given space
- **Framing Calculations** - Stud spacing, header sizes, etc.

## Installation

This is designed as an OpenClaw skill. Place it in your skills directory or clone:

```bash
git clone https://github.com/staticwarp/carpentry-agent-skills.git
```

## Usage

As an OpenClaw agent, you can ask questions like:

> "How do I center 4 recessed lights in a 73-inch wide room?"

> "I need to build stairs with an 8-foot total rise. What's the rise per step?"

> "What's the minimum size header for a 10-foot deck ledger?"

> "Calculate the roof pitch if my rafters have 6 feet of run and 2 feet of rise"

> "How many cubic yards of concrete do I need for a 12x12 patio slab?"

## Examples

### Centering Items

```
Q: How do I center 4 lights in a 73" space?

A: To center 4 items in 73 inches:
   - Spacing between centers: 73" / 4 = 18.25" (or 18 1/4")
   - Edge to first/last: 18.25" / 2 = 9.125" (or 9 1/8")
   
   Measurements from left edge:
   - Light 1: 9 1/8"
   - Light 2: 27 3/8" 
   - Light 3: 45 5/8"
   - Light 4: 63 7/8"
```

### Stair Calculator

```
Q: Build stairs for 10-foot deck height

A: Using standard residential proportions (7" rise, 11" run):
   - Total Rise: 120" (10 feet)
   - Number of Steps: 120 / 7 = 17.14 → 17 steps
   - Actual Rise per Step: 120 / 17 = 7.06" (7 1/16")
   - Total Run: 17 × 11" = 187" (15' 7")
   - Stringer Length: √(120² + 187²) = 221.8"
   - Stair Angle: arctan(120/187) = 32.7°
```

### Roof Pitch

```
Q: What's the roof pitch with 6' run and 2' rise?

A: - Roof Pitch: 4:12 (4" rise per 12" run)
   - Pitch Angle: arctan(2/6) = 18.4°
   - Rafter Length: √(6² + 2²) = 6.32' = 6' 3.9"
   - Slope: 33.3%
```

## Math Reference

### Pythagorean Theorem
- A² + B² = C²
- Used for: diagonal measurements, stringer length, rafter length

### 3-4-5 Rule
- 3 × 4 × 5 = right angle
- Use multiples: 6-8-10, 9-12-15, etc.

### Standard Measurements
- Stud spacing: 16" or 24" on center
- Riser height: 7" - 7.75" (max 7-3/4")
- Tread depth: 10" - 11" (min 10")
- Plywood sheets: 4' × 8'

## Project Structure

```
carpentry-agent-skills/
├── src/carpentry/
│   ├── __init__.py      # Main skill interface
│   ├── calculators.py   # All calculation functions
│   └── math_utils.py    # Basic math utilities
├── tests/               # Unit tests
├── examples/            # Example problems
└── README.md
```

## License

MIT
