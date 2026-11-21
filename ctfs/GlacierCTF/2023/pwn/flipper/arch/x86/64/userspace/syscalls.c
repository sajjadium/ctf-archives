#include "types.h"

size_t __syscall(size_t arg1, size_t arg2, size_t arg3, size_t arg4, size_t arg5,
                        size_t arg6)
                        {
  asm("int $0x80\n" : "=a"(arg1) : "a"(arg1), "b"(arg2), "c"(arg3), "d"(arg4), "S"(arg5), "D"(arg6));
  return arg1;
}
