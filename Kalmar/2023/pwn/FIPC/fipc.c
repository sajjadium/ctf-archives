#include <asm/io.h>
#include <linux/device.h>
#include <linux/gfp.h>
#include <linux/init.h>
#include <linux/ioctl.h>
#include <linux/kernel.h>
#include <linux/list.h>
#include <linux/log2.h>
#include <linux/mm.h>
#include <linux/module.h>
#include <linux/random.h>
#include <linux/slab.h>

#define PTE_PD_MASK 0x67
#define PTE_MASK 0x400000000000367

#define DEVICE_NAME "fipc"
#define CLASS_NAME "fipc"
#define MAX_SIZE PAGE_SIZE * 0x10

static struct class *class;
static struct device *device;
static int major;

typedef struct {
    refcount_t count;
    unsigned int key;
    struct page *page;
    struct page *tables;
    unsigned long size;
    struct list_head ipcs;
    unsigned long oo;
} ipc_t;

static DEFINE_MUTEX(fipc_lock);
static LIST_HEAD(fipcs);

ipc_t *find_ipc(int key)
{
    ipc_t *ipc;
    list_for_each_entry(ipc, &fipcs, ipcs)
    {
        if (ipc->key == key) {
            return ipc;
        }
    }

    return NULL;
}

void inc_ipc(ipc_t *ipc)
{
    if (!ipc)
        return;
    atomic_inc((atomic_t *)(&ipc->count));
}

void dec_ipc(ipc_t *ipc)
{
    if (!ipc)
        return;
    if (refcount_dec_and_test(&ipc->count)) {
        struct page *page = ipc->page;
        struct page *tables = ipc->tables;
        __free_pages(page, ipc->oo);
        __free_pages(tables, 2);
        list_del(&ipc->ipcs);
        kfree(ipc);
    }
}

void vma_open(struct vm_area_struct *vma)
{
    mutex_lock(&fipc_lock);
    vma->vm_end = vma->vm_start;
    mutex_unlock(&fipc_lock);
}

void vma_close(struct vm_area_struct *vma)
{
    pgd_t *pgd_entry;
    unsigned long start = vma->vm_start;
    struct mm_struct *mm = vma->vm_mm;
    mutex_lock(&fipc_lock);
    pgd_entry = pgd_offset(mm, start);
    pgd_entry->pgd = 0;
    vma->vm_private_data = NULL;
    vma->vm_file->private_data = NULL;
    atomic_long_set(&mm->pgtables_bytes, 0);
    mutex_unlock(&fipc_lock);
}

struct vm_operations_struct vm_ops = {
    .open = vma_open,
    .close = vma_close,
};

static int fipc_mmap(struct file *filp, struct vm_area_struct *vma)
{
    pgd_t *pgd_entry;
    pud_t *pud_entry;
    pmd_t *pmd_entry;
    pte_t *pte_entry;
    ipc_t *ipc;
    unsigned long pud_phys, pmd_phys, pte_phys;
    unsigned long page_phys_start, page_phys_end, page_phys_map_start,
                  page_phys_map_end;
    unsigned long offset = vma->vm_pgoff * PAGE_SIZE;
    unsigned long start = vma->vm_start + offset;
    unsigned long end = vma->vm_end;
    unsigned long size = end - start;
    pgprot_t prot = vma->vm_page_prot;
    struct mm_struct *mm = vma->vm_mm;
    vma->vm_private_data = filp->private_data;
    ipc = (ipc_t *)vma->vm_private_data;
    if (!ipc) {
        return -EINVAL;
    }

    vma->vm_ops = &vm_ops;

    pud_phys = page_to_phys(ipc->tables);
    pmd_phys = page_to_phys(ipc->tables) + PAGE_SIZE;
    pte_phys = page_to_phys(ipc->tables) + PAGE_SIZE * 2;

    page_phys_start = page_to_phys(ipc->page);
    page_phys_end = page_phys_start + ipc->size;

    page_phys_map_start = page_phys_start;
    page_phys_map_end = page_phys_map_start + size;

    if (size > ipc->size)
        return -EINVAL;

    if (start >= end)
        return -EINVAL;

    if (start < vma->vm_start)
        return -EINVAL;

    if (page_phys_map_start >= page_phys_end)
        return -EINVAL;

    while (start != end) {

        pgd_entry = pgd_offset(mm, start);

        if (pgd_entry->pgd == 0) {
            pgd_entry->pgd = pud_phys | PTE_PD_MASK;
            atomic_long_add(PTRS_PER_PUD * sizeof(pud_t), &mm->pgtables_bytes);
        }

        pud_entry = pud_offset((p4d_t *)pgd_entry, start);

        if (pud_entry->pud == 0) {
            pud_entry->pud = pmd_phys | PTE_PD_MASK;
            atomic_long_add(PTRS_PER_PMD * sizeof(pmd_t), &mm->pgtables_bytes);
        }

        pmd_entry = pmd_offset(pud_entry, start);

        if (pmd_entry->pmd == 0) {
            pmd_entry->pmd = pte_phys | PTE_PD_MASK;
            atomic_long_add(PTRS_PER_PTE * sizeof(pte_t), &mm->pgtables_bytes);
        }

        pte_entry = pte_offset_map(pmd_entry, start);
        pte_entry->pte = (page_phys_map_start + (size - (end - start))) |
            prot.pgprot | PTE_MASK;

        start += PAGE_SIZE;
    }

    vma_open(vma);
    return 0;
}

