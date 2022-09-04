#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/random.h>
#include <linux/slab.h>
#include <linux/uaccess.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("ptr-yudai");
MODULE_DESCRIPTION("welkerme - CakeCTF 2022");

#define DEVICE_NAME "welkerme"
#define CMD_ECHO 0xc0de0001
#define CMD_EXEC 0xc0de0002

static int module_open(struct inode *inode, struct file *filp) {
  printk("'module_open' called\n");
  return 0;
}

static int module_close(struct inode *inode, struct file *filp) {
  printk("'module_close' called\n");
  return 0;
}

static long module_ioctl(struct file *filp,
                         unsigned int cmd,
                         unsigned long arg) {
  long (*code)(void);
  printk("'module_ioctl' called with cmd=0x%08x\n", cmd);

  switch (cmd) {
    case CMD_ECHO:
      printk("CMD_ECHO: arg=0x%016lx\n", arg);
      return arg;

    case CMD_EXEC:
      printk("CMD_EXEC: arg=0x%016lx\n", arg);
      code = (long (*)(void))(arg);
      return code();

    default:
      return -EINVAL;
  }
}

static struct file_operations module_fops = {
  .owner   = THIS_MODULE,
  .open    = module_open,
  .release = module_close,
  .unlocked_ioctl = module_ioctl
};

static dev_t dev_id;
static struct cdev c_dev;

static int __init module_initialize(void)
{
  if (alloc_chrdev_region(&dev_id, 0, 1, DEVICE_NAME))
    return -EBUSY;

  cdev_init(&c_dev, &module_fops);
  c_dev.owner = THIS_MODULE;

  if (cdev_add(&c_dev, dev_id, 1)) {
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
