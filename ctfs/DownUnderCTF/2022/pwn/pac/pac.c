#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/fs.h>
#include <linux/device.h>

#include "encryption.c"

MODULE_LICENSE("GPL"); 
MODULE_AUTHOR("joseph");

#define DEVICE_NAME "ductf-pac"

typedef int (*func)(char*);

int major = 0x68;

unsigned long enc_hello;

int hello(char* buf) {
    char* msg = "hello!\n";
    return copy_to_user(buf+8, msg, strlen(msg));
}

static int device_open(struct inode *inode, struct file *file) {
    pr_alert("Device opened.");
    return 0;
}

static int device_release(struct inode *inode, struct file *file) {
    pr_alert("Device released.");
    return 0;
}

static ssize_t device_read(struct file *file, char *buffer, size_t length, loff_t *offset) {
    char msg[0x100];
    sprintf(msg, "Lost? Here's a pointer:\nenc_hello = 0x%16lx", enc_hello);
    return strlen(msg) - copy_to_user(buffer, msg, strlen(msg));
}

static ssize_t device_write(struct file *file, const char *buf, size_t len, loff_t *off) {
    unsigned long f = *((unsigned long*)buf);
    if(verify_ptr(f)) {
        unsigned long t;
        asm(
            "mov %1, %%rax;"
            "mov %%rax, %0"
            : "=r"(t)
            : "r"(_copy_to_user)
            :"%rax"
        );
        if((f & 0xffffffff) < 0x00500000) {
            f = f & 0xffffffff;
        } else {
            f = (t & 0xffffffff00000000) | (f & 0xffffffff);
        }
        return ((func)(f))((char*)buf);
    }
    return 0;
}

static struct file_operations fops = {
    .read = device_read,
    .write = device_write,
    .open = device_open,
    .release = device_release
};

static int __init pac_init(void) { 
    major = register_chrdev(major, DEVICE_NAME, &fops);

    if (major < 0) {
        pr_alert("Registering char device failed with %d\n", major);
        return major;
    }

    pr_info("I was assigned major number %d.\n", major);

    init_pac_encryptor();
    enc_hello = encrypt_ptr((unsigned long)hello);

    return 0;
} 

static void __exit pac_exit(void) { 
    unregister_chrdev(major, DEVICE_NAME); 
}

module_init(pac_init); 
module_exit(pac_exit);
