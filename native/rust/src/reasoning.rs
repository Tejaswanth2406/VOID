#[derive(Clone, Debug)]
pub struct ReasoningResult {
    pub confidence: f64,
    pub evidence_mean: f64,
    pub contradiction_risk: f64,
    pub actionable: bool,
}

pub fn evidence_mean(evidence: &[f64]) -> f64 {
    if evidence.is_empty() { return 0.0; }
    (evidence.iter().sum::<f64>() / evidence.len() as f64).clamp(0.0, 1.0)
}

pub fn contradiction_risk(evidence: &[f64]) -> f64 {
    if evidence.len() < 2 { return 0.0; }
    let spread: f64 = evidence.windows(2).map(|pair| (pair[1] - pair[0]).abs()).sum();
    (spread / (evidence.len() - 1) as f64).clamp(0.0, 1.0)
}

pub fn confidence(evidence: &[f64], entropy: f64) -> f64 {
    if evidence.is_empty() || !entropy.is_finite() { return 0.0; }
    (evidence_mean(evidence) * (1.0 - entropy.clamp(0.0, 1.0))).clamp(0.0, 1.0)
}

pub fn assess(evidence: &[f64], entropy: f64) -> ReasoningResult {
    let confidence = confidence(evidence, entropy);
    let contradiction_risk = contradiction_risk(evidence);
    ReasoningResult { confidence, evidence_mean: evidence_mean(evidence), contradiction_risk, actionable: confidence >= 0.5 && contradiction_risk <= 0.5 }
}

pub fn actionable(result: &ReasoningResult, threshold: f64) -> bool {
    result.actionable && result.confidence >= threshold.clamp(0.0, 1.0)
}

pub fn summary(result: &ReasoningResult) -> String {
    format!("confidence={}, evidence_mean={}, contradiction_risk={}, actionable={}", result.confidence, result.evidence_mean, result.contradiction_risk, result.actionable)
}

pub fn confidence_band(value: f64) -> &'static str { if value < 0.33 { "low" } else if value < 0.66 { "medium" } else { "high" } }
pub fn risk_band(value: f64) -> &'static str { if value < 0.33 { "low" } else if value < 0.66 { "medium" } else { "high" } }
pub fn needs_more_evidence(result: &ReasoningResult) -> bool { result.confidence < 0.5 || result.contradiction_risk > 0.5 }
pub fn decision(result: &ReasoningResult) -> &'static str { if result.actionable { "commit" } else { "investigate" } }
pub fn diagnostic(result: &ReasoningResult) -> String { format!("{} confidence_band={} risk_band={} decision={}", summary(result), confidence_band(result.confidence), risk_band(result.contradiction_risk), decision(result)) }
