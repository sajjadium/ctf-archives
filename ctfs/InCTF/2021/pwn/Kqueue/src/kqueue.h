/* Generic header files */

#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/device.h>
#include <linux/mutex.h>
#include <linux/fs.h>
#include <linux/slab.h>
#include <linux/uaccess.h>
#include <linux/miscdevice.h>

MODULE_AUTHOR("amritabi0s1@gmail.com");                        
MODULE_DESCRIPTION("A module to save all your beloved queues");
MODULE_LICENSE("GPL");                                         
                                                            

#define CREATE_KQUEUE 0xDEADC0DE
#define EDIT_KQUEUE   0xDAADEEEE
#define DELETE_KQUEUE 0xBADDCAFE
#define SAVE          0xB105BABE


#define INVALID      -1
#define NOT_EXISTS   -3
#define MAX_QUEUES    5
#define MAX_DATA_SIZE 0x20

typedef unsigned long long ull;
ull queueCount = 0;

/* We need this to mitigate rat races */

static DEFINE_MUTEX(operations_lock);

static int reg;
static long kqueue_ioctl(struct file *file, unsigned int cmd, unsigned long arg);
static struct file_operations kqueue_fops = {.unlocked_ioctl = kqueue_ioctl};

/* Sometimes , waiting in a queue is so boring, but wait , this isn't any ordinary queue */

typedef struct{
    uint16_t data_size;
    uint64_t queue_size; /* This needs to handle larger numbers */
    uint32_t max_entries;
    uint16_t idx;
    char* data;
}queue;

/* Every kqueue has it's own entries */

typedef struct queue_entry queue_entry;

struct queue_entry{
    uint16_t idx;
    char *data;
    queue_entry *next;
};

/* I wish I could go limitless */

queue *kqueues[MAX_QUEUES] = {(queue *)NULL};

/* Boolean array to make sure you dont save queue's over and over again */

bool isSaved[MAX_QUEUES] = {false};


/* This is how a typical request looks */

typedef struct{
    uint32_t max_entries;
    uint16_t data_size;
    uint16_t entry_idx;
    uint16_t queue_idx;
    char* data;
}request_t;

/* commiting errors is not a crime, handling them incorrectly is */

static long err(char* msg){
    printk(KERN_ALERT "%s\n",msg);
    return -1;
}

static noinline long create_kqueue(request_t request);
static noinline long delete_kqueue(request_t request);
static noinline long edit_kqueue(request_t request);
static noinline long save_kqueue_entries(request_t request);

/* Initialize a flag to check for existence of stuff */
bool exists = false;

/* For Validating pointers */
static noinline void* validate(void *ptr){
    if(!ptr){
        mutex_unlock(&operations_lock);
        err("[-] oops! Internal operation error");
    }
    return ptr;
}

struct miscdevice kqueue_device = {
    .minor = MISC_DYNAMIC_MINOR,
    .name = "kqueue",
    .fops = &kqueue_fops,
};


