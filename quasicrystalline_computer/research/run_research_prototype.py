#!/usr/bin/env python3
"""Run a lightweight research prototype for quasicrystalline layouts."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "research"))

from geometry_generator import (
    coherence_proxy,
    crosstalk_proxy,
    generate_fibonacci_lattice,
)


def main() -> None:
    for n_points in (8, 16, 32):
        points = generate_fibonacci_lattice(n_points, spacing=1.0)
        coherence = coherence_proxy(points, scale=2.0)
        crosstalk = crosstalk_proxy(points, scale=1.5)
        print(
            f"n_points={n_points} coherence_proxy={coherence} crosstalk_proxy={crosstalk}"
        )


if __name__ == "__main__":
    main()
