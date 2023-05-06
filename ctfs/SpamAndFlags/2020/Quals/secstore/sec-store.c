#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/io.h>

#include <linux/miscdevice.h>
#include <linux/platform_device.h>
#include <linux/mod_devicetable.h>
#include <linux/of.h>
#include <linux/interrupt.h>

#include <linux/types.h>   // for dev_t typedef
#include <linux/kdev_t.h>  // for format_dev_t
#include <linux/fs.h>      // for alloc_chrdev_region()
#include <linux/string.h>
#include <linux/mm.h>
#include <linux/highmem.h>

#include <asm/io.h> //for debug purposes


#define DEVICE_NAME "sec-store"


MODULE_AUTHOR("gym");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Flawless secure storage device");
MODULE_VERSION("0.1");

int majorNum;

#define SEC_DMA_MAX  0x00800000
#define PL666_CONF_EN 0x0001

#define PL666_LLI_MORE 0x0001
#define PL666_LLI_READ 0x0002

#define PL666_RD_IT_MASK 0
#define PL666_RD_IT_VAL 4
#define PL666_RD_CONF 8
#define PL666_RD_TEST 12

#define PL666_WR_IT 0
#define PL666_WR_IT_CLR 4
#define PL666_WR_CONF 8
#define PL666_WR_ADDR_LOW 12
#define PL666_WR_ADDR_HIGH 16

#define DMA_READ 0
#define DMA_WRITE 1

struct pl666_data{
    char __iomem * dma_base;
    unsigned dma_done;
    wait_queue_head_t dma_wait;
    struct mutex io_lock;
};

static struct pl666_data * pdata;

#define MAX_LLI 8
struct lli{
    uint64_t src;
    uint64_t dst;
    uint32_t size;
    uint32_t ctrl;
};

// This is used to map userspace memory for kernel and dma access
// pins the page in physical memory
static int map_to_kernel(uint64_t uaddr, struct page** page, void ** kaddr){
    int err;

    if(!access_ok((void*)uaddr, PAGE_SIZE)){
        return -1;
    }
    down_read(&current->mm->mmap_sem);
    err = pin_user_pages((uint64_t)uaddr, 1, FOLL_TOUCH |FOLL_POPULATE, page, 0);
    up_read(&current->mm->mmap_sem);
    if (err != 1) {
        return -2;
    }

    *kaddr = vmap(page, 1, VM_MAP, PAGE_KERNEL);

    if (!*kaddr){
        return -3;
    }
    return 0;

}


static ssize_t secs_do_dma(const char* __user buffer, size_t len, unsigned dir)
{
    int ret, err, i;
    struct lli* items;
    void* kaddr[MAX_LLI + 1] = {0,};
    struct page* pages[MAX_LLI + 1] = {0,};
    int mapped = 0;
    uint64_t data;
    uint64_t offset;

    if (len > sizeof(struct lli) * MAX_LLI || len % sizeof(struct lli)){
        printk(KERN_INFO "%s Invalid size %lu\n", __func__, len);
        return -EFAULT;
    }

    // serialize dma access
    if (!mutex_trylock(&pdata->io_lock)) {
        printk(KERN_INFO "%s Failed to aquire mutex\n", __func__);
        return -EBUSY;
    }
 
    pdata->dma_done = 0;

    if ((uint64_t)buffer & 0xfff){
        printk(KERN_INFO "%s Buffer is not aligned\n", __func__);
        return -EFAULT;
    
    }

    err = map_to_kernel((uint64_t)buffer, &pages[mapped], &kaddr[mapped]);

    mapped++;

    if (err < 0){
        printk(KERN_INFO "%s Failed to map userpage %d\n", __func__, err);
        ret = -EFAULT;
        goto out;
    }

    items = (struct lli*)kaddr[0];

    // change the list items to work on kernel addresses
    // the dma hw can only resolve kernel pages
    for (i=0; i < len / sizeof(struct lli); i++ ){

        if (dir == DMA_READ) {
            data = items[i].dst;
            offset = items[i].src;

        } else {
            data = items[i].src;
            offset = items[i].dst;
        }

        if (offset >= SEC_DMA_MAX || (offset + items[i].size) > SEC_DMA_MAX || !items[i].size){
            printk(KERN_INFO "%s Invalid offset %llx or size %x \n", __func__, offset, items[i].size);
            ret = -EFAULT;
            goto out;
            
        }

        err = map_to_kernel(data, &pages[mapped], &kaddr[mapped]);
        mapped++;

        if (err < 0){
            printk(KERN_INFO "%s Failed to map userpage %d %llx\n", __func__, err, data);
            ret = -EFAULT;
            goto out;
        }

        items[i].ctrl = PL666_LLI_MORE;

        if (dir == DMA_READ) {
            items[i].dst = (uint64_t)kaddr[i+1];
            items[i].ctrl |= PL666_LLI_READ;
        } else {
            items[i].src = (uint64_t)kaddr[i+1];
        }
    
        flush_kernel_dcache_page(pages[0]);
    }

    items[(len/sizeof(struct lli)) - 1].ctrl &= ~PL666_LLI_MORE;
    flush_kernel_dcache_page(pages[0]);

    // set up the address of the transaction array
    writel((uint32_t)((uint64_t)items & 0xffffffff), pdata->dma_base + PL666_WR_ADDR_LOW);
    writel((uint32_t)((uint64_t)items >> 32), pdata->dma_base + PL666_WR_ADDR_HIGH);

    // start the dma transaction
    writel(PL666_CONF_EN, pdata->dma_base + PL666_WR_CONF);

    if (dir == DMA_READ){
        ret = 0;
    } else {
        ret = len;
    }

    // wait for the dma to complete
    err = wait_event_interruptible_timeout(pdata->dma_wait, pdata->dma_done, HZ*2);
    if (!err) {
        printk(KERN_ALERT "%s, dma request timed out\n", __func__);
        ret =  -EIO;
        goto out;
    } else if (err < 0) {
        printk(KERN_ALERT "%s, dma request interrupted\n", __func__);
        ret = -EINTR;
        goto out;
    
    }

out:

    // release userpages
    while (mapped--){
        if (kaddr[mapped]){
            vunmap(kaddr[mapped]);
        }
        if (pages[mapped]){
            down_read(&current->mm->mmap_sem);
            unpin_user_pages(&pages[mapped], 1);
            up_read(&current->mm->mmap_sem);
        }
    }


    mutex_unlock(&pdata->io_lock);
    return ret;
}

