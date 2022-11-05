set(CMAKE_CXX_STANDARD 17)

find_package(PkgConfig REQUIRED)
pkg_check_modules(FUSE3 REQUIRED fuse3)

add_executable(mkfs.myfuse ./mkfs.myfuse.cc)
target_link_libraries(mkfs.myfuse PUBLIC ${FUSE3_LIBRARIES} mkfs_lib myfuse_static_base)
target_include_directories(mkfs.myfuse PUBLIC ${FUSE3_INCLUDE_DIRS} ${CMAKE_SOURCE_DIR}/test)
