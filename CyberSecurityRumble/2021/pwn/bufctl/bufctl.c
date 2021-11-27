#include <linux/init.h>
#include <linux/ioctl.h>
#include <linux/kernel.h>
#include <linux/list.h>
#include <linux/module.h>
#include <linux/mutex.h>
#include <linux/proc_fs.h>
#include <linux/rculist.h>
#include <linux/slab.h>
#include <linux/uaccess.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("LevitatingLion");
MODULE_DESCRIPTION("bufctl challenge for CSR 2021");
MODULE_VERSION("1.0");

#define BUFCTL_IOCTL_CREATE _IOW(0, 0, struct ioctl_arg)
#define BUFCTL_IOCTL_READ _IOWR(0, 1, struct ioctl_arg)
#define BUFCTL_IOCTL_WRITE _IOW(0, 2, struct ioctl_arg)
#define BUFCTL_IOCTL_DELETE _IOW(0, 3, struct ioctl_arg)

struct ioctl_arg {
    unsigned long id;
    size_t len;
    char __user *data;
};

struct buffer {
    struct list_head list;
    unsigned long id;
    size_t len;
    char data[];
};

static LIST_HEAD(buffers);
static DEFINE_MUTEX(lock_modify);

static int bufctl_create(struct ioctl_arg *arg) {
    struct buffer *b = kmalloc(offsetof(struct buffer, data) + arg->len, GFP_KERNEL);
    if (!b)
        return -ENOMEM;

    b->id = arg->id;
    b->len = arg->len;
    memset(b->data, 0, b->len);

    mutex_lock(&lock_modify);
    list_add_rcu(&b->list, &buffers);
    mutex_unlock(&lock_modify);

    return 0;
}

static int bufctl_read(struct ioctl_arg *arg) {
    int ret = 0;
    bool found = false;
    struct buffer *b;

    rcu_read_lock();

    list_for_each_entry_rcu(b, &buffers, list) {
        if (b->id == arg->id) {
            found = true;
            break;
        }
    }
    if (!found || b->len < arg->len) {
        ret = -EINVAL;
        goto out;
    }

    if (copy_to_user(arg->data, b->data, arg->len)) {
        ret = -EFAULT;
        goto out;
    }

out:
    rcu_read_unlock();
    return ret;
}

static int bufctl_write(struct ioctl_arg *arg) {
    int ret = 0;
    bool found = false;
    struct buffer *b;

    rcu_read_lock();

    list_for_each_entry_rcu(b, &buffers, list) {
        if (b->id == arg->id) {
            found = true;
            break;
        }
    }
    if (!found || b->len < arg->len) {
        ret = -EINVAL;
        goto out;
    }

    if (copy_from_user(b->data, arg->data, arg->len)) {
        ret = -EFAULT;
        goto out;
    }

out:
    rcu_read_unlock();
    return ret;
}

static int bufctl_delete(struct ioctl_arg *arg) {
    bool found = false;
    struct buffer *b;

    mutex_lock(&lock_modify);

    list_for_each_entry(b, &buffers, list) {
        if (b->id == arg->id) {
            found = true;
            break;
        }
    }
    if (!found) {
        mutex_unlock(&lock_modify);
        return -EINVAL;
    }

    list_del_rcu(&b->list);
    mutex_unlock(&lock_modify);

    synchronize_rcu();
    kfree(b);
    return 0;
}

static long bufctl_ioctl(struct file *file, unsigned int cmd, unsigned long user_arg) {
    struct ioctl_arg arg;
    if (copy_from_user(&arg, (const void __user *)user_arg, sizeof arg))
        return -EFAULT;
    if (arg.len > 0x10000)
        return -EINVAL;

    switch (cmd) {
        case BUFCTL_IOCTL_CREATE:
            return bufctl_create(&arg);
        case BUFCTL_IOCTL_READ:
            return bufctl_read(&arg);
        case BUFCTL_IOCTL_WRITE:
            return bufctl_write(&arg);
        case BUFCTL_IOCTL_DELETE:
            return bufctl_delete(&arg);
        default:
            return -EINVAL;
    }
}

static struct proc_ops bufctl_ops = {
    .proc_ioctl = bufctl_ioctl,
};

static int __init bufctl_init(void) {
    if (!proc_create("bufctl", 0666, NULL, &bufctl_ops))
        return -ENOMEM;
    return 0;
}

static void __exit bufctl_exit(void) {
    remove_proc_entry("bufctl", NULL);
}

module_init(bufctl_init);
module_exit(bufctl_exit);
