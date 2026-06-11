"""
CSTI Engine — Configuration
All tunable parameters in one place.
Override via environment variables or pass a Config object to CSTIEngine.
"""

from __future__ import annotations
import os
from dataclasses import dataclass, field


@dataclass
class ModelConfig:
    """Claude model settings."""
    primary_model: str   = "claude-opus-4-5"     # used for all reasoning layers
    fast_model: str      = "claude-haiku-4-5-20251001"  # used for quick extraction tasks
    max_tokens_main: int  = 2000
    max_tokens_fast: int  = 1200
    max_tokens_draft: int = 1000
    temperature: float   = 1.0    # keep at default; most calls are structured JSON


@dataclass
class MemoryConfig:
    """Memory layer settings."""
    memory_file: str         = "memory/cognitive_memory.json"
    max_concepts_per_cycle: int = 6       # max new concepts extracted per query
    gravity_decay_days: float   = 30.0   # days before gravity decays
    max_nodes: int              = 5000   # cap on total nodes
    recall_top_n: int           = 8      # how many nodes to surface per query
    strengthen_factor: float    = 1.1    # gravity boost for revisited concepts


@dataclass
class SimulationConfig:
    """Simulation layer settings."""
    default_simulations: int = 3    # simulations per cycle (overridden by meta-reasoner)
    min_simulations: int     = 1
    max_simulations: int     = 5
    min_confidence: float    = 0.3  # discard simulations below this confidence


@dataclass
class ReflectionConfig:
    """Reflection layer settings."""
    max_biases_tracked: int    = 20
    reflection_depth_target: int = 2  # default meta-depth target
    quality_threshold: float   = 0.5  # below this, flag response as low quality


@dataclass
class DimensionConfig:
    """Dimension engine settings."""
    min_expansion_potential: float = 0.4   # minimum to accept a new dimension
    max_dimensions: int            = 50    # cap on total dimensions
    seed_concepts_per_dim: int     = 3     # concepts seeded into new dimension
    max_new_dims_per_cycle: int    = 2     # maximum new dimensions per cycle


@dataclass
class CoherenceConfig:
    """Coherence filter settings."""
    severity_threshold: float  = 0.6   # above this, penalize node coherence
    coherence_penalty: float   = 0.3   # multiplier applied on violation
    gravity_penalty: float     = 0.9   # gravity reduction for contradicted nodes
    scan_top_n: int            = 10    # attractors to compare against


@dataclass
class MetaReasonerConfig:
    """Meta-reasoner settings."""
    strategy_window: int        = 20    # history window for strategy performance
    min_performance_samples: int = 3    # min samples before using performance data


@dataclass
class EngineConfig:
    """Master config object passed to CSTIEngine."""
    model:       ModelConfig       = field(default_factory=ModelConfig)
    memory:      MemoryConfig      = field(default_factory=MemoryConfig)
    simulation:  SimulationConfig  = field(default_factory=SimulationConfig)
    reflection:  ReflectionConfig  = field(default_factory=ReflectionConfig)
    dimension:   DimensionConfig   = field(default_factory=DimensionConfig)
    coherence:   CoherenceConfig   = field(default_factory=CoherenceConfig)
    meta:        MetaReasonerConfig = field(default_factory=MetaReasonerConfig)

    # Engine-level settings
    verbose: bool      = True
    log_level: str     = "INFO"    # DEBUG | INFO | WARN | ERROR | SILENT
    log_file: str | None = None    # path to log file, or None for stdout only
    auto_save: bool    = True      # save memory after every cycle
    export_dir: str    = "exports" # where auto_export writes files

    @classmethod
    def from_env(cls) -> "EngineConfig":
        """Build config from environment variables."""
        cfg = cls()
        # Model
        if m := os.getenv("CSTI_MODEL"):
            cfg.model.primary_model = m
        if m := os.getenv("CSTI_FAST_MODEL"):
            cfg.model.fast_model = m
        # Memory
        if v := os.getenv("CSTI_MAX_NODES"):
            cfg.memory.max_nodes = int(v)
        if v := os.getenv("CSTI_MEMORY_FILE"):
            cfg.memory.memory_file = v
        # Simulation
        if v := os.getenv("CSTI_SIM_COUNT"):
            cfg.simulation.default_simulations = int(v)
        # Logging
        if v := os.getenv("CSTI_LOG_LEVEL"):
            cfg.log_level = v.upper()
        if v := os.getenv("CSTI_LOG_FILE"):
            cfg.log_file = v
        if v := os.getenv("CSTI_VERBOSE"):
            cfg.verbose = v.lower() not in ("0", "false", "no")
        return cfg

    def summary(self) -> str:
        lines = ["[EngineConfig]"]
        lines.append(f"  primary_model:    {self.model.primary_model}")
        lines.append(f"  fast_model:       {self.model.fast_model}")
        lines.append(f"  default_sims:     {self.simulation.default_simulations}")
        lines.append(f"  max_nodes:        {self.memory.max_nodes}")
        lines.append(f"  max_dimensions:   {self.dimension.max_dimensions}")
        lines.append(f"  log_level:        {self.log_level}")
        lines.append(f"  verbose:          {self.verbose}")
        lines.append(f"  auto_save:        {self.auto_save}")
        return "\n".join(lines)


# ── Preset Configurations ──────────────────────────────────────────────────────

def fast_config() -> EngineConfig:
    """Optimized for speed: fewer simulations, haiku for extraction."""
    cfg = EngineConfig()
    cfg.simulation.default_simulations = 1
    cfg.simulation.max_simulations = 2
    cfg.memory.max_concepts_per_cycle = 4
    cfg.verbose = False
    cfg.log_level = "WARN"
    return cfg


def deep_config() -> EngineConfig:
    """Maximum depth: more simulations, higher reflection target."""
    cfg = EngineConfig()
    cfg.simulation.default_simulations = 5
    cfg.simulation.max_simulations = 5
    cfg.reflection.reflection_depth_target = 4
    cfg.memory.max_concepts_per_cycle = 8
    cfg.dimension.min_expansion_potential = 0.3
    cfg.log_level = "DEBUG"
    return cfg


def research_config() -> EngineConfig:
    """For deep research sessions: large node cap, full logging."""
    cfg = EngineConfig()
    cfg.memory.max_nodes = 20000
    cfg.dimension.max_dimensions = 200
    cfg.simulation.default_simulations = 4
    cfg.log_file = "logs/research_session.jsonl"
    cfg.log_level = "INFO"
    return cfg