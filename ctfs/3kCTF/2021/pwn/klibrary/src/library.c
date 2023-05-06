#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/mutex.h>
#include <linux/slab.h>
#include <linux/module.h>
#include <linux/uaccess.h>
#include <linux/device.h>

#define DEVICE_NAME "library"
#define CLASS_NAME "library"
#define BOOK_DESCRIPTION_SIZE 0x300

#define CMD_ADD			0x3000
#define CMD_REMOVE		0x3001
#define CMD_REMOVE_ALL	0x3002
#define CMD_ADD_DESC	0x3003
#define CMD_GET_DESC 	0x3004

static DEFINE_MUTEX(ioctl_lock);
static DEFINE_MUTEX(remove_all_lock);

MODULE_AUTHOR("MaherAzzouzi");
MODULE_DESCRIPTION("A library implemented inside the kernel.");
MODULE_LICENSE("GPL");

static int major;
static long library_ioctl(struct file* file, unsigned int cmd, unsigned long arg);
static int library_open(struct inode* inode, struct file *filp); 
static int library_release(struct inode* inode, struct file *filp); 

static struct file_operations library_fops = {
	.owner = 			THIS_MODULE,
	.unlocked_ioctl = 	library_ioctl,
	.open = 			library_open,
	.release = 			library_release
};

static struct class* library_class = NULL;
static struct device* library_device = NULL;

struct Book {
	char book_description[BOOK_DESCRIPTION_SIZE];
	unsigned long index;
	struct Book* next;
	struct Book* prev;
} *root;

struct Request {
	unsigned long index;
	char __user * userland_pointer;
};

unsigned long counter = 1;

static int add_book(unsigned long index);
static int remove_book(unsigned long index);
static noinline int remove_all(void);
static int add_description_to_book(struct Request request);
static int get_book_description(struct Request request);

static int library_open(struct inode* inode, struct file *filp) {
	
	printk(KERN_INFO "[library] : manage your books safely here!\n");
	return 0;
}


static int library_release(struct inode* inode, struct file *filp) {
	printk(KERN_INFO "[library] : vulnerable device closed! try harder.\n");
	remove_all();
	return 0;
}

static long library_ioctl(struct file* file, unsigned int cmd, unsigned long arg) {
	struct Request request;
	
	if(copy_from_user((void*)&request, (void*)arg, sizeof(struct Request))) {
		return -1;
	}
		
	if(cmd == CMD_REMOVE_ALL) {
		mutex_lock(&remove_all_lock);
		remove_all();
		mutex_unlock(&remove_all_lock);	
	} else {
		mutex_lock(&ioctl_lock);

		switch(cmd) {
				case CMD_ADD:
						add_book(request.index);
						break;
				case CMD_REMOVE:
						remove_book(request.index);
						break;
				case CMD_ADD_DESC:
						add_description_to_book(request);
						break;
				case CMD_GET_DESC:
						get_book_description(request);
						break;
		}

		mutex_unlock(&ioctl_lock);
	}
	return 0;

}

static int add_book(unsigned long index) {
	
	if(counter >= 10) {
		printk(KERN_INFO "[library] can only hold 10 books here\n");
		return -1;
	}

	struct Book *b, *p;
	b = (struct Book*)kzalloc(sizeof(struct Book), GFP_KERNEL);
	
	if(b == NULL) {
		printk(KERN_INFO "[library] : allocation failed! \n");
		return -1;
	}

	b->index = index;
	if(root == NULL) {
		root = b;
		root->prev = NULL;
		root->next = NULL;
	} else {
		p = root;
		while(p->next != NULL)
			p = p->next;
		p->next = b;
		b->prev = p;
		b->next = NULL;
	}

	counter++;

	return 0;
}

static int remove_book(unsigned long index) {
	struct Book *p, *prev, *next;
	if(root == NULL) {
		printk(KERN_INFO "[library] : no books in the library yet.");
		return -1;
	} 
	else if (root->index == index) {
		p = root;
		root = root->next;
		kfree(p);
	}
	else {
		p = root;
		while(p != NULL && p->index != index)
			p = p->next;
		
		if(p == NULL) {
			printk(KERN_INFO "[library] : can't remove %ld reason : not found\n", index);
		}

		prev = p->prev;
		next = p->next;
		prev->next = next;
		next->prev = prev;
		
		kfree(p);
	}

	counter--;

	return 0;
}

static noinline int remove_all(void) {
	struct Book *b, *p;
	b = root;
	
	while(b != NULL) {
		p = b->next;
		kfree(b);
		b = p;
	}
	
	root = NULL;
	counter = 1;
	return 0;
}

static int add_description_to_book(struct Request request) {
	struct Book* book = root;

	if(book == NULL){
		printk(KERN_INFO "[library] : no books in the library yet.\n");
		return -1;
	}
	

	for(; book != NULL && book->index != request.index; book = book->next);

	if(book == NULL) {
		printk(KERN_INFO "[library] : the given index wasn't found\n");
		return -1;
	}

	if(copy_from_user((void*)book->book_description,
					  (void*)(request.userland_pointer),
					  BOOK_DESCRIPTION_SIZE)) {
		printk(KERN_INFO "[library] : copy_from_user failed for some reason.\n");
		return -1;
	}
}

static int get_book_description(struct Request request) {
	struct Book* book;
	book = root;

	if(book == NULL) {
		printk("[library] : no books yet, can not read the description.\n");
		return -1;
	}

	while(book != NULL && book->index != request.index)
		book = book->next;

	if(book == NULL) {
		printk(KERN_INFO "[library] : no book with the index you provided\n");
		return -1;
	}

	if(copy_to_user((void*)request.userland_pointer,
					(void*)book->book_description,
					BOOK_DESCRIPTION_SIZE)) {
		printk("[library] : copy_to_user failed!\n");
		return -1;
	}
}

static int __init init_library(void) {
	major = register_chrdev(0, DEVICE_NAME, &library_fops);

	if(major < 0) {
		return -1;
	}

	library_class = class_create(THIS_MODULE, CLASS_NAME);
	if(IS_ERR(library_class)) {
		unregister_chrdev(major, DEVICE_NAME);
		return -1;
	}

	library_device = device_create(library_class, 
					0, 
					MKDEV(major, 0),
				   	0, 
					DEVICE_NAME);

	if(IS_ERR(library_device)) {
		class_destroy(library_class);
		unregister_chrdev(major, DEVICE_NAME);
		return -1;
	}

	root = NULL;
	mutex_init(&ioctl_lock);
	mutex_init(&remove_all_lock);
	printk(KERN_INFO "[library] : started!\n");
	return 0;
}

static void __exit exit_library(void) {
	
	device_destroy(library_class, MKDEV(major, 0));
	class_unregister(library_class);
	class_destroy(library_class);
	unregister_chrdev(major, DEVICE_NAME);

	mutex_destroy(&ioctl_lock);
	mutex_destroy(&remove_all_lock);
	printk(KERN_INFO "[library] : finished!\n");
}

module_init(init_library);
module_exit(exit_library);
