#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/slab.h>
#include <linux/random.h>

#define DEVICE_NAME "memo"
#define NOTE_SIZE sizeof(note_t)
#define CMD_NEW  0x11451401
#define CMD_EDIT 0x11451402
#define CMD_DEL  0x11451403

MODULE_LICENSE("GPL");
MODULE_AUTHOR("ptr-yudai");
MODULE_DESCRIPTION("minimemo - ASIS CTF 2021 Quals");

typedef struct {
  int id;
  char data[20];
} note_t;

typedef struct notelist_t {
  note_t note;
  struct notelist_t *fd;
  struct notelist_t *bk;
} notelist_t;

typedef struct {
  char data[20];
  int id;
  int size;
} request_t;

notelist_t top = { .fd=&top, .bk=&top };

static long module_ioctl(struct file *filp,
                        unsigned int cmd, unsigned long arg) {
  request_t req;
  long result = -EINVAL;

  if (copy_from_user(&req, (void*)arg, sizeof(request_t)))
    return -EINVAL;

  switch (cmd)
    {
    case CMD_NEW: {
      notelist_t *new = (notelist_t*)kzalloc(sizeof(notelist_t), GFP_ATOMIC);
      do {
        get_random_bytes(&new->note.id, sizeof(new->note.id));
      } while (new->note.id <= 0);
      new->fd = top.fd;
      new->bk = &top;
      top.fd->bk = new;
      top.fd = new;
      result = new->note.id;
      break;
    }

    case CMD_EDIT: {
      notelist_t *cur;
      for (cur = top.fd; cur != &top; cur = cur->fd) {
        if (req.id == cur->note.id) {
          if (req.size < 0 || req.size >= NOTE_SIZE)
            break;
          memcpy(cur->note.data, req.data, req.size);
          result = req.id;
          break;
        }
      }
      break;
    }

    case CMD_DEL: {
      notelist_t *cur;
      for (cur = top.fd; cur != &top; cur = cur->fd) {
        if (req.id == cur->note.id) {
          cur->bk->fd = cur->fd;
          cur->fd->bk = cur->bk;
          kfree(cur);
          result = req.id;
          break;
        }
      }
      break;
    }
  }

  return result;
}

static struct file_operations module_fops =
  {
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
