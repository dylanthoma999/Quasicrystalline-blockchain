from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "research"))

from geometry_generator import generate_fibonacci_lattice
from qiskit_integration import build_quasicrystalline_circuit, circuit_depth_estimate


def test_build_quasicrystalline_circuit_returns_circuit():
    layout = generate_fibonacci_lattice(8, spacing=1.0)
    circuit = build_quasicrystalline_circuit(layout, gate_count=4)
    assert circuit.num_qubits == 6
    assert circuit.num_clbits == 6


def test_circuit_depth_estimate_is_positive():
    layout = generate_fibonacci_lattice(8, spacing=1.0)
    depth = circuit_depth_estimate(layout, gate_count=4)
    assert depth > 0
