#pragma once
#include <string>
namespace void_native {
double reachable_score(unsigned long long nodes, unsigned long long dimensions, unsigned long long edges, double coherence, unsigned long long depth);
double connectivity(unsigned long long nodes, unsigned long long edges);
double node_capacity(unsigned long long nodes);
double dimension_capacity(unsigned long long dimensions);
bool valid_graph(unsigned long long nodes, unsigned long long edges);
std::string graph_summary(unsigned long long nodes, unsigned long long dimensions, unsigned long long edges);
double graph_growth_rate(unsigned long long previous_nodes, unsigned long long current_nodes);
}
