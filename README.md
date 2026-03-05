# Package Sorter — Smarter Technology Technical Screen

A robotic arm package dispatcher that sorts packages into stacks based on volume and mass.

## Quick Start

```bash
git clone https://github.com/sagardesai90/SmarterTechnology-primer.git
cd SmarterTechnology-primer
python -m unittest test_package_sorter -v
python package_sorter.py   # run examples
```

## Rules

| Criteria | Definition |
|----------|------------|
| **Bulky** | Volume (W × H × L) ≥ 1,000,000 cm³ **or** any dimension ≥ 150 cm |
| **Heavy** | Mass ≥ 20 kg |

| Stack | Condition |
|-------|-----------|
| **STANDARD** | Neither bulky nor heavy |
| **SPECIAL** | Bulky **or** heavy (but not both) |
| **REJECTED** | Both bulky **and** heavy |

## Usage

```python
from package_sorter import sort

# Standard package: small and light
sort(10, 10, 10, 5)  # → "STANDARD"

# Special: bulky only (volume = 1,000,000)
sort(100, 100, 100, 10)  # → "SPECIAL"

# Special: heavy only
sort(10, 10, 10, 20)  # → "SPECIAL"

# Rejected: both bulky and heavy
sort(100, 100, 100, 20)  # → "REJECTED"
```

## Run Tests

```bash
python -m unittest test_package_sorter -v
```

## Requirements

- Python 3.6+
