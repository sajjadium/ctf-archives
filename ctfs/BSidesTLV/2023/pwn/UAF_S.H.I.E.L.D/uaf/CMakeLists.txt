cmake_minimum_required(VERSION 3.13)


add_executable(uaf uaf.c)
target_link_libraries(uaf PUBLIC uaf_wrapper)
target_compile_options(uaf PRIVATE "-fstack-protector-all" "-fpic" "-fpie")
target_link_options(uaf PRIVATE "-Wl,-z,relro,-z,now")
target_link_options(uaf PRIVATE "-Wl,--wrap=malloc,--wrap=free,--wrap=realloc")
