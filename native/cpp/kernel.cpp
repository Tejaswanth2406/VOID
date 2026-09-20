#include "kernel.h"

#include <algorithm>
#include <cmath>
#include <sstream>

namespace void_native {

const char* kernel_name() {
	return "VOID native cognitive kernel";
}

unsigned int kernel_version() {
	return 2;
}

unsigned int kernel_abi_version() {
	return 1;
}

KernelInfo kernel_info() {
	return {kernel_name(), kernel_version(), kernel_abi_version(), true};
}

bool supports_dimensions(unsigned int dimensions) {
	return dimensions > 0 && dimensions <= 4096;
}

bool supports_batch(unsigned int batch_size) {
	return batch_size > 0 && batch_size <= 4096;
}

double clamp_unit(double value) {
	if (!std::isfinite(value)) return 0.0;
	return std::clamp(value, 0.0, 1.0);
}

double safe_divide(double numerator, double denominator) {
	if (!std::isfinite(numerator) || !std::isfinite(denominator) || denominator == 0.0) return 0.0;
	return numerator / denominator;
}

std::string kernel_diagnostics(unsigned int dimensions, unsigned int batch_size) {
	const KernelInfo info = kernel_info();
	std::ostringstream result;
	result << info.name << " v" << info.version
		   << " abi=" << info.abi
		   << " dimensions=" << dimensions
		   << " batch=" << batch_size
		   << " valid=" << (supports_dimensions(dimensions) && supports_batch(batch_size));
	return result.str();
}

}  // namespace void_native