static ssize_t secs_read(struct file *flip, char * __user buffer, size_t len, loff_t *offset)
{
    printk(KERN_INFO "%s %px %lu\n", __func__, buffer, len);
    return secs_do_dma(buffer, len, DMA_READ);

}
static ssize_t secs_write(struct file *flip, const char * __user buffer, size_t len, loff_t *offset) {
    printk(KERN_INFO "%s %px %lu\n", __func__, buffer, len);
    return secs_do_dma(buffer, len, DMA_WRITE);
}

static int secs_open(struct inode *inode, struct file *file) {
    printk(KERN_INFO "%s\n", __func__);
    return 0;
}

static int secs_release(struct inode *inode, struct file *file) {
    printk(KERN_INFO "%s\n", __func__);
    return 0;
}

static struct file_operations sec_ops = {
 .read = secs_read,
 .write = secs_write,
 .open = secs_open,
 .release = secs_release
};

static int secs_init(void) { 
    majorNum = register_chrdev(0, DEVICE_NAME, &sec_ops);
    if (majorNum < 0) {
        printk(KERN_ALERT "Failed to register %s, major %d\n", DEVICE_NAME, majorNum);
        return majorNum;
    }
    printk(KERN_INFO "Registered %s, major %d\n", DEVICE_NAME, majorNum);

    return 0; 
}

static void __exit secs_exit(void) { 
    unregister_chrdev(majorNum, DEVICE_NAME);
    printk(KERN_INFO "Bye from %s\n", DEVICE_NAME);
}


irqreturn_t pl666_irq_handler(int irq, void *dev_h){
    struct pl666_data* pd = (struct pl666_data*)dev_h;
    unsigned cause = readl(pd->dma_base + PL666_RD_IT_VAL);
    
    printk(KERN_INFO "Transaction result %x\n", readl(pd->dma_base + PL666_RD_TEST));

    if (!cause){
        return IRQ_NONE;
    }

    // clear IRQ
    writel(cause, pd->dma_base + PL666_WR_IT_CLR);

    // signal that the dma trz is completed
    pd->dma_done = 1;
    wake_up_interruptible(&pd->dma_wait);

    return IRQ_HANDLED;
}


static int pl666_probe(struct platform_device* pdev) {
	struct device *dev = &pdev->dev;
    //struct pl666_data* pdata;
    struct resource* res;
    int irq, ret;

    printk(KERN_INFO "pl666 secure storage dma probe\n");

	pdata = devm_kzalloc(dev, sizeof(struct pl666_data), GFP_KERNEL);
	if (!pdata) {
		printk(KERN_ALERT "pl666 alloc fail\n");
		return -ENOMEM;
	}
    printk(KERN_INFO "vmmod %lx\n", (unsigned long)&pdata);

    irq = platform_get_irq(pdev, 0);
    ret = devm_request_irq(dev, irq, pl666_irq_handler, 0, NULL, pdata);
    if (ret < 0){
		printk(KERN_ALERT "pl666 request IRQ fail\n");
        return ret;
    }
    
    res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
    pdata->dma_base = devm_ioremap_resource(dev, res);
    if (IS_ERR(pdata->dma_base)){
		printk(KERN_ALERT "pl666 ioremap fail\n");
        return PTR_ERR(pdata->dma_base);
    }

    init_waitqueue_head(&pdata->dma_wait);
    mutex_init(&pdata->io_lock);

    secs_init();
    return 0;
}

static void pl666_shutdown(struct platform_device* pdev) {
    printk(KERN_INFO "pl666 secure storage dma shutdown\n");
    secs_exit();
}

static const struct of_device_id sec_dev_match[] = {
	{ .compatible = "gym,pl666", },
	{},
};
MODULE_DEVICE_TABLE(of, sec_dev_match);

static struct platform_driver pl666_driver = {
	.probe = pl666_probe,
	.shutdown = pl666_shutdown,
	.driver = {
		.name = "pl666",
		.owner = THIS_MODULE,
		.suppress_bind_attrs = true,
		.of_match_table = of_match_ptr(sec_dev_match),
	},
};

module_platform_driver(pl666_driver);
