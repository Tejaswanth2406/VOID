"""
Dimension Engine
The most radical layer.
Not storing knowledge within existing dimensions.
Creating entirely NEW dimensions of thought.

Every time a concept cannot be adequately represented in existing dimensions,
a new one is born.
"""

from __future__ import annotations
import json
from dataclasses import dataclass
from anthropic import Anthropic
from core.space import CognitiveSpace, CognitiveDimension


@dataclass
class DimensionProposal:
    name: str
    description: str
    motivation: str          # why the existing dimensions were insufficient
    abstraction_level: int
    parent_dimension: str | None
    example_concepts: list[str]
    expansion_potential: float  # 0-1: how much new territory this opens


class DimensionEngine:
    """
    In science, the greatest breakthroughs created new dimensions of thought.
    - Calculus: a new dimension of continuous change
    - Probability: a new dimension of uncertainty
    - Information theory: a new dimension of structure vs noise

    This layer continuously asks: are we missing a dimension?
    """

    def __init__(self, space: CognitiveSpace, client: Anthropic):
        self.space = space
        self.client = client
        self.created_dimensions: list[str] = []
        self.rejected_proposals: list[str] = []

    def analyze(self, query: str, concepts_added: list[str]) -> list[DimensionProposal]:
        """
        After each cognitive cycle, check if any concepts couldn't be
        well-represented in existing dimensions. If so, propose new ones.
        """
        existing_dims = {k: v.description for k, v in self.space.dimensions.items()}

        prompt = f"""You are the dimension creation engine of a cognitive architecture.
Your job: identify if existing cognitive dimensions are insufficient,
and propose genuinely new ones.

Recent query: {query}
Concepts added: {concepts_added}
Existing dimensions: {json.dumps(existing_dims, indent=2)}

Critically evaluate: are there concepts or relationships in this exchange
that genuinely cannot be represented in the existing dimensions?

A new dimension is warranted ONLY if:
1. The concept requires a fundamentally new axis of representation
2. It's not a subcategory of an existing dimension
3. It would unlock multiple new concepts currently unreachable

Be conservative. Propose 0-2 new dimensions max.
If existing dimensions are sufficient, return empty list.

Examples of what a truly new dimension looks like:
- "emergence": properties arising from system-level interactions (not reducible to causality)
- "paradox_resolution": frameworks for holding contradictions productively
- "telos": purpose-structure not captured by causality

Respond ONLY as JSON:
{{
  "proposals": [
    {{
      "name": "...",
      "description": "...",
      "motivation": "why existing dims are insufficient...",
      "abstraction_level": 2,
      "parent_dimension": "causality or null",
      "example_concepts": ["concept1", "concept2"],
      "expansion_potential": 0.7
    }}
  ]
}}"""

        resp = self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        proposals = []
        try:
            raw = resp.content[0].text.strip()
            if "```" in raw:
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            data = json.loads(raw.strip())
            for p in data.get("proposals", []):
                prop = DimensionProposal(**{k: p[k] for k in DimensionProposal.__dataclass_fields__ if k in p})
                proposals.append(prop)
        except Exception:
            pass

        return proposals

    def commit(self, proposal: DimensionProposal) -> CognitiveDimension | None:
        """Accept a dimension proposal and integrate it into the cognitive space."""
        if proposal.name in self.space.dimensions:
            return None  # already exists

        if proposal.expansion_potential < 0.4:
            self.rejected_proposals.append(proposal.name)
            return None

        dim = self.space.add_dimension(
            name=proposal.name,
            description=proposal.description,
            created_by="dimension_engine",
            parent=proposal.parent_dimension,
            abstraction_level=proposal.abstraction_level
        )
        self.created_dimensions.append(proposal.name)

        # Seed example concepts into this new dimension
        for concept_label in proposal.example_concepts[:3]:
            self.space.add_node(
                label=concept_label,
                content=f"Seed concept for dimension: {proposal.name}",
                dimension=proposal.name,
                depth=proposal.abstraction_level,
                gravity=1.5,
            )

        return dim

    def run_cycle(self, query: str, concepts_added: list[str]) -> list[CognitiveDimension]:
        proposals = self.analyze(query, concepts_added)
        created = []
        for prop in proposals:
            dim = self.commit(prop)
            if dim:
                created.append(dim)
                print(f"  [Dimension Engine] ✦ New dimension created: '{dim.name}' "
                      f"(level={dim.abstraction_level})")
        return created