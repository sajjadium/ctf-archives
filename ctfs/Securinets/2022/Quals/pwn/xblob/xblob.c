#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/slab.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("ptr-yudai");
MODULE_DESCRIPTION("xblob - Securinets CTF Quals 2022");

#define DEVICE_NAME "xblob"
#define BUFFER_SIZE 0x100

int mutex = 0;
char *g_buf = NULL;

static int module_open(struct inode *inode, struct file *file)
{
  if (mutex)
    return -EBUSY;
  else
    mutex = 1;

  g_buf = kzalloc(BUFFER_SIZE, GFP_KERNEL);
  if (!g_buf)
    return -ENOMEM;

  return 0;
}

static ssize_t module_read(struct file *file,
                           char __user *buf, size_t count,
                           loff_t *f_pos)
{
  if (count > BUFFER_SIZE)
    return -EINVAL;

  if (copy_to_user(buf, g_buf, count))
    return -EINVAL;

  return count;
}

static ssize_t module_write(struct file *file,
                            const char __user *buf, size_t count,
                            loff_t *f_pos)
{
  if (count > BUFFER_SIZE)
    return -EINVAL;

  if (copy_from_user(g_buf, buf, count))
    return -EINVAL;

  return count;
}

static int module_close(struct inode *inode, struct file *file)
{
  kfree(g_buf);
  mutex = 0;
  return 0;
}

static struct file_operations module_fops = {
  .owner   = THIS_MODULE,
  .read    = module_read,
  .write   = module_write,
  .open    = module_open,
  .release = module_close,
};

static dev_t dev_id;
static struct cdev c_dev;

static int __init module_initialize(void)
{
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

static void __exit module_cleanup(void)
{
  cdev_del(&c_dev);
  unregister_chrdev_region(dev_id, 1);
}

module_init(module_initialize);
module_exit(module_cleanup);
