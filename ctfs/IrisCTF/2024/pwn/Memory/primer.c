#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/fs.h>
#include <asm/uaccess.h>
#include "primer.h"

MODULE_LICENSE("GPL");

static int device_open(struct inode *inode, struct file *file) {
	try_module_get(THIS_MODULE);
	return 0;
}

static int device_release(struct inode *inode, struct file *file) {
	module_put(THIS_MODULE);
	return 0;
}

static ssize_t device_read(struct file *file, char __user * buffer, size_t length, loff_t * offset) {
	return 0;
}

static ssize_t device_write(struct file *file, const char __user * buffer, size_t length, loff_t * offset) {
	return 0;
}

volatile const unsigned char data[] = "fakeflg{fake_flag_for_you}";
unsigned long user = 0;

long int device_ioctl(
		struct file *file,
		unsigned int ioctl_num,
		unsigned long ioctl_param)
{
	switch (ioctl_num) {

    case IOCTL_QUERY: {
      size_t user = ioctl_param >> 56;
      unsigned char* ptr = (unsigned char*)(ioctl_param & 0x00ffffffffffffff);
      if(__builtin_expect(user < sizeof(data), 1)) {
        unsigned char c;
        get_user(c, &(ptr[data[user]]));
        return 0;
	    }
    }
	}

	return 0;
}

struct file_operations Fops = {
	.read = device_read,
	.write = device_write,
	.unlocked_ioctl = device_ioctl,
	.open = device_open,
	.release = device_release,
};

int init_module() {
	int ret_val;
	ret_val = register_chrdev(MAJOR_NUM, "primer", &Fops);

	if (ret_val < 0) {
		return ret_val;
	}

	return 0;
}

void cleanup_module() {
	unregister_chrdev(MAJOR_NUM, "primer");
}
