pub fn sanitize(values: &[f64]) -> Vec<f64> {
    let mut result: Vec<f64> = values.iter().map(|value| if value.is_finite() { value.max(0.0) } else { 0.0 }).collect();
    let total: f64 = result.iter().sum();
    if total > 0.0 { result.iter_mut().for_each(|value| *value /= total); }
    result
}

pub fn valid(weights: &[f64]) -> bool {
    if weights.is_empty() { return false; }
    (sanitize(weights).iter().sum::<f64>() - 1.0).abs() < 1e-9
}

pub fn shannon(weights: &[f64]) -> f64 {
    sanitize(weights).iter().filter(|weight| **weight > 0.0).map(|weight| -weight * weight.ln()).sum()
}

pub fn normalized(weights: &[f64]) -> f64 {
    if weights.len() <= 1 { return 0.0; }
    shannon(weights) / (weights.len() as f64).ln()
}

pub fn concentration(weights: &[f64]) -> f64 { sanitize(weights).into_iter().reduce(f64::max).unwrap_or(0.0) }

pub fn summary(weights: &[f64]) -> String {
    format!("valid={}, normalized_entropy={}, concentration={}", valid(weights), normalized(weights), concentration(weights))
}

pub fn normalize(values: &[f64]) -> Vec<f64> { sanitize(&values.iter().map(|value| value.abs()).collect::<Vec<_>>()) }
