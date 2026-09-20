"""Optional Rust/C++ acceleration for hot cognitive-space metrics."""

from __future__ import annotations

import ctypes
import hashlib
import math
import os
import platform
from pathlib import Path


_ROOT = Path(__file__).resolve().parents[1]
_LIBRARY_NAMES = {
    "Windows": ("void_metrics.dll", "libvoid_metrics.dll"),
    "Darwin": ("libvoid_metrics.dylib",),
    "Linux": ("libvoid_metrics.so",),
}
_REQUIRED_SYMBOLS = (
    "void_reachable_reality_score",
    "void_assign_vector",
    "void_normalize_weights",
    "void_entropy",
    "void_blend_vectors",
    "void_occam_score",
    "void_decay_weight",
    "void_bayesian_confidence",
    "void_algorithm_count",
)


def _library_candidates(requested: str) -> list[Path]:
    names = _LIBRARY_NAMES.get(platform.system(), ("libvoid_metrics.so",))
    candidates: list[Path] = []
    if requested in {"auto", "rust"}:
        candidates.extend(
            _ROOT / "native" / "rust" / "target" / "release" / name
            for name in names
        )
    if requested in {"auto", "cpp"}:
        candidates.extend(
            _ROOT / "native" / "build" / suffix / name
            for suffix in ("", "Release", "Debug")
            for name in names
        )
    return candidates


def _load_backend() -> tuple[ctypes.CDLL | None, str]:
    requested = os.getenv("VOID_NATIVE_BACKEND", "auto").lower()
    if requested == "python":
        return None, "python"

    candidates = _library_candidates(requested)
    for candidate in candidates:
        if candidate.exists():
            try:
                library = ctypes.CDLL(str(candidate))
                if any(not hasattr(library, symbol) for symbol in _REQUIRED_SYMBOLS):
                    if requested in {"rust", "cpp"}:
                        raise RuntimeError(f"Native backend at {candidate} has an outdated ABI")
                    continue
                function = library.void_reachable_reality_score
                function.argtypes = [
                    ctypes.c_ulonglong,
                    ctypes.c_ulonglong,
                    ctypes.c_ulonglong,
                    ctypes.c_double,
                    ctypes.c_ulonglong,
                ]
                function.restype = ctypes.c_double
                return library, candidate.parent.name
            except (OSError, AttributeError):
                if requested in {"rust", "cpp"}:
                    raise

    if requested in {"rust", "cpp"}:
        raise RuntimeError(f"Requested native backend '{requested}' is not built")
    return None, "python"


_LIBRARY, BACKEND_NAME = _load_backend()


def _configure_array_function(name: str, argument_types: list, return_type=None):
    if _LIBRARY is None:
        return None
    function = getattr(_LIBRARY, name)
    function.argtypes = argument_types
    function.restype = return_type
    return function


if _LIBRARY is not None:
    _native_assign_vector = _configure_array_function(
        "void_assign_vector", [ctypes.c_void_p, ctypes.c_ulonglong, ctypes.c_uint, ctypes.POINTER(ctypes.c_double)]
    )
    _native_normalize_weights = _configure_array_function(
        "void_normalize_weights", [ctypes.POINTER(ctypes.c_double), ctypes.c_uint, ctypes.POINTER(ctypes.c_double)]
    )
    _native_entropy = _configure_array_function(
        "void_entropy", [ctypes.POINTER(ctypes.c_double), ctypes.c_uint], ctypes.c_double
    )
    _native_blend_vectors = _configure_array_function(
        "void_blend_vectors", [ctypes.POINTER(ctypes.c_double), ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_double)]
    )
    _native_occam_score = _configure_array_function(
        "void_occam_score", [ctypes.c_double, ctypes.c_double, ctypes.c_double], ctypes.c_double
    )
    _native_decay_weight = _configure_array_function(
        "void_decay_weight", [ctypes.c_double, ctypes.c_double, ctypes.c_double], ctypes.c_double
    )
    _native_bayesian_confidence = _configure_array_function(
        "void_bayesian_confidence", [ctypes.c_double, ctypes.c_double, ctypes.c_double], ctypes.c_double
    )
    _native_algorithm_count = _configure_array_function("void_algorithm_count", [], ctypes.c_uint)
else:
    _native_assign_vector = _native_normalize_weights = _native_entropy = _native_blend_vectors = None
    _native_occam_score = _native_decay_weight = _native_bayesian_confidence = _native_algorithm_count = None


