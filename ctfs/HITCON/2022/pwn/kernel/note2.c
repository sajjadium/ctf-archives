#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/fs.h>
#include <linux/slab.h>
#include <linux/uaccess.h>
#include <linux/miscdevice.h>
#include <linux/ioctl.h>
#include <linux/random.h>

#define IOC_MAGIC '\xFF'

#define IO_ADD     _IOWR(IOC_MAGIC, 0, struct ioctl_arg)
#define IO_EDIT    _IOWR(IOC_MAGIC, 1, struct ioctl_arg)
#define IO_SHOW    _IOWR(IOC_MAGIC, 2, struct ioctl_arg) 
#define IO_DEL	   _IOWR(IOC_MAGIC, 3, struct ioctl_arg) 

struct ioctl_arg
{
	uint64_t idx;
	uint64_t size;
	uint64_t addr;
};

struct node
{
	uint64_t key;
	uint64_t size;
	uint64_t addr;
};

static struct node *table[0x10];
static int drv_open(struct inode *inode, struct file *filp);
static long drv_unlocked_ioctl(struct file *filp, unsigned int cmd, unsigned long arg);


static struct file_operations drv_fops = {
	open : drv_open,
	unlocked_ioctl : drv_unlocked_ioctl
};


static struct miscdevice note_miscdev = {
    .minor      = 11,
    .name       = "note2",
    .fops       = &drv_fops,
    .mode	= 0666,
};

static int drv_open(struct inode *inode, struct file *filp){
	return 0;
}


static long drv_unlocked_ioctl(struct file *filp, unsigned int cmd, unsigned long arg){
    int ret = 0;
    int i = 0;
    uint64_t buf[0x200/8];
    uint64_t addr = 0;
    uint64_t size = 0;
    struct ioctl_arg data;
    
    memset(&data, 0, sizeof(data));
    memset(buf,0,sizeof(buf));

    if (copy_from_user(&data, (struct ioctl_arg __user *)arg, sizeof(data))){
		ret = -EFAULT;
		goto done;
    }

    data.idx &=0xf;
    data.size &=0x1ff;

    switch (cmd){
		case IO_ADD:
			{
				data.idx = -1;
				for(i=0;i<0x10;i++){
					if( !table[i] ){
						data.idx = i;
						break;
					}
				}

				if( data.idx == -1){
					ret = -ENOMEM;
					goto done;
				}
				table[data.idx] = (struct node*)kzalloc(sizeof(struct node),GFP_KERNEL);
				table[data.idx]->size = data.size;
				get_random_bytes(&table[data.idx]->key,sizeof(table[data.idx]->key));
				addr = (uint64_t)kzalloc(data.size,GFP_KERNEL);
				ret = copy_from_user(buf, (void __user *)data.addr, data.size);
				for(i=0;i*8 < data.size; i++)
					buf[i]^= table[data.idx]->key;
				memcpy((void*)addr,(void*)buf,data.size);
				table[data.idx]->addr =  addr ^ table[data.idx]->key;
			}
			break;
		case IO_EDIT:
			{
				if( table[data.idx] ){
					addr = table[data.idx]->addr ^ table[data.idx]->key;
					size = table[data.idx]->size & 0x1ff;
					ret = copy_from_user(buf, (void __user *)data.addr, size);
					for(i=0; i*8 < size; i++)
						buf[i]^= table[data.idx]->key;
					memcpy((void*)addr,buf,size);
				}
			}
			break;
		case IO_SHOW:
			{	
				if( table[data.idx] ){
					addr = table[data.idx]->addr ^ table[data.idx]->key;
					size = table[data.idx]->size & 0x1ff;
					memcpy(buf,(void*)addr,size);
					for(i=0;i*8 < size; i++)
						buf[i]^= table[data.idx]->key;
					ret = copy_to_user((void __user *)data.addr, buf, size);
				}
			}	
			break;
		case IO_DEL:
			{
				if( table[data.idx] ){
					addr = table[data.idx]->addr ^ table[data.idx]->key;
					kfree((void*)addr);
					kfree(table[data.idx]);
					table[data.idx] = 0;
				}
			}
			break;
		default:
			ret = -ENOTTY;
			break;
	}	
    done:
        return ret;
}


static int note_init(void){
	return misc_register(&note_miscdev);
}

static void note_exit(void){
	 misc_deregister(&note_miscdev);
}

module_init(note_init);
module_exit(note_exit);

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Secret Note v2");
