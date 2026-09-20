#include "dream_engine.h"
#include "vector_ops.h"
#include "entropy.h"

#include <algorithm>
#include <cmath>
#include <sstream>

namespace void_native {

std::vector<double> dream_direction(const std::vector<std::vector<double>>& memories) { return blend_vectors(memories); }

std::vector<double> dream_direction(const std::vector<std::vector<double>>& memories, const std::vector<double>& weights) {
	if (memories.empty()) return {};
	auto result = std::vector<double>(memories.front().size(), 0.0);
	for (std::size_t row = 0; row < memories.size(); ++row) {
		const double weight = row < weights.size() ? std::max(0.0, weights[row]) : 1.0;
		for (std::size_t index = 0; index < result.size(); ++index) result[index] += memories[row][index] * weight;
	}
	return result;
}

unsigned int dream_novelty_index(const std::vector<double>& vector) {
	if (vector.empty()) return 0;
	return static_cast<unsigned int>(std::distance(vector.begin(), std::max_element(vector.begin(), vector.end(), [](double left, double right) { return std::abs(left) < std::abs(right); })));
}

double dream_entropy(const std::vector<double>& vector) { return normalized_entropy(vector); }

DreamResult run_dream(const std::vector<std::vector<double>>& memories) {
	const auto vector = dream_direction(memories);
	const double entropy = dream_entropy(vector);
	return {vector, dream_novelty_index(vector), entropy, !vector.empty() && entropy < 0.9};
}

bool dream_is_actionable(const DreamResult& result, double threshold) { return result.actionable && result.entropy <= std::clamp(threshold, 0.0, 1.0); }
std::string dream_summary(const DreamResult& result) { std::ostringstream out; out << "novelty_index=" << result.novelty_index << ", entropy=" << result.entropy << ", actionable=" << result.actionable; return out.str(); }

}  // namespace void_native
