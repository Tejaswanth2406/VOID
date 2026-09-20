pub fn assign_vector(text: &[u8], dimensions: usize) -> Vec<f64> {
    let mut values = Vec::with_capacity(dimensions);
    for dimension in 0..dimensions {
        let mut hash = 1469598103934665603_u64 ^ dimension as u64;
        for byte in text { hash ^= *byte as u64; hash = hash.wrapping_mul(1099511628211); }
        values.push((hash % 2_000_001) as f64 / 1_000_000.0 - 1.0);
    }
    let length = values.iter().map(|value| value * value).sum::<f64>().sqrt().max(1.0);
    values.into_iter().map(|value| value / length).collect()
}

pub fn blend(vectors: &[Vec<f64>]) -> Vec<f64> {
    if vectors.is_empty() { return Vec::new(); }
    let mut result = vec![0.0; vectors[0].len()];
    for vector in vectors { for (index, value) in vector.iter().enumerate() { result[index] += value; } }
    result.iter_mut().for_each(|value| *value /= vectors.len() as f64);
    result
}

pub fn norm(values: &[f64]) -> f64 { values.iter().map(|value| value * value).sum::<f64>().sqrt() }
pub fn dot(left: &[f64], right: &[f64]) -> f64 { left.iter().zip(right).map(|(a, b)| a * b).sum() }
pub fn same_dimensions(left: &[f64], right: &[f64]) -> bool { left.len() == right.len() }
pub fn cosine(left: &[f64], right: &[f64]) -> f64 { let denominator = norm(left) * norm(right); if denominator == 0.0 { 0.0 } else { dot(left, right) / denominator } }
pub fn scale(values: &[f64], factor: f64) -> Vec<f64> { values.iter().map(|value| value * factor).collect() }
pub fn add(left: &[f64], right: &[f64]) -> Vec<f64> { left.iter().zip(right).map(|(a, b)| a + b).collect() }
pub fn subtract(left: &[f64], right: &[f64]) -> Vec<f64> { left.iter().zip(right).map(|(a, b)| a - b).collect() }
pub fn distance(left: &[f64], right: &[f64]) -> f64 { norm(&subtract(left, right)) }
pub fn dominant(values: &[f64]) -> usize { values.iter().enumerate().max_by(|(_, a), (_, b)| a.abs().total_cmp(&b.abs())).map(|(index, _)| index).unwrap_or(0) }
pub fn finite(values: &[f64]) -> bool { values.iter().all(|value| value.is_finite()) }
pub fn summary(values: &[f64]) -> String { format!("dimensions={}, norm={}, dominant={}, finite={}", values.len(), norm(values), dominant(values), finite(values)) }
