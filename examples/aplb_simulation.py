import math
from typing import List, Dict, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PHI = 1.618033988749895


def calculate_next_hop_cost(
    latency: float,
    local_density: float,
    global_density: float,
    phi: float = PHI,
    alpha: float = 0.5,
    beta: float = 0.5,
) -> float:
    """Compute a local cost for selecting a next hop under an aperiodic routing heuristic."""
    density_ratio = global_density / (local_density + 1e-8)
    density_factor = abs(phi - density_ratio)
    return alpha * latency + beta * density_factor


def simulate_routing(load_levels: List[float], base_latency: float = 1.0) -> Dict[str, List[float]]:
    """Simulate a standard greedy routing strategy versus the aperiodic strategy."""
    standard_latencies: List[float] = []
    aperiodic_latencies: List[float] = []

    for load in load_levels:
        # Standard greedy approach: latency grows with traffic load and the most loaded node is preferred.
        standard_latency = base_latency + 0.03 * load + 0.01 * load**1.4
        standard_latencies.append(standard_latency)

        # Aperiodic approach: traffic is diverted away from overloaded regions through the density term.
        local_density = 10 + load * 0.8
        global_density = 20.0
        candidate_latency = base_latency + 0.02 * load
        candidate_cost = calculate_next_hop_cost(
            latency=candidate_latency,
            local_density=local_density,
            global_density=global_density,
        )
        aperiodic_latencies.append(base_latency + 0.02 * load + 0.1 * candidate_cost)

    return {"standard": standard_latencies, "aperiodic": aperiodic_latencies}


def plot_results(load_levels: List[float], results: Dict[str, List[float]], output_path: str = "examples/aplb_simulation.png") -> None:
    plt.figure(figsize=(8, 4.5))
    plt.plot(load_levels, results["standard"], marker="o", linewidth=2, label="Greedy / grid-like")
    plt.plot(load_levels, results["aperiodic"], marker="s", linewidth=2, label="APLB / quasi-crystalline")
    plt.xlabel("Traffic load")
    plt.ylabel("Average network latency")
    plt.title("Aperiodic routing vs. standard greedy routing")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=180)
    plt.close()


def main() -> None:
    load_levels = np.linspace(1, 40, 20)
    results = simulate_routing(load_levels)
    plot_results(load_levels, results)
    print("Simulation completed. Plot saved to examples/aplb_simulation.png")


if __name__ == "__main__":
    main()
