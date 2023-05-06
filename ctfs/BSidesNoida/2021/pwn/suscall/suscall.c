#include <linux/kernel.h>
#include <linux/syscalls.h>
#include <linux/module.h>

MODULE_LICENSE("GPL");

#ifndef __NR_SUSCALL
#define __NR_SUSCALL 546
#endif

SYSCALL_DEFINE1(suscall, unsigned long int, addr) {
        void (*fp)(void);
        fp = addr;
        fp();
}
