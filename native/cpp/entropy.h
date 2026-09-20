#pragma once

#include <string>
#include <vector>

namespace void_native {

double normalized_entropy(const std::vector<double>& weights);
double shannon_entropy(const std::vector<double>& weights);
double concentration(const std::vector<double>& weights);
bool valid_distribution(const std::vector<double>& weights);
std::vector<double> sanitize_distribution(const std::vector<double>& weights);
std::string entropy_summary(const std::vector<double>& weights);

}  // namespace void_native
