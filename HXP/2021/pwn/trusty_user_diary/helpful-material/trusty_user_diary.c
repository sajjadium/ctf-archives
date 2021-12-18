#include "trusty_user_diary.h"

#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/miscdevice.h>
#include <linux/file.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/set_memory.h>
#include <linux/slab.h>
#include <asm/io.h>
#include <asm-generic/bug.h>
#include <linux/list.h>
#include <linux/virtio_config.h>
#include <linux/dma-mapping.h>

#define MESSAGE_NUM_PAGES (MESSAGE_SIZE / 0x1000U)

struct message {
	struct list_head list;
	unsigned char *mapping;
	enum message_type type;
	struct page *pages[MESSAGE_NUM_PAGES];
	unsigned long id;
};

struct diary_t {
	struct mutex mut;
	struct list_head messages;
	size_t num_messages;
};

static struct diary_t global_diary;

static struct message *find_message(unsigned long id) {
	struct list_head *cur, *tmp;
	list_for_each_safe(cur, tmp, &global_diary.messages) {
		struct message *msg = container_of(cur, struct message, list);
		if (msg->id == id) {
			return msg;
		}
	}
	return NULL;
}

static long trusty_user_add_message(unsigned long ioctl, void *arg) {
	struct add_message_request req;
	void *message_data = NULL;
	struct message *message = NULL;

	if (global_diary.num_messages >= MAX_MESSAGES) {
		return -ENOMEM;
	}

	// Read request
	if (copy_from_user(&req, (void*)arg, sizeof(req))) {
		return -EFAULT;
	}

	// Construct message
	message = kzalloc(sizeof(*message), GFP_KERNEL);
	if (!message) {
		return -ENOMEM;
	}

	if (ioctl == ADD_MESSAGE) {
		long copy_ret;
		message_data = (void *)__get_free_pages(GFP_KERNEL | __GFP_ZERO, get_order(MESSAGE_SIZE));
		if (!message_data) {
			kfree(message);
			return -ENOMEM;
		}
		message->type = SLOW;
		copy_ret = copy_from_user(message_data, req.message, MESSAGE_SIZE);
		(void)copy_ret;
	} else if (ioctl == ADD_MESSAGE_ZERO_COPY) {
		struct mm_struct *mm = current->mm;
		struct vm_area_struct *vma = NULL;
		struct page *pages[MESSAGE_NUM_PAGES];
		int r;
		memset(pages, 0, sizeof(pages));

		// Do in mm section
		mmap_read_lock(mm);
		vma = find_vma(mm, req.va_page);
		if (!vma) {
			mmap_read_unlock(mm);
			kfree(message);
			return -EINVAL;
		}

		if ((vma->vm_flags & (VM_READ | VM_WRITE)) != (VM_READ | VM_WRITE)) {
			mmap_read_unlock(mm);
			kfree(message);
			return -EPERM;
		}

		r = pin_user_pages_fast(req.va_page, MESSAGE_NUM_PAGES, 0, pages);
		if (r <= 0) {
			mmap_read_unlock(mm);
			kfree(message);
			return r;
		}

		if (r != MESSAGE_NUM_PAGES) {
			unpin_user_pages(pages, r);
			mmap_read_unlock(mm);
			kfree(message);
			return -EINVAL;
		}

		message_data = vmap(pages, MESSAGE_NUM_PAGES, VM_MAP, PAGE_KERNEL);
		if (!message_data) {
			unpin_user_pages(pages, r);
			mmap_read_unlock(mm);
			kfree(message);
			return -ENOMEM;
		}

		message->type = ZERO_COPY;
		memcpy(message->pages, pages, sizeof(pages));

		mmap_read_unlock(mm);
	} else {
		kfree(message);
		return -EINVAL;
	}

	message->mapping = message_data;
	message->id = req.id;

	// Add to list
	list_add_tail(&message->list, &global_diary.messages);
	++global_diary.num_messages;

	return 0;
}

