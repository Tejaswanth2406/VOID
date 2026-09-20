cmake_minimum_required(VERSION 3.15)
project(void_metrics LANGUAGES CXX)

add_library(void_metrics SHARED cpp/void_metrics.cpp)
target_include_directories(void_metrics PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_compile_features(void_metrics PRIVATE cxx_std_17)