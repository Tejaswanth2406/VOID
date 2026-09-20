pub const NAME: &str = "VOID native cognitive kernel";
pub const VERSION: u32 = 2;
pub const ABI_VERSION: u32 = 1;
pub const MAX_DIMENSIONS: usize = 4096;
pub const MAX_BATCH: usize = 4096;

pub fn signature() -> String { format!("{} v{} abi={}", NAME, VERSION, ABI_VERSION) }

pub fn supports_dimensions(dimensions: usize) -> bool { dimensions > 0 && dimensions <= MAX_DIMENSIONS }

pub fn supports_batch(batch: usize) -> bool { batch > 0 && batch <= MAX_BATCH }

pub fn clamp_unit(value: f64) -> f64 {
	if !value.is_finite() { return 0.0; }
	value.clamp(0.0, 1.0)
}

pub fn safe_divide(numerator: f64, denominator: f64) -> f64 {
	if !numerator.is_finite() || !denominator.is_finite() || denominator == 0.0 { return 0.0; }
	numerator / denominator
}

pub fn diagnostics(dimensions: usize, batch: usize) -> String {
	format!("{} dimensions={} batch={} valid={}", signature(), dimensions, batch, supports_dimensions(dimensions) && supports_batch(batch))
}
