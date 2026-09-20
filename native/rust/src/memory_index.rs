pub fn top_indices(scores: &[f64], limit: usize) -> Vec<usize> {
    let mut indices: Vec<usize> = (0..scores.len()).collect();
    indices.sort_by(|left, right| scores[*right].total_cmp(&scores[*left]));
    indices.truncate(limit);
    indices
}

pub fn mean(scores: &[f64]) -> f64 {
    if scores.is_empty() { return 0.0; }
    scores.iter().sum::<f64>() / scores.len() as f64
}

pub fn variance(scores: &[f64]) -> f64 {
    if scores.is_empty() { return 0.0; }
    let average = mean(scores);
    scores.iter().map(|score| (score - average).powi(2)).sum::<f64>() / scores.len() as f64
}

pub fn normalize(scores: &[f64]) -> Vec<f64> {
    let maximum = scores.iter().copied().fold(0.0, f64::max);
    if maximum == 0.0 { return vec![0.0; scores.len()]; }
    scores.iter().map(|score| score / maximum).collect()
}

pub fn valid_indices(indices: &[usize], size: usize) -> bool {
    indices.iter().all(|index| *index < size)
}

pub fn summary(indices: &[usize]) -> String {
    format!("count={}, first={}", indices.len(), indices.first().copied().unwrap_or(0))
}
