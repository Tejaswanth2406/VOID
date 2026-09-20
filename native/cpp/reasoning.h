#pragma once

#include <string>
#include <vector>

namespace void_native {

struct ReasoningResult {
	double confidence;
	double evidence_mean;
	double contradiction_risk;
	bool actionable;
};

double reasoning_confidence(const std::vector<double>& evidence, double entropy);
double evidence_mean(const std::vector<double>& evidence);
double contradiction_risk(const std::vector<double>& evidence);
ReasoningResult assess_reasoning(const std::vector<double>& evidence, double entropy);
bool reasoning_is_actionable(const ReasoningResult& result, double threshold);
std::string reasoning_summary(const ReasoningResult& result);

}  // namespace void_native
