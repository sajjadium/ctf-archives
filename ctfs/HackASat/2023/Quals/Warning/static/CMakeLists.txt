cmake_minimum_required( VERSION 3.15.0 )
project( warning CXX )

set( headers )
set( src main.cpp )

add_executable( warning main.cpp )

target_compile_options( warning PUBLIC )