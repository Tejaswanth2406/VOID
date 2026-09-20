#[derive(Clone, Debug)]
pub struct SpaceState {
	pub nodes: u64,
	pub dimensions: u64,
	pub edges: u64,
	pub entropy: f64,
	pub coherence: f64,
}

pub fn valid(state: &SpaceState) -> bool {
	state.entropy.is_finite() && state.coherence.is_finite()
		&& (0.0..=1.0).contains(&state.entropy)
		&& (0.0..=1.0).contains(&state.coherence)
}

pub fn density(state: &SpaceState) -> f64 {
	if !valid(state) || state.nodes < 2 { return 0.0; }
	let possible = state.nodes as f64 * (state.nodes - 1) as f64 / 2.0;
	(state.edges as f64 / possible).clamp(0.0, 1.0)
}

pub fn pressure(state: &SpaceState) -> f64 {
	if !valid(state) { return 0.0; }
	(state.nodes as f64 + 1.0).ln() * (1.0 + state.dimensions as f64) * (1.0 - state.entropy) * state.coherence
}

pub fn stability(state: &SpaceState) -> f64 {
	if !valid(state) { return 0.0; }
	((1.0 - state.entropy) * state.coherence * (0.5 + density(state))).clamp(0.0, 1.0)
}

pub fn summary(state: &SpaceState) -> String {
	format!("nodes={}, dimensions={}, edges={}, pressure={}, stability={}", state.nodes, state.dimensions, state.edges, pressure(state), stability(state))
}

pub fn density_band(state: &SpaceState) -> &'static str { let value = density(state); if value < 0.25 { "sparse" } else if value < 0.75 { "connected" } else { "dense" } }
pub fn entropy_band(state: &SpaceState) -> &'static str { if state.entropy < 0.33 { "focused" } else if state.entropy < 0.66 { "balanced" } else { "diffuse" } }
pub fn safe_for_commit(state: &SpaceState) -> bool { valid(state) && stability(state) >= 0.5 }
pub fn pressure_band(state: &SpaceState) -> &'static str { if pressure(state) < 10.0 { "low" } else if pressure(state) < 100.0 { "medium" } else { "high" } }
pub fn diagnostics(state: &SpaceState) -> String { format!("{} density={} entropy_band={} pressure_band={}", summary(state), density_band(state), entropy_band(state), pressure_band(state)) }
