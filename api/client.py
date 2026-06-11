"""
CSTI Engine — Python API Client
Thin client for interacting with the CSTI REST API.
Use this when the engine runs as a separate server process.

Example:
    client = CSTIClient("http://localhost:8000")
    result = client.query("What is the nature of causality?")
    print(result["response"])
    print(result["key_insight"])
"""

from __future__ import annotations
import json
from typing import Any

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class CSTIClient:
    """REST client for the CSTI Engine API."""

    def __init__(self, base_url: str = "http://localhost:8000", timeout: int = 120):
        if not REQUESTS_AVAILABLE:
            raise RuntimeError("requests not installed. Run: pip install requests")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _get(self, path: str, params: dict | None = None) -> dict:
        resp = self.session.get(f"{self.base_url}{path}", params=params, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def _post(self, path: str, data: dict) -> dict:
        resp = self.session.post(f"{self.base_url}{path}", json=data, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def health(self) -> dict:
        """Check engine health."""
        return self._get("/health")

    def query(self, query: str, mode: str = "standard", save: bool = True) -> dict:
        """
        Run a cognitive cycle.
        Returns full report including response, key_insight, expansion metrics.
        """
        return self._post("/query", {"query": query, "mode": mode, "save": save})

    def status(self) -> dict:
        """Full engine status."""
        return self._get("/status")

    def space(self) -> dict:
        """Cognitive space snapshot."""
        return self._get("/space")

    def attractors(self, top_n: int = 10) -> list[dict]:
        """Top attractor nodes."""
        return self._get("/attractors", {"top_n": top_n})["attractors"]

    def dimensions(self) -> dict:
        """All cognitive dimensions."""
        return self._get("/dimensions")["dimensions"]

    def nodes(
        self,
        dimension: str | None = None,
        min_gravity: float = 0.0,
        limit: int = 50,
    ) -> list[dict]:
        """Query nodes with optional filters."""
        params: dict[str, Any] = {"min_gravity": min_gravity, "limit": limit}
        if dimension:
            params["dimension"] = dimension
        return self._get("/nodes", params)["nodes"]

    def history(self, last_n: int = 10) -> list[dict]:
        """Recent cycle summaries."""
        return self._get("/history", {"last_n": last_n})["cycles"]

    def export(self, output_dir: str = "exports") -> dict:
        """Trigger export on the server side."""
        return self._post("/export", {"output_dir": output_dir})

    def save(self) -> dict:
        """Trigger memory save on the server."""
        return self._post("/save", {})

    def print_response(self, result: dict):
        """Pretty-print a query result."""
        import textwrap
        print("\n" + "─" * 60)
        print("RESPONSE")
        print("─" * 60)
        for line in result.get("response", "").splitlines():
            if line.strip():
                print(textwrap.fill(line, width=68))
            else:
                print()

        if result.get("key_insight"):
            print(f"\nKEY INSIGHT: {result['key_insight']}")

        exp = result.get("cognitive_expansion", {})
        print(f"\nRR Score: {exp.get('rr_before', 0):.4f} → {exp.get('rr_after', 0):.4f} "
              f"(Δ{exp.get('rr_delta', 0):+.4f})")
        print(f"New concepts: {result.get('new_concepts', [])}")
        if result.get("new_dimensions"):
            print(f"✦ New dimensions: {result['new_dimensions']}")
        print("─" * 60)


# ── CLI usage ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    client = CSTIClient(url)

    try:
        h = client.health()
        print(f"Engine online | cycles={h['cycles']} | "
              f"nodes={h['cognitive_volume']} | RR={h['rr_score']:.4f}")
    except Exception as e:
        print(f"Cannot connect to {url}: {e}")
        sys.exit(1)

    print(f"\nConnected to CSTI Engine at {url}")
    print("Type queries, or 'status', 'attractors', 'dimensions', 'quit'\n")

    while True:
        try:
            q = input("client ▶ ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not q:
            continue
        if q.lower() in ("quit", "q", "exit"):
            break
        elif q.lower() == "status":
            import pprint
            pprint.pprint(client.status())
        elif q.lower() == "attractors":
            for a in client.attractors(8):
                print(f"  {a['label']:<25} g={a['gravity']:.2f}  [{a['dimension']}]")
        elif q.lower() == "dimensions":
            for name, dim in client.dimensions().items():
                print(f"  [{dim['abstraction_level']}] {name}: {dim['description'][:50]}")
        else:
            try:
                result = client.query(q)
                client.print_response(result)
            except Exception as e:
                print(f"Error: {e}")