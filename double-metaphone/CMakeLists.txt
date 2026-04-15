cmake_minimum_required(VERSION 3.14)
project(dm_benchmark CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_BUILD_TYPE Release)

# Google Benchmark
include(FetchContent)
FetchContent_Declare(
    googlebenchmark
    GIT_REPOSITORY https://github.com/google/benchmark.git
    GIT_TAG        v1.9.1
)
FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG        v1.14.0
)

set(BENCHMARK_ENABLE_TESTING OFF CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googlebenchmark googletest)

# pixelglow — header-only
set(PIXELGLOW_INCLUDE_DIR "${CMAKE_SOURCE_DIR}/libs/pixelglow" CACHE PATH "")

# mtfn — один .cpp + один .h в корне репозитория
set(MTFN_DIR "${CMAKE_SOURCE_DIR}/libs/mtfn")

add_library(mtfn_lib STATIC "${MTFN_DIR}/mtfn.cpp")
target_include_directories(mtfn_lib PUBLIC "${MTFN_DIR}")
target_compile_options(mtfn_lib PRIVATE "-include" "cstdarg")

# Бенчмарк
add_executable(dm_bench bench_main.cpp)
target_include_directories(dm_bench PRIVATE ${PIXELGLOW_INCLUDE_DIR})
target_link_libraries(dm_bench
    PRIVATE
        benchmark::benchmark
        benchmark::benchmark_main
        mtfn_lib
)
