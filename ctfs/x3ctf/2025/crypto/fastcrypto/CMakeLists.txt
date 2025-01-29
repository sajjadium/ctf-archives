cmake_minimum_required(VERSION 3.18)
project(nttmul)

find_package(Python 3.12
  REQUIRED COMPONENTS Interpreter Development.Module
  OPTIONAL_COMPONENTS Development.SABIModule)

add_subdirectory(nanobind)
nanobind_add_module(
	nttmul
	# STABLE_ABI
	# NB_STATIC
	nttmul.cpp
)

# install(TARGETS nttmul LIBRARY DESTINATION .)
