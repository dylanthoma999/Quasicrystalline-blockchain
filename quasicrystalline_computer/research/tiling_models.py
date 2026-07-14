"""Additional quasicrystalline-inspired topology generators.

This module introduces simple prototype generators for Penrose-like and
Ammann-Beenker-like point layouts, intended for research exploration.
"""

from __future__ import annotations

from math import cos, pi, sin
from typing import List, Tuple


def generate_penrose_like_points(n_points: int, radius: float = 1.0) -> List[Tuple[float, float]]:
    """Generate a simple Penrose-inspired point cloud using angular steps."""
    if n_points <= 0:
        raise ValueError("n_points must be positive")

    points: List[Tuple[float, float]] = []
    golden_angle = 2 * pi / ((1 + 5**0.5) / 2.0)
    for i in range(n_points):
        angle = i * golden_angle
        points.append((radius * cos(angle), radius * sin(angle)))
    return points


def generate_ammann_beenker_like_points(n_points: int, radius: float = 1.0) -> List[Tuple[float, float]]:
    """Generate a simple Ammann-Beenker-inspired point cloud."""
    if n_points <= 0:
        raise ValueError("n_points must be positive")

    points: List[Tuple[float, float]] = []
    for i in range(n_points):
        angle = (i * pi) / (2 * n_points)
        r = radius * (1.0 + 0.15 * (i % 3))
        points.append((r * cos(angle), r * sin(angle)))
    return points
