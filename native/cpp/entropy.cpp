#include "entropy.h"

#include <algorithm>
#include <cmath>
#include <numeric>
#include <sstream>

namespace void_native {

std::vector<double> sanitize_distribution(const std::vector<double>& weights) {
    std::vector<double> result;
    result.reserve(weights.size());
    for (double weight : weights) result.push_back(std::isfinite(weight) ? std::max(0.0, weight) : 0.0);
    const double total = std::accumulate(result.begin(), result.end(), 0.0);
    if (total > 0.0) for (double& weight : result) weight /= total;
    return result;
}

bool valid_distribution(const std::vector<double>& weights) {
    if (weights.empty()) return false;
    const auto normalized = sanitize_distribution(weights);
    const double total = std::accumulate(normalized.begin(), normalized.end(), 0.0);
    return std::abs(total - 1.0) < 1e-9;
}

double shannon_entropy(const std::vector<double>& weights) {
    const auto normalized = sanitize_distribution(weights);
    double value = 0.0;
    for (double weight : normalized) if (weight > 0.0) value -= weight * std::log(weight);
    return value;
}

double normalized_entropy(const std::vector<double>& weights) {
    if (weights.size() <= 1) return 0.0;
    return shannon_entropy(weights) / std::log(static_cast<double>(weights.size()));
}

double concentration(const std::vector<double>& weights) {
    const auto normalized = sanitize_distribution(weights);
    return normalized.empty() ? 0.0 : *std::max_element(normalized.begin(), normalized.end());
}

std::string entropy_summary(const std::vector<double>& weights) {
    std::ostringstream summary;
    summary << "valid=" << valid_distribution(weights)
            << ", normalized_entropy=" << normalized_entropy(weights)
            << ", concentration=" << concentration(weights);
    return summary.str();
}

}  // namespace void_native
