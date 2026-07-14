#!/usr/bin/env python3
"""Simple toy simulator for a quasicrystalline-inspired interconnect."""

from math import sqrt

PHI = (1 + sqrt(5)) / 2.0


def estimate_variant(kind: str, nodes: int, local_links: int) -> dict:
    """Return a simple performance-oriented estimate for a hardware variant."""
    if kind == "tower":
        base_power = 120.0
        scaling = 1.25
    elif kind == "laptop":
        base_power = 45.0
        scaling = 0.85
    else:
        raise ValueError("kind must be 'tower' or 'laptop'")

    density = (2 * local_links) / (nodes * (nodes - 1))
    resilience = 1.0 - (1.0 / (1.0 + nodes / 16.0))
    efficiency = (PHI * density) / (1.0 + (base_power / 100.0))

    return {
        "kind": kind,
        "nodes": nodes,
        "local_links": local_links,
        "density": round(density, 3),
        "resilience": round(resilience, 3),
        "efficiency": round(efficiency, 3),
        "scaled_power": round(base_power * scaling, 2),
    }


if __name__ == "__main__":
    tower = estimate_variant("tower", nodes=24, local_links=38)
    laptop = estimate_variant("laptop", nodes=12, local_links=16)
    print("Tower variant:", tower)
    print("Laptop variant:", laptop)
