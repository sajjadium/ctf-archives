#include <linux/cdev.h>
#include <linux/device.h>
#include <linux/fs.h>
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/slab.h>
#include <linux/delay.h>
#include <linux/kthread.h>

#include "secmsg.h"

DEFINE_MUTEX(g_mutex);

static struct secure_message *g_messages[N_MAX_MESSAGES] = {0};
static struct task_struct *redact_kth;

static struct chrdev_info cinfo = {};

static int secmsg_open(struct inode *inode, struct file *file) {
    return 0;
}

static int secmsg_release(struct inode *inode, struct file *file) {
    return 0;
}

static ssize_t secmsg_read(struct file *filp, char __user *buffer, size_t length, loff_t *offset) {
    return 0;
}

static ssize_t secmsg_write(struct file *filp, const char __user *buffer, size_t length, loff_t *offset) {
    return 0;
}

static void redact_message(struct work_struct *work) {
    struct secure_message *m = container_of(work, struct secure_message, work);

    // Redact the secret message
    get_random_bytes(m->content, m->content_size);
}

static int redact_loop(void *p) {
    struct secure_message *m;
    uint32_t min_lifetime;

    while (!kthread_should_stop()) {
        m = NULL;
        min_lifetime = MAX_LIFETIME;

        // Find the message with the shortest lifetime
        for (int i = 0; i < N_MAX_MESSAGES; i++) {
            if (g_messages[i] == NULL || g_messages[i]->lifetime == 0)
                continue;
            if (g_messages[i]->lifetime < min_lifetime) {
                m = g_messages[i];
                min_lifetime = m->lifetime;
            }
        }

        if (m == NULL) {
            msleep(100);
            continue;
        }

        // Expire lifetime
        msleep(min_lifetime);

        // Redact message asynchronously
        schedule_work(&m->work);

        // Update lifetimes
        for (int i = 0; i < N_MAX_MESSAGES; i++) {
            if (g_messages[i] == NULL || g_messages[i]->lifetime == 0)
                continue;
            g_messages[i]->lifetime -= min_lifetime;
        }
    }

    return 0;
}

static int find_free_slot(void) {
    for (int i = 0; i < N_MAX_MESSAGES; i++)
        if (g_messages[i] == NULL)
            return i;
    return -1;
}

static int add_message(struct params *args) {
    int idx;
    struct secure_message *m;

    if ((idx = find_free_slot()) == -1)
        return -ENOMEM;

    if (args->len < MESSAGE_MIN_SZ || args->len > MESSAGE_MAX_SZ)
        return -EINVAL;

    if (args->lifetime <= MIN_LIFETIME || args->lifetime >= MAX_LIFETIME)
        return -EINVAL;

    if ((m = kzalloc(sizeof(struct secure_message) + args->len, GFP_KERNEL_ACCOUNT)) == NULL)
        return -ENOMEM;

    if (copy_from_user(m->content, args->buf, args->len)) {
        kfree(m);
        return -EFAULT;
    }

    args->idx = idx;

    m->lifetime = args->lifetime;
    m->content_size = args->len;
    m->consumed = 0;

    INIT_WORK(&m->work, redact_message);

    g_messages[idx] = m;
    return 0;
}

static int read_message(struct params *args) {
    struct secure_message *m;
    uint32_t sz;

    if (args->idx >= N_MAX_MESSAGES)
        return -EINVAL;

    if ((m = g_messages[args->idx]) == NULL)
        return -ENOENT;

    if (m->consumed == m->content_size)
        return -ENODATA;

    sz = args->len;

    if (sz > m->content_size - m->consumed)
        sz = m->content_size - m->consumed;

    if (copy_to_user(args->buf, m->content + m->consumed, sz))
        return -EFAULT;

    m->consumed += args->len;
    return 0;
}

static int delete_message(struct params *args) {
    struct secure_message *m;

    if (args->idx >= N_MAX_MESSAGES)
        return -EINVAL;

    if ((m = g_messages[args->idx]) == NULL)
        return -ENOENT;
    
    g_messages[args->idx] = NULL;
    kfree(m);
    return 0;
}

static long secmsg_ioctl(struct file *filp, unsigned int cmd, unsigned long arg) {
    int ret = 0;
    struct params p;

    if (copy_from_user(&p, (void*)arg, sizeof(p)))
        return -EINVAL;

    mutex_lock(&g_mutex);

    switch(cmd) {
        case CMD_ADD_MESSAGE:
            ret = add_message(&p);
            if (!ret)
                put_user(p.idx, &(((struct params*)arg)->idx));
            break;
        case CMD_READ_MESSAGE:
            ret = read_message(&p);
            break;
        case CMD_DELETE_MESSAGE:
            ret = delete_message(&p);
            break;
        default:
            ret = -EINVAL;
    }

    mutex_unlock(&g_mutex);
    return ret;
}

static struct file_operations secmsg_fops = {
    .owner = THIS_MODULE,
    .open = secmsg_open,
    .release = secmsg_release,
    .read = secmsg_read,
    .write = secmsg_write,
    .unlocked_ioctl = secmsg_ioctl
};

static int __init secmsg_init(void) {
	dev_t dev;

    /* Init char dev */
	if (alloc_chrdev_region(&dev, 0, 1, DEVICE_NAME))
		return -EBUSY;

	cinfo.major = MAJOR(dev);

	cdev_init(&cinfo.cdev, &secmsg_fops);
	cinfo.cdev.owner = THIS_MODULE;

	if (cdev_add(&cinfo.cdev, dev, 1))
		goto ERR_CDEV_ADD;

	cinfo.class = class_create(THIS_MODULE, CLASS_NAME);
	if (IS_ERR(cinfo.class))
		goto ERR_CLASS_CREATE;

    /* Init kthread */
    if ((redact_kth = kthread_create(redact_loop, NULL, "kthread_redact")) == NULL)
        goto ERR_CLASS_CREATE;

    wake_up_process(redact_kth);

	device_create(cinfo.class, NULL, MKDEV(cinfo.major, 0), NULL, DEVICE_NAME);
	return 0;

ERR_CLASS_CREATE:
	cdev_del(&cinfo.cdev);
ERR_CDEV_ADD:
	unregister_chrdev_region(dev, 1);
	return -EBUSY;
}

static void __exit secmsg_exit(void) {
    kthread_stop(redact_kth);

	device_destroy(cinfo.class, MKDEV(cinfo.major, 0));
	class_destroy(cinfo.class);

	cdev_del(&cinfo.cdev);
	unregister_chrdev_region(MKDEV(cinfo.major, 0), 1);
}

module_init(secmsg_init);
module_exit(secmsg_exit);

MODULE_AUTHOR("Bonfee");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("kSMS - Secure Message Storage");