ipc_t *alloc_ipc(unsigned long size)
{
    struct page *page, *tables;
    unsigned long oo;
    unsigned int key;
    ipc_t *ipc;
    if (size > MAX_SIZE) {
        return NULL;
    }
    if (size == 0) {
        return NULL;
    }
    oo = PAGE_ALIGN(size);
    oo = roundup_pow_of_two(size);
    oo /= PAGE_SIZE;
    oo = ilog2(oo);

    page = alloc_pages(GFP_KERNEL | __GFP_ZERO, oo);
    if (!page)
        return NULL;

    memset(page_to_virt(page), 0, oo*PAGE_SIZE);
    tables = alloc_pages(GFP_KERNEL | __GFP_ZERO, 2);
    if (!tables || !page) {
        if (tables) {
            __free_pages(tables, 2);
        }
        if (page){
            __free_pages(tables, oo);
        }
        return NULL;
    }

    ipc = (ipc_t *)kmalloc(sizeof(ipc_t), GFP_KERNEL | __GFP_ZERO);
    if (!ipc) {
        __free_pages(page, 0);
        __free_pages(tables, 2);
        return NULL;
    }

    do {
        get_random_bytes(&key, sizeof(ipc->key));
    } while(find_ipc(key));


    ipc->key = key;
    ipc->page = page;
    ipc->size = size;
    ipc->oo = oo;
    ipc->tables = tables;
    refcount_set(&(ipc->count), 0);
    list_add(&ipc->ipcs, &fipcs);

    return ipc;
}

static long fipc_ioctl(struct file *filep, unsigned int cmd, unsigned long argv)
{
    ipc_t *ipc;
    int ret = -EINVAL;
    mutex_lock(&fipc_lock);
    switch (cmd) {
        case 0x1337:
            ipc = alloc_ipc(argv);
            inc_ipc(ipc);
            if (ipc) {
                filep->private_data = (void *)ipc;
                ret = ipc->key;
            }
            break;
        case 0x1338:
            ipc = find_ipc((int)argv);
            inc_ipc(ipc);
            if (ipc) {
                filep->private_data = (void *)ipc;
                ret = 0;
            }
            break;
        default:
            break;
    }

    mutex_unlock(&fipc_lock);
    return ret;
}

static int device_open(struct inode *node, struct file *filep) {
    filep->private_data = 0;
    return 0;
}

static int device_release(struct inode *node, struct file *filep) {
    ipc_t *ipc;
    ipc = filep->private_data;
    if (ipc) {
        dec_ipc(ipc);
    }
    return 0;
}

static const struct file_operations fops = {
    .mmap = fipc_mmap, .unlocked_ioctl = fipc_ioctl, .open = device_open, .release = device_release,
 .owner = THIS_MODULE};

int __init start_init(void)
{
    int ret;
    mutex_init(&fipc_lock);
    major = register_chrdev(0, DEVICE_NAME, &fops);

    if (major < 0) {
        pr_info("fpic: fail to register major number!");
        ret = major;
        return ret;
    }

    class = class_create(THIS_MODULE, CLASS_NAME);
    if (IS_ERR(class)) {
        unregister_chrdev(major, DEVICE_NAME);
        pr_info("fpic: failed to register device class");
        ret = PTR_ERR(class);
        return ret;
    }

    device = device_create(class, NULL, MKDEV(major, 0), NULL, DEVICE_NAME);
    if (IS_ERR(device)) {
        class_destroy(class);
        unregister_chrdev(major, DEVICE_NAME);
        ret = PTR_ERR(device);
        return ret;
    }

    return 0;
}

static void __exit end_exit(void) { 
    mutex_destroy(&fipc_lock);
    return; 
}

module_init(start_init);
module_exit(end_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Zander");
MODULE_DESCRIPTION("Playground");
