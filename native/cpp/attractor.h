#pragma once

#include <string>
#include <vector>

namespace void_native {

struct AttractorSnapshot {
	std::string name;
	std::string kind;
	double mass;
	std::vector<std::string> labels;
};

struct Attractor {
	std::string name;
	std::string kind;
	double mass = 0.0;
	std::vector<std::string> labels;

	Attractor(std::string attractor_name, std::string attractor_kind);
	void absorb(const std::string& label, double weight);
	void emit(const std::string& label, double weight);
	double normalized_mass(double scale) const;
	bool contains(const std::string& label) const;
	AttractorSnapshot snapshot() const;
};

double attractor_pressure(const Attractor& attractor);
bool valid_attractor(const Attractor& attractor);

}  // namespace void_native
