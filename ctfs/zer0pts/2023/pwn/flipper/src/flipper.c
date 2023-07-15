#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/slab.h>
#include <linux/types.h>
#include <linux/init.h>

#define DEVICE_NAME "flipper"

#define CMD_ALLOC 0x13370000
#define CMD_FLIP  0x13370001

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Xion");
MODULE_DESCRIPTION("flipper - zer0pts CTF 2023");

static dev_t dev_id;
static struct cdev c_dev;
struct mutex mtx;
static u8 *buffer;
static int flipped;

static long flipper_ioctl(struct file *filp, unsigned int cmd, unsigned long arg)
{
    int bitofs = (int)arg;
    long ret = 0;

    mutex_lock(&mtx);
    switch (cmd) {
        case CMD_ALLOC: {
            if (buffer) {
                ret = -EBUSY;
            } else if (arg > 0x100UL) {
                ret = -E2BIG;
            } else {
                buffer = kzalloc(arg, GFP_KERNEL);
            }
        }; break;
        case CMD_FLIP: {
            if (!buffer) {
                ret = -ENOENT;
            } else if (flipped) {
                ret = -EPERM;
            } else {
                flipped = 0x1337;
                buffer[bitofs >> 3] ^= (1 << (bitofs & 3));
            }
        }; break;
        default: {
            ret = -EINVAL;
        }
    }
    mutex_unlock(&mtx);

    return ret;
}

static struct file_operations module_fops = {
  .owner   = THIS_MODULE,
  .unlocked_ioctl = flipper_ioctl,
};

static int __init flipper_init(void)
{
    printk(KERN_INFO "Loading flipper module\n");

    mutex_init(&mtx);
    buffer = NULL;
    flipped = 0;

    if (alloc_chrdev_region(&dev_id, 0, 1, DEVICE_NAME)) {
        printk(KERN_WARNING "Failed to register device\n");
        return -EBUSY;
    }

    cdev_init(&c_dev, &module_fops);
    c_dev.owner = THIS_MODULE;

    if (cdev_add(&c_dev, dev_id, 1)) {
        printk(KERN_WARNING "Failed to add cdev\n");
        unregister_chrdev_region(dev_id, 1);
        return -EBUSY;
    }

    return 0;
}

static void __exit flipper_exit(void)
{
    printk(KERN_INFO "Unloading flipper module\n");
    cdev_del(&c_dev);
    unregister_chrdev_region(dev_id, 1);
}

module_init(flipper_init);
module_exit(flipper_exit);
