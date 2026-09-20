#include "../void_metrics.h"

#include <cmath>

extern "C" double void_reachable_reality_score(
    unsigned long long node_count,
    unsigned long long dimension_count,
    unsigned long long edge_count,
    double mean_coherence,
    unsigned long long max_depth
) {
    const double volume = std::log1p(static_cast<double>(node_count));
    const double dimensions = std::log1p(static_cast<double>(dimension_count));
        const double possible_edges = node_count > 1
                ? static_cast<double>(node_count) *
                    static_cast<double>(node_count - 1) / 2.0
                : 0.0;
    const double connectivity = possible_edges > 0.0
        ? static_cast<double>(edge_count) / possible_edges
        : 0.0;
    const double depth = std::log1p(static_cast<double>(max_depth));
    return volume * dimensions * (1.0 + connectivity) * mean_coherence * (1.0 + depth);
}