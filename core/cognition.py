"""Deterministic cognitive primitives for vectors, entropy, dreams, and mnemonics."""

from __future__ import annotations

from dataclasses import dataclass, field

from utils.native_backend import (
    assign_vector,
    bayesian_confidence,
    backend_status,
    blend_vectors,
    decay_weight,
    entropy,
    normalize_weights,
    occam_score,
)


ALGORITHMS = (
    "Occam's Razor", "Bayesian Updating", "Exponential Decay", "Entropy", "Vector Normalization",
    "Cosine Similarity", "Euclidean Distance", "Weighted Average", "Softmax", "Top-K Selection",
    "Kahan Summation", "Moving Average", "Exponential Smoothing", "Graph Connectivity", "PageRank",
    "Breadth-First Search", "Depth-First Search", "Dijkstra Shortest Path", "Union-Find", "Jaccard Similarity",
    "Min-Max Scaling", "Z-Score Normalization", "Reservoir Sampling", "Fisher-Yates Shuffle", "Bloom Filter",
    "LRU Eviction", "Leitner Scheduling", "Spaced Repetition", "Doomsday Algorithm", "Major System",
    "Dominic System", "Peg System", "Method of Loci", "Link Method", "Feynman Technique",
    "Counterfactual Simulation", "Monte Carlo Sampling", "Beam Search", "Constraint Propagation", "Conflict Resolution",
    "Blackhole Compression", "Whitehole Generation", "Dream Blending", "Coherence Filtering", "Reality Grounding",
    "Attractor Ranking", "Dimension Expansion", "Memory Recall", "Evidence Calibration", "Safety Bounds",
)


DEFAULT_DIMENSIONS = (
    "causality",
    "temporality",
    "abstraction",
    "self_model",
    "simulation",
    "reality",
    "meaning",
    "memory",
)


@dataclass
class Attractor:
    name: str
    kind: str
    mass: float = 0.0
    absorbed: list[str] = field(default_factory=list)

    def absorb(self, label: str, weight: float) -> None:
        self.mass += max(0.0, weight)
        if label not in self.absorbed:
            self.absorbed.append(label)


@dataclass(frozen=True)
class WorkflowAssessment:
    """Methodical decision trace for one cognitive pass."""

    phase: str
    simplicity: float
    retention: float
    confidence: float
    next_action: str

    def to_dict(self) -> dict:
        return {
            "phase": self.phase,
            "simplicity": self.simplicity,
            "retention": self.retention,
            "confidence": self.confidence,
            "next_action": self.next_action,
        }


