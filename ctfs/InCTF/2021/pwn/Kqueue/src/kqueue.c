/* Generic header files */

#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/device.h>
#include <linux/mutex.h>
#include <linux/fs.h>
#include <linux/slab.h>
#include <linux/uaccess.h>
#include "kqueue.h"

#pragma GCC push_options
#pragma GCC optimize ("O1")

static noinline long kqueue_ioctl(struct file *file, unsigned int cmd, unsigned long arg){

    long result;

    request_t request;
    
    mutex_lock(&operations_lock);

    if (copy_from_user((void *)&request, (void *)arg, sizeof(request_t))){
        err("[-] copy_from_user failed");
        goto ret;
    }

    switch(cmd){
        case CREATE_KQUEUE:
            result = create_kqueue(request);
            break;
        case DELETE_KQUEUE:
            result = delete_kqueue(request);
            break;
        case EDIT_KQUEUE:
            result = edit_kqueue(request);
            break;
        case SAVE:
            result = save_kqueue_entries(request);
            break;
        default:
            result = INVALID;
            break;
    }
ret: 
    mutex_unlock(&operations_lock);
    return result;
}


static noinline long create_kqueue(request_t request){
    long result = INVALID;

    if(queueCount > MAX_QUEUES)
        err("[-] Max queue count reached");

    /* You can't ask for 0 queues , how meaningless */
    if(request.max_entries<1)
        err("[-] kqueue entries should be greater than 0");

    /* Asking for too much is also not good */
    if(request.data_size>MAX_DATA_SIZE)
        err("[-] kqueue data size exceed");

    /* Initialize kqueue_entry structure */
    queue_entry *kqueue_entry;

    /* Check if multiplication of 2 64 bit integers results in overflow */
    ull space = 0;
    if(__builtin_umulll_overflow(sizeof(queue_entry),(request.max_entries+1),&space) == true)
        err("[-] Integer overflow");

    /* Size is the size of queue structure + size of entry * request entries */
    ull queue_size = 0;
    if(__builtin_saddll_overflow(sizeof(queue),space,&queue_size) == true)
        err("[-] Integer overflow");

    /* Total size should not exceed a certain limit */
    if(queue_size>sizeof(queue) + 0x10000)
        err("[-] Max kqueue alloc limit reached");

    /* All checks done , now call kmalloc */
    queue *queue = validate((char *)kmalloc(queue_size,GFP_KERNEL));

    /* Main queue can also store data */
    queue->data = validate((char *)kmalloc(request.data_size,GFP_KERNEL));

    /* Fill the remaining queue structure */
    queue->data_size   = request.data_size;
    queue->max_entries = request.max_entries;
    queue->queue_size  = queue_size;

    /* Get to the place from where memory has to be handled */
    kqueue_entry = (queue_entry *)((uint64_t)(queue + (sizeof(queue)+1)/8));

    /* Allocate all kqueue entries */
    queue_entry* current_entry = kqueue_entry;
    queue_entry* prev_entry = current_entry;

    uint32_t i=1;
    for(i=1;i<request.max_entries+1;i++){
        if(i!=request.max_entries)
            prev_entry->next = NULL;
        current_entry->idx = i;
        current_entry->data = (char *)(validate((char *)kmalloc(request.data_size,GFP_KERNEL)));

        /* Increment current_entry by size of queue_entry */
        current_entry += sizeof(queue_entry)/16;

        /* Populate next pointer of the previous entry */
        prev_entry->next = current_entry;
        prev_entry = prev_entry->next;
    }

    /* Find an appropriate slot in kqueues */
    uint32_t j = 0;
    for(j=0;j<MAX_QUEUES;j++){
        if(kqueues[j] == NULL)
            break;
    }

    if(j>MAX_QUEUES)
        err("[-] No kqueue slot left");

    /* Assign the newly created kqueue to the kqueues */
    kqueues[j] = queue;
    queueCount++;
    result = 0;
    return result;
}

