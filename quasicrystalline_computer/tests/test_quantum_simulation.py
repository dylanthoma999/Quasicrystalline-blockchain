from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "research"))

from geometry_generator import generate_fibonacci_lattice
from quantum_simulation import estimate_circuit_error, estimate_entanglement_proxy


def test_estimate_circuit_error_is_positive():
    layout = generate_fibonacci_lattice(8, spacing=1.0)
    error = estimate_circuit_error(layout, gate_count=10)
    assert error > 0.0


def test_estimate_entanglement_proxy_is_between_zero_and_one():
    layout = generate_fibonacci_lattice(8, spacing=1.0)
    proxy = estimate_entanglement_proxy(layout)
    assert 0.0 <= proxy <= 1.0
