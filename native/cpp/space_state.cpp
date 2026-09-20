#include "space_state.h"

#include <algorithm>
#include <cmath>
#include <sstream>

namespace void_native {

bool valid_space_state(const SpaceState& state) {
	return std::isfinite(state.entropy) && std::isfinite(state.coherence)
		&& state.entropy >= 0.0 && state.entropy <= 1.0
		&& state.coherence >= 0.0 && state.coherence <= 1.0;
}

double space_pressure(const SpaceState& state) {
	if (!valid_space_state(state)) return 0.0;
	return std::log1p(static_cast<double>(state.nodes))
		* (1.0 + static_cast<double>(state.dimensions))
		* (1.0 - state.entropy) * state.coherence;
}

double space_density(const SpaceState& state) {
	if (!valid_space_state(state) || state.nodes < 2) return 0.0;
	const double possible = static_cast<double>(state.nodes) * static_cast<double>(state.nodes - 1) / 2.0;
	return possible == 0.0 ? 0.0 : std::min(1.0, static_cast<double>(state.edges) / possible);
}

double space_stability(const SpaceState& state) {
	if (!valid_space_state(state)) return 0.0;
	return std::clamp((1.0 - state.entropy) * state.coherence * (0.5 + space_density(state)), 0.0, 1.0);
}

std::string space_state_summary(const SpaceState& state) {
	std::ostringstream result;
	result << "nodes=" << state.nodes << ", dimensions=" << state.dimensions
		   << ", edges=" << state.edges << ", pressure=" << space_pressure(state)
		   << ", stability=" << space_stability(state);
	return result.str();
}

}  // namespace void_native
