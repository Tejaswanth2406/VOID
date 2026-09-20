"""
CSTI Engine — REST API Server
FastAPI-based HTTP interface for the engine.
Allows integration with any frontend, other services, or remote clients.

Run:
    uvicorn api.server:app --reload --port 8000

Endpoints:
    POST /query          — run a cognitive cycle
    GET  /status         — full engine status
    GET  /space          — cognitive space snapshot
    GET  /attractors     — top attractor nodes
    GET  /dimensions     — all dimensions
    POST /export         — trigger export
    GET  /health         — health check
    WS   /stream         — streaming cognitive cycle (WebSocket)
"""

from __future__ import annotations
import os
import sys
import json
import time
import asyncio
from typing import Any

# Ensure project root on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel, Field
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

from core.engine import CSTIEngine
from config.settings import EngineConfig, fast_config, deep_config
from utils.exporter import auto_export


# ── Pydantic Models ────────────────────────────────────────────────────────────

if FASTAPI_AVAILABLE:
    class QueryRequest(BaseModel):
        query: str = Field(..., min_length=1, max_length=2000)
        mode: str  = Field("standard", pattern="^(fast|standard|deep)$")
        save:  bool = True

    class ExportRequest(BaseModel):
        output_dir: str = "exports"

    class HealthResponse(BaseModel):
        status: str
        cycles: int
        cognitive_volume: int
        rr_score: float
        uptime_seconds: float


# ── App Setup ──────────────────────────────────────────────────────────────────

