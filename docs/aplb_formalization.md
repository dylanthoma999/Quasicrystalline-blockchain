# Aperiodic Load Balancing (APLB): formalization of the next-hop cost

## 1. Motivation

In a conventional routing system, the next hop is typically selected by minimizing a local latency term. This is effective in low-load conditions, but it tends to favor the same short-range paths and creates congestion hotspots under heavy traffic. To move beyond greedy routing, we introduce an aperiodic optimization criterion in which each node evaluates both physical cost and geometric load pressure.

## 2. Cost function

For a candidate successor $N_j$ of node $N_i$, define the next-hop cost as:

$$
C_h(i,j) = \alpha L(i,j) + \beta \left| \Phi - \frac{D_{global}}{D_{local}(N_j)+\epsilon} \right|
$$

where:

- $L(i,j)$ is the physical latency between $N_i$ and $N_j$;
- $\Phi \approx 1.6180339887$ is the golden ratio;
- $D_{global}$ is the target average connectivity density of the network;
- $D_{local}(N_j)$ is the local connectivity density of the candidate node;
- $\epsilon$ is a small numerical stabilizer;
- $\alpha$ and $\beta$ are tunable weights balancing speed and structural stability.

## 3. Interpretation

The term involving $\Phi$ acts as a geometric pressure regulator. When a candidate node becomes locally overloaded, its density increases and the ratio $D_{global}/D_{local}(N_j)$ moves away from $\Phi$. The resulting penalty increases the total cost and pushes traffic toward less congested regions of the network.

This produces a routing logic that is:

- local, because each node evaluates only its immediate candidate set;
- resilient, because overloaded regions are naturally avoided;
- non-greedy, because the algorithm does not optimize latency alone.

## 4. Why this reduces loops and collisions

The aperiodic term discourages the selection of highly saturated nodes and reduces the probability that the network will repeatedly route packets through the same local shortcuts. In a quasi-crystalline geometry, the set of permissible local configurations is not periodic, so the routing process tends to disperse traffic across structurally compatible regions instead of reinforcing a single overloaded corridor.

## 5. Practical simulation

A minimal Python prototype is provided in [examples/aplb_simulation.py](examples/aplb_simulation.py). The script compares:

- a standard greedy routing strategy, where latency grows quickly with traffic load;
- an aperiodic strategy, where the next hop is selected with the golden-ratio-aware cost function.

The generated plot illustrates the expected qualitative behavior: the standard strategy exhibits a steeper latency increase, while the aperiodic strategy remains more stable under rising load.
