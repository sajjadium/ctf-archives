cmake_minimum_required(VERSION 3.17)
project(lel C)

set(CMAKE_C_STANDARD 11)

set(CMAKE_C_FLAGS "-O3")


add_executable(lel main.c libsodium-stable/src/libsodium/crypto_stream/chacha20/ref/chacha20_ref.c)
target_include_directories(lel PRIVATE libsodium-stable/src/libsodium/include/sodium)
target_include_directories(lel PRIVATE libsodium-stable/src/libsodium/include/sodium/private)
