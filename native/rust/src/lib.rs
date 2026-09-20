use std::ffi::c_ulonglong;

pub mod algorithm_catalog;
pub mod attractor;
pub mod dream_engine;
pub mod entropy;
pub mod graph_metrics;
pub mod kernel;
pub mod logic;
pub mod memory_index;
pub mod mnemonic;
pub mod reasoning;
pub mod space_state;
pub mod vector_ops;

#[no_mangle]
pub extern "C" fn void_reachable_reality_score(
    node_count: c_ulonglong,
    dimension_count: c_ulonglong,
    edge_count: c_ulonglong,
    mean_coherence: f64,
    max_depth: c_ulonglong,
) -> f64 {
    graph_metrics::reachable_score(node_count, dimension_count, edge_count, mean_coherence, max_depth)
}

#[no_mangle]
pub extern "C" fn void_assign_vector(
    text: *const u8,
    text_length: c_ulonglong,
    dimensions: u32,
    output: *mut f64,
) {
    if text.is_null() || output.is_null() || dimensions == 0 || dimensions > 4096 { return; }
    let bytes = unsafe { std::slice::from_raw_parts(text, text_length as usize) };
    let vector = vector_ops::assign_vector(bytes, dimensions as usize);
    let output = unsafe { std::slice::from_raw_parts_mut(output, dimensions as usize) };
    output.copy_from_slice(&vector);
}

#[no_mangle]
pub extern "C" fn void_normalize_weights(values: *const f64, count: u32, output: *mut f64) {
    if values.is_null() || output.is_null() || count == 0 || count > 4096 { return; }
    let values = unsafe { std::slice::from_raw_parts(values, count as usize) };
    let output = unsafe { std::slice::from_raw_parts_mut(output, count as usize) };
    output.copy_from_slice(&entropy::normalize(values));
}

#[no_mangle]
pub extern "C" fn void_entropy(weights: *const f64, count: u32) -> f64 {
    if weights.is_null() || count == 0 || count > 4096 { return 0.0; }
    let weights = unsafe { std::slice::from_raw_parts(weights, count as usize) };
    entropy::normalized(weights)
}

#[no_mangle]
pub extern "C" fn void_blend_vectors(
    vectors: *const f64,
    vector_count: u32,
    dimensions: u32,
    output: *mut f64,
) {
    if vectors.is_null() || output.is_null() || vector_count == 0 || dimensions == 0 || vector_count > 4096 || dimensions > 4096 { return; }
    let vectors = unsafe { std::slice::from_raw_parts(vectors, (vector_count * dimensions) as usize) };
    let output = unsafe { std::slice::from_raw_parts_mut(output, dimensions as usize) };
    let rows = vectors.chunks_exact(dimensions as usize).map(|row| row.to_vec()).collect::<Vec<_>>();
    output.copy_from_slice(&vector_ops::blend(&rows));
}

#[no_mangle]
pub extern "C" fn void_occam_score(evidence: f64, complexity: f64, assumptions: f64) -> f64 { logic::occam_score(evidence, complexity, assumptions) }

#[no_mangle]
pub extern "C" fn void_decay_weight(initial: f64, elapsed: f64, half_life: f64) -> f64 { logic::decay_weight(initial, elapsed, half_life) }

#[no_mangle]
pub extern "C" fn void_bayesian_confidence(prior: f64, likelihood: f64, contradiction: f64) -> f64 { logic::bayesian_confidence(prior, likelihood, contradiction) }

#[no_mangle]
pub extern "C" fn void_algorithm_count() -> u32 { algorithm_catalog::ALGORITHMS.len() as u32 }