pub fn connectivity(nodes: u64, edges: u64) -> f64 {
    if nodes < 2 { return 0.0; }
    let possible = nodes as f64 * (nodes - 1) as f64 / 2.0;
    edges as f64 / possible
}

pub fn reachable_score(nodes: u64, dimensions: u64, edges: u64, coherence: f64, depth: u64) -> f64 {
    (nodes as f64 + 1.0).ln() * (dimensions as f64 + 1.0).ln() * (1.0 + connectivity(nodes, edges)) * coherence * (1.0 + (depth as f64 + 1.0).ln())
}

pub fn node_capacity(nodes: u64) -> f64 { (nodes as f64 + 1.0).ln() }
pub fn dimension_capacity(dimensions: u64) -> f64 { (dimensions as f64 + 1.0).ln() }
pub fn valid_graph(nodes: u64, edges: u64) -> bool { nodes < 2 || edges <= nodes * (nodes - 1) / 2 }
pub fn growth_rate(previous: u64, current: u64) -> f64 { if previous == 0 { current as f64 } else { current.saturating_sub(previous) as f64 / previous as f64 } }
pub fn summary(nodes: u64, dimensions: u64, edges: u64) -> String { format!("nodes={}, dimensions={}, edges={}, connectivity={}", nodes, dimensions, edges, connectivity(nodes, edges)) }

pub fn edge_capacity(nodes: u64) -> u64 { nodes.saturating_mul(nodes.saturating_sub(1)) / 2 }
pub fn edge_pressure(nodes: u64, edges: u64) -> f64 { if edge_capacity(nodes) == 0 { 0.0 } else { edges as f64 / edge_capacity(nodes) as f64 } }
pub fn growth_direction(previous: u64, current: u64) -> &'static str { if current > previous { "expanding" } else if current < previous { "contracting" } else { "stable" } }
pub fn score_is_safe(score: f64) -> bool { score.is_finite() && score >= 0.0 }
pub fn bounded_connectivity(nodes: u64, edges: u64) -> f64 { connectivity(nodes, edges).clamp(0.0, 1.0) }
pub fn report(nodes: u64, dimensions: u64, edges: u64) -> String { format!("{}; capacity={}; direction={}", summary(nodes, dimensions, edges), edge_capacity(nodes), growth_direction(0, nodes)) }
