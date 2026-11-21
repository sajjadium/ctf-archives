FILE(GLOB userspace_libc_SOURCES ${CMAKE_CURRENT_LIST_DIR}/*.c)

target_sources(userspace_libc
  PRIVATE
    ${userspace_libc_SOURCES})
