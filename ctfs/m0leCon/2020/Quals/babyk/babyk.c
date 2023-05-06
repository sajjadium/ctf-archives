#include <linux/module.h>
#include <linux/moduleparam.h>
#include <linux/init.h>
#include <linux/kernel.h>   
#include <linux/proc_fs.h>
#include <asm/uaccess.h>
#define BUFSIZE  100

static int leetness=20;
module_param(leetness,int,0660);

static struct proc_dir_entry *ent;

static ssize_t babywrite(struct file *file, const char __user *ubuf, size_t count, loff_t *ppos) 
{
	int num, c, m;

	char buf[BUFSIZE];

	// if(*ppos > 0 || count > BUFSIZE)
		// return -EFAULT;

	if(raw_copy_from_user(buf, ubuf, count))
		return -EFAULT;

	num = sscanf(buf,"%d",&m);

	if(num != 1)
		return -EFAULT;

	leetness = m;

	c = strlen(buf);
	printk("LEETNESS SCORE: %d", leetness);

	*ppos = c;

	return c;
}

static ssize_t babyread(struct file *file, char __user *ubuf,size_t count, loff_t *ppos) 
{
	printk("READ NOT IMPLEMENTED YET");
	return 0;
}

static struct file_operations myops = 
{
	.owner = THIS_MODULE,
	.read = babyread,
	.write = babywrite,
};

static int baby_init(void)
{
	ent=proc_create("babydev",0660,NULL,&myops);
	printk(KERN_ALERT "Baby initialized!");
    return 0;
}

static void baby_cleanup(void)
{
	proc_remove(ent);
	printk(KERN_WARNING "BYE!");
}

module_init(baby_init);
module_exit(baby_cleanup);
