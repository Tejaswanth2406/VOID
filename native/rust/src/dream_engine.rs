use crate::vector_ops;

pub fn dream(vectors: &[Vec<f64>]) -> Vec<f64> { vector_ops::blend(vectors) }

pub fn novelty(vector: &[f64]) -> usize {
    vector.iter().enumerate().max_by(|(_, left), (_, right)| left.abs().total_cmp(&right.abs())).map(|(index, _)| index).unwrap_or(0)
}

pub fn entropy(vector: &[f64]) -> f64 { crate::entropy::normalized(vector) }
pub fn actionable(vector: &[f64], threshold: f64) -> bool { !vector.is_empty() && entropy(vector) <= threshold.clamp(0.0, 1.0) }
pub fn weighted(vectors: &[Vec<f64>], weights: &[f64]) -> Vec<f64> {
    if vectors.is_empty() { return Vec::new(); }
    let mut output = vec![0.0; vectors[0].len()];
    for (row, vector) in vectors.iter().enumerate() { let weight = weights.get(row).copied().unwrap_or(1.0).max(0.0); for (index, value) in vector.iter().enumerate() { output[index] += value * weight; } }
    output
}
pub fn summary(vector: &[f64]) -> String { format!("dimensions={}, novelty={}, entropy={}, actionable={}", vector.len(), novelty(vector), entropy(vector), actionable(vector, 0.9)) }
