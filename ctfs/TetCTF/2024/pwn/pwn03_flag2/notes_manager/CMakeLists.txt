cmake_minimum_required(VERSION 3.0)

set(CMAKE_SYSTEM_NAME Linux)
#set(CMAKE_SYSTEM_PROCESSOR aarch64)
#set(CMAKE_C_COMPILER "aarch64-linux-gnu-gcc")

project(simple_ipc C)
set(SOURCES1 ipc.c backend.c)
set(SOURCES2 ipc.c interface.c)

find_package(OpenSSL REQUIRED)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O1 -fstack-protector -Wl,-z,relro,-z,now -fPIE")

add_executable(backend ${SOURCES1})
target_include_directories(backend PUBLIC ${CMAKE_SOURCE_DIR} ${OPENSSL_INCLUDE_DIR})
target_link_libraries(backend PUBLIC ssl crypto)

add_executable(interface ${SOURCES2})
target_include_directories(interface PUBLIC ${CMAKE_SOURCE_DIR} ${OPENSSL_INCLUDE_DIR})
target_link_libraries(interface PUBLIC ssl crypto cap)
