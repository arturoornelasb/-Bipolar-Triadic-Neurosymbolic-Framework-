# Project File Inventory & Technical Description

This directory contains the complete **Unified Semantic Engine** validation environment. Below is a detailed description of the files and their roles in the system.

---

## 1. Core Logic (`triadic_framework/core/`)
These are the "gears" of the engine.

*   **`triadic_engine.py`**: **Arithmetic Validator**. Takes 4 numbers (A, B, C, D) and calculates their "Simplicity Factor" (K). If K=1.0, the relationship is "true".
*   **`triadic_search.py`**: **Combinatorial Explorer**. Takes 4 unordered variables (e.g., F, m, a, 1) and tests all 24 permutations to find the one with K=1.0.
*   **`dimensional_units.py`**: **Unit Dictionary**. Defines that "Force" is [M L T^-2], etc. Handles dimensional analysis.
*   **`network.py`**: **Graph Builder**. Integrates the engine, searcher, and dimensional guard. Adds validated laws to the graph and visualizes them.
*   **`generic_inference.py`**: **Solver Brain**. Uses the graph to solve physics problems step-by-step, combining multiplicative inference (Triads) with additive inference (Conservation).
*   **`additive_laws.py`**: **Conservation Module**. Defines additive laws like E_total = KE + PE.

---

## 2. Reverse Engineering Scripts (Work In Progress)
These "robots" ingest external data to build knowledge. **Note: These scripts are currently experimental and under active development.**

*   **`ingest_physics_db.py`**: **The Omnivorous Ingestor**. Reads `final_physics_database.json`, cleans variables, unifies synonyms, and injects laws into the graph. Generates `physics_universe_v7.png`.
*   **`final_physics_database.json`**: **Data Source**. Contains ~400 raw physics laws extracted from the Romiti paper.
*   **`arxiv_miner.py`**: **Neurosymbolic Miner (WIP)**. Connects to arXiv, downloads papers, and extracts laws using the `knowledge_miner.py`.
*   **`knowledge_miner.py`**: **Extraction Logic (WIP)**. Uses LLM and Triadic Logic to verify candidate formulas extracted from text.

---

## 3. Validation & Test Scripts (Root)
These "lab tests" demonstrate the theory.

*   **`Master_Experiment_Log.ipynb`**: **Main Executable**. The central notebook that runs all major experiments and validates the paper's claims.
*   **`final_demo_unified.py`**: **Quick Start Demo**. A simple script demonstrating Physics (F=ma), Semantics (King:Man::Queen:Woman), and Scalability in one run.
*   **`calculus_convergence_test.py`**: **Calculus Test**. Demonstrates that discrete triadic logic converges to continuous calculus (Integration) at high resolution.
*   **`validate_graph_topology.py`**: **Topology Validator**. Calculates scientific metrics (Gamma, Clustering) to prove the graph is Scale-Free.
*   **`validate_romiti_discovery.py`**: **Discovery Validator**. Replicates SOTA results by finding paths between "Plasma" and "Quantum Physics".
*   **`real_world_glove_validation.py`**: **Real World Data**. Downloads and tests with GloVe-50d vectors.
*   **`test_fuzzy_logic.py`**: **Fuzzy Logic Experiment**. Tests the system's robustness against noise and semantic drift.

---

## 4. Documentation
*   **`paper/`**: Contains the LaTeX source and PDF of the scientific paper associated with this project.