static noinline long delete_kqueue(request_t request){
    /* Check for out of bounds requests */
    if(request.queue_idx>MAX_QUEUES)
        err("[-] Invalid idx");

    /* Check for existence of the request kqueue */
    queue *queue = kqueues[request.queue_idx];
    if(!queue)
        err("[-] Requested kqueue does not exist");
    
    memset(queue,0,queue->queue_size);
    kfree(queue);
    kqueues[request.queue_idx] = NULL;
    return 0;
}

static noinline long edit_kqueue(request_t request){
    /* Check the idx of the kqueue */
    if(request.queue_idx > MAX_QUEUES)
        err("[-] Invalid kqueue idx");

    /* Check if the kqueue exists at that idx */
    queue *queue = kqueues[request.queue_idx];
    if(!queue)
        err("[-] kqueue does not exist");

    /* Check the idx of the kqueue entry */
    if(request.entry_idx > queue->max_entries)
        err("[-] Invalid kqueue entry_idx");

    /* Get to the kqueue entry memory */
    queue_entry *kqueue_entry = (queue_entry *)(queue + (sizeof(queue)+1)/8);

    /* Check for the existence of the kqueue entry */
    exists = false;
    uint32_t i=1;
    for(i=1;i<queue->max_entries+1;i++){
        
        /* If kqueue entry found , do the necessary */
        if(kqueue_entry && request.data && queue->data_size){
            if(kqueue_entry->idx == request.entry_idx){
                validate(memcpy(kqueue_entry->data,request.data,queue->data_size));
                exists = true;
            }
        }
        kqueue_entry = kqueue_entry->next;
    }

    /* What if the idx is 0, it means we have to update the main kqueue's data */
    if(request.entry_idx==0 && kqueue_entry && request.data && queue->data_size){
        validate(memcpy(queue->data,request.data,queue->data_size));
        return 0;
    }

    if(!exists)
        return NOT_EXISTS;
    return 0;
} 

/* Now you have the option to safely preserve your precious kqueues */
static noinline long save_kqueue_entries(request_t request){

    /* Check for out of bounds queue_idx requests */
    if(request.queue_idx > MAX_QUEUES)
        err("[-] Invalid kqueue idx");

    /* Check if queue is already saved or not */
    if(isSaved[request.queue_idx]==true)
        err("[-] Queue already saved");

    queue *queue = validate(kqueues[request.queue_idx]);

    /* Check if number of requested entries exceed the existing entries */
    if(request.max_entries < 1 || request.max_entries > queue->max_entries)
        err("[-] Invalid entry count");

    /* Allocate memory for the kqueue to be saved */
    char *new_queue = validate((char *)kzalloc(queue->queue_size,GFP_KERNEL));

    /* Each saved entry can have its own size */
    if(request.data_size > queue->queue_size)
        err("[-] Entry size limit exceed");

    /* Copy main's queue's data */
    if(queue->data && request.data_size)
        validate(memcpy(new_queue,queue->data,request.data_size));
    else
        err("[-] Internal error");
    new_queue += queue->data_size;

    /* Get to the entries of the kqueue */
    queue_entry *kqueue_entry = (queue_entry *)(queue + (sizeof(queue)+1)/8);

    /* copy all possible kqueue entries */
    uint32_t i=0;
    for(i=1;i<request.max_entries+1;i++){
        if(!kqueue_entry || !kqueue_entry->data)
            break;
        if(kqueue_entry->data && request.data_size)
            validate(memcpy(new_queue,kqueue_entry->data,request.data_size));
        else
            err("[-] Internal error");
        kqueue_entry = kqueue_entry->next;
        new_queue += queue->data_size;
    }

    /* Mark the queue as saved */
    isSaved[request.queue_idx] = true;
    return 0;
}

#pragma GCC pop_options

static int __init init_kqueue(void){
    mutex_init(&operations_lock);
    reg = misc_register(&kqueue_device);
    if(reg < 0){
        mutex_destroy(&operations_lock);
        err("[-] Failed to register kqueue");
    }
    return 0;
}


static void __exit exit_kqueue(void){
    misc_deregister(&kqueue_device);
}

module_init(init_kqueue);
module_exit(exit_kqueue);
