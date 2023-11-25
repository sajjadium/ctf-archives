# do not cross compile host tools
set(CMAKE_CXX_COMPILER g++)
set(CMAKE_C_COMPILER gcc)
set(CMAKE_AR ar)
set(CMAKE_RANLIB ranlib)

# Ugly hack for preventing kernel CFLAGS from preventing utils build
# TODO: These should not be set for utils/ in the first place
set(CMAKE_C_FLAGS   "")
set(CMAKE_CXX_FLAGS "")

add_compile_options(-O0 -g -Wall -Wextra -Werror -std=gnu++11)




add_subdirectory(exe2minixfs)
add_subdirectory(add-debug)
add_subdirectory(images)
