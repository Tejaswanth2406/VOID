#include "algorithm_catalog.h"
#include <string>
#include <sstream>

namespace void_native {
unsigned int algorithm_count() { return static_cast<unsigned int>(algorithm_catalog().size()); }
std::string algorithm_name(unsigned int index) { const auto values = algorithm_catalog(); return index < values.size() ? std::string(values[index]) : std::string(); }
bool algorithm_index_valid(unsigned int index) { return index < algorithm_count(); }
std::string algorithm_summary() { std::ostringstream result; result << "count=" << algorithm_count() << ", first=" << algorithm_name(0) << ", last=" << algorithm_name(algorithm_count() - 1); return result.str(); }
bool catalog_is_complete() { return algorithm_count() == 50; }
}
