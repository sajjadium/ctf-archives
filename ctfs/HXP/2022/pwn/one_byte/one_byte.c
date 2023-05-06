#define pr_fmt(fmt) KBUILD_MODNAME ": " fmt
#include <linux/miscdevice.h>
#include <linux/mm.h>
#include <linux/module.h>
#include <linux/vmalloc.h>
#pragma GCC diagnostic ignored "-Wmultichar"

static struct page *page_for(struct mm_struct *mm, unsigned long addr)
{
	unsigned long result = -EFAULT;
	spinlock_t *lock;
	pte_t *pte;
	if (!mm || (result = (unsigned long) follow_pte(mm, addr, &pte, &lock)))
		return ERR_PTR(result); /* Not mapped (or some other kernel insanity). */
	result = !pte_exec(*pte) ? pte_pfn(*pte) : 0;
	pte_unmap_unlock(pte, lock);
	return result && pfn_valid(result) ? pfn_to_page(result) : NULL;
}

static atomic_t challenge_once = ATOMIC_INIT('hxp');
static ssize_t challenge_write(struct file *file, const char __user *data, size_t size, loff_t *offset)
{
	struct { unsigned long addr; char value; } __attribute__((packed)) arg;
	struct page *page;
	char *mapping;
	if (size != sizeof(arg))
		return -EINVAL; /* Pass exactly the arguments we expect. */
	if (copy_from_user(&arg, data, size))
		return -EFAULT; /* Invalid userspace address. */
	if (arg.addr < TASK_SIZE_MAX || (arg.addr & PAGE_MASK) == VSYSCALL_ADDR)
		return -EINVAL; /* I'm not going to write there. */
	if (atomic_xchg(&challenge_once, 0) != 'hxp')
		return -EBUSY; /* You can only do this once. */
	if (IS_ERR_OR_NULL(page = page_for(current->mm, arg.addr)))
		return (ssize_t) page ?: -EFAULT; /* We tried really hard to find this page, but alas. */
	if (!(mapping = vmap(&page, 1, VM_MAP, PAGE_KERNEL)))
		return -EFAULT; /* Couldn't map that page. */
	mapping[arg.addr & ~PAGE_MASK] = arg.value;
	vunmap(mapping);
	return size;
}

static const struct file_operations challenge_ops = { .write = challenge_write };
static struct miscdevice challenge_dev = { .minor = MISC_DYNAMIC_MINOR, .name = KBUILD_MODNAME, .fops = &challenge_ops, .mode = 0666 };

static int __init challenge_init(void)
{
	return misc_register(&challenge_dev);
}

static void __exit challenge_exit(void)
{
	misc_deregister(&challenge_dev);
}

module_init(challenge_init);
module_exit(challenge_exit);

MODULE_DESCRIPTION("hxp CTF 2022/2023 - one_byte");
MODULE_AUTHOR("hlt <contact@hxp.io>");
MODULE_LICENSE("GPL");
