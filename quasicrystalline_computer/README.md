# Quasicrystalline Computer Repository

This repository collects a conceptual proposal for a quasicrystalline computing architecture designed for two hardware classes:

- Tower systems for workstations, edge servers, and high-throughput scientific computing
- Laptop systems for portable, low-power, resilient computation

The design is inspired by non-periodic quasicrystalline tilings, where communication, memory access, and task scheduling are organized through a self-similar, locally dense but globally aperiodic structure.

## Objectives

- Define a reusable architecture for quasicrystalline computing
- Provide separate specifications for tower and laptop implementations
- Offer a reproducible reference model and an initial scientific article draft

## Repository structure

- docs/architecture.md — conceptual architecture and theoretical framing
- docs/tower_variant.md — design for tower-class systems
- docs/laptop_variant.md — design for laptop-class systems
- docs/phase1_research_plan.md — detailed roadmap for the first research and prototyping phase
- docs/phase1_deliverables.md — milestone-oriented deliverables for phase 1
- docs/implementation_notes.md — current implementation status and next steps
- docs/research_report.md — generated prototype report
- docs/quantum_architecture_blueprint.md — first architecture blueprint for the quantum prototype
- examples/mesh_simulation.py — lightweight simulator for the proposed topology
- research/geometry_generator.py — layout generator and spacing metrics
- research/tiling_models.py — Penrose-like and Ammann-Beenker-like topology prototypes
- research/quantum_simulation.py — quantum-inspired error and entanglement proxy model
- research/qiskit_integration.py — minimal Qiskit-based circuit construction example
- research/run_research_prototype.py — execution entry point for the prototype
- research/generate_report.py — report generator
- papers/scientific_article.md — article-style manuscript

## Suggested use

The repository can be used as a research artifact, a design note, or the basis for a future hardware-software co-design project.

## Phase 1 focus

The first phase is centered on a research program for quasicrystalline quantum architectures, including mathematical analysis, computational simulations, and theoretical prototypes. The detailed plan is available in [docs/phase1_research_plan.md](docs/phase1_research_plan.md).

## Active implementation

The repository now includes a first executable research prototype:

- [research/geometry_generator.py](research/geometry_generator.py) — generates quasicrystalline-inspired layouts and evaluates spacing-based proxies
- [research/run_research_prototype.py](research/run_research_prototype.py) — runs the prototype for multiple node counts
- [tests/test_geometry_generator.py](tests/test_geometry_generator.py) — regression tests for the generator and proxies
- [docs/implementation_notes.md](docs/implementation_notes.md) — current implementation status and next steps
