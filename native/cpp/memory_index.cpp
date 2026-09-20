#include "memory_index.h"
#include <algorithm>
#include <numeric>
#include <sstream>
namespace void_native {
std::vector<unsigned int> top_indices(const std::vector<double>& scores, unsigned int limit) { std::vector<unsigned int> indices(scores.size()); for (unsigned int i = 0; i < indices.size(); ++i) indices[i] = i; std::sort(indices.begin(), indices.end(), [&scores](auto a, auto b) { return scores[a] > scores[b]; }); if (indices.size() > limit) indices.resize(limit); return indices; }
double score_mean(const std::vector<double>& scores) { return scores.empty() ? 0.0 : std::accumulate(scores.begin(), scores.end(), 0.0) / scores.size(); }
double score_variance(const std::vector<double>& scores) { if (scores.empty()) return 0.0; const double mean = score_mean(scores); double total = 0.0; for (double score : scores) total += (score - mean) * (score - mean); return total / scores.size(); }
std::vector<double> normalize_scores(const std::vector<double>& scores) { const double maximum = scores.empty() ? 1.0 : *std::max_element(scores.begin(), scores.end()); if (maximum == 0.0) return std::vector<double>(scores.size(), 0.0); std::vector<double> result; for (double score : scores) result.push_back(score / maximum); return result; }
bool index_is_valid(const std::vector<unsigned int>& indices, unsigned int size) { return std::all_of(indices.begin(), indices.end(), [size](auto index) { return index < size; }); }
std::string index_summary(const std::vector<unsigned int>& indices) { std::ostringstream out; out << "count=" << indices.size() << ", first=" << (indices.empty() ? 0 : indices.front()); return out.str(); }
}
