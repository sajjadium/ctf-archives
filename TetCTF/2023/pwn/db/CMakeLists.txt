cmake_minimum_required(VERSION 3.10)

project(db CXX C)

option (FORCE_COLORED_OUTPUT "Always produce ANSI-colored output (GNU/Clang only)." TRUE)
if (${FORCE_COLORED_OUTPUT})
    if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
       add_compile_options (-fdiagnostics-color=always)
    elseif ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
       add_compile_options (-fcolor-diagnostics)
    endif ()
endif ()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(PROJECT_SRC
	./src/main.cpp
	./src/db.cpp
	./src/utils.c
	./src/IOObjects.cpp
)

if(CMAKE_BUILD_TYPE MATCHES DEBUG)
	set(PROJECT_CXX_FLAGS ${CMAKE_CXX_FLAGS} -g -O0)
	set(PROJECT_C_FLAGS ${CMAKE_C_FLAGS} -g -O0)
else()
	set(PROJECT_CXX_FLAGS ${CMAKE_CXX_FLAGS} -DRELEASE -O2)
	set(PROJECT_C_FLAGS ${CMAKE_C_FLAGS} -DRELEASE -O2)
endif()

set(PROJECT_CXX_FLAGS ${PROJECT_CXX_FLAGS})

# set flags for libzone
set(CMAKE_C_CFLAGS ${CMAKE_C_CFLAGS} -DUSEZMALLOC=1 -DUSECOOKIE=1)
add_subdirectory(libzone)

include_directories(${CMAKE_CURRENT_BINARY_DIR})
include_directories(libzone)

add_executable(db ${PROJECT_SRC})
target_compile_options(db PRIVATE ${PROJECT_CXX_FLAGS} ${PROJECT_C_FLAGS})
target_link_libraries(db PRIVATE zone)
if(CMAKE_BUILD_TYPE MATCHES RELEASE)
set_target_properties(db PROPERTIES LINK_FLAGS_RELEASE -s)
endif()
