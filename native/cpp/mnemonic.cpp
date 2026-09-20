#include "mnemonic.h"
#include <cctype>
#include <string>
namespace void_native {
std::string major_code(const std::string& digits) {
	static const char* codes[] = {"S/Z", "T/D", "N", "M", "R", "L", "J/SH", "K/G", "F/V", "P/B"};
	std::string result;
	for (char digit : digits) {
		if (!std::isdigit(static_cast<unsigned char>(digit))) continue;
		if (!result.empty()) result += ' ';
		result += codes[digit - '0'];
	}
	return result;
}

std::string dominic_code(const std::string& digits) {
	static const char codes[] = {'O', 'A', 'B', 'C', 'D', 'E', 'S', 'G', 'H', 'N'};
	std::string result;
	for (char digit : digits) {
		if (std::isdigit(static_cast<unsigned char>(digit))) result += codes[digit - '0'];
	}
	return result;
}
}
