pub fn occam_score(evidence: f64, complexity: f64, assumptions: f64) -> f64 {
    let evidence = if evidence.is_finite() { evidence.max(0.0) } else { 0.0 };
    let complexity = if complexity.is_finite() { complexity.max(0.0) } else { 0.0 };
    let assumptions = if assumptions.is_finite() { assumptions.max(0.0) } else { 0.0 };
    (evidence / (1.0 + complexity + assumptions)).clamp(0.0, 1.0)
}

pub fn decay_weight(initial: f64, elapsed: f64, half_life: f64) -> f64 {
    if !half_life.is_finite() || half_life <= 0.0 { return 0.0; }
    let initial = if initial.is_finite() { initial.max(0.0) } else { 0.0 };
    let elapsed = if elapsed.is_finite() { elapsed.max(0.0) } else { 0.0 };
    initial * (-std::f64::consts::LN_2 * elapsed / half_life).exp()
}

pub fn bayesian_confidence(prior: f64, likelihood: f64, contradiction: f64) -> f64 {
    let prior = if prior.is_finite() { prior.clamp(0.0, 1.0) } else { 0.0 };
    let likelihood = if likelihood.is_finite() { likelihood.clamp(0.0, 1.0) } else { 0.0 };
    let numerator = prior * likelihood;
    let denominator = numerator + (1.0 - prior) * (1.0 - likelihood);
    if denominator <= 0.0 { return 0.0; }
    let contradiction = if contradiction.is_finite() { contradiction.clamp(0.0, 1.0) } else { 1.0 };
    (numerator / denominator * (1.0 - contradiction)).clamp(0.0, 1.0)
}

pub fn evidence_penalty(contradiction: f64) -> f64 { 1.0 - contradiction.clamp(0.0, 1.0) }
pub fn simplicity_bonus(complexity: f64) -> f64 { 1.0 / (1.0 + complexity.max(0.0)) }
pub fn confidence_margin(confidence: f64, threshold: f64) -> f64 { confidence - threshold }
pub fn decision_ready(confidence: f64, threshold: f64) -> bool { confidence >= threshold && (0.0..=1.0).contains(&threshold) }
pub fn bounded_decay(value: f64, elapsed: f64, half_life: f64) -> f64 { decay_weight(value, elapsed, half_life).clamp(0.0, value.max(0.0)) }
pub fn principle_summary(evidence: f64, complexity: f64, elapsed: f64) -> String {
    format!("simplicity={}, retention={}, evidence={}", simplicity_bonus(complexity), decay_weight(evidence, elapsed, 30.0), evidence)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn decay_reaches_half_at_half_life() { assert!((decay_weight(1.0, 30.0, 30.0) - 0.5).abs() < 1e-9); }
    #[test]
    fn contradiction_reduces_confidence() { assert!(bayesian_confidence(0.5, 0.9, 1.0) < bayesian_confidence(0.5, 0.9, 0.0)); }
}
