"""Deterministic cognitive primitives for vectors, entropy, dreams, and mnemonics."""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass, field


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


class CognitiveSubstrate:
    """A small, transparent state machine behind higher-level reasoning."""

    def __init__(self, dimensions: tuple[str, ...] = DEFAULT_DIMENSIONS):
        self.dimensions = dimensions
        self.blackhole = Attractor("blackhole", "compression")
        self.whitehole = Attractor("whitehole", "generation")
        self.history: list[dict] = []
        self.last_state: dict = {}

    def assign_vector(self, text: str) -> tuple[float, ...]:
        values = []
        for index, dimension in enumerate(self.dimensions):
            digest = hashlib.sha256(f"{dimension}:{text}".encode()).digest()
            raw = int.from_bytes(digest[index:index + 4], "big") / 2**32
            values.append(raw * 2.0 - 1.0)
        length = math.sqrt(sum(value * value for value in values)) or 1.0
        return tuple(round(value / length, 6) for value in values)

    def weight_distribution(self, vector: tuple[float, ...]) -> dict[str, float]:
        magnitudes = [abs(value) for value in vector]
        total = sum(magnitudes) or 1.0
        return {
            dimension: round(magnitude / total, 6)
            for dimension, magnitude in zip(self.dimensions, magnitudes)
        }

    @staticmethod
    def entropy(weights: dict[str, float]) -> float:
        probabilities = [value for value in weights.values() if value > 0]
        if len(probabilities) <= 1:
            return 0.0
        value = -sum(probability * math.log(probability) for probability in probabilities)
        return round(value / math.log(len(probabilities)), 6)

    def dream(self, query: str, concepts: list[str], steps: int = 3) -> dict:
        seeds = concepts[: max(1, steps)] or [query]
        vectors = [self.assign_vector(seed) for seed in seeds]
        blended = tuple(
            round(sum(vector[index] for vector in vectors) / len(vectors), 6)
            for index in range(len(self.dimensions))
        )
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
        self.blackhole.absorb(dominant, weights[dominant])
        state = {
            "vector": vector,
            "weights": weights,
            "entropy": entropy,
            "dominant_dimension": dominant,
            "dream": self.dream(query, concepts),
        }
        self.last_state = state
        self.history.append(state)
        return state

    def snapshot(self) -> dict:
        return {
            "dimensions": list(self.dimensions),
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