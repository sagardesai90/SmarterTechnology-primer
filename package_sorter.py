"""
Package Sorter for Smarter Technology's Robotic Automation Factory

Sorts packages into stacks based on volume and mass criteria.
Stacks: STANDARD (normal handling), SPECIAL (manual handling), REJECTED (both bulky & heavy).
"""

# Threshold constants for classification
BULKY_VOLUME_THRESHOLD = 1_000_000  # cm³ — volume at or above this is bulky
BULKY_DIMENSION_THRESHOLD = 150  # cm — any dimension at or above this is bulky
HEAVY_MASS_THRESHOLD = 20  # kg — mass at or above this is heavy


def sort(width: float, height: float, length: float, mass: float, verbose: bool = False) -> str:
    """
    Dispatch a package to the correct stack based on volume and mass.

    Args:
        width: Package width in centimeters
        height: Package height in centimeters
        length: Package length in centimeters
        mass: Package mass in kilograms
        verbose: If True, print debug output (default: False)

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

    if verbose:
        print(f"Package: {width}×{height}×{length} cm, mass={mass} kg")
        print(f"Volume: {volume:,.0f} cm³")
        print(f"Bulky: {is_bulky} (vol≥{BULKY_VOLUME_THRESHOLD:,} or dim≥{BULKY_DIMENSION_THRESHOLD})")
        print(f"Heavy: {is_heavy} (mass≥{HEAVY_MASS_THRESHOLD})")

    # Dispatch logic: REJECTED first (both), then SPECIAL (either), else STANDARD
    if is_bulky and is_heavy:
        if verbose:
            print("→ REJECTED")
        return "REJECTED"
    if is_bulky or is_heavy:
        if verbose:
            print("→ SPECIAL")
        return "SPECIAL"
    if verbose:
        print("→ STANDARD")
    return "STANDARD"


# Run example cases when executed directly (e.g. python package_sorter.py)
if __name__ == "__main__":
    # STANDARD: neither bulky nor heavy
    print("=== Example 1: STANDARD (small & light) ===")
    sort(10, 10, 10, 5, verbose=True)
    print()
    print("=== Example 2: STANDARD (near limits) ===")
    sort(149, 10, 10, 19, verbose=True)
    print()
    # SPECIAL: bulky OR heavy (but not both)
    print("=== Example 3: SPECIAL (bulky by volume) ===")
    sort(100, 100, 100, 10, verbose=True)
    print()
    print("=== Example 4: SPECIAL (bulky by dimension) ===")
    sort(150, 10, 10, 10, verbose=True)
    print()
    print("=== Example 5: SPECIAL (heavy only) ===")
    sort(10, 10, 10, 20, verbose=True)
    print()
    # REJECTED: both bulky AND heavy
    print("=== Example 6: REJECTED (bulky + heavy) ===")
    sort(100, 100, 100, 20, verbose=True)
