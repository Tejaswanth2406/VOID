#include "reasoning.h"

#include <algorithm>
#include <cmath>
#include <numeric>
#include <sstream>

namespace void_native {

double evidence_mean(const std::vector<double>& evidence) {
	if (evidence.empty()) return 0.0;
	const double total = std::accumulate(evidence.begin(), evidence.end(), 0.0);
	return std::clamp(total / static_cast<double>(evidence.size()), 0.0, 1.0);
}

double contradiction_risk(const std::vector<double>& evidence) {
	if (evidence.size() < 2) return 0.0;
	double spread = 0.0;
	for (std::size_t index = 1; index < evidence.size(); ++index) {
		spread += std::abs(evidence[index] - evidence[index - 1]);
	}
	return std::clamp(spread / static_cast<double>(evidence.size() - 1), 0.0, 1.0);
}

double reasoning_confidence(const std::vector<double>& evidence, double entropy) {
	if (evidence.empty() || !std::isfinite(entropy)) return 0.0;
	return std::clamp(evidence_mean(evidence) * (1.0 - std::clamp(entropy, 0.0, 1.0)), 0.0, 1.0);
}

ReasoningResult assess_reasoning(const std::vector<double>& evidence, double entropy) {
	const double confidence = reasoning_confidence(evidence, entropy);
	const double risk = contradiction_risk(evidence);
	return {confidence, evidence_mean(evidence), risk, confidence >= 0.5 && risk <= 0.5};
}

bool reasoning_is_actionable(const ReasoningResult& result, double threshold) {
	return result.actionable && result.confidence >= std::clamp(threshold, 0.0, 1.0);
}

std::string reasoning_summary(const ReasoningResult& result) {
	std::ostringstream summary;
	summary << "confidence=" << result.confidence
			<< ", evidence_mean=" << result.evidence_mean
			<< ", contradiction_risk=" << result.contradiction_risk
			<< ", actionable=" << result.actionable;
	return summary.str();
}

}  // namespace void_native
