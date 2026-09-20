#include "../void_metrics.h"
#include "algorithm_catalog.h"
#include "graph_metrics.h"
#include "logic.h"
#include "vector_ops.h"
#include "entropy.h"

#include <cmath>
#include <string>

extern "C" double void_reachable_reality_score(
    unsigned long long node_count,
    unsigned long long dimension_count,
    unsigned long long edge_count,
    double mean_coherence,
    unsigned long long max_depth
) {
    return void_native::reachable_score(node_count, dimension_count, edge_count, mean_coherence, max_depth);
}

static unsigned long long hash_dimension(
    const unsigned char* text,
    unsigned long long text_length,
    unsigned int dimension
) {
    unsigned long long hash = 1469598103934665603ULL ^ dimension;
    for (unsigned long long index = 0; index < text_length; ++index) {
        hash ^= text[index];
        hash *= 1099511628211ULL;
    }
    return hash;
}

extern "C" void void_assign_vector(
    const unsigned char* text,
    unsigned long long text_length,
    unsigned int dimensions,
    double* output
) {
    if (text == nullptr || output == nullptr || dimensions == 0 || dimensions > 4096) return;
    const std::string input(reinterpret_cast<const char*>(text), text_length);
    const auto vector = void_native::assign_vector(input, dimensions);
    for (unsigned int index = 0; index < dimensions; ++index) output[index] = vector[index];
}

extern "C" void void_normalize_weights(
    const double* values,
    unsigned int count,
    double* output
) {
    if (values == nullptr || output == nullptr || count == 0 || count > 4096) return;
    const std::vector<double> source(values, values + count);
    const auto normalized = void_native::normalize_weights(source);
    for (unsigned int index = 0; index < count; ++index) output[index] = normalized[index];
}

extern "C" double void_entropy(const double* weights, unsigned int count) {
    if (weights == nullptr || count == 0 || count > 4096) return 0.0;
    return void_native::normalized_entropy(std::vector<double>(weights, weights + count));
}

extern "C" void void_blend_vectors(
    const double* vectors,
    unsigned int vector_count,
    unsigned int dimensions,
    double* output
) {
    if (vectors == nullptr || output == nullptr || vector_count == 0 || dimensions == 0 || vector_count > 4096 || dimensions > 4096) return;
    std::vector<std::vector<double>> source(vector_count, std::vector<double>(dimensions));
    for (unsigned int vector = 0; vector < vector_count; ++vector)
        for (unsigned int dimension = 0; dimension < dimensions; ++dimension)
            source[vector][dimension] = vectors[vector * dimensions + dimension];
    const auto blended = void_native::blend_vectors(source);
    for (unsigned int dimension = 0; dimension < dimensions; ++dimension) output[dimension] = blended[dimension];
}

extern "C" double void_occam_score(double evidence, double complexity, double assumptions) { return void_native::occam_score(evidence, complexity, assumptions); }
extern "C" double void_decay_weight(double initial, double elapsed, double half_life) { return void_native::decay_weight(initial, elapsed, half_life); }
extern "C" double void_bayesian_confidence(double prior, double likelihood, double contradiction) { return void_native::bayesian_confidence(prior, likelihood, contradiction); }
extern "C" unsigned int void_algorithm_count(void) { return void_native::algorithm_count(); }