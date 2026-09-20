#include "attractor.h"

#include <algorithm>
#include <cmath>

namespace void_native {

Attractor::Attractor(std::string attractor_name, std::string attractor_kind)
	: name(std::move(attractor_name)), kind(std::move(attractor_kind)) {}

void Attractor::absorb(const std::string& label, double weight) {
	if (!std::isfinite(weight) || weight <= 0.0) return;
	mass += weight;
	if (!contains(label)) labels.push_back(label);
}

void Attractor::emit(const std::string& label, double weight) {
	if (!std::isfinite(weight) || weight <= 0.0) return;
	mass = std::max(0.0, mass - weight);
	if (!contains(label)) labels.push_back(label);
}

double Attractor::normalized_mass(double scale) const {
	if (!std::isfinite(scale) || scale <= 0.0) return 0.0;
	return std::clamp(mass / scale, 0.0, 1.0);
}

bool Attractor::contains(const std::string& label) const {
	return std::find(labels.begin(), labels.end(), label) != labels.end();
}

AttractorSnapshot Attractor::snapshot() const { return {name, kind, mass, labels}; }
double attractor_pressure(const Attractor& attractor) { return attractor.mass * (1.0 + attractor.labels.size()); }
bool valid_attractor(const Attractor& attractor) { return !attractor.name.empty() && !attractor.kind.empty() && std::isfinite(attractor.mass) && attractor.mass >= 0.0; }

}  // namespace void_native
