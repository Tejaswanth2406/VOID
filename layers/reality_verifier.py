"""
Reality Verifier Layer
The engine that tests internal models against external reality.
Intelligence without grounding drifts into hallucination.
This layer is the anchor.
"""

from __future__ import annotations
import json
from dataclasses import dataclass
from anthropic import Anthropic
from core.space import CognitiveSpace


@dataclass
class VerificationResult:
    verified_claims: list[str]
    unverified_claims: list[str]
    contradicted_claims: list[str]
    reality_fidelity_score: float   # 0-1
    confidence_adjustment: float    # how much to adjust output confidence
    grounding_notes: str


class RealityVerifier:
    """
    After simulation and synthesis, verify claims against grounded knowledge.
    
    Three outcomes for each claim:
    - VERIFIED: consistent with established knowledge
    - UNVERIFIED: plausible but uncertain — mark clearly
    - CONTRADICTED: conflicts with established reality — flag or remove
    
    Reality fidelity is tracked across the cognitive space.
    Nodes with verified claims gain higher gravity.
    """

    def __init__(self, space: CognitiveSpace, client: Anthropic):
        self.space = space
        self.client = client
        self.verification_history: list[VerificationResult] = []
        self.cumulative_fidelity: list[float] = []

    def verify(self, query: str, draft_response: str, plan_strategy: str) -> VerificationResult:
        """Extract and verify claims from the draft response."""

        prompt = f"""You are the reality verification layer of a cognitive architecture.
Your job: extract factual claims from a draft response and assess their accuracy.

Query: {query}
Draft response (first 800 chars): {draft_response[:800]}
Reasoning strategy used: {plan_strategy}

For each factual or empirical claim:
1. VERIFIED: You are confident this is accurate based on established knowledge
2. UNVERIFIED: Plausible but uncertain — should be marked with appropriate hedging
3. CONTRADICTED: This conflicts with established knowledge — should be removed/corrected

Also assess:
- Overall reality fidelity score (0-1): how grounded is this response?
- Confidence adjustment: positive if response is well-grounded, negative if speculative

Respond ONLY as JSON:
{{
  "verified_claims": ["claim1", "claim2"],
  "unverified_claims": ["claim3"],
  "contradicted_claims": ["claim4"],
  "reality_fidelity_score": 0.8,
  "confidence_adjustment": 0.1,
  "grounding_notes": "brief notes on reliability of response..."
}}"""

        resp = self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=900,
            messages=[{"role": "user", "content": prompt}]
        )

        result = VerificationResult(
            verified_claims=[],
            unverified_claims=[],
            contradicted_claims=[],
            reality_fidelity_score=0.7,
            confidence_adjustment=0.0,
            grounding_notes="Verification incomplete"
        )

        try:
            raw = resp.content[0].text.strip()
            if "```" in raw:
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            data = json.loads(raw.strip())
            result = VerificationResult(**{k: data[k] for k in VerificationResult.__dataclass_fields__ if k in data})
        except Exception:
            pass

        # Update node reality grounding
        for claim in result.verified_claims:
            # Boost gravity of nodes whose content appears in verified claims
            for node in self.space.nodes.values():
                if node.label.lower() in claim.lower():
                    node.reality_grounded = True
                    node.gravity = min(5.0, node.gravity * 1.05)

        # Penalize nodes mentioned in contradicted claims
        for claim in result.contradicted_claims:
            for node in self.space.nodes.values():
                if node.label.lower() in claim.lower():
                    node.coherence *= 0.8
                    node.gravity *= 0.9

        self.cumulative_fidelity.append(result.reality_fidelity_score)
        self.verification_history.append(result)
        return result

    @property
    def mean_fidelity(self) -> float:
        if not self.cumulative_fidelity:
            return 1.0
        return sum(self.cumulative_fidelity) / len(self.cumulative_fidelity)

    def format_summary(self, result: VerificationResult) -> str:
        lines = ["\n[Reality Verifier]\n"]
        lines.append(f"  Fidelity score: {result.reality_fidelity_score:.2f}")
        lines.append(f"  Verified claims: {len(result.verified_claims)}")
        if result.unverified_claims:
            lines.append(f"  ⚠ Unverified: {len(result.unverified_claims)}")
        if result.contradicted_claims:
            lines.append(f"  ✗ Contradicted: {len(result.contradicted_claims)}")
        lines.append(f"  Notes: {result.grounding_notes}")
        return "\n".join(lines)