def reachable_reality_score(
    node_count: int,
    dimension_count: int,
    edge_count: int,
    mean_coherence: float,
    max_depth: int,
) -> float:
    """Calculate the score through Rust/C++ when available, otherwise Python."""
    if _LIBRARY is not None:
        return _LIBRARY.void_reachable_reality_score(
            node_count, dimension_count, edge_count, mean_coherence, max_depth
        )

    volume = math.log1p(node_count)
    dimensions = math.log1p(dimension_count)
    possible_edges = node_count * (node_count - 1) / 2
    connectivity = edge_count / possible_edges if possible_edges > 0 else 0.0
    depth = math.log1p(max_depth)
    return volume * dimensions * (1 + connectivity) * mean_coherence * (1 + depth)


def assign_vector(text: str, dimensions: int) -> tuple[float, ...]:
    if _LIBRARY is not None:
        output = (ctypes.c_double * dimensions)()
        encoded = text.encode()
        _native_assign_vector(encoded, len(encoded), dimensions, output)
        return tuple(round(value, 6) for value in output)
    values = []
    for index in range(dimensions):
        digest = hashlib.sha256(f"{index}:{text}".encode()).digest()
        raw = int.from_bytes(digest[index:index + 4], "big") / 2**32
        values.append(raw * 2.0 - 1.0)
    length = math.sqrt(sum(value * value for value in values)) or 1.0
    return tuple(round(value / length, 6) for value in values)


def normalize_weights(values: tuple[float, ...]) -> tuple[float, ...]:
    if _LIBRARY is not None:
        source = (ctypes.c_double * len(values))(*values)
        output = (ctypes.c_double * len(values))()
        _native_normalize_weights(source, len(values), output)
        return tuple(round(value, 6) for value in output)
    magnitudes = [abs(value) for value in values]
    total = sum(magnitudes) or 1.0
    return tuple(round(value / total, 6) for value in magnitudes)


def entropy(weights: tuple[float, ...]) -> float:
    if _LIBRARY is not None:
        source = (ctypes.c_double * len(weights))(*weights)
        return round(_native_entropy(source, len(weights)), 6)
    probabilities = [value for value in weights if value > 0]
    if len(probabilities) <= 1:
        return 0.0
    return round(-sum(value * math.log(value) for value in probabilities) / math.log(len(probabilities)), 6)


def blend_vectors(vectors: list[tuple[float, ...]], dimensions: int) -> tuple[float, ...]:
    if not vectors:
        return tuple(0.0 for _ in range(dimensions))
    if _LIBRARY is not None:
        flattened = (ctypes.c_double * (len(vectors) * dimensions))(
            *(value for vector in vectors for value in vector)
        )
        output = (ctypes.c_double * dimensions)()
        _native_blend_vectors(flattened, len(vectors), dimensions, output)
        return tuple(round(value, 6) for value in output)
    return tuple(round(sum(vector[index] for vector in vectors) / len(vectors), 6) for index in range(dimensions))


def backend_status() -> dict[str, str | bool]:
    return {
        "name": BACKEND_NAME,
        "native": _LIBRARY is not None,
        "algorithm_count": int(_native_algorithm_count()) if _native_algorithm_count else 50,
    }


def occam_score(evidence: float, complexity: float, assumptions: float) -> float:
    if _native_occam_score:
        return _native_occam_score(evidence, complexity, assumptions)
    return max(0.0, min(1.0, max(0.0, evidence) / (1.0 + max(0.0, complexity) + max(0.0, assumptions))))


def decay_weight(initial: float, elapsed: float, half_life: float) -> float:
    if _native_decay_weight:
        return _native_decay_weight(initial, elapsed, half_life)
    if half_life <= 0.0:
        return 0.0
    return max(0.0, initial) * math.exp(-math.log(2.0) * max(0.0, elapsed) / half_life)


def bayesian_confidence(prior: float, likelihood: float, contradiction: float) -> float:
    if _native_bayesian_confidence:
        return _native_bayesian_confidence(prior, likelihood, contradiction)
    prior = max(0.0, min(1.0, prior))
    likelihood = max(0.0, min(1.0, likelihood))
    numerator = prior * likelihood
    denominator = numerator + (1.0 - prior) * (1.0 - likelihood)
    if denominator <= 0.0:
        return 0.0
    return max(0.0, min(1.0, numerator / denominator * (1.0 - max(0.0, min(1.0, contradiction)))))