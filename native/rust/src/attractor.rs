#[derive(Clone, Debug)]
pub struct Attractor { pub mass: f64, pub labels: Vec<String> }

impl Attractor {
    pub fn new() -> Self { Self { mass: 0.0, labels: Vec::new() } }
    pub fn absorb(&mut self, label: impl Into<String>, weight: f64) { self.mass += weight.max(0.0); self.labels.push(label.into()); }
    pub fn emit(&mut self, label: impl Into<String>, weight: f64) { self.mass = (self.mass - weight.max(0.0)).max(0.0); self.labels.push(label.into()); }
    pub fn contains(&self, label: &str) -> bool { self.labels.iter().any(|value| value == label) }
    pub fn normalized_mass(&self, scale: f64) -> f64 { if scale <= 0.0 { 0.0 } else { (self.mass / scale).clamp(0.0, 1.0) } }
    pub fn pressure(&self) -> f64 { self.mass * (1.0 + self.labels.len() as f64) }
    pub fn valid(&self) -> bool { self.mass.is_finite() && self.mass >= 0.0 }
    pub fn summary(&self) -> String { format!("mass={}, labels={}, valid={}", self.mass, self.labels.len(), self.valid()) }
}
