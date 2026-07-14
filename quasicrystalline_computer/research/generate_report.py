#!/usr/bin/env python3
"""Generate a concise research report from the current prototype metrics."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "research"))

from geometry_generator import coherence_proxy, crosstalk_proxy, generate_fibonacci_lattice
from quantum_simulation import estimate_circuit_error, estimate_entanglement_proxy
from qiskit_integration import build_quasicrystalline_circuit, circuit_depth_estimate
from tiling_models import generate_ammann_beenker_like_points, generate_penrose_like_points


def build_report() -> str:
    sections = []
    sections.append("# Quasicrystalline Research Prototype Report")
    sections.append("")
    sections.append("## Summary")
    sections.append("This report summarizes the first prototype metrics for non-periodic layouts.")
    sections.append("")
    sections.append("## Fibonacci-inspired layout")
    for n_points in (8, 16, 32):
        points = generate_fibonacci_lattice(n_points, spacing=1.0)
        coherence = coherence_proxy(points, scale=2.0)
        crosstalk = crosstalk_proxy(points, scale=1.5)
        sections.append(f"- n_points={n_points}: coherence={coherence}, crosstalk={crosstalk}")
    sections.append("")
    sections.append("## Additional topology prototypes")
    penrose = generate_penrose_like_points(10)
    ammann = generate_ammann_beenker_like_points(10)
    sections.append(f"- Penrose-like prototype points: {len(penrose)}")
    sections.append(f"- Ammann-Beenker-like prototype points: {len(ammann)}")
    sections.append("")
    sections.append("## Quantum-inspired metrics")
    fibonacci_layout = generate_fibonacci_lattice(12, spacing=1.0)
    error_proxy = estimate_circuit_error(fibonacci_layout, gate_count=12)
    entanglement_proxy = estimate_entanglement_proxy(fibonacci_layout)
    circuit = build_quasicrystalline_circuit(fibonacci_layout, gate_count=4)
    sections.append(f"- Circuit error proxy: {error_proxy}")
    sections.append(f"- Entanglement proxy: {entanglement_proxy}")
    sections.append(f"- Qiskit circuit qubits: {circuit.num_qubits}")
    sections.append(f"- Qiskit circuit depth proxy: {circuit_depth_estimate(fibonacci_layout, gate_count=4)}")
    sections.append("")
    sections.append("## Next steps")
    sections.append("- Extend the analysis with Qiskit-based quantum simulation.")
    sections.append("- Compare coherence and crosstalk across multiple topology families.")
    return "\n".join(sections) + "\n"


if __name__ == "__main__":
    report = build_report()
    output_path = ROOT / "docs" / "research_report.md"
    output_path.write_text(report, encoding="utf-8")
    print(output_path)
