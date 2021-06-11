#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/slab.h>

#define DEVICE_NAME "memo"
#define MAX_SIZE 0x400

MODULE_LICENSE("GPL");
MODULE_AUTHOR("ptr-yudai");
MODULE_DESCRIPTION("zer0pts CTF 2020 meowmow");

char *memo = NULL;

static int __init module_initialize(void);
static void __exit module_cleanup(void);
static loff_t mod_llseek(struct file*, loff_t, int);
static int mod_open(struct inode*, struct file*);
static ssize_t mod_read(struct file*, char __user*, size_t, loff_t*);
static ssize_t mod_write(struct file*, const char __user*, size_t, loff_t *);
static int mod_close(struct inode*, struct file*);
static dev_t dev_id;
static struct cdev c_dev;

static struct file_operations module_fops = {
  .owner = THIS_MODULE,
  .llseek  = mod_llseek,
  .read    = mod_read,
  .write   = mod_write,
  .open    = mod_open,
  .release = mod_close,
};

static int mod_open(struct inode *inode, struct file *file)
{
  if (memo == NULL) {
    memo = kmalloc(MAX_SIZE, GFP_KERNEL);
    memset(memo, 0, MAX_SIZE);
  }
  return 0;
}

static ssize_t mod_read(struct file *filp, char __user *buf, size_t count, loff_t *f_pos)
{
  if (filp->f_pos < 0 || filp->f_pos >= MAX_SIZE) return 0;
  if (count < 0) return 0;
  if (count > MAX_SIZE) count = MAX_SIZE - *f_pos;
  if (copy_to_user(buf, &memo[filp->f_pos], count)) return -EFAULT;
  *f_pos += count;
  return count;
}

static ssize_t mod_write(struct file *filp, const char __user *buf, size_t count, loff_t *f_pos)
{
  if (filp->f_pos < 0 || filp->f_pos >= MAX_SIZE) return 0;
  if (count < 0) return 0;
  if (count > MAX_SIZE) count = MAX_SIZE - *f_pos;
  if (copy_from_user(&memo[filp->f_pos], buf, count)) return -EFAULT;
  *f_pos += count;
  return count;
}

static loff_t mod_llseek(struct file *filp, loff_t offset, int whence)
{
  loff_t newpos;
  switch(whence) {
  case SEEK_SET:
    newpos = offset;
    break;
  case SEEK_CUR:
    newpos = filp->f_pos + offset;
    break;
  case SEEK_END:
    newpos = strlen(memo) + offset;
    break;
  default:
    return -EINVAL;
  }
  if (newpos < 0) return -EINVAL;
  filp->f_pos = newpos;
  return newpos;
}

static int mod_close(struct inode *inode, struct file *file)
{
  return 0;
}

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
