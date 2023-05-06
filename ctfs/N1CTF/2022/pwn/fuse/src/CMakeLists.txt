cmake_minimum_required(VERSION 3.22)

project(myfuse)

option(CodeCoverage "CodeCoverage" OFF)
option(UseTmpfs "use tmpfs (ramdisk) to bump the test speed" OFF)

set(CMAKE_C_STANDARD 11)

set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake/modules/)

find_package(PkgConfig REQUIRED)
pkg_check_modules(FUSE3 REQUIRED fuse3)

if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  if(CMAKE_BUILD_TYPE STREQUAL "Debug" AND CodeCoverage MATCHES ON)
    SET(GCC_COVERAGE_COMPILE_FLAGS "-fprofile-arcs -ftest-coverage")
    SET(GCC_COVERAGE_LINK_FLAGS    "-lgcov")
  endif()
endif()

if(CMAKE_BUILD_TYPE STREQUAL "Debug" AND UseTmpfs MATCHES ON AND EXISTS ${TmpfsPath})
  MESSAGE("use tmpfs (ramdisk) to bump the test speed")
  add_compile_definitions(DISK_IMG_PATH="${TmpfsPath}/myfuse/disk.img")
  set(DISK_IMG_PATH "${TmpfsPath}/myfuse/disk.img")
else()
  add_compile_definitions(DISK_IMG_PATH="${CMAKE_BINARY_DIR}/test/disk.img")
  set(DISK_IMG_PATH "${CMAKE_BINARY_DIR}/test/disk.img")
endif()



set(CMAKE_C_FLAGS_DEBUG "${GCC_COVERAGE_COMPILE_FLAGS} -DVERBOSE -DDEBUG -ggdb -O0 -g3 -Wall -DMAP_DISK_IMG_TO_MEMORY")
set(CMAKE_CXX_FLAGS_DEBUG ${CMAKE_C_FLAGS_DEBUG})
set(CMAKE_C_FLAGS_RELEASE "-O0 -no-pie")
set(CMAKE_CXX_FLAGS_RELEASE ${CMAKE_C_FLAGS_RELEASE})

set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${GCC_COVERAGE_LINK_FLAGS}")

enable_testing()

set(DIR_SRC "${CMAKE_SOURCE_DIR}/src")
aux_source_directory(${CMAKE_SOURCE_DIR}/src/ ALL_SRC)
list(REMOVE_ITEM ALL_SRC "src/main.c")
include_directories(${CMAKE_SOURCE_DIR}/include)
add_library(myfuse_static_base STATIC ${ALL_SRC})
add_executable(myfuse ${DIR_SRC}/main.c)
target_include_directories(myfuse PUBLIC ${FUSE3_INCLUDE_DIRS})
target_include_directories(myfuse_static_base PUBLIC ${FUSE3_INCLUDE_DIRS})
target_link_libraries(myfuse PUBLIC ${FUSE3_LIBRARIES} myfuse_static_base)

add_library(mkfs_lib STATIC ${CMAKE_SOURCE_DIR}/mkfs/mkfs.myfuse-util.cc)
target_include_directories(mkfs_lib PUBLIC ${CMAKE_SOURCE_DIR}/include PUBLIC ${FUSE3_INCLUDE_DIRS} myfuse_static_base)

add_subdirectory(mkfs)
#add_subdirectory(test)
#add_subdirectory(diagnostic)