class CognitiveSubstrate:
    """A small, transparent state machine behind higher-level reasoning."""

    def __init__(self, dimensions: tuple[str, ...] = DEFAULT_DIMENSIONS):
        self.dimensions = dimensions
        self.blackhole = Attractor("blackhole", "compression")
        self.whitehole = Attractor("whitehole", "generation")
        self.history: list[dict] = []
        self.last_state: dict = {}

    def assign_vector(self, text: str) -> tuple[float, ...]:
        return assign_vector(text, len(self.dimensions))

    def weight_distribution(self, vector: tuple[float, ...]) -> dict[str, float]:
        weights = normalize_weights(vector)
        return dict(zip(self.dimensions, weights))

    @staticmethod
    def entropy(weights: dict[str, float]) -> float:
        return entropy(tuple(weights.values()))

    def dream(self, query: str, concepts: list[str], steps: int = 3) -> dict:
        seeds = concepts[: max(1, steps)] or [query]
        vectors = [self.assign_vector(seed) for seed in seeds]
        blended = blend_vectors(vectors, len(self.dimensions))
        weights = self.weight_distribution(blended)
        dream = {
            "seeds": seeds,
            "vector": blended,
            "weights": weights,
            "entropy": self.entropy(weights),
            "novel_direction": max(weights, key=weights.get),
        }
        self.whitehole.absorb(dream["novel_direction"], 1.0 - dream["entropy"])
        return dream

    def analyze(self, query: str, concepts: list[str]) -> dict:
        vector = self.assign_vector(query)
        weights = self.weight_distribution(vector)
        entropy = self.entropy(weights)
        dominant = max(weights, key=weights.get)
        principles = {
            "occam_score": round(occam_score(1.0, sum(abs(value) for value in vector), len(concepts)), 6),
            "decay_weight": round(decay_weight(1.0, len(self.history), 30.0), 6),
            "bayesian_confidence": round(bayesian_confidence(0.5, 1.0 - entropy, 0.0), 6),
        }
        workflow = self._assess_workflow(principles, entropy)
        self.blackhole.absorb(dominant, weights[dominant])
        state = {
            "vector": vector,
            "weights": weights,
            "entropy": entropy,
            "dominant_dimension": dominant,
            "principles": principles,
            "workflow": workflow.to_dict(),
            "dream": self.dream(query, concepts),
        }
        self.last_state = state
        self.history.append(state)
        return state

    @staticmethod
    def _assess_workflow(principles: dict[str, float], entropy_value: float) -> WorkflowAssessment:
        """Apply observe -> compress -> simulate -> verify -> commit gates."""
        simplicity = principles["occam_score"]
        retention = principles["decay_weight"]
        confidence = principles["bayesian_confidence"]
        if simplicity < 0.25:
            return WorkflowAssessment("observe", simplicity, retention, confidence, "reduce assumptions")
        if entropy_value > 0.85:
            return WorkflowAssessment("compress", simplicity, retention, confidence, "focus the dominant dimension")
        if confidence < 0.45:
            return WorkflowAssessment("simulate", simplicity, retention, confidence, "generate competing hypotheses")
        if retention < 0.5:
            return WorkflowAssessment("verify", simplicity, retention, confidence, "refresh stale evidence")
        return WorkflowAssessment("commit", simplicity, retention, confidence, "store the verified concept")

    def snapshot(self) -> dict:
        return {
            "dimensions": list(self.dimensions),
            "backend": backend_status(),
            "algorithm_count": len(ALGORITHMS),
            "algorithms": list(ALGORITHMS),
            "last_state": self.last_state,
            "blackhole": self.blackhole.__dict__.copy(),
            "whitehole": self.whitehole.__dict__.copy(),
            "analyses": len(self.history),
        }


MAJOR_SYSTEM = {
    0: "S/Z", 1: "T/D", 2: "N", 3: "M", 4: "R", 5: "L",
    6: "J/SH", 7: "K/G", 8: "F/V", 9: "P/B",
}
DOMINIC_SYSTEM = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "S", 7: "G", 8: "H", 9: "N", 0: "O"}
PEG_SYSTEM = {1: "candle", 2: "swan", 3: "tree", 4: "door", 5: "hook", 6: "sticks", 7: "cliff", 8: "hourglass", 9: "balloon", 10: "bat"}


class MnemonicRegistry:
    """Encodings used by memory, palace, language, and calculation layers."""

    techniques = (
        "major", "peg_00_99", "pao", "dominic", "number_shape", "number_rhyme",
        "memory_palace", "gridland", "cicero", "card_palace", "link", "keyword",
        "phonetic_script", "acronym_matrix", "doomsday", "mental_abacus",
        "blindfold_chess", "feynman", "leitner", "synesthetic_mapping",
    )

    def encode(self, value: int, system: str = "major") -> str | dict:
        if system == "major":
            return " ".join(MAJOR_SYSTEM[int(digit)] for digit in str(abs(value)))
        if system == "dominic":
            return "".join(DOMINIC_SYSTEM[int(digit)] for digit in f"{abs(value):02d}")
        if system in {"number_shape", "number_rhyme"}:
            return PEG_SYSTEM.get(value, "unassigned")
        if system == "peg_00_99":
            return {"index": abs(value) % 100, "hook": f"peg-{abs(value) % 100:02d}"}
        raise ValueError(f"Unknown mnemonic system: {system}")

    def snapshot(self) -> dict:
        return {"techniques": list(self.techniques)}