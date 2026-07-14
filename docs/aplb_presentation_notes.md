# APLB presentation notes

## Core message

The next-hop decision should not be based on latency alone. A more resilient routing policy evaluates both physical proximity and local structural pressure.

## Key idea

Use the golden-ratio-aware cost function:

$$
C_h(i,j) = \alpha L(i,j) + \beta \left| \Phi - \frac{D_{global}}{D_{local}(N_j)+\epsilon} \right|
$$

## Why it matters

- It prevents overloaded nodes from absorbing too much traffic.
- It reduces the emergence of congestion clusters.
- It supports a distributed routing logic without centralized orchestration.

## Presentation slide structure

1. Problem: greedy routing causes hotspots and oscillations.
2. Proposal: APLB uses local geometric pressure to guide next-hop selection.
3. Mechanism: the golden-ratio term penalizes locally dense candidates.
4. Result: lower latency variance and improved load distribution.
5. PoC: the Python script in examples/aplb_simulation.py produces a visual comparison.
