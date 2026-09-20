<img width="667" height="367" alt="image" src="https://github.com/user-attachments/assets/f339401d-ad2e-41ef-9705-78c23e42b07b" />

# CSTI Engine — Computational Space Theory of Intelligence

A frontier AI architecture implementing the **Computational Space Theory of Intelligence**.
Intelligence is not modeled as a prediction function — it is modeled as a **self-expanding cognitive universe**.

---

## Architecture Overview

```
Input
  ↓
Cognitive Space Initializer
  ↓
┌─────────────────────────────────────────┐
│           COGNITIVE SPACE               │
│                                         │
│  Memory Layer    ←→  Concept Graph      │
│       ↕                   ↕             │
│  Simulation Layer ←→ Reflection Layer   │
│       ↕                   ↕             │
│  Dimension Engine ←→ Meta-Reasoner      │
│       ↕                   ↕             │
│  Reality Verifier ←→ Coherence Filter   │
└─────────────────────────────────────────┘
  ↓
Meaning Synthesizer
  ↓
Output + Cognitive Space Expansion Report
```

## Layers

| Layer | Role |
|-------|------|
| `MemorySpace` | Persistent knowledge graph with weighted concept nodes |
| `SimulationLayer` | Generates hypotheses and counterfactual futures |
| `ReflectionLayer` | Self-models the reasoning process |
| `DimensionEngine` | Creates new representational dimensions |
| `MetaReasoner` | Reasons about reasoning strategies |
| `RealityVerifier` | Tests models against grounded facts |
| `CoherenceFilter` | Eliminates self-contradictions, cognitive black holes |
| `MeaningSynthesizer` | Compresses insights into high-density meaning |

## Install

```bash
pip install -r requirements.txt
```

Set your API key:
```bash
export ANTHROPIC_API_KEY=your_key_here
```

## Run

```bash
# Interactive REPL
python main.py

# Single query
python main.py --query "What is the nature of causality?"

# Full expansion mode (all layers active)
python main.py --query "..." --mode full

# Benchmark cognitive space growth
python main.py --benchmark
```

## Native acceleration

VOID keeps the Python implementation as the portable default, and can use the
same C ABI implemented in either Rust or C++ for the reachable-reality metric.

Build the Rust backend:

```bash
cd native/rust
cargo build --release
```

Build the C++ backend with CMake:

```bash
cmake -S native -B native/build
cmake --build native/build --config Release
```

The loader discovers built libraries automatically. Set
`VOID_NATIVE_BACKEND=python` to force the fallback, or `rust`/`cpp` to require
a native library. The backend name is available as `utils.native_backend.BACKEND_NAME`.

## Core Concept

Each query does not just produce an answer.
It **expands the cognitive space** — adding nodes, edges, dimensions, and coherence structures
that persist across queries and compound over time.

The system tracks:
- `cognitive_volume` — total representational nodes
- `dimension_count` — active reasoning dimensions
- `coherence_score` — internal consistency
- `reality_fidelity` — grounding accuracy
- `meaning_density` — significance per unit structure

## Cognitive substrate

The engine now includes a deterministic substrate for experimental reasoning:

- **Vector assigning and weight distribution** map every query across causal,
  temporal, abstract, self-model, simulation, reality, meaning, and memory dimensions.
- **Space entropy** measures how concentrated or distributed the current reasoning
  weights are.
- **Blackhole and whitehole attractors** compress dominant signals and emit a
  novel direction for exploration.
- **Dreaming** blends recalled concept vectors before the simulation layer runs.
- **MnemonicRegistry** provides Major, Dominic, peg, and number-shape encodings,
  with the broader memory-palace, PAO, Leitner, Feynman, calculation, and
  synesthetic systems registered as extension points.

The latest substrate state is included in `/status`, `/space`, and `/cognition`.
Use `/mnemonics/encode?value=42&system=major` to test an encoding.
