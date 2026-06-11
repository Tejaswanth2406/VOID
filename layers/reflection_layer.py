"""
Reflection Layer
The system models itself.
Not just "what is the answer" but "how am I reasoning, and how can I reason better."
Self-reference creates new cognitive dimensions.
"""

from __future__ import annotations
import json
from dataclasses import dataclass, field
from anthropic import Anthropic
from core.space import CognitiveSpace


@dataclass
class ReflectionReport:
    reasoning_quality: float          # 0-1
    identified_biases: list[str]
    blind_spots: list[str]
    reasoning_strategy_used: str
    suggested_better_strategy: str
    new_dimension_candidates: list[str]
    meta_depth: int                    # how many levels of self-reference achieved
    self_model_update: str             # what the system learned about itself


class ReflectionLayer:
    """
    After reasoning, the system reflects on its own reasoning.
    This creates meta-cognitive depth — recursive self-modeling.
    
    Depth 0: knows facts
    Depth 1: knows how it knows facts
    Depth 2: knows how it knows how it knows facts
    ...
    """

    def __init__(self, space: CognitiveSpace, client: Anthropic):
        self.space = space
        self.client = client
        self.self_model: dict = {
            "known_biases": [],
            "strong_dimensions": [],
            "weak_dimensions": [],
            "meta_depth_reached": 0,
        }
        self.reflection_history: list[ReflectionReport] = []

    def reflect(self, query: str, draft_response: str, simulations_used: str) -> ReflectionReport:
        """
        Examine the draft response + reasoning process.
        Identify weaknesses, biases, blind spots.
        Suggest improvements. Update self-model.
        """
        prompt = f"""You are the reflection layer of a cognitive architecture.
Your job: analyze the reasoning process that produced a draft response.
Find biases, blind spots, and ways to improve.

Query: {query}

Draft response (first 600 chars): {draft_response[:600]}

Simulations used: {simulations_used[:400]}

Current self-model: {json.dumps(self.self_model, indent=2)}

Reflect deeply. Consider:
1. What reasoning strategy was used?
2. What biases might have crept in?
3. What perspectives were NOT considered?
4. Would a different reasoning strategy produce better results?
5. Did any new cognitive dimensions emerge that should be tracked?
6. What did this exchange reveal about the system's own reasoning?

Rate reasoning quality 0-1 honestly.

Respond ONLY as JSON:
{{
  "reasoning_quality": 0.75,
  "identified_biases": ["..."],
  "blind_spots": ["..."],
  "reasoning_strategy_used": "...",
  "suggested_better_strategy": "...",
  "new_dimension_candidates": ["..."],
  "meta_depth": 2,
  "self_model_update": "..."
}}"""

        resp = self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        report = ReflectionReport(
            reasoning_quality=0.7,
            identified_biases=[],
            blind_spots=[],
            reasoning_strategy_used="default",
            suggested_better_strategy="none",
            new_dimension_candidates=[],
            meta_depth=1,
            self_model_update="no update"
        )

        try:
            raw = resp.content[0].text.strip()
            if "```" in raw:
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            data = json.loads(raw.strip())
            report = ReflectionReport(**{k: data[k] for k in ReflectionReport.__dataclass_fields__ if k in data})
        except Exception:
            pass

        # Update self-model
        for bias in report.identified_biases:
            if bias not in self.self_model["known_biases"]:
                self.self_model["known_biases"].append(bias)
        self.self_model["meta_depth_reached"] = max(
            self.self_model["meta_depth_reached"], report.meta_depth
        )

        # Add new dimension candidates to cognitive space
        for dim_candidate in report.new_dimension_candidates:
            if dim_candidate and dim_candidate not in self.space.dimensions:
                self.space.add_dimension(
                    name=dim_candidate,
                    description=f"Discovered through self-reflection: {dim_candidate}",
                    created_by="reflection_layer",
                    abstraction_level=2
                )

        # Add a meta-cognitive node
        self.space.add_node(
            label=f"self_reflection_{len(self.reflection_history)}",
            content=report.self_model_update,
            dimension="meta_cognition",
            depth=report.meta_depth,
            gravity=report.reasoning_quality * 2
        )

        self.reflection_history.append(report)
        return report

    def format_for_refinement(self, report: ReflectionReport) -> str:
        lines = ["\n[Reflection Layer — Self-Analysis]\n"]
        lines.append(f"  Reasoning quality: {report.reasoning_quality:.2f}")
        if report.identified_biases:
            lines.append(f"  Detected biases: {', '.join(report.identified_biases)}")
        if report.blind_spots:
            lines.append(f"  Blind spots: {', '.join(report.blind_spots)}")
        lines.append(f"  Better strategy: {report.suggested_better_strategy}")
        lines.append(f"  Meta-depth achieved: {report.meta_depth}")
        return "\n".join(lines)