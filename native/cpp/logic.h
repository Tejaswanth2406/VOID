#pragma once

#include <algorithm>
#include <cmath>
namespace void_native {
double occam_score(double evidence, double complexity, double assumptions);
double decay_weight(double initial, double elapsed, double half_life);
double bayesian_confidence(double prior, double likelihood, double contradiction);
double evidence_penalty(double contradiction);
double simplicity_bonus(double complexity);
double confidence_margin(double confidence, double threshold);
bool is_decision_ready(double confidence, double threshold);
double bounded_decay(double value, double elapsed, double half_life);
}
