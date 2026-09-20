#pragma once
#include <string>
#include <vector>

namespace void_native {
std::vector<double> assign_vector(const std::string& text, unsigned int dimensions);
std::vector<double> normalize_weights(const std::vector<double>& values);
std::vector<double> blend_vectors(const std::vector<std::vector<double>>& vectors);
double vector_norm(const std::vector<double>& values);
double vector_dot(const std::vector<double>& left, const std::vector<double>& right);
double cosine_similarity(const std::vector<double>& left, const std::vector<double>& right);
bool same_dimensions(const std::vector<double>& left, const std::vector<double>& right);
bool finite_vector(const std::vector<double>& values);
std::vector<double> scale_vector(const std::vector<double>& values, double scale);
std::vector<double> add_vectors(const std::vector<double>& left, const std::vector<double>& right);
std::vector<double> subtract_vectors(const std::vector<double>& left, const std::vector<double>& right);
double vector_distance(const std::vector<double>& left, const std::vector<double>& right);
unsigned int dominant_index(const std::vector<double>& values);
std::string vector_summary(const std::vector<double>& values);
}
