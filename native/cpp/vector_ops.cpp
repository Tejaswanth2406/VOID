#include "vector_ops.h"
#include <cmath>
#include <cstdint>

namespace void_native {
static std::uint64_t hash_text(const std::string& text, unsigned int dimension) {
    std::uint64_t hash = 1469598103934665603ULL ^ dimension;
    for (unsigned char byte : text) { hash ^= byte; hash *= 1099511628211ULL; }
    return hash;
}

std::vector<double> assign_vector(const std::string& text, unsigned int dimensions) {
    std::vector<double> result(dimensions);
    double length = 0.0;
    for (unsigned int index = 0; index < dimensions; ++index) {
        result[index] = static_cast<double>(hash_text(text, index) % 2000001ULL) / 1000000.0 - 1.0;
        length += result[index] * result[index];
    }
    length = std::sqrt(length);
    if (length == 0.0) length = 1.0;
    for (double& value : result) value /= length;
    return result;
}

std::vector<double> normalize_weights(const std::vector<double>& values) {
    std::vector<double> result(values.size());
    double total = 0.0;
    for (double value : values) total += std::abs(value);
    if (total == 0.0) total = 1.0;
    for (std::size_t i = 0; i < values.size(); ++i) result[i] = std::abs(values[i]) / total;
    return result;
}

std::vector<double> blend_vectors(const std::vector<std::vector<double>>& vectors) {
    if (vectors.empty()) return {};
    std::vector<double> result(vectors.front().size(), 0.0);
    for (const auto& vector : vectors)
        for (std::size_t i = 0; i < result.size() && i < vector.size(); ++i) result[i] += vector[i];
    for (double& value : result) value /= static_cast<double>(vectors.size());
    return result;
}
}
