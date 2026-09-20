#pragma once

#ifdef __cplusplus
extern "C" {
#endif

double void_reachable_reality_score(
    unsigned long long node_count,
    unsigned long long dimension_count,
    unsigned long long edge_count,
    double mean_coherence,
    unsigned long long max_depth
);

void void_assign_vector(
    const unsigned char* text,
    unsigned long long text_length,
    unsigned int dimensions,
    double* output
);

void void_normalize_weights(
    const double* values,
    unsigned int count,
    double* output
);

double void_entropy(const double* weights, unsigned int count);

double void_occam_score(double evidence, double complexity, double assumptions);
double void_decay_weight(double initial, double elapsed, double half_life);
double void_bayesian_confidence(double prior, double likelihood, double contradiction);
unsigned int void_algorithm_count(void);

void void_blend_vectors(
    const double* vectors,
    unsigned int vector_count,
    unsigned int dimensions,
    double* output
);

#ifdef __cplusplus
}
#endif