"""Prototype tools for generating quasicrystalline-inspired layouts.

The implementation is intentionally lightweight and meant for research
scaffolding rather than hardware-validated design.
"""

from __future__ import annotations

from math import sqrt
from typing import List, Tuple

PHI = (1 + sqrt(5)) / 2.0


def generate_fibonacci_lattice(n_points: int, spacing: float = 1.0) -> List[Tuple[float, float]]:
    """Generate a simple 2D Fibonacci-inspired point set.

    The layout is constructed from a golden-ratio modulation and is suitable as
    a toy model for exploring non-periodic qubit placement.
    """
    if n_points <= 0:
        raise ValueError("n_points must be positive")

    points: List[Tuple[float, float]] = []
    for i in range(n_points):
        x = i * spacing
        y = (i * spacing / PHI) % spacing
        points.append((x, y))
    return points


def nearest_neighbor_distances(points: List[Tuple[float, float]]) -> List[float]:
    """Compute shortest distances from each point to its nearest neighbour."""
    if len(points) < 2:
        return []

    distances: List[float] = []
    for idx, (x0, y0) in enumerate(points):
        min_distance = float("inf")
        for jdx, (x1, y1) in enumerate(points):
            if idx == jdx:
                continue
            distance = sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)
            if distance < min_distance:
                min_distance = distance
        distances.append(min_distance)
    return distances


def coherence_proxy(points: List[Tuple[float, float]], scale: float = 1.0) -> float:
    """Return a simple proxy for coherence quality based on spacing."""
    distances = nearest_neighbor_distances(points)
    if not distances:
        return 0.0

    mean_distance = sum(distances) / len(distances)
    return round(1.0 / (1.0 + mean_distance / scale), 6)


def crosstalk_proxy(points: List[Tuple[float, float]], scale: float = 1.0) -> float:
    """Return a simplified crosstalk proxy where smaller spacing raises risk."""
    distances = nearest_neighbor_distances(points)
    if not distances:
        return 0.0

    mean_distance = sum(distances) / len(distances)
    return round(1.0 / (1.0 + scale / max(mean_distance, 1e-6)), 6)
