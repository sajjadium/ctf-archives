cmake_minimum_required(VERSION 3.10)

project(zone C)

set(PROJECT_SRC
	libzone.c
	bltree.c
)

set(CMAKE_C_CFLAGS
	-DUSECOOKIE=1
	-DUSEZMALLOC=1
	${CMAKE_C_CFLAGS}
)

if(CMAKE_BUILD_TYPE STREQUAL "Debug")
	set(CMAKE_C_CFLAGS ${CMAKE_C_CFLAGS} -DDEBUG -g)
else()
	set(CMAKE_C_CFLAGS ${CMAKE_C_CFLAGS})
endif()


include_directories(${CMAKE_CURRENT_BINARY_DIR})
include_directories(${PROJECT_DIR})

add_library(zone SHARED ${PROJECT_SRC})
target_compile_options(zone PUBLIC ${CMAKE_C_CFLAGS})

if(CMAKE_BUILD_TYPE STREQUAL "Debug")
	add_executable(test test.c)
	target_compile_options(test PUBLIC ${CMAKE_C_CFLAGS})
	target_link_libraries(test zone)
endif()
