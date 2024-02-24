#include <linux/compiler.h>
#include <linux/kobject.h>
#include <asm/page_types.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/device.h>
#include <linux/mutex.h>
#include <linux/fs.h>
#include <linux/slab.h>
#include <linux/uaccess.h>
#include <linux/miscdevice.h>
#include <linux/gfp.h>
#include <linux/random.h>
#include <linux/gfp_types.h>
#include <linux/slab.h>
#include <linux/list.h>

MODULE_AUTHOR("k1R4");                        
MODULE_DESCRIPTION("\"palindromatic\" - bi0s CTF 2023");
MODULE_LICENSE("GPL");

enum : unsigned int
{
    QUEUE = 0xb10500a,
    SANITIZE,
    RESET,
    PROCESS,
    REAP,
    QUERY
};

typedef enum ptype : unsigned long
{
    RAW = 0x1337,
    SANITIZED,
    PALINDROME,
    NONPALINDROME
} ptype;

#define TARGET_SZ   0x400
#define STRING_SZ   ((TARGET_SZ-2*sizeof(unsigned long))/2)

typedef struct request_t 
{
    ptype type;
    unsigned long magic;
    char str[STRING_SZ];
    char sanstr[STRING_SZ];
} request_t;

typedef struct arg_t
{
    char *buffer;
} arg_t;

#define QUEUE_SZ     0x100

typedef struct queue_t
{
    int front;
    int rear;
    request_t *reqs[QUEUE_SZ];
} queue_t;

DEFINE_MUTEX(lock);
struct kmem_cache *pm_cache;

static noinline long pm_ioctl(struct file *file, unsigned int cmd, unsigned long uarg);

static struct file_operations pm_fops = { .unlocked_ioctl = pm_ioctl };

struct miscdevice pm_device = {
    .minor = MISC_DYNAMIC_MINOR,
    .name = "palindromatic",
    .fops = &pm_fops,
};                                               