"""
Coherence Filter
Intelligence requires not just expansion, but coherent expansion.
Contradictions, paradoxes, and cognitive black holes must be identified and handled.

This is the immune system of the cognitive space.
"""

from __future__ import annotations
import json
from dataclasses import dataclass
from anthropic import Anthropic
from core.space import CognitiveSpace


@dataclass
class CoherenceIssue:
    issue_type: str          # "contradiction" | "black_hole" | "orphan" | "instability"
    node_ids: list[str]
    description: str
    severity: float          # 0-1
    resolution: str


class CoherenceFilter:
    """
    Not all expansion is healthy.
    Some concepts trap computation in infinite loops.
    Some contradict established nodes.
    Some are orphaned from the main structure.

    The coherence filter maintains the health of the cognitive space.
    """

    def __init__(self, space: CognitiveSpace, client: Anthropic):
        self.space = space
        self.client = client
        self.issues_found: list[CoherenceIssue] = []
        self.resolutions_applied: int = 0

    def scan(self, new_node_labels: list[str]) -> list[CoherenceIssue]:
        """Scan newly added concepts for coherence issues."""
        if not new_node_labels:
            return []

        attractor_context = [
            {"label": n.label, "content": n.content[:100], "dimension": n.dimension}
            for n in self.space.get_attractor_nodes(10)
        ]

        prompt = f"""You are the coherence filter of a cognitive architecture.
Scan these newly added concepts for coherence issues.

New concepts: {new_node_labels}
Established attractor concepts: {json.dumps(attractor_context, indent=2)}

Check for:
1. CONTRADICTION: new concept directly contradicts an established attractor
2. BLACK_HOLE: concept is so self-referential it traps reasoning
3. ORPHAN: concept has no meaningful connection to the existing space
4. INSTABILITY: concept definition is internally incoherent

Only flag genuine problems. If all is coherent, return empty list.

Respond ONLY as JSON:
{{
  "issues": [
    {{
      "issue_type": "contradiction",
      "node_ids": [],
      "description": "...",
      "severity": 0.7,
      "resolution": "how to fix or quarantine this..."
    }}
  ]
}}"""

        resp = self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}]
        )

        issues = []
        try:
            raw = resp.content[0].text.strip()
            if "```" in raw:
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            data = json.loads(raw.strip())
            for i in data.get("issues", []):
                issue = CoherenceIssue(**{k: i[k] for k in CoherenceIssue.__dataclass_fields__ if k in i})
                issues.append(issue)
                self.issues_found.append(issue)

                # Penalize incoherent nodes
                for label in i.get("node_ids", []):
                    node = self.space.find_by_label(label)
                    if node and i.get("severity", 0) > 0.6:
                        node.coherence *= (1 - i["severity"] * 0.3)
                        self.space.coherence_violations.append(label)

        except Exception:
            pass

        return issues

    def apply_resolution(self, issue: CoherenceIssue):
        """Apply resolution strategy for an issue."""
        if issue.issue_type == "orphan":
            # Connect orphan to nearest attractor
            for label in issue.node_ids:
                orphan = self.space.find_by_label(label)
                attractors = self.space.get_attractor_nodes(3)
                if orphan and attractors:
                    self.space.connect(orphan.id, attractors[0].id, weight=0.3)
        self.resolutions_applied += 1

    def get_coherence_report(self) -> dict:
        return {
            "total_issues": len(self.issues_found),
            "resolutions_applied": self.resolutions_applied,
            "violations_in_space": len(self.space.coherence_violations),
            "space_coherence_score": round(self.space.mean_coherence, 3),
            "recent_issues": [
                {"type": i.issue_type, "severity": i.severity}
                for i in self.issues_found[-5:]
            ]
        }