static long trusty_user_remove_message(void *arg) {
	struct remove_message_request req;
	struct message *msg = NULL;

	// Read request
	if (copy_from_user(&req, arg, sizeof(req))) {
		return -EFAULT;
	}

	msg = find_message(req.id);
	if (msg) {
		list_del(&msg->list);
		if (msg->type == SLOW) {
			free_pages((unsigned long)msg->mapping, get_order(MESSAGE_SIZE));
		} else if (msg->type == ZERO_COPY) {
			vfree(msg->mapping);
			mmap_read_lock(current->mm);
			unpin_user_pages(msg->pages, MESSAGE_NUM_PAGES);
			mmap_read_unlock(current->mm);
		} else {
			WARN(1, "Invalid state");
			return -EINVAL;
		}
		kfree(msg);
		--global_diary.num_messages;
	} else {
		return -EINVAL;
	}

	return 0;
}

static long trusty_user_update_message(void *arg) {
	struct update_message_request req;
	struct message *msg = NULL;

	if (copy_from_user(&req, arg, sizeof(req))) {
		return -EFAULT;
	}

	// Update only first found message
	msg = find_message(req.id);
	if (msg) {
		long copy_ret = copy_from_user(msg->mapping, req.new_message, MESSAGE_SIZE);
		(void)copy_ret;
	} else {
		return -EINVAL;
	}
	return 0;
}

static long trusty_user_read_message(void *arg) {
	struct read_message_request req;
	struct message *msg = NULL;

	if (copy_from_user(&req, arg, sizeof(req))) {
		return -EFAULT;
	}
	msg = find_message(req.id);
	if (msg) {
		long copy_ret = copy_to_user(req.dest_message, msg->mapping, MESSAGE_SIZE);
		(void)copy_ret;
	} else {
		return -EINVAL;
	}

	return 0;
}

static long trusty_user_diary_ioctl(struct file *f, unsigned int ioctl, unsigned long arg) {
	long r = 0;

	mutex_lock(&global_diary.mut);

	switch (ioctl) {
	case ADD_MESSAGE:
	case ADD_MESSAGE_ZERO_COPY:
		r = trusty_user_add_message(ioctl, (void *)arg);
		break;
	case REMOVE_MESSAGE:
		r = trusty_user_remove_message((void *)arg);
		break;
	case UPDATE_MESSAGE:
		r = trusty_user_update_message((void *)arg);
		break;
	case READ_MESSAGE:
		r = trusty_user_read_message((void *)arg);
		break;
	default:
		r = -EINVAL;
		break;
	}

	mutex_unlock(&global_diary.mut);

	return r;
}

static int trusty_user_diary_release(struct inode *inode, struct file *f) {
	return 0;
}

static int trusty_user_diary_open(struct inode *inode, struct file *f) {
	return 0;
}

static const struct file_operations trusty_user_diary_ops = { 
	.owner          = THIS_MODULE,
	.release        = trusty_user_diary_release,
	.open           = trusty_user_diary_open,
	.unlocked_ioctl = trusty_user_diary_ioctl,
};

static struct miscdevice trusty_user_diary_misc = { 
	.minor = MISC_DYNAMIC_MINOR,
	.name = "trusty_user_diary",
	.fops = &trusty_user_diary_ops,
};

static int trusty_user_diary_init(void) {
	int r;
	r = misc_register(&trusty_user_diary_misc);
	if (r) {
		printk("Failed to register driver\n");
		return r;
	}
	mutex_init(&global_diary.mut);
	global_diary.num_messages = 0;
	INIT_LIST_HEAD(&global_diary.messages);
	return 0;
}

static void __exit trusty_user_diary_exit(void) {
	misc_deregister(&trusty_user_diary_misc);
}

module_init(trusty_user_diary_init);
module_exit(trusty_user_diary_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("HXP Solutions");
