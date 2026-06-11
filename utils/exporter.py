"""
CSTI Engine — Export Tools
Export cognitive space snapshots, cycle reports, and conversation history
to JSON, Markdown, and plain text formats.
"""

from __future__ import annotations
import json
import time
from pathlib import Path
from datetime import datetime
from core.space import CognitiveSpace


def export_json(space: CognitiveSpace, path: str | Path, include_edges: bool = True) -> Path:
    """Export full cognitive space to JSON."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "exported_at": datetime.now().isoformat(),
        "snapshot": space.snapshot(),
        "nodes": [
            {k: getattr(n, k) for k in n.__dataclass_fields__}
            for n in space.nodes.values()
        ],
        "dimensions": {k: v.to_dict() for k, v in space.dimensions.items()},
        "expansion_log": space.expansion_log[-200:],  # last 200 events
    }
    if include_edges:
        data["edges"] = {k: v for k, v in space.edges.items()}

    path.write_text(json.dumps(data, indent=2, default=str))
    return path


def export_markdown_report(
    space: CognitiveSpace,
    cycle_reports: list[dict],
    path: str | Path,
) -> Path:
    """Export a full Markdown report of the session."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    snap = space.snapshot()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# CSTI Engine Session Report",
        f"*Generated: {now}*",
        "",
        "---",
        "",
        "## Cognitive Space Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Cognitive Volume | {snap['cognitive_volume']} nodes |",
        f"| Dimensions | {snap['dimension_count']} |",
        f"| Edge Count | {snap['edge_count']} |",
        f"| Connectivity Density | {snap['connectivity_density']:.4f} |",
        f"| Mean Coherence | {snap['mean_coherence']:.3f} |",
        f"| Max Depth | {snap['max_depth']} |",
        f"| Reachable Reality Score | **{snap['reachable_reality_score']:.4f}** |",
        f"| Expansion Events | {snap['expansion_events']} |",
        "",
        "---",
        "",
        "## Active Dimensions",
        "",
    ]

    for name, dim in snap["dimensions"].items():
        lines.append(f"### `{name}` (Level {dim['abstraction_level']})")
        lines.append(f"*{dim['description']}*  ")
        lines.append(f"Nodes: {dim['node_count']} | Created by: `{dim['created_by']}`")
        lines.append("")

    lines += [
        "---",
        "",
        "## Top Cognitive Attractors",
        "",
    ]

    attractors = space.get_attractor_nodes(10)
    for i, node in enumerate(attractors, 1):
        grounded = "✓" if node.reality_grounded else "·"
        lines.append(
            f"{i}. **{node.label}** "
            f"(dim=`{node.dimension}`, depth={node.depth}, "
            f"gravity={node.gravity:.2f}, coherence={node.coherence:.2f}) {grounded}"
        )
        lines.append(f"   > {node.content[:150]}")
        lines.append("")

    if cycle_reports:
        lines += [
            "---",
            "",
            "## Cycle Log",
            "",
        ]
        for report in cycle_reports:
            rr_before = report["space_before"]["rr_score"]
            rr_after  = report["space_after"]["rr_score"]
            lines.append(f"### Cycle {report['cycle']}: *{report['query'][:80]}*")
            lines.append("")
            lines.append(f"**Key Insight:** {report.get('key_insight', 'N/A')}")
            lines.append("")
            lines.append(
                f"| Metric | Value |\n|--------|-------|\n"
                f"| RR Score | {rr_before:.4f} → {rr_after:.4f} (Δ{rr_after-rr_before:+.4f}) |\n"
                f"| New Concepts | {report.get('new_concepts', [])} |\n"
                f"| New Dimensions | {report.get('new_dimensions', [])} |\n"
                f"| Meaning Density | {report.get('meaning_density', 0):.3f} |\n"
                f"| Reality Fidelity | {report['verification']['fidelity_score']:.2f} |\n"
                f"| Reasoning Quality | {report['reflection']['quality']:.2f} |\n"
                f"| Cycle Time | {report['cycle_time_seconds']}s |"
            )
            lines.append("")

            if report.get("follow_on_frontiers"):
                lines.append("**Frontiers opened:**")
                for f in report["follow_on_frontiers"]:
                    if f.strip():
                        lines.append(f"- {f}")
                lines.append("")

            lines.append("**Response excerpt:**")
            excerpt = report.get("response", "")[:400]
            lines.append(f"> {excerpt}...")
            lines.append("")
            lines.append("---")
            lines.append("")

    path.write_text("\n".join(lines))
    return path


def export_conversation(
    cycle_reports: list[dict],
    path: str | Path,
    include_metadata: bool = False,
) -> Path:
    """Export Q&A conversation as clean text."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = ["CSTI Engine — Conversation Export", "=" * 50, ""]

    for report in cycle_reports:
        lines.append(f"[Cycle {report['cycle']}]")
        lines.append(f"Q: {report['query']}")
        lines.append("")
        lines.append(report.get("response", ""))
        if report.get("key_insight"):
            lines.append(f"\nKEY INSIGHT: {report['key_insight']}")
        if include_metadata:
            exp = report.get("cognitive_expansion", {})
            lines.append(
                f"\n[Meta: RR Δ{exp.get('rr_delta', 0):+.4f}, "
                f"nodes+{exp.get('nodes_added', 0)}, "
                f"fidelity={report['verification']['fidelity_score']:.2f}]"
            )
        lines.append("\n" + "─" * 50 + "\n")

    path.write_text("\n".join(lines))
    return path


def auto_export(
    space: CognitiveSpace,
    cycle_reports: list[dict],
    output_dir: str = "exports",
) -> dict[str, Path]:
    """Run all export formats at once."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    return {
        "json":     export_json(space, out / f"space_{ts}.json"),
        "markdown": export_markdown_report(space, cycle_reports, out / f"report_{ts}.md"),
        "conversation": export_conversation(cycle_reports, out / f"conversation_{ts}.txt"),
    }