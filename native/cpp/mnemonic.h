#pragma once
#include <string>
#include <vector>
#include <cctype>

namespace void_native {
std::string major_code(const std::string& digits);
std::string dominic_code(const std::string& digits);
bool valid_digits(const std::string& digits);
std::string normalize_digits(const std::string& digits);
std::vector<std::string> major_tokens(const std::string& digits);
unsigned int digit_count(const std::string& digits);
std::string mnemonic_summary(const std::string& digits);
inline bool is_digit(char value) { return std::isdigit(static_cast<unsigned char>(value)) != 0; }
inline bool is_even_digit(char value) { return is_digit(value) && ((value - '0') % 2 == 0); }
inline bool is_odd_digit(char value) { return is_digit(value) && ((value - '0') % 2 != 0); }
inline unsigned int digit_value(char value) { return is_digit(value) ? static_cast<unsigned int>(value - '0') : 0; }
inline bool has_repeated_digit(const std::string& digits) { for (std::size_t i = 1; i < digits.size(); ++i) if (digits[i] == digits[i - 1]) return true; return false; }
inline std::string reverse_digits(const std::string& digits) { return std::string(digits.rbegin(), digits.rend()); }
inline bool is_palindrome(const std::string& digits) { return digits == reverse_digits(digits); }
inline std::string safe_major(const std::string& digits) { return valid_digits(digits) ? major_code(digits) : std::string(); }
inline std::string safe_dominic(const std::string& digits) { return valid_digits(digits) ? dominic_code(digits) : std::string(); }
inline unsigned int checksum(const std::string& digits) { unsigned int result = 0; for (char digit : digits) result += digit_value(digit); return result % 10; }
}  // namespace void_native