def create_app(config: EngineConfig | None = None) -> Any:
    if not FASTAPI_AVAILABLE:
        raise RuntimeError(
            "FastAPI not installed. Run: pip install fastapi uvicorn"
        )

    cfg = config or EngineConfig.from_env()
    engine = CSTIEngine(verbose=cfg.verbose)
    start_time = time.time()

    app = FastAPI(
        title="CSTI Engine API",
        description="Computational Space Theory of Intelligence — REST API",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    cycle_history: list[dict] = []

    # ── Routes ─────────────────────────────────────────────────────────────────

    @app.get("/health", response_model=HealthResponse)
    def health():
        snap = engine.space.snapshot()
        return {
            "status": "ok",
            "cycles": engine.cycle_count,
            "cognitive_volume": snap["cognitive_volume"],
            "rr_score": snap["reachable_reality_score"],
            "uptime_seconds": round(time.time() - start_time, 1),
        }

    @app.post("/query")
    def run_query(req: QueryRequest):
        """Run a full cognitive cycle and return the report."""
        try:
            report = engine.process(req.query)
            cycle_history.append(report)
            if req.save and cfg.auto_save:
                engine.memory.save()
            return {
                "ok": True,
                "cycle": report["cycle"],
                "response": report["response"],
                "key_insight": report.get("key_insight", ""),
                "meaning_density": report.get("meaning_density", 0),
                "follow_on_frontiers": report.get("follow_on_frontiers", []),
                "cognitive_expansion": report.get("cognitive_expansion", {}),
                "new_concepts": report.get("new_concepts", []),
                "new_dimensions": report.get("new_dimensions", []),
                "verification": report.get("verification", {}),
                "reflection": report.get("reflection", {}),
                "reasoning_plan": report.get("reasoning_plan", {}),
                "cycle_time_seconds": report.get("cycle_time_seconds", 0),
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/status")
    def get_status():
        """Full engine status including all layer summaries."""
        return engine.get_status()

    @app.get("/space")
    def get_space():
        """Cognitive space snapshot."""
        return engine.space.snapshot()

    @app.get("/cognition")
    def get_cognition():
        """Latest vector, weight distribution, entropy, and dream state."""
        return engine.space.substrate.snapshot()

    @app.get("/mnemonics")
    def get_mnemonics():
        """Available mnemonic encoding systems."""
        return engine.space.mnemonics.snapshot()

    @app.get("/mnemonics/encode")
    def encode_mnemonic(value: int, system: str = "major"):
        """Encode a number through one of the registered mnemonic systems."""
        try:
            return {
                "value": value,
                "system": system,
                "encoding": engine.space.mnemonics.encode(value, system),
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))

    @app.get("/attractors")
    def get_attractors(top_n: int = 10):
        """Top attractor nodes by cognitive gravity."""
        nodes = engine.space.get_attractor_nodes(top_n)
        return {
            "count": len(nodes),
            "attractors": [n.to_dict() for n in nodes],
        }

    @app.get("/dimensions")
    def get_dimensions():
        """All cognitive dimensions."""
        return {
            "count": len(engine.space.dimensions),
            "dimensions": {
                name: dim.to_dict()
                for name, dim in engine.space.dimensions.items()
            }
        }

    @app.get("/nodes")
    def get_nodes(dimension: str | None = None, min_gravity: float = 0.0, limit: int = 50):
        """Query nodes with optional filters."""
        nodes = list(engine.space.nodes.values())
        if dimension:
            nodes = [n for n in nodes if n.dimension == dimension]
        nodes = [n for n in nodes if n.gravity >= min_gravity]
        nodes.sort(key=lambda n: n.gravity, reverse=True)
        return {
            "count": len(nodes),
            "nodes": [n.to_dict() for n in nodes[:limit]],
        }

    @app.get("/history")
    def get_history(last_n: int = 10):
        """Recent cycle reports."""
        recent = cycle_history[-last_n:]
        return {
            "total_cycles": len(cycle_history),
            "returned": len(recent),
            "cycles": [
                {
                    "cycle": r["cycle"],
                    "query": r["query"],
                    "key_insight": r.get("key_insight", ""),
                    "rr_delta": r["cognitive_expansion"].get("rr_delta", 0),
                    "meaning_density": r.get("meaning_density", 0),
                    "cycle_time_seconds": r.get("cycle_time_seconds", 0),
                }
                for r in recent
            ]
        }

    @app.post("/export")
    def export(req: ExportRequest):
        """Export cognitive space to JSON, Markdown, and text."""
        try:
            paths = auto_export(engine.space, cycle_history, req.output_dir)
            return {"ok": True, "files": {k: str(v) for k, v in paths.items()}}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/save")
    def save():
        """Manually trigger memory save."""
        engine.memory.save()
        return {"ok": True, "message": "Cognitive space saved to disk."}

    @app.delete("/memory")
    def clear_memory():
        """
        Clear session memory (does not delete disk file).
        WARNING: This resets the in-memory cognitive space.
        """
        engine.space.nodes.clear()
        engine.space.edges.clear()
        engine.space.expansion_log.clear()
        engine.space._init_core_dimensions()
        return {"ok": True, "message": "In-memory cognitive space cleared."}

    # ── WebSocket streaming ─────────────────────────────────────────────────────

    @app.websocket("/stream")
    async def stream_query(ws: WebSocket):
        """
        WebSocket endpoint for streaming cognitive cycle progress.
        Send: {"query": "..."}
        Receive: multiple JSON messages, one per step, then final report.
        """
        await ws.accept()
        try:
            data = await ws.receive_json()
            query = data.get("query", "")
            if not query:
                await ws.send_json({"error": "No query provided"})
                return

            # Stream step notifications
            steps = [
                "MetaReasoner: planning reasoning strategy",
                "Memory: recalling relevant concepts",
                "Simulation: running internal models",
                "Draft: generating initial response",
                "Reflection: self-modeling reasoning",
                "Memory: extracting new concepts",
                "DimensionEngine: scanning for new dimensions",
                "CoherenceFilter: checking space integrity",
                "RealityVerifier: grounding in reality",
                "MeaningSynthesizer: compressing to output",
            ]

            # Send step notifications asynchronously while engine runs
            for i, step in enumerate(steps):
                await ws.send_json({"type": "step", "step": i + 1, "total": len(steps), "label": step})
                await asyncio.sleep(0.05)

            # Run engine in executor to avoid blocking the event loop
            loop = asyncio.get_event_loop()
            report = await loop.run_in_executor(None, engine.process, query)
            cycle_history.append(report)

            await ws.send_json({"type": "complete", "report": {
                "cycle": report["cycle"],
                "response": report["response"],
                "key_insight": report.get("key_insight", ""),
                "cognitive_expansion": report.get("cognitive_expansion", {}),
                "new_concepts": report.get("new_concepts", []),
                "new_dimensions": report.get("new_dimensions", []),
                "meaning_density": report.get("meaning_density", 0),
                "follow_on_frontiers": report.get("follow_on_frontiers", []),
            }})

        except WebSocketDisconnect:
            pass
        except Exception as e:
            try:
                await ws.send_json({"type": "error", "detail": str(e)})
            except Exception:
                pass

    return app


# ── Entry point ────────────────────────────────────────────────────────────────

# Only instantiate at module level when FastAPI is available (avoids import errors)
app = create_app() if FASTAPI_AVAILABLE else None


if __name__ == "__main__":
    try:
        import uvicorn
    except ImportError:
        print("uvicorn not installed. Run: pip install uvicorn fastapi")
        sys.exit(1)

    uvicorn.run(
        "api.server:app",
        host=os.getenv("CSTI_HOST", "0.0.0.0"),
        port=int(os.getenv("CSTI_PORT", "8000")),
        reload=os.getenv("CSTI_RELOAD", "true").lower() == "true",
        log_level="info",
    )