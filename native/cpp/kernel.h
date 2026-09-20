#pragma once

#include <string>

namespace void_native {

struct KernelInfo {
	std::string name;
	unsigned int version;
	unsigned int abi;
	bool deterministic;
};

const char* kernel_name();
unsigned int kernel_version();
unsigned int kernel_abi_version();
KernelInfo kernel_info();
bool supports_dimensions(unsigned int dimensions);
bool supports_batch(unsigned int batch_size);
double clamp_unit(double value);
double safe_divide(double numerator, double denominator);
std::string kernel_diagnostics(unsigned int dimensions, unsigned int batch_size);

}  // namespace void_native
