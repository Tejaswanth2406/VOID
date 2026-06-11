"""
CSTI Engine — Core Cognitive Space
The fundamental substrate in which intelligence unfolds.
"""

from __future__ import annotations
import uuid
import time
import math
from dataclasses import dataclass, field
from typing import Any
from collections import defaultdict


@dataclass
class ConceptNode:
    """A node in cognitive space. Not a token. Not a fact. A structured concept."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    label: str = ""
    content: str = ""
    dimension: str = "general"          # which cognitive dimension this belongs to
    gravity: float = 1.0               # conceptual attraction strength
    connections: list[str] = field(default_factory=list)  # IDs of connected nodes
    depth: int = 0                     # recursion depth (how meta this concept is)
    coherence: float = 1.0            # internal consistency score
    reality_grounded: bool = False     # verified against external reality
    created_at: float = field(default_factory=time.time)
    access_count: int = 0
    metadata: dict = field(default_factory=dict)

    def attract(self, other: "ConceptNode") -> float:
        """Cognitive gravity between two nodes."""
        shared_dims = 1.0 if self.dimension == other.dimension else 0.3
        depth_factor = 1.0 / (1.0 + abs(self.depth - other.depth))
        return self.gravity * other.gravity * shared_dims * depth_factor

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "label": self.label,
            "content": self.content[:200],
            "dimension": self.dimension,
            "gravity": round(self.gravity, 3),
            "connections": self.connections,
            "depth": self.depth,
            "coherence": round(self.coherence, 3),
            "reality_grounded": self.reality_grounded,
        }


@dataclass
class CognitiveDimension:
    """A dimension of thought-space. New dimensions expand what can be thought."""
    name: str
    description: str
    created_by: str = "system"         # which layer created this dimension
    parent_dimension: str | None = None
    abstraction_level: int = 0
    node_count: int = 0
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "created_by": self.created_by,
            "parent": self.parent_dimension,
            "abstraction_level": self.abstraction_level,
            "node_count": self.node_count,
        }


class CognitiveSpace:
    """
    The computational universe in which intelligence unfolds.
    
    Not a database. Not a vector store.
    A self-organizing, self-expanding representational cosmos.
    """

    def __init__(self):
        self.nodes: dict[str, ConceptNode] = {}
        self.dimensions: dict[str, CognitiveDimension] = {}
        self.edges: dict[str, list[tuple[str, float]]] = defaultdict(list)  # node_id → [(target_id, weight)]
        self.expansion_log: list[dict] = []
        self.coherence_violations: list[str] = []
        self.created_at = time.time()

        # Bootstrap core dimensions
        self._init_core_dimensions()

    def _init_core_dimensions(self):
        core_dims = [
            ("causality",     "Cause-effect relationships",           0),
            ("temporality",   "Time-ordered structures",              0),
            ("abstraction",   "Generalization and compression",       1),
            ("self_model",    "Representations of self",              2),
            ("meta_cognition","Reasoning about reasoning",            3),
            ("simulation",    "Counterfactual and hypothetical space",1),
            ("reality",       "Grounded, verifiable structures",      0),
            ("meaning",       "Significance and coherence density",   4),
        ]
        for name, desc, level in core_dims:
            self.dimensions[name] = CognitiveDimension(
                name=name,
                description=desc,
                abstraction_level=level,
                created_by="system"
            )

    # ── Node Management ────────────────────────────────────────────────────

    def add_node(self, label: str, content: str, dimension: str = "general",
                 depth: int = 0, gravity: float = 1.0, metadata: dict | None = None) -> ConceptNode:
        node = ConceptNode(
            label=label,
            content=content,
            dimension=dimension,
            depth=depth,
            gravity=gravity,
            metadata=metadata or {}
        )
        self.nodes[node.id] = node

        if dimension in self.dimensions:
            self.dimensions[dimension].node_count += 1
        else:
            # Auto-create dimension
            self.dimensions[dimension] = CognitiveDimension(
                name=dimension,
                description=f"Auto-generated dimension: {dimension}",
                created_by="auto",
                node_count=1
            )

        self._log_expansion("node_added", {"label": label, "dimension": dimension, "depth": depth})
        return node

    def connect(self, node_a_id: str, node_b_id: str, weight: float = 1.0):
        """Create a bidirectional edge between concepts."""
        if node_a_id in self.nodes and node_b_id in self.nodes:
            self.edges[node_a_id].append((node_b_id, weight))
            self.edges[node_b_id].append((node_a_id, weight))
            self.nodes[node_a_id].connections.append(node_b_id)
            self.nodes[node_b_id].connections.append(node_a_id)

    def add_dimension(self, name: str, description: str, created_by: str,
                      parent: str | None = None, abstraction_level: int = 1) -> CognitiveDimension:
        dim = CognitiveDimension(
            name=name,
            description=description,
            created_by=created_by,
            parent_dimension=parent,
            abstraction_level=abstraction_level
        )
        self.dimensions[name] = dim
        self._log_expansion("dimension_created", {"name": name, "created_by": created_by, "level": abstraction_level})
        return dim

    # ── Metrics ────────────────────────────────────────────────────────────

    @property
    def cognitive_volume(self) -> int:
        return len(self.nodes)

    @property
    def dimension_count(self) -> int:
        return len(self.dimensions)

    @property
    def edge_count(self) -> int:
        return sum(len(v) for v in self.edges.values()) // 2

    @property
    def connectivity_density(self) -> float:
        n = self.cognitive_volume
        if n < 2:
            return 0.0
        max_edges = n * (n - 1) / 2
        return self.edge_count / max_edges if max_edges > 0 else 0.0

    @property
    def mean_gravity(self) -> float:
        if not self.nodes:
            return 0.0
        return sum(n.gravity for n in self.nodes.values()) / len(self.nodes)

    @property
    def mean_coherence(self) -> float:
        if not self.nodes:
            return 1.0
        return sum(n.coherence for n in self.nodes.values()) / len(self.nodes)

    @property
    def max_depth(self) -> int:
        if not self.nodes:
            return 0
        return max(n.depth for n in self.nodes.values())

    def reachable_reality_score(self) -> float:
        """
        Composite metric: how much structured reality this space can represent.
        R = f(volume, dimensions, connectivity, coherence, depth)
        """
        v = math.log1p(self.cognitive_volume)
        d = math.log1p(self.dimension_count)
        c = self.connectivity_density
        coh = self.mean_coherence
        depth = math.log1p(self.max_depth)
        return round((v * d * (1 + c) * coh * (1 + depth)), 4)

    def snapshot(self) -> dict:
        return {
            "cognitive_volume": self.cognitive_volume,
            "dimension_count": self.dimension_count,
            "edge_count": self.edge_count,
            "connectivity_density": round(self.connectivity_density, 4),
            "mean_gravity": round(self.mean_gravity, 3),
            "mean_coherence": round(self.mean_coherence, 3),
            "max_depth": self.max_depth,
            "reachable_reality_score": self.reachable_reality_score(),
            "expansion_events": len(self.expansion_log),
            "coherence_violations": len(self.coherence_violations),
            "dimensions": {k: v.to_dict() for k, v in self.dimensions.items()},
        }

    def _log_expansion(self, event_type: str, data: dict):
        self.expansion_log.append({
            "timestamp": time.time(),
            "event": event_type,
            **data
        })

    def get_attractor_nodes(self, top_n: int = 5) -> list[ConceptNode]:
        """Return highest-gravity nodes — the cognitive attractors."""
        return sorted(self.nodes.values(), key=lambda n: n.gravity * len(n.connections), reverse=True)[:top_n]

    def find_by_label(self, label: str) -> ConceptNode | None:
        for node in self.nodes.values():
            if node.label.lower() == label.lower():
                return node
        return None