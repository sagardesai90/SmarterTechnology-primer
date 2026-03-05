"""
Package Sorter for Smarter Technology's Robotic Automation Factory

Sorts packages into stacks based on volume and mass criteria.
Stacks: STANDARD (normal handling), SPECIAL (manual handling), REJECTED (both bulky & heavy).
"""

# Threshold constants for classification
BULKY_VOLUME_THRESHOLD = 1_000_000  # cm³ — volume at or above this is bulky
BULKY_DIMENSION_THRESHOLD = 150  # cm — any dimension at or above this is bulky
HEAVY_MASS_THRESHOLD = 20  # kg — mass at or above this is heavy


def sort(width: float, height: float, length: float, mass: float) -> str:
    """
    Dispatch a package to the correct stack based on volume and mass.

    Args:
        width: Package width in centimeters
        height: Package height in centimeters
        length: Package length in centimeters
        mass: Package mass in kilograms

    Returns:
        Stack name: "STANDARD", "SPECIAL", or "REJECTED"
    """
    # Compute volume (Width × Height × Length)
    volume = width * height * length

    # Bulky: volume ≥ 1M cm³ OR any dimension ≥ 150 cm
    is_bulky = (
        volume >= BULKY_VOLUME_THRESHOLD
        or width >= BULKY_DIMENSION_THRESHOLD
        or height >= BULKY_DIMENSION_THRESHOLD
        or length >= BULKY_DIMENSION_THRESHOLD
    )
    # Heavy: mass ≥ 20 kg
    is_heavy = mass >= HEAVY_MASS_THRESHOLD

    # Dispatch logic: REJECTED first (both), then SPECIAL (either), else STANDARD
    if is_bulky and is_heavy:
        return "REJECTED"
    if is_bulky or is_heavy:
        return "SPECIAL"
    return "STANDARD"


# Run example cases when executed directly (e.g. python package_sorter.py)
if __name__ == "__main__":
    examples = [
        ((10, 10, 10, 5), "STANDARD (small & light)"),
        ((149, 10, 10, 19), "STANDARD (near limits)"),
        ((100, 100, 100, 10), "SPECIAL (bulky by volume)"),
        ((150, 10, 10, 10), "SPECIAL (bulky by dimension)"),
        ((10, 10, 10, 20), "SPECIAL (heavy only)"),
        ((100, 100, 100, 20), "REJECTED (bulky + heavy)"),
    ]
    for (w, h, l, m), label in examples:
        result = sort(w, h, l, m)
        print(f"sort{w, h, l, m} → {result}  ({label})")
