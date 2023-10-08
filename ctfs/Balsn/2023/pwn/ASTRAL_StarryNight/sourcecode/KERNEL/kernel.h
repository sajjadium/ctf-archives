#ifndef __KERNEL_HEADER__
#define __KERNEL_HEADER__

#include <stdint.h>
#include "const.h"
#include "panic.h"
#include "memory.h"
#include "applet.h"
#include "elf.h"

#define MSR_STAR 0xc0000081 /* legacy mode SYSCALL target */
#define MSR_LSTAR 0xc0000082 /* long mode SYSCALL target */
#define MSR_SYSCALL_MASK 0xc0000084

#define USER_STACK_SIZE 0x20000

typedef struct KERNEL_RUNTIME_CONTEXT {
  uint64_t kernelMmapBase;
  uint64_t userMmapBase;
} KERNEL_RUNTIME_CONTEXT;

extern KERNEL_RUNTIME_CONTEXT g_runtimeContext;

#endif
