use std::ffi::c_ulonglong;

#[no_mangle]
pub extern "C" fn void_reachable_reality_score(
    node_count: c_ulonglong,
    dimension_count: c_ulonglong,
    edge_count: c_ulonglong,
    mean_coherence: f64,
    max_depth: c_ulonglong,
) -> f64 {
    let volume = (node_count as f64 + 1.0).ln();
    let dimensions = (dimension_count as f64 + 1.0).ln();
    let possible_edges = node_count as f64 * (node_count.saturating_sub(1) as f64) / 2.0;
    let connectivity = if possible_edges > 0.0 {
        edge_count as f64 / possible_edges
    } else {
        0.0
    };
    let depth = (max_depth as f64 + 1.0).ln();
    volume * dimensions * (1.0 + connectivity) * mean_coherence * (1.0 + depth)
}