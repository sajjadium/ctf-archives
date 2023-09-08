#include <linux/atomic.h>
#include <linux/device.h>
#include <linux/fs.h>
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/miscdevice.h>
#include <linux/module.h>
#include <linux/slab.h>
#include <linux/uaccess.h>
#include <asm/errno.h>
#include <linux/printk.h>

#define MAX_DATA_HEIGHT 0x400

MODULE_AUTHOR("wxrdnx");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Wall Rose");

static char *data;

static int rose_open(struct inode *inode, struct file *file) {
    data = kmalloc(MAX_DATA_HEIGHT, GFP_KERNEL);
    if (!data) {
        printk(KERN_ERR "Wall Rose: kmalloc error\n");
        return -1;
    }
    memset(data, 0, MAX_DATA_HEIGHT);
    return 0;
}

static int rose_release(struct inode *inode, struct file *file) {
    kfree(data);
    return 0;
}

static ssize_t rose_read(struct file *filp, char __user *buffer, size_t length, loff_t *offset) {
    pr_info("Wall Rose: data dropped");
    return 0;
}

static ssize_t rose_write(struct file *filp, const char __user *buffer, size_t length, loff_t *offset) {
    pr_info("Wall Rose: data dropped");
    return 0;
}

static struct file_operations rose_fops = { 
    .owner = THIS_MODULE, 
    .open = rose_open, 
    .release = rose_release, 
    .read = rose_read, 
    .write = rose_write, 
}; 

static struct miscdevice rose_device = {
    .minor = MISC_DYNAMIC_MINOR,
    .name = "rose",
    .fops = &rose_fops,
};

static int __init rose_init(void) {
    return misc_register(&rose_device);
}

static void __exit rose_exit(void) {
    misc_deregister(&rose_device);
}

module_init(rose_init);
module_exit(rose_exit);
