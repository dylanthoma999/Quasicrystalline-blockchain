from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "research"))

from geometry_generator import (
    coherence_proxy,
    crosstalk_proxy,
    generate_fibonacci_lattice,
    nearest_neighbor_distances,
)


def test_generate_fibonacci_lattice_returns_expected_count():
    points = generate_fibonacci_lattice(8, spacing=1.0)
    assert len(points) == 8


def test_nearest_neighbor_distances_are_positive():
    points = generate_fibonacci_lattice(8, spacing=1.0)
    distances = nearest_neighbor_distances(points)
    assert len(distances) == 8
    assert all(distance > 0.0 for distance in distances)


def test_coherence_and_crosstalk_are_in_expected_range():
    points = generate_fibonacci_lattice(8, spacing=1.0)
    coherence = coherence_proxy(points, scale=2.0)
    crosstalk = crosstalk_proxy(points, scale=1.5)
    assert 0.0 < coherence <= 1.0
    assert 0.0 < crosstalk <= 1.0
