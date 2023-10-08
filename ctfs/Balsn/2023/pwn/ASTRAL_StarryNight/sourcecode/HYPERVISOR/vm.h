#ifndef __VM_HEADER__
#define __VM_HEADER__

#include <stdint.h>
#include <stdbool.h>
#include <linux/kvm.h>

#define MEM_SIZE 0x4000000
#define PAGE_TABLE_SIZE 0xc000
#define KERNEL_SIZE 0x40000
#define USER_SIZE 0x10000
#define KERNEL_STACK_SIZE 0x100000

#define PT_PADDR 0
#define DIRECT_MAP_PT_PADDR 0x1000
#define KERNEL_PT_PADDR 0x3000
#define KERNEL_STACK_PT_PADDR 0x6000
#define KERNEL_INTERRUPT_STACK_PT_PADDR 0x9000
#define KERNEL_PADDR (PT_PADDR + PAGE_TABLE_SIZE)
#define USER_PADDR (KERNEL_PADDR + KERNEL_SIZE)
#define KERNEL_STACK_PADDR (USER_PADDR + USER_SIZE)
#define KERNEL_INTERRUPT_STACK_PADDR (KERNEL_STACK_PADDR + KERNEL_STACK_SIZE)
#define KERNEL_HEAP_PADDR (KERNEL_INTERRUPT_STACK_PADDR + KERNEL_STACK_SIZE)

typedef struct VM {
  void *mem;
  uint64_t mem_size;
  uint32_t vcpufd;
  struct kvm_run *run;
  bool withinInterrupt;
} VM;

#endif
