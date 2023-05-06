#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/slab.h>

#define DEVICE_NAME "sknote"
#define MAX_NOTE_SIZE 0x400

MODULE_LICENSE("GPL");
MODULE_AUTHOR("ptr-yudai");
MODULE_DESCRIPTION("shared knote - BSides AHM 2021");

typedef struct {
  ssize_t length;
  char *data;
} note_t;

typedef struct {
  unsigned long refcnt;
  note_t *noteptr;
} shared_note;

shared_note sknote = {.refcnt = 0, .noteptr = NULL};

static int module_open(struct inode *inode, struct file *file)
{
  unsigned long old = __atomic_fetch_add(&sknote.refcnt, 1, __ATOMIC_SEQ_CST);
  if (old == 0) {

    /* First one to open the note */
    if (!(sknote.noteptr = kzalloc(sizeof(note_t), GFP_KERNEL)))
      return -ENOMEM;
    if (!(sknote.noteptr->data = kzalloc(MAX_NOTE_SIZE, GFP_KERNEL)))
      return -ENOMEM;

  } else if (old >= 0xff) {

    /* Too many references */
    __atomic_sub_fetch(&sknote.refcnt, 1, __ATOMIC_SEQ_CST);
    return -EBUSY;

  }

  return 0;
}

static ssize_t module_read(struct file *file,
                        char __user *buf, size_t count,
                        loff_t *f_pos)
{
  note_t *note;
  ssize_t ecount;

  note = (note_t*)sknote.noteptr;

  /* Security checks to prevent out-of-bounds read */
  if (count < 0)
    return -EINVAL; // Invalid count
  if (__builtin_saddl_overflow(file->f_pos, count, &ecount))
    return -EINVAL; // Too big count
  if (ecount > note->length)
    count = note->length - file->f_pos; // Update count

  /* Copy note to user-land */
  if (copy_to_user(buf, &note->data[file->f_pos], count))
    return -EFAULT; // Invalid user pointer

  /* Update current position */
  *f_pos += count;

  return count;
}

static ssize_t module_write(struct file *file,
                            const char __user *buf, size_t count,
                            loff_t *f_pos)
{
  note_t *note;
  ssize_t ecount;

  note = (note_t*)sknote.noteptr;

  /* Security checks to prevent out-of-bounds write */
  if (count < 0)
    return -EINVAL; // Invalid count
  if (__builtin_saddl_overflow(file->f_pos, count, &ecount))
    return -EINVAL; // Too big count
  if (ecount > MAX_NOTE_SIZE)
    count = MAX_NOTE_SIZE - file->f_pos; // Update count

  /* Copy data from user-land */
  if (copy_from_user(&note->data[file->f_pos], buf, count))
    return -EFAULT; // Invalid user pointer

  /* Update current position and length */
  *f_pos += count;
  if (*f_pos > note->length)
    note->length = *f_pos;

  return count;
}

static loff_t module_llseek(struct file *file, loff_t offset, int whence)
{
  loff_t newpos;

  note_t *note = (note_t*)sknote.noteptr;

  switch (whence) {
  case SEEK_SET:
    newpos = offset;
    break;

  case SEEK_CUR:
    if (__builtin_saddll_overflow(file->f_pos, offset, &newpos))
      return -EINVAL; // Integer overflow
    break;

  case SEEK_END:
    if (__builtin_saddll_overflow(note->length, offset, &newpos))
      return -EINVAL; // Integer overflow
    break;

  default:
    return -EINVAL;
  }

  if (newpos < 0)
    newpos = 0;
  else if (newpos > note->length)
    newpos = note->length;

  file->f_pos = newpos;
  return newpos;
}

static int module_close(struct inode *inode, struct file *file)
{
  if (__atomic_add_fetch(&sknote.refcnt, -1, __ATOMIC_SEQ_CST) == 0) {
    /* We can free the note as nobody references it */
    kfree(sknote.noteptr->data);
    kfree(sknote.noteptr);
    sknote.noteptr = NULL;
  }

  return 0;
}

static struct file_operations module_fops =
  {
   .owner   = THIS_MODULE,
   .llseek  = module_llseek,
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
