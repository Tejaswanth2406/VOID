#pragma once

#include <string>

namespace void_native {

struct SpaceState {
	unsigned long long nodes = 0;
	unsigned long long dimensions = 0;
	unsigned long long edges = 0;
	double entropy = 0.0;
	double coherence = 1.0;
};

double space_pressure(const SpaceState& state);
double space_density(const SpaceState& state);
double space_stability(const SpaceState& state);
bool valid_space_state(const SpaceState& state);
std::string space_state_summary(const SpaceState& state);

}  // namespace void_native
