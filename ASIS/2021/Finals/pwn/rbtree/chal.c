#include <linux/device.h>
#include <linux/fs.h>
#include <linux/kernel.h>
#include <linux/list.h>
#include <linux/module.h>
#include <linux/mutex.h>
#include <linux/random.h>
#include <linux/slab.h>
#include <linux/uaccess.h>

#define MSG_MAX_SIZE 0x40
#define DEVICE_NAME "chall"
#define CLASS_NAME "chall"
#define ADD_MSG 0x100001
#define GET_MSG 0x100002

MODULE_AUTHOR("r4j");
MODULE_LICENSE("GPL");

static DEFINE_MUTEX(chall_ioctl_lock);
static long chall_ioctl(struct file *file, unsigned int cmd, unsigned long arg);
static int chall_open(struct inode *inode, struct file *file);
static int chall_release(struct inode *inode, struct file *file);

static int major;
static struct class *chall_class = NULL;
static struct device *chall_device = NULL;
static struct file_operations chall_fops = {
    .open = chall_open,
    .unlocked_ioctl = chall_ioctl,
    .release = chall_release,
    .owner = THIS_MODULE
};

struct queue_msg {
    struct rb_node node;
    struct list_head msg_list;
    size_t len;
    uint64_t key;
};

struct msg_user {
    size_t len;
    void *data;
    uint64_t key;
};

struct chall_t {
    struct list_head msg_list;
    struct rb_root msg_tree;
};

static int chall_open(struct inode *inode, struct file *file) {
    struct chall_t *chall;
    chall = kzalloc(sizeof(*chall), GFP_KERNEL);
    if (IS_ERR_OR_NULL(chall))
        return -ENOMEM;

    INIT_LIST_HEAD(&chall->msg_list);
    file->private_data = (void *)chall;
    return 0;
}

static int chall_release(struct inode *inode, struct file *file) {
    struct chall_t *chall;
    struct list_head *entry, *next;
    struct queue_msg *queue_msg;

    struct list_head *msg_list;
    chall = (struct chall_t *)file->private_data;
    msg_list = &chall->msg_list;

    list_for_each_safe(entry, next, msg_list) {
        queue_msg = list_entry(entry, struct queue_msg, msg_list);
        list_del(entry);
        kfree(queue_msg);
    }

    kfree(chall);
    return 0;
}

static struct queue_msg *msg_tree_search(struct rb_root *root, uint64_t key) {
    struct rb_node *node = root->rb_node;

    while (node) {
        struct queue_msg *msg = rb_entry(node, struct queue_msg, node);
        if (key < msg->key)
            node = node->rb_left;
        else if (key > msg->key)
            node = node->rb_right;
        else
            return msg;
    }
    return NULL;
}

static void msg_tree_insert(struct queue_msg *msg, struct rb_root *root) {
    struct rb_node **new = &(root->rb_node), *parent = NULL;

    while (*new) {
        struct queue_msg *this = rb_entry(*new, struct queue_msg, node);
        parent = *new;
        if (msg->key < this->key)
            new = &((*new)->rb_left);
        else if (msg->key > this->key)
            new = &((*new)->rb_right);
        else
            BUG();
    }

    rb_link_node(&msg->node, parent, new);
    rb_insert_color(&msg->node, root);
}

static struct queue_msg *find_msg_by_key(struct chall_t *chall, uint64_t key) {
    return msg_tree_search(&chall->msg_tree, key);
}

static long chall_ioctl(struct file *file, unsigned int cmd,
                        unsigned long arg) {
    struct msg_user msg_user;
    long res;
    struct queue_msg *queue_msg;

    struct chall_t *chall;
    mutex_lock(&chall_ioctl_lock);
    chall = (struct chall_t *)file->private_data;

    if (copy_from_user(&msg_user, (void *)arg, sizeof(struct msg_user))) {
        res = -EFAULT;
        goto ret;
    }

    switch (cmd) {
    case ADD_MSG:
        if (!msg_user.len || msg_user.len > MSG_MAX_SIZE) {
            res = -EINVAL;
            break;
        }

        queue_msg = kmalloc(sizeof(*queue_msg) + msg_user.len, GFP_KERNEL);
        if (IS_ERR_OR_NULL(queue_msg)) {
            res = -ENOMEM;
            break;
        }

        if (copy_from_user((unsigned char *)queue_msg + sizeof(*queue_msg),
                           msg_user.data, msg_user.len)) {
            kfree(queue_msg);
            res = -EFAULT;
            break;
        }

        do {
            get_random_bytes(&queue_msg->key, sizeof(queue_msg->key));
        } while (!queue_msg->key || find_msg_by_key(chall, queue_msg->key));

        if (copy_to_user((unsigned char *)arg + offsetof(struct msg_user, key),
                         &queue_msg->key, sizeof(queue_msg->key))) {
            kfree(queue_msg);
            res = -EFAULT;
            break;
        }

        queue_msg->len = msg_user.len;
        res = 0;
        list_add_tail(&queue_msg->msg_list, &chall->msg_list);
        msg_tree_insert(queue_msg, &chall->msg_tree);
        break;
    case GET_MSG:
        if (list_empty(&chall->msg_list)) {
            res = -EINVAL;
            break;
        }

        if (msg_user.key) {
            queue_msg = find_msg_by_key(chall, msg_user.key);
            if (queue_msg == NULL) {
                res = -EINVAL;
                break;
            }
        } else {
            res = -EINVAL;
            break;
        }

        rb_erase(&queue_msg->node, &chall->msg_tree);
        msg_user.len =
            (msg_user.len <= queue_msg->len) ? msg_user.len : queue_msg->len;

        if (copy_to_user(msg_user.data,
                         (unsigned char *)queue_msg + sizeof(*queue_msg),
                         msg_user.len)) {
            res = -EFAULT;
        } else {
            res = msg_user.len;
            list_del(&queue_msg->msg_list);
        }

        kfree(queue_msg);
        break;
    default:
        res = -EINVAL;
        break;
    }

ret:
    mutex_unlock(&chall_ioctl_lock);
    return res;
}

static int __init init_chall(void) {
    major = register_chrdev(0, DEVICE_NAME, &chall_fops);
    if (major < 0)
        return -1;

    chall_class = class_create(THIS_MODULE, CLASS_NAME);
    if (IS_ERR(chall_class)) {
        unregister_chrdev(major, DEVICE_NAME);
        return -1;
    }

    chall_device =
        device_create(chall_class, 0, MKDEV(major, 0), 0, DEVICE_NAME);
    if (IS_ERR(chall_device)) {
        class_destroy(chall_class);
        unregister_chrdev(major, DEVICE_NAME);
        return -1;
    }

    return 0;
}

static void __exit exit_chall(void) {
    device_destroy(chall_class, MKDEV(major, 0));
    class_unregister(chall_class);
    class_destroy(chall_class);
    unregister_chrdev(major, DEVICE_NAME);
}

module_init(init_chall);
module_exit(exit_chall);
