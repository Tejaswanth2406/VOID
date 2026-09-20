"""
CSTI Engine — Core Orchestrator
Coordinates all layers in the correct sequence.

The cognitive cycle:
  1. MetaReasoner     → select reasoning strategy
  2. MemorySpace      → recall relevant prior knowledge
  3. SimulationLayer  → expand into possibility space
  4. ReflectionLayer  → self-model the reasoning
  5. DimensionEngine  → create new dimensions if needed
  6. CoherenceFilter  → maintain space integrity
  7. RealityVerifier  → ground in reality
  8. MeaningSynthesizer → compress to high-density output

This is not a pipeline. It is a cognitive cycle.
Each pass expands the cognitive space permanently.
"""

from __future__ import annotations
import time
from anthropic import Anthropic

from core.space import CognitiveSpace
from layers.memory_layer import MemorySpace
from layers.simulation_layer import SimulationLayer
from layers.reflection_layer import ReflectionLayer
from layers.dimension_engine import DimensionEngine
from layers.coherence_filter import CoherenceFilter
from layers.reality_verifier import RealityVerifier
from layers.meaning_synthesizer import MeaningSynthesizer
from layers.meta_reasoner import MetaReasoner


class CSTIEngine:
    """
    The Reality Engine.
    Each query expands the cognitive universe.
    Intelligence compounds over time.
    """

    def __init__(self, api_key: str | None = None, verbose: bool = True):
        self.client = Anthropic(api_key=api_key) if api_key else Anthropic()
        self.verbose = verbose
        self.cycle_count = 0

        # Initialize cognitive space
        self.space = CognitiveSpace()

        # Initialize all layers
        self.memory        = MemorySpace(self.space, self.client)
        self.meta_reasoner = MetaReasoner(self.space, self.client)
        self.simulator     = SimulationLayer(self.space, self.client)
        self.reflector     = ReflectionLayer(self.space, self.client)
        self.dim_engine    = DimensionEngine(self.space, self.client)
        self.coherence     = CoherenceFilter(self.space, self.client)
        self.verifier      = RealityVerifier(self.space, self.client)
        self.synthesizer   = MeaningSynthesizer(self.space, self.client)

        self._log("CSTI Engine initialized.")
        self._log(f"Cognitive space: {self.space.cognitive_volume} nodes, "
                  f"{self.space.dimension_count} dimensions")

    def _log(self, msg: str):
        if self.verbose:
            print(f"[Engine] {msg}")

    def process(self, query: str) -> dict:
        """
        Run a full cognitive cycle on a query.
        Returns the synthesized output + full cycle report.
        """
        self.cycle_count += 1
        cycle_start = time.time()
        self._log(f"\n{'='*60}")
        self._log(f"Cycle #{self.cycle_count}: {query[:80]}")
        self._log(f"{'='*60}")

        # Snapshot BEFORE expansion
        pre_snapshot = self.space.snapshot()

        # ── STEP 1: MetaReasoner ─────────────────────────────────────────
        self._log("Step 1/8: MetaReasoner — planning reasoning strategy...")
        plan = self.meta_reasoner.plan(query, self.reflector.self_model)
        if self.verbose:
            print(self.meta_reasoner.format_plan(plan))

        # ── STEP 2: Memory Recall ─────────────────────────────────────────
        self._log("Step 2/8: Memory — recalling relevant concepts...")
        relevant_nodes = self.memory.recall_relevant(query, top_n=8)
        memory_context = self.memory.get_summary()
        substrate = self.space.analyze_query(query, [node.label for node in relevant_nodes])
        self._log(f"  Recalled {len(relevant_nodes)} relevant concepts")

        # ── STEP 3: Simulation ────────────────────────────────────────────
        self._log(f"Step 3/8: Simulation — running {plan.simulation_count} internal models...")
        simulations = self.simulator.run(
            query=query,
            memory_context=memory_context,
            n_simulations=plan.simulation_count,
            substrate_context=str(substrate),
        )
        best_sim = self.simulator.select_best(simulations)
        sim_context = self.simulator.format_for_context(simulations)
        self._log(f"  {len(simulations)} simulations generated, best: "
                  f"{best_sim.simulation_type if best_sim else 'none'} "
                  f"(conf={best_sim.confidence:.2f if best_sim else 0})")

        # ── STEP 4: Draft synthesis (for reflection) ──────────────────────
        self._log("Step 4/8: Generating draft for reflection...")
        draft_resp = self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1000,
            system="You are a reasoning system. Produce a thoughtful draft answer.",
            messages=[{
                "role": "user",
                "content": f"{memory_context}\n{sim_context}\n\nQuery: {query}\n\nDraft answer:"
            }]
        )
        draft = draft_resp.content[0].text

        # ── STEP 5: Reflection ────────────────────────────────────────────
        self._log("Step 5/8: Reflection — self-modeling the reasoning process...")
        reflection = self.reflector.reflect(query, draft, sim_context)
        self._log(f"  Reasoning quality: {reflection.reasoning_quality:.2f}, "
                  f"meta-depth: {reflection.meta_depth}")

        # Record strategy performance
        self.meta_reasoner.record_outcome(plan.primary_strategy, reflection.reasoning_quality)

        # ── STEP 6: Memory Integration ────────────────────────────────────
        self._log("Step 6/8: Memory — extracting and storing new concepts...")
        new_nodes = self.memory.extract_and_store(query, draft, {
            "plan": plan.primary_strategy,
            "sim_count": len(simulations)
        })
        new_labels = [n.label for n in new_nodes]
        self._log(f"  {len(new_nodes)} new concepts integrated: {new_labels}")

        # ── STEP 6b: Dimension Engine ─────────────────────────────────────
        self._log("Step 6b/8: Dimension Engine — scanning for new dimensions...")
        new_dims = self.dim_engine.run_cycle(query, new_labels)

        # ── STEP 6c: Coherence Filter ──────────────────────────────────────
        self._log("Step 6c/8: Coherence Filter — checking space integrity...")
        issues = self.coherence.scan(new_labels)
        if issues:
            self._log(f"  ⚠ {len(issues)} coherence issues found")
            for issue in issues:
                self.coherence.apply_resolution(issue)
        else:
            self._log("  ✓ Space coherent")

        # ── STEP 7: Reality Verification ──────────────────────────────────
        self._log("Step 7/8: Reality Verifier — grounding in reality...")
        verification = self.verifier.verify(query, draft, plan.primary_strategy)
        if self.verbose:
            print(self.verifier.format_summary(verification))

        # ── STEP 8: Meaning Synthesis ──────────────────────────────────────
        self._log("Step 8/8: Meaning Synthesizer — compressing to high-density output...")
        output = self.synthesizer.synthesize(
            query=query,
            memory_context=memory_context,
            simulations=simulations,
            best_simulation=best_sim,
            reflection=reflection,
            pre_expansion_snapshot=pre_snapshot,
        )

        cycle_time = round(time.time() - cycle_start, 2)
        post_snapshot = self.space.snapshot()

        # Build full cycle report
        report = {
            "query": query,
            "cycle": self.cycle_count,
            "cycle_time_seconds": cycle_time,
            "response": output.response,
            "key_insight": output.key_insight,
            "meaning_density": output.meaning_density,
            "follow_on_frontiers": output.follow_on_frontiers,
            "cognitive_expansion": output.cognitive_expansion,
            "reasoning_plan": {
                "strategy": plan.primary_strategy,
                "secondary": plan.secondary_strategy,
                "rationale": plan.rationale,
                "depth_target": plan.depth_target,
            },
            "verification": {
                "fidelity_score": verification.reality_fidelity_score,
                "verified_count": len(verification.verified_claims),
                "unverified_count": len(verification.unverified_claims),
                "contradicted_count": len(verification.contradicted_claims),
                "notes": verification.grounding_notes,
            },
            "reflection": {
                "quality": reflection.reasoning_quality,
                "meta_depth": reflection.meta_depth,
                "biases": reflection.identified_biases,
                "self_model_update": reflection.self_model_update,
            },
            "space_before": {
                "volume": pre_snapshot["cognitive_volume"],
                "dimensions": pre_snapshot["dimension_count"],
                "rr_score": pre_snapshot["reachable_reality_score"],
            },
            "space_after": {
                "volume": post_snapshot["cognitive_volume"],
                "dimensions": post_snapshot["dimension_count"],
                "rr_score": post_snapshot["reachable_reality_score"],
            },
            "new_concepts": new_labels,
            "new_dimensions": [d.name for d in new_dims],
            "coherence_issues": len(issues),
            "simulations_run": len(simulations),
            "substrate": substrate,
        }

        self._log(f"\n✓ Cycle #{self.cycle_count} complete in {cycle_time}s")
        self._log(f"  RR Score: {pre_snapshot['reachable_reality_score']:.4f} → "
                  f"{post_snapshot['reachable_reality_score']:.4f} "
                  f"(+{output.cognitive_expansion['rr_delta']:.4f})")

        return report

    def get_status(self) -> dict:
        """Return full engine status."""
        snap = self.space.snapshot()
        return {
            "cycles_completed": self.cycle_count,
            "cognitive_space": snap,
            "memory": {
                "session_concepts_added": len(self.memory.session_concepts),
            },
            "meta_reasoner": {
                "plans_executed": len(self.meta_reasoner.plans_executed),
                "strategy_performance": {
                    s: round(sum(v)/len(v), 3) if v else None
                    for s, v in self.meta_reasoner.strategy_performance.items()
                }
            },
            "reflection": {
                "reflections_completed": len(self.reflector.reflection_history),
                "current_self_model": self.reflector.self_model,
            },
            "dimension_engine": {
                "dimensions_created": self.dim_engine.created_dimensions,
                "proposals_rejected": self.dim_engine.rejected_proposals,
            },
            "coherence": self.coherence.get_coherence_report(),
            "reality_verifier": {
                "verifications": len(self.verifier.verification_history),
                "mean_fidelity": round(self.verifier.mean_fidelity, 3),
            },
            "simulations_total": len(self.simulator.simulation_history),
        }