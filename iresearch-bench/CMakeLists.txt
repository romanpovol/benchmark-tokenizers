cmake_minimum_required(VERSION 3.16)

# This file is designed to be built INSIDE serenedb's cmake tree
# make iresearch-build will sync it there and call:
#   cmake --build ${IRESEARCH_SRC}/build --target iresearch-bench
#
# All compiler settings, include paths, and link deps are inherited
# from the serenedb build (iresearch-static carries them transitively)

add_executable(iresearch-bench main.cpp)
target_link_libraries(iresearch-bench PRIVATE iresearch-static)
