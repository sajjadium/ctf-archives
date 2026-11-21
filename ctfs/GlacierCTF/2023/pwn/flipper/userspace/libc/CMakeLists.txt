target_include_directories(userspace_libc
  PUBLIC
    include
    include/sys
)

add_subdirectory(src)
