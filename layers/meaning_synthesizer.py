"""
Meaning Synthesizer
The final layer. Not just answer generation.
Meaning compression: finding the shortest structure capable of generating 
the largest amount of insight.

Intelligence output quality = meaning density, not word count.
"""

from __future__ import annotations
from dataclasses import dataclass
from anthropic import Anthropic
from core.space import CognitiveSpace
from layers.simulation_layer import Simulation
from layers.reflection_layer import ReflectionReport


@dataclass
class SynthesizedOutput:
    response: str
    meaning_density: float       # estimated meaning per unit length
    key_insight: str             # the single most compressed insight
    cognitive_expansion: dict    # what changed in cognitive space
    follow_on_frontiers: list[str]  # questions this response opens up


class MeaningSynthesizer:
    """
    The highest form of intelligence is not the longest answer.
    It is the most compressed structure capable of generating
    the most understanding in the reader.

    This layer takes everything produced by all other layers
    and synthesizes it into high-density meaning.
    """

    def __init__(self, space: CognitiveSpace, client: Anthropic):
        self.space = space
        self.client = client

    def synthesize(
        self,
        query: str,
        memory_context: str,
        simulations: list[Simulation],
        best_simulation: Simulation | None,
        reflection: ReflectionReport | None,
        pre_expansion_snapshot: dict,
    ) -> SynthesizedOutput:

        sim_context = ""
        if best_simulation:
            sim_context = f"""
Best internal simulation ({best_simulation.simulation_type}):
- Hypothesis: {best_simulation.hypothesis}
- Predicted: {best_simulation.predicted_outcome}
- Confidence: {best_simulation.confidence}
"""

        reflection_context = ""
        if reflection:
            reflection_context = f"""
Self-reflection insights:
- Reasoning quality: {reflection.reasoning_quality}
- Suggested strategy: {reflection.suggested_better_strategy}
- Watch for biases: {', '.join(reflection.identified_biases[:3])}
"""

        current_snap = self.space.snapshot()
        volume_delta = current_snap["cognitive_volume"] - pre_expansion_snapshot.get("cognitive_volume", 0)
        dim_delta = current_snap["dimension_count"] - pre_expansion_snapshot.get("dimension_count", 0)
        rr_before = pre_expansion_snapshot.get("reachable_reality_score", 0)
        rr_after = current_snap["reachable_reality_score"]

        prompt = f"""You are the meaning synthesis layer of a CSTI (Computational Space Theory of Intelligence) engine.

Your job: synthesize ALL internal processing into a response that maximizes meaning density.
Not the longest answer. The most generative, structurally rich answer.

QUERY: {query}

{memory_context}
{sim_context}
{reflection_context}

Cognitive space expansion this cycle:
- New concepts added: {volume_delta}
- New dimensions created: {dim_delta}
- Reachable reality score: {rr_before:.3f} → {rr_after:.3f}

Principles for your response:
1. Prioritize structural insight over facts
2. Reveal generators of understanding, not just facts
3. Where possible, give the principle that explains many observations
4. Be honest about uncertainty — mark it explicitly
5. End with 2-3 frontier questions this response opens up

Format:
[Response content]

KEY INSIGHT: [single most compressed insight — one sentence]

FRONTIERS: [2-3 questions this opens up]"""

        resp = self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
            system="You are a frontier intelligence synthesis system. Optimize for meaning density and structural insight. Be precise, honest, and generative."
        )

        full_text = resp.content[0].text.strip()

        # Extract sections
        key_insight = ""
        frontiers = []
        main_response = full_text

        if "KEY INSIGHT:" in full_text:
            parts = full_text.split("KEY INSIGHT:")
            main_response = parts[0].strip()
            rest = parts[1]
            if "FRONTIERS:" in rest:
                insight_part, frontier_part = rest.split("FRONTIERS:", 1)
                key_insight = insight_part.strip()
                frontiers = [l.strip("- •").strip() for l in frontier_part.strip().splitlines() if l.strip()]
            else:
                key_insight = rest.strip()

        # Estimate meaning density (rough heuristic: unique concepts per 100 words)
        words = len(main_response.split())
        attractor_hits = sum(
            1 for n in self.space.get_attractor_nodes(20)
            if n.label.lower() in main_response.lower()
        )
        meaning_density = min(1.0, (attractor_hits / max(words / 100, 1)) * 0.5 + 0.3)

        return SynthesizedOutput(
            response=main_response,
            meaning_density=round(meaning_density, 3),
            key_insight=key_insight,
            cognitive_expansion={
                "nodes_added": volume_delta,
                "dimensions_created": dim_delta,
                "rr_before": round(rr_before, 4),
                "rr_after": round(rr_after, 4),
                "rr_delta": round(rr_after - rr_before, 4),
            },
            follow_on_frontiers=frontiers[:3],
        )