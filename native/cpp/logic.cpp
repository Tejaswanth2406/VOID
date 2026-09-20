#include "logic.h"
#include <algorithm>
#include <cmath>

namespace void_native {
static double clamp_probability(double value) { return std::isfinite(value) ? std::clamp(value, 0.0, 1.0) : 0.0; }

double occam_score(double evidence, double complexity, double assumptions) {
    const double denominator = 1.0 + std::max(0.0, complexity) + std::max(0.0, assumptions);
    return clamp_probability(std::max(0.0, evidence) / denominator);
}

double decay_weight(double initial, double elapsed, double half_life) {
    if (half_life <= 0.0) return 0.0;
    const double safe_initial = std::isfinite(initial) ? std::max(0.0, initial) : 0.0;
    const double safe_elapsed = std::isfinite(elapsed) ? std::max(0.0, elapsed) : 0.0;
    return safe_initial * std::exp(-0.6931471805599453 * safe_elapsed / half_life);
}

double bayesian_confidence(double prior, double likelihood, double contradiction) {
    const double p = clamp_probability(prior);
    const double l = clamp_probability(likelihood);
    const double numerator = p * l;
    const double denominator = numerator + (1.0 - p) * (1.0 - l);
    if (denominator <= 0.0) return 0.0;
    return clamp_probability((numerator / denominator) * (1.0 - clamp_probability(contradiction)));
}

double evidence_penalty(double contradiction) { return 1.0 - clamp_probability(contradiction); }
double simplicity_bonus(double complexity) { return 1.0 / (1.0 + std::max(0.0, complexity)); }
double confidence_margin(double confidence, double threshold) { return confidence - threshold; }
bool is_decision_ready(double confidence, double threshold) { return confidence >= threshold && threshold >= 0.0 && threshold <= 1.0; }
double bounded_decay(double value, double elapsed, double half_life) { return std::clamp(decay_weight(value, elapsed, half_life), 0.0, std::max(0.0, value)); }
}
