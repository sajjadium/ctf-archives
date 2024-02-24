#include "linux/random.h"
#include "palindromatic_util.c"

char *temp_buffer;
unsigned long magic;
queue_t incoming_queue;
queue_t outgoing_queue;
bool sanitized = false;

/*
 Copy request from user and add to start of queue
*/
static noinline long pm_add_request(arg_t *arg)
{
    long idx = -1;
    request_t *req = kmem_cache_zalloc(pm_cache, GFP_KERNEL);
    if(!req) goto end;

    req->type = RAW;
    req->magic = magic;
    if(copy_from_user(req->str, arg->buffer, STRING_SZ))
    {
        kfree(req);
        goto end;
    }
    idx = pm_queue_enqueue(&incoming_queue, req);
    
end:
    return idx;
}

/*
 Accept characters only in [A-Z|a-z] and translate to [A-Z]
 Only 1 sanitize is allowed
*/
static noinline long pm_sanitize_request(void)
{
    long idx = -1;

    request_t *req = pm_queue_peek(&incoming_queue);
    if(!req) goto end;
    if(req->type == SANITIZED) goto end;

    memset(temp_buffer, 0x0, STRING_SZ);

    int ptr = 0;
    for(int i = 0; i < STRING_SZ; i++)
    {
        if(!req->str[i]) break;

        if(req->str[i] > 0x60 && req->str[i] < 0x7b)
            temp_buffer[ptr++] = req->str[i]-0x20;

        else if(req->str[i] > 0x40 && req->str[i] < 0x5b)
            temp_buffer[ptr++] = req->str[i];

        else continue;
    }

    temp_buffer[ptr] = 0;
    strcpy(req->sanstr, temp_buffer);
    req->type = SANITIZED;

    idx = pm_queue_enqueue(&incoming_queue, pm_queue_dequeue(&incoming_queue));

end:
    return idx;
}

/*
 If request is raw, remove it
 else, set it to raw and send it back to start of the queue
*/
static noinline long pm_reset_request(void)
{
    request_t *req = pm_queue_dequeue(&incoming_queue);
    if(!req) return -1;

    if(req->type != RAW)
    {
        req->type = RAW;
        memset(req->sanstr, 0x0, sizeof(req->sanstr));
        pm_queue_enqueue(&incoming_queue, req);
    }

    else
    {
        kfree(req);
    }
    return 0;
}

/*
 Check if it is a palindrome or not and set type accordingly
 Remove from incoming queue and add to outgoing queue
*/
static noinline long pm_process_request(void)
{
    long idx = -1;

    request_t *req = pm_queue_peek(&incoming_queue);
    if(!req) goto end;
    if(req->magic != magic) goto end;
    int len = req->type==SANITIZED?strlen(req->sanstr):strlen(req->str);
    if(!len) goto end;
    idx = pm_queue_enqueue(&outgoing_queue, req);
    if(idx < 0) goto end;

    memset(temp_buffer, 0x0, STRING_SZ);
    if(req->type == RAW)
    {
        for(int i = (len/2)-1; i > -1; i--)
        {
            if(req->str[i] < 0x41 || req->str[i] > 0x5a) break;
            temp_buffer[i] = req->str[i];
        }
        temp_buffer[len/2] = 0;
        
        if(strcmp(temp_buffer, &req->str[len/2]+len%2)) req->type = NONPALINDROME;
        else req->type = PALINDROME;
        pm_queue_dequeue(&incoming_queue);
    }

    if(req->type == SANITIZED)
    {
        for(int i = (len/2)-1; i > -1; i--) temp_buffer[i] = req->sanstr[i];
        temp_buffer[len/2] = 0;

        if(strcmp(temp_buffer, &req->sanstr[len/2]+len%2)) req->type = NONPALINDROME;
        else req->type = PALINDROME;
        pm_queue_dequeue(&incoming_queue);
    } 

end:
    return idx;
}

/*
 Get result of first request in outgoing queue
*/
static noinline long pm_reap_request(void)
{
    request_t *req = pm_queue_dequeue(&outgoing_queue);
    if(!req) return -1;
    if(req->magic != magic) return -1;
    
    long ret = req->type==PALINDROME?1:0;
    kfree(req);

    return ret;
}

/*
 Get the available slots in both queues
*/
static noinline long pm_query_capacity(void)
{
    long ret = (QUEUE_SZ-pm_queue_count(&outgoing_queue))<<16 
                | (QUEUE_SZ-pm_queue_count(&incoming_queue));
    return ret;
}


static long pm_ioctl(struct file *file, unsigned int cmd, unsigned long uarg)
{   
    arg_t arg;
    long ret = -1;
    mutex_lock(&lock);

    switch(cmd)
    {
        case QUEUE:
            if(copy_from_user(&arg, (void *)uarg, sizeof(arg_t))) goto end;
            ret = pm_add_request(&arg);
            break;

        case SANITIZE:
            if(sanitized) goto end;
            sanitized = true;
            ret = pm_sanitize_request();
            break;

        case RESET:
            ret = pm_reset_request();
            break;

        case PROCESS:
            ret = pm_process_request();
            break;

        case REAP:
            ret = pm_reap_request();
            break;

        case QUERY:
            ret = pm_query_capacity();
            break;

        default:
            goto end;
    }

end:
    mutex_unlock(&lock);
    return ret;
}


static int __init init_palindromatic(void)
{
    if(misc_register(&pm_device) < 0) goto err;

    pm_cache = kmem_cache_create("palindromatic", TARGET_SZ, __alignof__(request_t), 
                            SLAB_ACCOUNT | SLAB_PANIC | SLAB_HWCACHE_ALIGN | SLAB_NO_MERGE, NULL);
    if(!pm_cache) goto err; 

    temp_buffer = kzalloc(TARGET_SZ, GFP_KERNEL);
    if(!temp_buffer) goto err;

    get_random_bytes(&magic, sizeof(magic));
    pm_queue_init(&incoming_queue);
    pm_queue_init(&outgoing_queue);

    return 0;

err:
    if(pm_cache) kmem_cache_destroy(pm_cache);
    printk(KERN_ALERT "[-] Failed to register pipeparty");
    return -1;
}


static void __exit exit_palindromatic(void)
{
    kfree(temp_buffer);
    kmem_cache_destroy(pm_cache);
    misc_deregister(&pm_device);
}

module_init(init_palindromatic);
module_exit(exit_palindromatic);