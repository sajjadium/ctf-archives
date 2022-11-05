set(CMAKE_CXX_STANDARD 17)

find_package(PkgConfig REQUIRED)
pkg_check_modules(FUSE3 REQUIRED fuse3)

add_executable(disk-diagnostic ./disk-diagnostic.cc)
target_link_libraries(disk-diagnostic PUBLIC ${FUSE3_LIBRARIES} mkfs_lib myfuse_static_base)
target_include_directories(disk-diagnostic PUBLIC ${FUSE3_INCLUDE_DIRS} ${CMAKE_SOURCE_DIR}/test)
