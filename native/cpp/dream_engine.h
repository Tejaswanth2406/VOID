#pragma once
#include <string>
#include <vector>
namespace void_native {
struct DreamResult { std::vector<double> vector; unsigned int novelty_index; double entropy; bool actionable; };
std::vector<double> dream_direction(const std::vector<std::vector<double>>& memories);
std::vector<double> dream_direction(const std::vector<std::vector<double>>& memories, const std::vector<double>& weights);
unsigned int dream_novelty_index(const std::vector<double>& vector);
double dream_entropy(const std::vector<double>& vector);
DreamResult run_dream(const std::vector<std::vector<double>>& memories);
bool dream_is_actionable(const DreamResult& result, double threshold);
std::string dream_summary(const DreamResult& result);
}
