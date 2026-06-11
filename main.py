#!/usr/bin/env python3
"""
CSTI Engine — Main Entry Point
Computational Space Theory of Intelligence

Usage:
  python main.py                          # Interactive REPL
  python main.py --query "..."            # Single query
  python main.py --query "..." --mode full # Full verbose mode
  python main.py --status                  # Show cognitive space status
  python main.py --benchmark               # Run benchmark queries
"""

import os
import sys
import json
import argparse
import textwrap

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from core.engine import CSTIEngine


BANNER = """
╔══════════════════════════════════════════════════════════════════╗
║           CSTI ENGINE — Reality Engine v1.0                     ║
║      Computational Space Theory of Intelligence                 ║
║                                                                  ║
║  Intelligence is not a model.                                    ║
║  Intelligence is a continuously expanding computational          ║
║  universe that constructs increasingly accurate                  ║
║  representations of reality.                                     ║
╚══════════════════════════════════════════════════════════════════╝
"""

BENCHMARK_QUERIES = [
    "What is the relationship between entropy and information?",
    "How does consciousness relate to self-reference?",
    "What makes a mathematical proof beautiful?",
    "Why does the universe have laws at all?",
    "What is the nature of causality at the quantum level?",
]


def print_response(report: dict, verbose: bool = False):
    """Pretty-print a cycle report."""
    print("\n" + "─" * 65)
    print("RESPONSE")
    print("─" * 65)

    # Word-wrap response
    for line in report["response"].splitlines():
        if line.strip():
            print(textwrap.fill(line, width=70))
        else:
            print()

    if report.get("key_insight"):
        print("\n" + "─" * 65)
        print(f"KEY INSIGHT: {report['key_insight']}")

    if report.get("follow_on_frontiers"):
        print("\n" + "─" * 65)
        print("FRONTIERS OPENED:")
        for f in report["follow_on_frontiers"]:
            if f.strip():
                print(f"  → {f}")

    print("\n" + "─" * 65)
    print("COGNITIVE EXPANSION")
    print("─" * 65)
    exp = report["cognitive_expansion"]
    before = report["space_before"]
    after = report["space_after"]
    print(f"  Nodes:       {before['volume']} → {after['volume']} "
          f"(+{exp['nodes_added']})")
    print(f"  Dimensions:  {before['dimensions']} → {after['dimensions']} "
          f"(+{exp['nodes_added'] and exp.get('dimensions_created', 0) or len(report.get('new_dimensions', []))})")
    print(f"  RR Score:    {exp['rr_before']:.4f} → {exp['rr_after']:.4f} "
          f"(Δ{exp['rr_delta']:+.4f})")
    print(f"  Meaning density: {report['meaning_density']:.3f}")

    if report.get("new_concepts"):
        print(f"  New concepts: {', '.join(report['new_concepts'])}")
    if report.get("new_dimensions"):
        print(f"  ✦ New dimensions: {', '.join(report['new_dimensions'])}")

    if verbose:
        print("\n" + "─" * 65)
        print("REASONING PLAN")
        print("─" * 65)
        rp = report["reasoning_plan"]
        print(f"  Strategy: {rp['strategy']} + {rp['secondary']}")
        print(f"  Rationale: {rp['rationale']}")
        print(f"  Simulations run: {report['simulations_run']}")

        print("\n" + "─" * 65)
        print("VERIFICATION")
        print("─" * 65)
        v = report["verification"]
        print(f"  Fidelity: {v['fidelity_score']:.2f} | "
              f"Verified: {v['verified_count']} | "
              f"Unverified: {v['unverified_count']} | "
              f"Contradicted: {v['contradicted_count']}")
        print(f"  Notes: {v['notes']}")

        print("\n" + "─" * 65)
        print("SELF-REFLECTION")
        print("─" * 65)
        r = report["reflection"]
        print(f"  Reasoning quality: {r['quality']:.2f} | Meta-depth: {r['meta_depth']}")
        if r.get("biases"):
            print(f"  Detected biases: {', '.join(r['biases'])}")
        print(f"  Self-model update: {r['self_model_update']}")

    print(f"\n  Cycle time: {report['cycle_time_seconds']}s | "
          f"Coherence issues: {report['coherence_issues']}")
    print("─" * 65)


