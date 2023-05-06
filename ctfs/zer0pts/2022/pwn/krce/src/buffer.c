#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/slab.h>
#include <linux/random.h>

#define DEVICE_NAME "buffer"
#define BUF_NUM  0x10

#define CMD_NEW  0xeb15
#define CMD_EDIT 0xac1ba
#define CMD_SHOW 0x7aba7a
#define CMD_DEL  0x0da1ba

MODULE_LICENSE("GPL");
MODULE_AUTHOR("ptr-yudai");
MODULE_DESCRIPTION("kRCE - zer0pts CTF 2022");

typedef struct {
  uint32_t index;
  uint32_t size;
  char *data;
} request_t;

char *buffer[BUF_NUM];

long buffer_new(uint32_t index, uint32_t size) {
  if (index >= BUF_NUM)
    return -EINVAL;

  if (!(buffer[index] = (char*)kzalloc(size, GFP_KERNEL)))
    return -EINVAL;

  return 0;
}

long buffer_del(uint32_t index) {
  if (index >= BUF_NUM)
    return -EINVAL;

  if (!buffer[index])
    return -EINVAL;

  kfree(buffer[index]);
  buffer[index] = NULL;

  return 0;
}

long buffer_edit(int32_t index, char *data, int32_t size) {
  if (index >= BUF_NUM)
    return -EINVAL;

  if (!buffer[index])
    return -EINVAL;

  if (copy_from_user(buffer[index], data, size))
    return -EINVAL;

  return 0;
}

long buffer_show(int32_t index, char *data, int32_t size) {
  if (index >= BUF_NUM)
    return -EINVAL;

  if (!buffer[index])
    return -EINVAL;

  if (copy_to_user(data, buffer[index], size))
    return -EINVAL;

  return 0;
}

static long module_ioctl(struct file *filp,
                         unsigned int cmd,
                         unsigned long arg) {
  request_t req;

  if (copy_from_user(&req, (void*)arg, sizeof(request_t)))
    return -EINVAL;

  switch (cmd) {
    case CMD_NEW : return buffer_new (req.index, req.size);
    case CMD_EDIT: return buffer_edit(req.index, req.data, req.size);
    case CMD_SHOW: return buffer_show(req.index, req.data, req.size);
    case CMD_DEL : return buffer_del (req.index);
    default: return -EINVAL;
  }
}

static struct file_operations module_fops = {
  .owner   = THIS_MODULE,
  .unlocked_ioctl = module_ioctl,
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
