"""Optional Rust/C++ acceleration for hot cognitive-space metrics."""

from __future__ import annotations

import ctypes
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