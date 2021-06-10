#ifndef _SANDBOX_H
#define _SANDBOX_H

#define LAST_PAGE       (void *)((1L << 32) - PAGE_SIZE)
#define KERNEL_PAGE     (void *)(1L << 32)
#define USER_CODE       (void *)0xdead0000
#define USER_STACK      (void *)0xbeef0000
#define STACK_SIZE      (16 * PAGE_SIZE)

extern int kernel(unsigned int argv0, unsigned int argv1, unsigned int argv2,
                  unsigned int argv3);

#endif
