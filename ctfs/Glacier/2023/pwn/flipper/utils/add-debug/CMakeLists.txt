cmake_minimum_required(VERSION 3.1.0)

set(CMAKE_CXX_STANDARD 11)

add_subdirectory(elf)
add_subdirectory(dwarf)

add_executable(add-dbg add-dbg.cc)
target_include_directories(add-dbg PRIVATE elf dwarf)
target_link_libraries(add-dbg elf++ dwarf++)
 
target_compile_features(add-dbg INTERFACE cxx_range_for)