def print_status(engine: CSTIEngine):
    """Print full engine status."""
    status = engine.get_status()
    print("\n" + "═" * 65)
    print("COGNITIVE SPACE STATUS")
    print("═" * 65)

    cs = status["cognitive_space"]
    print(f"\n  Cycles completed:     {status['cycles_completed']}")
    print(f"  Cognitive volume:     {cs['cognitive_volume']} nodes")
    print(f"  Dimensions:           {cs['dimension_count']}")
    print(f"  Edge count:           {cs['edge_count']}")
    print(f"  Connectivity density: {cs['connectivity_density']:.4f}")
    print(f"  Mean coherence:       {cs['mean_coherence']:.3f}")
    print(f"  Max depth:            {cs['max_depth']}")
    print(f"  Reachable Reality:    {cs['reachable_reality_score']:.4f}")

    print("\n  DIMENSIONS:")
    for name, dim in cs["dimensions"].items():
        print(f"    [{dim['abstraction_level']}] {name}: "
              f"{dim['node_count']} nodes | {dim['description'][:50]}")

    print("\n  LAYER STATUS:")
    print(f"    Memory:          {status['memory']['session_concepts_added']} concepts this session")
    print(f"    Simulations:     {status['simulations_total']} total")
    print(f"    Reflections:     {status['reflection']['reflections_completed']}")
    print(f"    New dimensions:  {status['dimension_engine']['dimensions_created']}")
    print(f"    Coherence issues:{status['coherence']['total_issues']}")
    print(f"    Reality fidelity:{status['reality_verifier']['mean_fidelity']:.3f}")

    print("\n  STRATEGY PERFORMANCE:")
    for strat, perf in status["meta_reasoner"]["strategy_performance"].items():
        if perf is not None:
            bar = "█" * int(perf * 10)
            print(f"    {strat:15s} {bar:10s} {perf:.3f}")

    print("═" * 65)


def run_benchmark(engine: CSTIEngine):
    """Run benchmark queries to test cognitive expansion."""
    print("\n[BENCHMARK MODE — Running standard query set]")
    print("This measures cognitive space expansion across diverse queries.\n")

    results = []
    for i, query in enumerate(BENCHMARK_QUERIES, 1):
        print(f"\nBenchmark {i}/{len(BENCHMARK_QUERIES)}: {query}")
        report = engine.process(query)
        results.append({
            "query": query,
            "rr_delta": report["cognitive_expansion"]["rr_delta"],
            "nodes_added": report["cognitive_expansion"]["nodes_added"],
            "meaning_density": report["meaning_density"],
            "time": report["cycle_time_seconds"],
        })
        print_response(report, verbose=False)

    print("\n" + "═" * 65)
    print("BENCHMARK RESULTS")
    print("═" * 65)
    total_rr = sum(r["rr_delta"] for r in results)
    total_nodes = sum(r["nodes_added"] for r in results)
    avg_density = sum(r["meaning_density"] for r in results) / len(results)
    print(f"  Total RR expansion:   {total_rr:.4f}")
    print(f"  Total nodes added:    {total_nodes}")
    print(f"  Avg meaning density:  {avg_density:.3f}")
    print(f"  Final RR Score:       {engine.space.reachable_reality_score():.4f}")
    print("═" * 65)


def interactive_repl(engine: CSTIEngine, verbose: bool):
    """Run interactive REPL."""
    print(BANNER)
    print("Commands: 'status', 'benchmark', 'export', 'quit' | or enter any query\n")

    while True:
        try:
            query = input("CSTI ▶ ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[Engine shutting down. Cognitive space saved.]")
            engine.memory.save()
            break

        if not query:
            continue

        cmd = query.lower()

        if cmd in ("quit", "exit", "q"):
            print("[Engine shutting down. Cognitive space saved.]")
            engine.memory.save()
            break

        elif cmd == "status":
            print_status(engine)

        elif cmd == "benchmark":
            run_benchmark(engine)

        elif cmd == "export":
            fname = f"cognitive_snapshot_{engine.cycle_count}.json"
            with open(fname, "w") as f:
                json.dump(engine.get_status(), f, indent=2)
            print(f"[Exported to {fname}]")

        elif cmd.startswith("verbose"):
            verbose = not verbose
            print(f"[Verbose mode: {'ON' if verbose else 'OFF'}]")

        else:
            try:
                report = engine.process(query)
                print_response(report, verbose=verbose)
            except Exception as e:
                print(f"[Error in cognitive cycle: {e}]")
                raise


def main():
    parser = argparse.ArgumentParser(
        description="CSTI Engine — Computational Space Theory of Intelligence"
    )
    parser.add_argument("--query", "-q", type=str, help="Single query to process")
    parser.add_argument("--mode", "-m", choices=["full", "compact"], default="compact",
                        help="Output verbosity")
    parser.add_argument("--status", action="store_true", help="Show cognitive space status and exit")
    parser.add_argument("--benchmark", action="store_true", help="Run benchmark queries")
    parser.add_argument("--export", type=str, help="Export cognitive space to JSON file")
    parser.add_argument("--quiet", action="store_true", help="Suppress engine logs")
    args = parser.parse_args()

    verbose_output = args.mode == "full"
    engine_verbose = not args.quiet

    engine = CSTIEngine(verbose=engine_verbose)

    if args.status:
        print_status(engine)
        return

    if args.benchmark:
        run_benchmark(engine)
        print_status(engine)
        return

    if args.export:
        with open(args.export, "w") as f:
            json.dump(engine.get_status(), f, indent=2)
        print(f"[Exported to {args.export}]")
        return

    if args.query:
        report = engine.process(args.query)
        print_response(report, verbose=verbose_output)
        engine.memory.save()
        return

    # Default: interactive REPL
    interactive_repl(engine, verbose=verbose_output)


if __name__ == "__main__":
    main()