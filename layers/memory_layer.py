"""
Memory Space Layer
Persistent, weighted, self-organizing knowledge graph.
Intelligence grows by increasing what can be remembered AND related.
"""

from __future__ import annotations
import json
import os
import time
from pathlib import Path
from anthropic import Anthropic
from core.space import CognitiveSpace, ConceptNode

MEMORY_FILE = Path("memory/cognitive_memory.json")


class MemorySpace:
    """
    Not a database. Not a cache.
    A living knowledge structure that strengthens frequently-used paths
    and weakens unused ones — like synaptic plasticity.
    """

    def __init__(self, space: CognitiveSpace, client: Anthropic):
        self.space = space
        self.client = client
        self.session_concepts: list[str] = []   # node IDs added this session
        self._load_persistent()

    def _load_persistent(self):
        """Restore cognitive space from disk."""
        if MEMORY_FILE.exists():
            try:
                data = json.loads(MEMORY_FILE.read_text())
                for nd in data.get("nodes", []):
                    node = ConceptNode(**{k: nd[k] for k in nd if k in ConceptNode.__dataclass_fields__})
                    self.space.nodes[node.id] = node
                for dim_name, dim_data in data.get("dimensions", {}).items():
                    if dim_name not in self.space.dimensions:
                        from core.space import CognitiveDimension
                        self.space.dimensions[dim_name] = CognitiveDimension(
                            name=dim_name,
                            description=dim_data.get("description", ""),
                            abstraction_level=dim_data.get("abstraction_level", 0),
                        )
                for src, targets in data.get("edges", {}).items():
                    self.space.edges[src] = targets
                print(f"[Memory] Restored {self.space.cognitive_volume} nodes, "
                      f"{self.space.dimension_count} dimensions from disk.")
            except Exception as e:
                print(f"[Memory] Could not restore: {e}")

    def save(self):
        """Persist cognitive space to disk."""
        MEMORY_FILE.parent.mkdir(exist_ok=True)
        data = {
            "saved_at": time.time(),
            "nodes": [
                {k: getattr(n, k) for k in ConceptNode.__dataclass_fields__}
                for n in self.space.nodes.values()
            ],
            "dimensions": {k: v.to_dict() for k, v in self.space.dimensions.items()},
            "edges": {k: v for k, v in self.space.edges.items()},
        }
        MEMORY_FILE.write_text(json.dumps(data, indent=2))

    def extract_and_store(self, query: str, response: str, context: dict) -> list[ConceptNode]:
        """
        Use Claude to extract concepts from a query+response pair
        and integrate them into the cognitive space.
        """
        existing = [n.label for n in self.space.get_attractor_nodes(10)]
        existing_dims = list(self.space.dimensions.keys())

        prompt = f"""You are extracting structured knowledge for a cognitive space.

Query: {query}
Response summary: {response[:800]}
Existing attractor concepts: {existing}
Existing dimensions: {existing_dims}

Extract 3-6 key concepts from this exchange. For each concept provide:
- label: short name (2-4 words)
- content: 1-2 sentence explanation
- dimension: which cognitive dimension (causality/temporality/abstraction/self_model/meta_cognition/simulation/reality/meaning, or propose a new one)
- depth: abstraction depth (0=concrete, 1=model, 2=meta-model, 3=meta-meta)
- gravity: importance score 0.5-3.0
- connects_to: list of existing concept labels it should connect to

Also suggest 0-1 NEW dimensions if the content truly requires one.

Respond ONLY as JSON:
{{
  "concepts": [
    {{"label":"...", "content":"...", "dimension":"...", "depth":0, "gravity":1.0, "connects_to":[]}}
  ],
  "new_dimensions": [
    {{"name":"...", "description":"...", "abstraction_level":1}}
  ]
}}"""

        resp = self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1200,
            messages=[{"role": "user", "content": prompt}]
        )
        try:
            raw = resp.content[0].text.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            data = json.loads(raw.strip())
        except Exception:
            return []

        new_nodes = []

        # Add new dimensions first
        for dim in data.get("new_dimensions", []):
            if dim["name"] not in self.space.dimensions:
                self.space.add_dimension(
                    name=dim["name"],
                    description=dim["description"],
                    created_by="memory_layer",
                    abstraction_level=dim.get("abstraction_level", 1)
                )

        # Add concepts
        for c in data.get("concepts", []):
            existing_node = self.space.find_by_label(c["label"])
            if existing_node:
                # Strengthen existing node
                existing_node.gravity = min(5.0, existing_node.gravity * 1.1)
                existing_node.access_count += 1
                node = existing_node
            else:
                node = self.space.add_node(
                    label=c["label"],
                    content=c["content"],
                    dimension=c.get("dimension", "general"),
                    depth=c.get("depth", 0),
                    gravity=c.get("gravity", 1.0),
                )
                new_nodes.append(node)
                self.session_concepts.append(node.id)

            # Connect to existing concepts
            for target_label in c.get("connects_to", []):
                target = self.space.find_by_label(target_label)
                if target:
                    self.space.connect(node.id, target.id, weight=node.gravity)

        # Strengthen connections between all new nodes (they co-occurred)
        for i, n1 in enumerate(new_nodes):
            for n2 in new_nodes[i+1:]:
                self.space.connect(n1.id, n2.id, weight=0.5)

        self.save()
        return new_nodes

    def recall_relevant(self, query: str, top_n: int = 8) -> list[ConceptNode]:
        """Surface the most relevant nodes for a query via gravity + recency."""
        if not self.space.nodes:
            return []

        # Score by gravity * access_count * recency
        now = time.time()
        scored = []
        for node in self.space.nodes.values():
            recency = 1.0 / (1.0 + (now - node.created_at) / 86400)  # decay over days
            score = node.gravity * (1 + node.access_count * 0.1) * (1 + recency)
            scored.append((score, node))

        scored.sort(reverse=True)
        return [n for _, n in scored[:top_n]]

    def get_summary(self) -> str:
        """Compact summary of memory state for injection into prompts."""
        attractors = self.space.get_attractor_nodes(6)
        if not attractors:
            return "No prior memory."
        lines = ["[Cognitive Memory — Active Concepts]"]
        for n in attractors:
            lines.append(f"  • {n.label} ({n.dimension}, depth={n.depth}, gravity={n.gravity:.1f}): {n.content[:100]}")
        return "\n".join(lines)