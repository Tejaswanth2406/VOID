#include "graph_metrics.h"
#include <cmath>
#include <sstream>
namespace void_native {
double connectivity(unsigned long long nodes, unsigned long long edges) {
    if (nodes < 2) return 0.0;
    double possible = static_cast<double>(nodes) * static_cast<double>(nodes - 1) / 2.0;
    return possible > 0.0 ? static_cast<double>(edges) / possible : 0.0;
}
double reachable_score(unsigned long long nodes, unsigned long long dimensions, unsigned long long edges, double coherence, unsigned long long depth) {
    return std::log1p(static_cast<double>(nodes)) * std::log1p(static_cast<double>(dimensions)) * (1.0 + connectivity(nodes, edges)) * coherence * (1.0 + std::log1p(static_cast<double>(depth)));
}
double node_capacity(unsigned long long nodes) { return std::log1p(static_cast<double>(nodes)); }
double dimension_capacity(unsigned long long dimensions) { return std::log1p(static_cast<double>(dimensions)); }
bool valid_graph(unsigned long long nodes, unsigned long long edges) { return nodes < 2 || edges <= nodes * (nodes - 1) / 2; }
double graph_growth_rate(unsigned long long previous_nodes, unsigned long long current_nodes) { return previous_nodes == 0 ? static_cast<double>(current_nodes) : static_cast<double>(current_nodes - previous_nodes) / previous_nodes; }
std::string graph_summary(unsigned long long nodes, unsigned long long dimensions, unsigned long long edges) { std::ostringstream out; out << "nodes=" << nodes << ", dimensions=" << dimensions << ", edges=" << edges << ", connectivity=" << connectivity(nodes, edges); return out.str(); }
}
