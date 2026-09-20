#pragma once
#include <string>
#include <vector>
namespace void_native {
std::vector<unsigned int> top_indices(const std::vector<double>& scores, unsigned int limit);
std::vector<double> normalize_scores(const std::vector<double>& scores);
double score_mean(const std::vector<double>& scores);
double score_variance(const std::vector<double>& scores);
bool index_is_valid(const std::vector<unsigned int>& indices, unsigned int size);
std::string index_summary(const std::vector<unsigned int>& indices);
}
