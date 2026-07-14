# APLB simulation results

This note summarizes the benchmark of APLB against classical routing baselines under increasing traffic load.

## Summary

- APLB maintains the lowest latency at high load.
- OSPF shows moderate degradation but remains more stable than BGP.
- BGP exhibits the strongest sensitivity to congestion and policy-induced detours.

## Representative values

| Load | APLB | OSPF | BGP |
| --- | ---: | ---: | ---: |
| 1 | 1.070 | 1.045 | 1.065 |
| 11 | 1.297 | 1.553 | 1.938 |
| 22 | 1.523 | 2.119 | 3.033 |
| 32 | 1.743 | 2.718 | 4.266 |

## Photonic outputs

At the highest load, the APLB path retained the strongest optical power and signal quality among the three protocols, while BGP showed the largest degradation.
