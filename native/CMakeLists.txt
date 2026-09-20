cmake_minimum_required(VERSION 3.15)
project(void_metrics LANGUAGES CXX)

add_library(void_metrics SHARED
	cpp/void_metrics.cpp
	cpp/algorithm_catalog.cpp
	cpp/attractor.cpp
	cpp/dream_engine.cpp
	cpp/entropy.cpp
	cpp/graph_metrics.cpp
	cpp/kernel.cpp
	cpp/logic.cpp
	cpp/memory_index.cpp
	cpp/mnemonic.cpp
	cpp/reasoning.cpp
	cpp/space_state.cpp
	cpp/vector_ops.cpp
)
target_include_directories(void_metrics PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_compile_features(void_metrics PRIVATE cxx_std_17)
target_compile_options(void_metrics PRIVATE $<$<CXX_COMPILER_ID:MSVC>:/W4> $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall -Wextra -Wpedantic>)