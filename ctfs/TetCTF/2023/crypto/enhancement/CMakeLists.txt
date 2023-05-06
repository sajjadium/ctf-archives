cmake_minimum_required(VERSION 3.22)
project(enhancement C)

set(CMAKE_C_STANDARD 11)

add_executable(enhancement main.c)
target_link_libraries(enhancement -lsecp256k1 -v)
