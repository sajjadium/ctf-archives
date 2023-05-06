#include <linux/module.h>
#include <linux/version.h>
#include <linux/kernel.h>
#include <linux/types.h>
#include <linux/kdev_t.h>
#include <linux/fs.h>
#include <linux/device.h>
#include <linux/cdev.h>
#include <linux/uaccess.h>
#include <linux/slab.h>
#include <linux/string.h>

#define DEVICE_NAME "char_dev"

MODULE_LICENSE("GPL");


char *message;
static dev_t first; // Global variable for the first device number
static struct cdev c_dev; // Global variable for the character device structure
static struct class *cl; // Global variable for the device class

void *memcpy(void *dest, const void *src, size_t count)
{
	char *tmp = dest;
	const char *s = src;

	while (count--)
		*tmp++ = *s++;
	return dest;
}


size_t strlen(const char *s)
{
	const char *sc;

	for (sc = s; *sc != '\n'; ++sc)
		/* nothing */;
	return sc - s;
}

static int dev_open(struct inode *i, struct file *f)
{
	message = kmalloc(48, GFP_KERNEL);
	strcpy(message, "My char device, currently has a version v5.4.0\n");
    return 0;
}
static ssize_t dev_read(struct file *fp, char *buf, size_t size, loff_t *off)
{
	char kernel_stack[48];
	int len = strlen(message);
    if (*off >= len) {
        return 0; /* end of file */
    }
    memcpy(kernel_stack, message, len);
	if(len > size - *off) {
        len = size - *off;
    }
    if(copy_to_user(buf, kernel_stack + *off, len)) {
        return -EFAULT;
    }

    *off += len;
    return len;
}
static int dev_close(struct inode *i, struct file *f)
{
	kfree(message);
	message = NULL;
    return 0;
}

static struct file_operations pugs_fops =
{
    .owner = THIS_MODULE,
    .open = dev_open,
    .release = dev_close,
    .read = dev_read
};

static int __init dev_init(void) /* Constructor */
{
    int ret;
    struct device *dev_ret;

    if ((ret = alloc_chrdev_region(&first, 0, 1, DEVICE_NAME)) < 0)
    {
        return ret;
    }
    if (IS_ERR(cl = class_create(THIS_MODULE, DEVICE_NAME)))
    {
        unregister_chrdev_region(first, 1);
        return PTR_ERR(cl);
    }
    if (IS_ERR(dev_ret = device_create(cl, NULL, first, NULL, DEVICE_NAME)))
    {
        class_destroy(cl);
        unregister_chrdev_region(first, 1);
        return PTR_ERR(dev_ret);
    }

    cdev_init(&c_dev, &pugs_fops);
    if ((ret = cdev_add(&c_dev, first, 1)) < 0)
    {
        device_destroy(cl, first);
        class_destroy(cl);
        unregister_chrdev_region(first, 1);
        return ret;
    }
    return 0;
}

static void __exit dev_exit(void) /* Destructor */
{
    cdev_del(&c_dev);
    device_destroy(cl, first);
    class_destroy(cl);
    unregister_chrdev_region(first, 1);
}

module_init(dev_init);
module_exit(dev_exit);