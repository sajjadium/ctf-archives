cmake_minimum_required(VERSION 3.15.0 )
project( magic_space_bus CXX )

add_subdirectory( bus )

add_executable( magic main.cpp )

target_link_libraries( magic PUBLIC bus )
target_compile_features( magic PRIVATE cxx_std_17) 
