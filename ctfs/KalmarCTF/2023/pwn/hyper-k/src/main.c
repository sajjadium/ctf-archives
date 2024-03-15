#include <linux/init.h>
#include <linux/module.h>
#include <linux/uaccess.h>
#include <linux/mm.h>
#include <linux/mutex.h>
#include <linux/fs.h>
#include <linux/proc_fs.h>
#include "../includes/main.h"
#include "../includes/memory.h"
#include "../includes/ioctls.h"

MODULE_LICENSE("GPL v2");
MODULE_AUTHOR("Zanderdk");
MODULE_DESCRIPTION("hypervisor challenge for Kalmar-CTF");
MODULE_VERSION("0.1");


static int device_open(struct inode *node, struct file *file);
static int device_release(struct inode *node, struct file *file);
ssize_t device_read(struct file *file, char *buff, size_t count, loff_t *offp);
ssize_t device_write(struct file *file, const char *buff, size_t count, loff_t *offp);
static long device_ioctl(struct file *file, unsigned int cmd, unsigned long arg);
static int device_mmap(struct file *file, struct vm_area_struct *vm);

#ifndef VM_RESERVED
#define  VM_RESERVED   (VM_DONTEXPAND | VM_DONTDUMP)
#endif

static struct file_operations fips =
{
    .owner = THIS_MODULE,
    .open = device_open,
    .release = device_release,
    .read = device_read,
    .write = device_write,
    .mmap = device_mmap,
    .unlocked_ioctl = device_ioctl,
};

int init_module(void)
{
    int register_error;
    printk(KERN_INFO "Initializing hyper-k.\n");
    register_error = register_chrdev('K', "hyper-k", &fips);
    if (register_error) return register_error;
    vmx_on();
    return  0;
}

void cleanup_module(void)
{
    unregister_chrdev('K', "hyper-k");
    vmx_off();
}

vcpu_t *get_vcpu(vm_t *vm)
{
    return &vm->vcpu;
}

static int device_open(struct inode *node, struct file *file) {
    vm_t *vm = vm_alloc();
    vcpu_t *vcpu;
    if (!vm) return -ENOMEM;
    file->private_data = vm;
    vm->memory = alloc_mem();
    vcpu = get_vcpu(vm);
    init_sregs(&vcpu->state.sregs);
    vcpu->state.regs.rflags = 0x2;
    mutex_init(&vm->vm_mutex);
    return 0;
}

static int device_release(struct inode *node, struct file *file) {
    vm_t *vm = file->private_data;
    mutex_lock(&vm->vm_mutex);
    if (vm)
    {
        if (vm->memory) {
            destroy_mem(vm->memory);
        }
        vm_destroy(vm);
    } else 
        return 0;
    file->private_data = NULL;
    mutex_unlock(&vm->vm_mutex);
    return 0;
}

ssize_t device_read(struct file *file, char *buff, size_t count, loff_t *offp) {
    vm_t *vm = file->private_data;
    mutex_lock(&vm->vm_mutex);
    //code here
    mutex_unlock(&vm->vm_mutex);
    return -1;
}

ssize_t device_write(struct file *file, const char *buff, size_t count,
        loff_t *offp) {
    vm_t *vm = file->private_data;
    mutex_lock(&vm->vm_mutex);
    //code here
    mutex_unlock(&vm->vm_mutex);
    return -1;
}

static long device_ioctl_pinned(struct file *file, unsigned int cmd, unsigned long arg)
{
    userspace_regs_t user;
    __u64 i;
    long ret;

    vm_t *vm = file->private_data;
    vcpu_t *vcpu;

    if (!vm) return -ENOENT;
    mutex_lock(&vm->vm_mutex);

    switch (cmd)
    {
        case IOCTL_RUN:
            vcpu = get_vcpu(vm);
            if (!vcpu) return -EINVAL;
            do
            {
                i = vcpu_run(vcpu);
            }
            while (i == VMEXIT_HANDLED);
            clearvm(vcpu);
            ret = i;
            goto out;
        case IOCTL_GET:
            vcpu = get_vcpu(vm);
            if (!vcpu) return -EINVAL;
            memcpy(&user, &(vcpu->state.regs), sizeof(userspace_regs_t));
            if (copy_to_user((void *)arg, &user, sizeof(userspace_regs_t))) return -EINVAL;
            ret = 0;
            goto out;
        case IOCTL_PUT:
            vcpu = get_vcpu(vm);
            if (!vcpu) return -EINVAL;
            if (copy_from_user(&user, (void *)arg, sizeof(userspace_regs_t))) return -EINVAL;
            memcpy(&(vcpu->state.regs), &user, sizeof(userspace_regs_t));
            ret = 0;
            goto out;

        default:
            ret = -ENOTTY;
            goto out;
    }

out:
    mutex_unlock(&vm->vm_mutex);
    return ret;
}

static long device_ioctl(struct file *file, unsigned int cmd, unsigned long arg) {
    __u64 r;
    get_cpu();
    r = device_ioctl_pinned(file, cmd, arg);
    put_cpu();
    return r;
}

vm_fault_t vma_fault(struct vm_fault *vmf) {
    struct vm_area_struct *vma = vmf->vma;
    vm_fault_t ret = 0;
    vm_t *vm = vma->vm_private_data;
    __u64 paddr;
    memory_t *mem;
    mapping_t * map;
    struct page *page;
    if (!vm)
        return VM_FAULT_SIGBUS;

    mem = vm->memory;
    if (!mem) {
        ret = VM_FAULT_SIGBUS;
        goto out;
    }

    paddr = vmf->pgoff << PAGE_SHIFT;

    map = handle_mmap_fault(mem, paddr);
    page = map->page;
    if (!page) {
        ret = VM_FAULT_OOM;
        goto out;
    }
    get_page(page);
    vmf->page = page;

out:
    mutex_unlock(&vm->vm_mutex);
    return ret;
}

struct vm_operations_struct vm_ops = {
    .fault = vma_fault
};

static int device_mmap(struct file *file, struct vm_area_struct *vma) { 
    vm_t *vm;
    vma->vm_private_data = file->private_data;
    vm = vma->vm_private_data;
    if (!vm)
        return VM_FAULT_SIGBUS;
    mutex_lock(&vm->vm_mutex);

    vma->vm_ops = &vm_ops;

    mutex_unlock(&vm->vm_mutex);
    return 0;
}
