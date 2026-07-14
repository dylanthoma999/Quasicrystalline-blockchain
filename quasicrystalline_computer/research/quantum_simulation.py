#!/usr/bin/env python3
"""Minimal quantum-inspired simulation for quasicrystalline layouts.

The goal is to provide a simple, reproducible prototype that models how a
non-periodic placement can affect an abstract error metric for a small set of
qubits. The implementation is intentionally lightweight and does not require
hardware-specific dependencies.
"""

from __future__ import annotations

from math import sqrt
from typing import List, Tuple


def estimate_circuit_error(layout: List[Tuple[float, float]], gate_count: int = 10) -> float:
    """Estimate a simple error proxy from pairwise spacing and gate count."""
    if gate_count <= 0:
        raise ValueError("gate_count must be positive")

    if len(layout) < 2:
        return 0.0

    total_spacing = 0.0
    for idx, (x0, y0) in enumerate(layout):
        for jdx in range(idx + 1, len(layout)):
            x1, y1 = layout[jdx]
            distance = sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)
            total_spacing += distance

    mean_spacing = total_spacing / (len(layout) * (len(layout) - 1) / 2.0)
    return round((gate_count / max(mean_spacing, 1e-6)) * 0.01, 6)


def estimate_entanglement_proxy(layout: List[Tuple[float, float]]) -> float:
    """Return a simple proxy for reduced unwanted entanglement based on spacing."""
    if len(layout) < 2:
        return 0.0

    pairs = 0
    total_distance = 0.0
    for idx, (x0, y0) in enumerate(layout):
        for jdx in range(idx + 1, len(layout)):
            x1, y1 = layout[jdx]
            distance = sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)
            total_distance += distance
            pairs += 1

    mean_distance = total_distance / max(pairs, 1)
    return round(1.0 / (1.0 + mean_distance), 6)
