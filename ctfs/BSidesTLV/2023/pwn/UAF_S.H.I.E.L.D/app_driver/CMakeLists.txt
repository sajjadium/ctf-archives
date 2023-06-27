cmake_minimum_required(VERSION 3.13)

add_library(uaf_wrapper wrap_link.c)
target_include_directories(uaf_wrapper PUBLIC ../kernel_driver)
