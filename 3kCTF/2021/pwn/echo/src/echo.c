#include <linux/kernel.h>
#include <linux/syscalls.h>
#include <asm/uaccess_64.h>

// Syscall number : 548

SYSCALL_DEFINE2(echo, void*, to, void*, from) {
    return copy_user_generic_unrolled(to, from, 8);
}
