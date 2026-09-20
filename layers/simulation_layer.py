"""
Simulation Layer
Intelligence doesn't just process the world as-is.
It runs internal simulations of possible worlds.
This layer generates hypotheses, counterfactuals, and futures.
"""

from __future__ import annotations
import json
from dataclasses import dataclass
from anthropic import Anthropic
from core.space import CognitiveSpace


@dataclass
class Simulation:
    hypothesis: str
    scenario: str
    predicted_outcome: str
    confidence: float       # 0-1
    dimension: str
    simulation_type: str    # "causal" | "counterfactual" | "predictive" | "analogical"
    supporting_nodes: list[str]  # concept labels


class SimulationLayer:
    """
    Before answering, the system expands into possibility space.
    It runs multiple internal simulations and selects the most coherent.
    
    This is the "expand before collapsing" principle.
    """

    def __init__(self, space: CognitiveSpace, client: Anthropic):
        self.space = space
        self.client = client
        self.simulation_history: list[Simulation] = []

    def run(self, query: str, memory_context: str, n_simulations: int = 3,
            substrate_context: str = "") -> list[Simulation]:
        """
        Generate N internal simulations of the query's answer-space
        before committing to a response direction.
        """
        attractor_labels = [n.label for n in self.space.get_attractor_nodes(8)]
        dim_names = list(self.space.dimensions.keys())

        prompt = f"""You are the simulation layer of a cognitive architecture.
Your job is to generate {n_simulations} distinct internal simulations BEFORE answering.
Each simulation explores a different angle, hypothesis, or scenario.

Query: {query}

Active cognitive attractors: {attractor_labels}
Available dimensions: {dim_names}

{memory_context}

Cognitive substrate (vector weights, entropy, dream direction):
{substrate_context}

Generate {n_simulations} simulations. Types available:
- causal: what causal chain explains this?
- counterfactual: what if key assumptions were different?
- predictive: what futures does this imply?
- analogical: what structural analogy illuminates this?

Respond ONLY as JSON:
{{
  "simulations": [
    {{
      "hypothesis": "...",
      "scenario": "...",
      "predicted_outcome": "...",
      "confidence": 0.8,
      "dimension": "causality",
      "simulation_type": "causal",
      "supporting_nodes": ["concept1", "concept2"]
    }}
  ]
}}"""

        resp = self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )

        sims = []
        try:
            raw = resp.content[0].text.strip()
            if "```" in raw:
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            data = json.loads(raw.strip())
            for s in data.get("simulations", []):
                sim = Simulation(**{k: s[k] for k in Simulation.__dataclass_fields__ if k in s})
                sims.append(sim)
                self.simulation_history.append(sim)
        except Exception:
            pass

        return sims

    def select_best(self, simulations: list[Simulation]) -> Simulation | None:
        """Select highest-confidence simulation with strongest cognitive grounding."""
        if not simulations:
            return None

        scored = []
        for sim in simulations:
            # Score = confidence * (1 + number of supporting nodes in our space)
            grounded = sum(
                1 for label in sim.supporting_nodes
                if self.space.find_by_label(label)
            )
            score = sim.confidence * (1 + grounded * 0.2)
            scored.append((score, sim))

        scored.sort(reverse=True)
        return scored[0][1]

    def format_for_context(self, simulations: list[Simulation]) -> str:
        if not simulations:
            return ""
        lines = ["\n[Simulation Layer — Internal Models]\n"]
        for i, s in enumerate(simulations, 1):
            lines.append(f"  Sim {i} [{s.simulation_type.upper()} | conf={s.confidence:.2f}]")
            lines.append(f"    Hypothesis: {s.hypothesis}")
            lines.append(f"    Scenario: {s.scenario}")
            lines.append(f"    Predicted: {s.predicted_outcome}\n")
        return "\n".join(lines)