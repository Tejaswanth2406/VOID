"""
CSTI Engine — Cognitive Space Visualizer
ASCII-based visualization of the cognitive space.
Shows concept galaxies, dimension maps, gravity fields, and expansion history.
"""

from __future__ import annotations
import math
from collections import defaultdict
from core.space import CognitiveSpace, ConceptNode
from utils.helpers import Color, render_bar, format_table


def visualize_dimensions(space: CognitiveSpace) -> str:
    """Render a dimension map showing abstraction levels and node counts."""
    lines = [Color.bold("\n  COGNITIVE DIMENSION MAP"), ""]

    # Group by abstraction level
    by_level: dict[int, list] = defaultdict(list)
    for dim in space.dimensions.values():
        by_level[dim.abstraction_level].append(dim)

    level_labels = {
        0: "CONCRETE   (Level 0)",
        1: "MODEL      (Level 1)",
        2: "META-MODEL (Level 2)",
        3: "META-META  (Level 3)",
        4: "MEANING    (Level 4)",
    }

    max_nodes = max((d.node_count for d in space.dimensions.values()), default=1)

    for level in sorted(by_level.keys()):
        dims = by_level[level]
        label = level_labels.get(level, f"Level {level}")
        lines.append(f"  {Color.cyan(label)}")
        for dim in sorted(dims, key=lambda d: d.node_count, reverse=True):
            bar = render_bar(dim.node_count, max(max_nodes, 1), width=15)
            tag = Color.green(" [system]") if dim.created_by == "system" else \
                  Color.yellow(f" [{dim.created_by}]")
            lines.append(f"    {dim.name:<22} {Color.dim(bar)} {dim.node_count:>3} nodes{tag}")
        lines.append("")

    return "\n".join(lines)


def visualize_attractors(space: CognitiveSpace, top_n: int = 10) -> str:
    """Render the top cognitive attractor nodes."""
    lines = [Color.bold("\n  TOP COGNITIVE ATTRACTORS"), ""]
    attractors = space.get_attractor_nodes(top_n)
    if not attractors:
        return "  (no nodes yet)"

    max_g = max(n.gravity for n in attractors) if attractors else 1.0

    for i, node in enumerate(attractors, 1):
        bar = render_bar(node.gravity, max_g, width=12)
        grounded = Color.green("✓") if node.reality_grounded else Color.dim("·")
        depth_str = Color.magenta(f"d{node.depth}")
        coh = Color.green(f"{node.coherence:.2f}") if node.coherence > 0.7 else \
              Color.yellow(f"{node.coherence:.2f}")
        lines.append(
            f"  {i:>2}. {Color.bold(node.label):<30} "
            f"{Color.dim(bar)}  g={node.gravity:.2f}  "
            f"coh={coh}  {depth_str}  {grounded}  "
            f"{Color.dim(f'[{node.dimension}]')}"
        )
        if node.content:
            lines.append(f"      {Color.dim(node.content[:70])}")

    return "\n".join(lines)


def visualize_concept_graph(space: CognitiveSpace, max_nodes: int = 20) -> str:
    """Render a simple adjacency visualization of the top nodes."""
    lines = [Color.bold("\n  CONCEPT GRAPH (top connections)"), ""]
    attractors = space.get_attractor_nodes(max_nodes)
    if not attractors:
        return "  (no nodes yet)"

    attractor_ids = {n.id for n in attractors}
    attractor_map = {n.id: n for n in attractors}

    for node in attractors[:12]:
        neighbors = []
        for (target_id, weight) in space.edges.get(node.id, []):
            if target_id in attractor_map:
                neighbors.append((attractor_map[target_id].label, weight))
        if neighbors:
            neighbors.sort(key=lambda x: x[1], reverse=True)
            neighbor_str = ", ".join(
                f"{Color.cyan(label)}{Color.dim(f'({w:.1f})')}"
                for label, w in neighbors[:4]
            )
            lines.append(f"  {Color.bold(node.label):<28} → {neighbor_str}")

    return "\n".join(lines)


