#include <linux/module.h>
#include <linux/init.h>
#include <linux/proc_fs.h>
#include <linux/seq_file.h>
#include <linux/sched.h>
#include <linux/uaccess.h>
#include <linux/slab.h>
#include "kstack.h"

static long proc_ioctl(struct file*, unsigned int, unsigned long);

struct proc_dir_entry *proc_file_entry;
static const struct file_operations proc_file_fops = {
  .owner = THIS_MODULE,
  .unlocked_ioctl = proc_ioctl
};

Element *head = NULL;

static long proc_ioctl(struct file *filp, unsigned int cmd, unsigned long arg)
{
  Element *tmp, *prev;
  int pid = task_tgid_nr(current);
  switch(cmd) {
  case CMD_PUSH:
    tmp = kmalloc(sizeof(Element), GFP_KERNEL);
    tmp->owner = pid;
    tmp->fd = head;
    head = tmp;
    if (copy_from_user((void*)&tmp->value, (void*)arg, sizeof(unsigned long))) {
      head = tmp->fd;
      kfree(tmp);
      return -EINVAL;
    }
    break;
    
  case CMD_POP:
    for(tmp = head, prev = NULL; tmp != NULL; prev = tmp, tmp = tmp->fd) {
      if (tmp->owner == pid) {
        if (copy_to_user((void*)arg, (void*)&tmp->value, sizeof(unsigned long)))
          return -EINVAL;
        if (prev) {
          prev->fd = tmp->fd;
        } else {
          head = tmp->fd;
        }
        kfree(tmp);
        break;
      }
      if (tmp->fd == NULL) return -EINVAL;
    }
    break;
  }
  return 0;
}

static int proc_init(void) {
  proc_file_entry = proc_create("stack", 0, NULL, &proc_file_fops);
  if (proc_file_entry == NULL) return -ENOMEM;
  return 0;
}

static void proc_exit(void) {
  remove_proc_entry("stack", NULL);
}

module_init(proc_init);
module_exit(proc_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("ptr-yudai");
MODULE_DESCRIPTION("SECCON 2020 - kstack");
