cmake_minimum_required(VERSION 2.8 FATAL_ERROR)
project(jail)

set(src "src/main.c" "src/process.c" "src/ptrace.c")
add_executable(vuln ${src})
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -std=c11")