def visualize_expansion_history(space: CognitiveSpace, last_n: int = 20) -> str:
    """Render a timeline of cognitive expansion events."""
    lines = [Color.bold("\n  EXPANSION HISTORY"), ""]

    events = space.expansion_log[-last_n:]
    if not events:
        return "  (no expansion events yet)"

    event_counts: dict[str, int] = defaultdict(int)
    for e in events:
        event_counts[e["event"]] += 1

    for event_type, count in sorted(event_counts.items(), key=lambda x: x[1], reverse=True):
        bar = render_bar(count, max(event_counts.values()), width=15)
        lines.append(f"  {event_type:<25} {Color.dim(bar)} {count}")

    lines.append("")
    lines.append(f"  {Color.dim('Recent events:')}")
    for e in events[-8:]:
        import datetime as dt
        ts = dt.datetime.fromtimestamp(e["timestamp"]).strftime("%H:%M:%S")
        evt = e["event"]
        detail = e.get("label") or e.get("name") or e.get("dimension") or ""
        lines.append(f"  {Color.dim(ts)}  {Color.cyan(evt):<25} {Color.dim(detail)}")

    return "\n".join(lines)


def visualize_metrics_dashboard(space: CognitiveSpace, metrics_tracker=None) -> str:
    """Full metrics dashboard."""
    snap = space.snapshot()
    lines = []

    lines.append(Color.bold("\n╔══════════════════════════════════════════════════════╗"))
    lines.append(Color.bold(  "║          COGNITIVE SPACE DASHBOARD                   ║"))
    lines.append(Color.bold(  "╚══════════════════════════════════════════════════════╝"))

    # Core metrics
    rr = snap["reachable_reality_score"]
    rr_bar = render_bar(min(rr / 100, 1.0), width=20)
    coh_bar = render_bar(snap["mean_coherence"], width=20)

    lines.append(f"\n  {'Cognitive Volume':<22} {snap['cognitive_volume']:>6} nodes")
    lines.append(f"  {'Dimensions':<22} {snap['dimension_count']:>6}")
    lines.append(f"  {'Edges':<22} {snap['edge_count']:>6}")
    lines.append(f"  {'Connectivity Density':<22} {snap['connectivity_density']:>6.4f}  {Color.dim(render_bar(snap['connectivity_density'], width=15))}")
    lines.append(f"  {'Mean Gravity':<22} {snap['mean_gravity']:>6.3f}")
    lines.append(f"  {'Mean Coherence':<22} {snap['mean_coherence']:>6.3f}  {Color.green(render_bar(snap['mean_coherence'], width=15))}")
    lines.append(f"  {'Max Depth':<22} {snap['max_depth']:>6}")
    lines.append(f"  {'Expansion Events':<22} {snap['expansion_events']:>6}")
    lines.append(f"  {'Coherence Violations':<22} {snap['coherence_violations']:>6}")

    rr_color = Color.green if rr > 50 else Color.yellow if rr > 10 else Color.dim
    lines.append(f"\n  {'Reachable Reality Score':<22} {rr_color(f'{rr:>8.4f}')}")
    lines.append(f"  {'':<22} {Color.green(rr_bar)}")

    if metrics_tracker:
        lines.append(f"\n  {'METRIC TRENDS':}")
        summary = metrics_tracker.summary()
        for name, stats in summary.items():
            spark = metrics_tracker.ascii_sparkline(name, width=15)
            trend = stats["trend"]
            trend_str = Color.green(f"+{trend:.4f}") if trend > 0 else Color.red(f"{trend:.4f}")
            lines.append(f"  {name:<22} {Color.dim(spark)}  trend={trend_str}")

    return "\n".join(lines)


def render_full_report(space: CognitiveSpace, metrics_tracker=None) -> str:
    """Render the complete cognitive space visualization."""
    parts = [
        visualize_metrics_dashboard(space, metrics_tracker),
        visualize_dimensions(space),
        visualize_attractors(space),
        visualize_concept_graph(space),
        visualize_expansion_history(space),
    ]
    return "\n".join(parts)