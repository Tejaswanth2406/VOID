"""
Meta-Reasoner Layer
Reasons about reasoning itself.
Selects and adapts reasoning strategies before processing begins.
The system doesn't just think — it chooses HOW to think.
"""

from __future__ import annotations
import json
from dataclasses import dataclass
from anthropic import Anthropic
from core.space import CognitiveSpace


REASONING_STRATEGIES = {
    "deductive":     "From general principles to specific conclusions",
    "inductive":     "From specific observations to general principles",
    "abductive":     "Best explanation for observed phenomena",
    "analogical":    "Transfer structure from known domain to unknown",
    "dialectical":   "Thesis → antithesis → synthesis",
    "systems":       "Understand through relationships and feedback loops",
    "compression":   "Find the shortest description generating the most structure",
    "generative":    "Produce multiple hypotheses before selecting",
    "recursive":     "Apply reasoning to itself at increasing depth",
}


@dataclass
class ReasoningPlan:
    primary_strategy: str
    secondary_strategy: str
    rationale: str
    depth_target: int          # how many recursive levels to attempt
    simulation_count: int      # how many simulations to run
    focus_dimensions: list[str]
    avoid_biases: list[str]
    confidence_prior: float    # expected answer confidence before reasoning


class MetaReasoner:
    """
    Before the cognitive cycle begins, the MetaReasoner decides:
    - Which reasoning strategy fits this query best?
    - How many simulations should the simulation layer run?
    - Which cognitive dimensions should be prioritized?
    - What known biases should be actively avoided?
    
    This is planning-before-thinking.
    """

    def __init__(self, space: CognitiveSpace, client: Anthropic):
        self.space = space
        self.client = client
        self.plans_executed: list[ReasoningPlan] = []
        self.strategy_performance: dict[str, list[float]] = {s: [] for s in REASONING_STRATEGIES}

    def plan(self, query: str, self_model: dict) -> ReasoningPlan:
        """Select optimal reasoning strategy for the given query."""
        attractor_dims = [n.dimension for n in self.space.get_attractor_nodes(6)]
        known_biases = self_model.get("known_biases", [])

        # Strategy performance summary
        perf = {
            s: sum(scores) / len(scores) if scores else 0.5
            for s, scores in self.strategy_performance.items()
        }

        prompt = f"""You are the meta-reasoning layer of a cognitive architecture.
Before any reasoning begins, you select the optimal reasoning strategy.

Query: {query}

Available strategies: {json.dumps(REASONING_STRATEGIES, indent=2)}
Strategy performance history: {json.dumps(perf, indent=2)}
Active cognitive dimensions: {list(self.space.dimensions.keys())}
Current attractor dimensions: {attractor_dims}
Known system biases to avoid: {known_biases}

Select the best reasoning plan. Consider:
- Query type (factual, philosophical, causal, creative, analytical)
- Depth needed (surface vs recursive self-reference)
- How many internal simulations are warranted (1-5)
- Which dimensions should be prioritized for this query

Respond ONLY as JSON:
{{
  "primary_strategy": "deductive",
  "secondary_strategy": "analogical",
  "rationale": "...",
  "depth_target": 2,
  "simulation_count": 3,
  "focus_dimensions": ["causality", "abstraction"],
  "avoid_biases": ["confirmation bias"],
  "confidence_prior": 0.6
}}"""

        resp = self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=700,
            messages=[{"role": "user", "content": prompt}]
        )

        plan = ReasoningPlan(
            primary_strategy="deductive",
            secondary_strategy="analogical",
            rationale="Default plan",
            depth_target=2,
            simulation_count=3,
            focus_dimensions=["causality", "abstraction"],
            avoid_biases=[],
            confidence_prior=0.6
        )

        try:
            raw = resp.content[0].text.strip()
            if "```" in raw:
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            data = json.loads(raw.strip())
            plan = ReasoningPlan(**{k: data[k] for k in ReasoningPlan.__dataclass_fields__ if k in data})
        except Exception:
            pass

        self.plans_executed.append(plan)
        return plan

    def record_outcome(self, strategy: str, quality: float):
        """Update strategy performance based on reflection feedback."""
        if strategy in self.strategy_performance:
            self.strategy_performance[strategy].append(quality)
            # Keep only last 20 scores per strategy
            if len(self.strategy_performance[strategy]) > 20:
                self.strategy_performance[strategy] = self.strategy_performance[strategy][-20:]

    def format_plan(self, plan: ReasoningPlan) -> str:
        return (
            f"\n[Meta-Reasoner — Reasoning Plan]\n"
            f"  Strategy: {plan.primary_strategy} + {plan.secondary_strategy}\n"
            f"  Rationale: {plan.rationale}\n"
            f"  Depth target: {plan.depth_target} | Simulations: {plan.simulation_count}\n"
            f"  Focus dims: {plan.focus_dimensions}\n"
            f"  Avoid biases: {plan.avoid_biases}\n"
        )