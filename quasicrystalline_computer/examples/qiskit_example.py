#!/usr/bin/env python3
"""Example script showing a minimal Qiskit integration workflow."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "research"))

from geometry_generator import generate_fibonacci_lattice
from qiskit_integration import build_quasicrystalline_circuit, circuit_depth_estimate


if __name__ == "__main__":
    layout = generate_fibonacci_lattice(8, spacing=1.0)
    circuit = build_quasicrystalline_circuit(layout, gate_count=4)
    print("Circuit depth:", circuit_depth_estimate(layout, gate_count=4))
    print(circuit)
