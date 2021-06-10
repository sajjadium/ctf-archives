#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/device.h>
#include <linux/mutex.h>
#include <linux/fs.h>
#include <linux/slab.h>
#include <linux/uaccess.h>

#define DEVICE_NAME "hashbrown"
#define CLASS_NAME  "hashbrown"

MODULE_AUTHOR("FizzBuzz101");
MODULE_DESCRIPTION("Here's a hashbrown for everyone!");
MODULE_LICENSE("GPL");

#define ADD_KEY 0x1337
#define DELETE_KEY 0x1338
#define UPDATE_VALUE 0x1339
#define DELETE_VALUE 0x133a
#define GET_VALUE 0x133b

#define SIZE_ARR_START 0x10
#define SIZE_ARR_MAX 0x200
#define MAX_ENTRIES 0x400
#define MAX_VALUE_SIZE 0xb0
#define GET_THRESHOLD(size) size - (size >> 2)

#define INVALID 1
#define EXISTS 2
#define NOT_EXISTS 3
#define MAXED 4

static DEFINE_MUTEX(operations_lock);
static DEFINE_MUTEX(resize_lock);
static long hashmap_ioctl(struct file *file, unsigned int cmd, unsigned long arg);

static int major;
static struct class *hashbrown_class  = NULL;
static struct device *hashbrown_device = NULL;
static struct file_operations hashbrown_fops = {.unlocked_ioctl = hashmap_ioctl};

typedef struct 
{
    uint32_t key;
    uint32_t size;
    char *src;
    char *dest;
}request_t;

struct hash_entry
{
    uint32_t key;
    uint32_t size;
    char *value;
    struct hash_entry *next;
};
typedef struct hash_entry hash_entry;

typedef struct
{
    uint32_t size;
    uint32_t threshold;
    uint32_t entry_count;
    hash_entry **buckets;
}hashmap_t;
hashmap_t hashmap;

static noinline uint32_t get_hash_idx(uint32_t key, uint32_t size);

static noinline long resize(request_t *arg);
static noinline void resize_add(uint32_t idx, hash_entry *entry, hash_entry **new_buckets);
static noinline void resize_clean_old(void);

static noinline long add_key(uint32_t idx, uint32_t key, uint32_t size, char *src);
static noinline long delete_key(uint32_t idx, uint32_t key);
static noinline long update_value(uint32_t idx, uint32_t key, uint32_t size, char *src);
static noinline long delete_value(uint32_t idx, uint32_t key);
static noinline long get_value(uint32_t idx, uint32_t key, uint32_t size, char *dest);

#pragma GCC push_options
#pragma GCC optimize ("O1")

static long hashmap_ioctl(struct file *file, unsigned int cmd, unsigned long arg)
{
    long result;
    request_t request;
    uint32_t idx;

    if (cmd == ADD_KEY) 
    {
        if (hashmap.entry_count == hashmap.threshold && hashmap.size < SIZE_ARR_MAX)
        {
            mutex_lock(&resize_lock);
            result = resize((request_t *)arg);
            mutex_unlock(&resize_lock);
            return result;
        }
    }

    mutex_lock(&operations_lock);
    if (copy_from_user((void *)&request, (void *)arg, sizeof(request_t)))
    {
        result = INVALID;
    }
    else if (cmd == ADD_KEY && hashmap.entry_count == MAX_ENTRIES)
    {
        result = MAXED;
    }
    else
    {
        idx = get_hash_idx(request.key, hashmap.size);
        switch(cmd)
        {
            case ADD_KEY:
                result = add_key(idx, request.key, request.size, request.src);
                break;
            case DELETE_KEY:
                result = delete_key(idx, request.key);
                break;
            case UPDATE_VALUE:
                result = update_value(idx, request.key, request.size, request.src);
                break;
            case DELETE_VALUE:
                result = delete_value(idx, request.key);
                break;
            case GET_VALUE:
                result = get_value(idx, request.key, request.size, request.dest);
                break;
            default:
                result = INVALID;
                break;
        }
    }
    mutex_unlock(&operations_lock);
    return result;
}

static uint32_t get_hash_idx(uint32_t key, uint32_t size)
{
    uint32_t hash;
    key ^= (key >> 20) ^ (key >> 12);
    hash = key ^ (key >> 7) ^ (key >> 4);
    return hash & (size - 1);
}

static noinline void resize_add(uint32_t idx, hash_entry *entry, hash_entry **new_buckets)
{
    if (!new_buckets[idx])
    {
        new_buckets[idx] = entry;
    }
    else
    {
        entry->next = new_buckets[idx];
        new_buckets[idx] = entry;
    }
}

static noinline void resize_clean_old()
{
    int i;
    hash_entry *traverse, *temp;    
    for (i = 0; i < hashmap.size; i++)
    {
        if (hashmap.buckets[i])
        {
            traverse = hashmap.buckets[i];
            while (traverse)
            {
                temp = traverse;
                traverse = traverse->next;
                kfree(temp);
            }
            hashmap.buckets[i] = NULL;
        }
    }   
    kfree(hashmap.buckets);
    hashmap.buckets = NULL;
    return;
}

static long resize(request_t *arg)
{
    hash_entry **new_buckets, *temp_entry, *temp;
    request_t request;
    char *temp_data;
    uint32_t new_size, new_threshold, new_idx;
    int i, duplicate;

    if (copy_from_user((void *)&request, (void *)arg, sizeof(request_t)))
    {
        return INVALID;
    }
    if (request.size < 1 || request.size > MAX_VALUE_SIZE)
    {
        return INVALID;
    }

    new_size = hashmap.size * 2;
    new_threshold = GET_THRESHOLD(new_size);
    new_buckets = kzalloc(sizeof(hash_entry *) * new_size, GFP_KERNEL);

    if (!new_buckets)
    {
        return INVALID;
    }

    duplicate = 0;
    for (i = 0; i < hashmap.size; i++)
    {
        if (hashmap.buckets[i])
        {
            for (temp_entry = hashmap.buckets[i]; temp_entry != NULL; temp_entry = temp_entry->next)
            {
                if (temp_entry->key == request.key)
                {
                    duplicate = 1;
                }
                new_idx = get_hash_idx(temp_entry->key, new_size);
                temp = kzalloc(sizeof(hash_entry), GFP_KERNEL);
                if (!temp) 
                {
                    kfree(new_buckets);
                    return INVALID;
                }
                temp->key = temp_entry->key;
                temp->size = temp_entry->size;
                temp->value = temp_entry->value;
                resize_add(new_idx, temp, new_buckets);
            }
        }
    }
    if (!duplicate)
    {
        new_idx = get_hash_idx(request.key, new_size);
        temp = kzalloc(sizeof(hash_entry), GFP_KERNEL);
        if (!temp)
        {
            kfree(new_buckets);
            return INVALID;
        }
        temp_data = kzalloc(request.size, GFP_KERNEL);
        if (!temp_data)
        {
            kfree(temp);
            kfree(new_buckets);
            return INVALID;
        }
        if (copy_from_user(temp_data, request.src, request.size))
        {
            kfree(temp_data);
            kfree(temp);
            kfree(new_buckets);
            return INVALID;
        }
        temp->size = request.size;
        temp->value = temp_data;
        temp->key = request.key;
        temp->next = NULL;
        resize_add(new_idx, temp, new_buckets);
        hashmap.entry_count++;
    }
    resize_clean_old();
    hashmap.size = new_size;
    hashmap.threshold = new_threshold;
    hashmap.buckets = new_buckets;
    return (duplicate)?EXISTS:0;
}

static long add_key(uint32_t idx, uint32_t key, uint32_t size, char *src)
{
    hash_entry *temp_entry, *temp;
    char *temp_data;
    if (size < 1 || size > MAX_VALUE_SIZE)
    {
        return INVALID;
    }

    temp_entry = kzalloc(sizeof(hash_entry), GFP_KERNEL);
    temp_data = kzalloc(size, GFP_KERNEL);
    if (!temp_entry || !temp_data)
    {
        return INVALID;
    }
    if (copy_from_user(temp_data, src, size))
    {
        return INVALID;
    }
    temp_entry->key = key;
    temp_entry->size = size;
    temp_entry->value = temp_data;
    temp_entry->next = NULL;

    if (!hashmap.buckets[idx])
    {
        hashmap.buckets[idx] = temp_entry;
        hashmap.entry_count++;
        return 0;
    }
    else 
    {
        for (temp = hashmap.buckets[idx]; temp->next != NULL; temp = temp->next)
        {
            if (temp->key == key)
            {
                kfree(temp_data);
                kfree(temp_entry);
                return EXISTS;
            }
        }
        if (temp->key == key)
        {
            kfree(temp_data);
            kfree(temp_entry);
            return EXISTS;
        }
        temp->next = temp_entry;
        hashmap.entry_count++;
        return 0;
    }
}

static long delete_key(uint32_t idx, uint32_t key)
{
    hash_entry *temp, *prev;

    if (!hashmap.buckets[idx])
    {
        return NOT_EXISTS;
    }
    if (hashmap.buckets[idx]->key == key)
    {
        temp = hashmap.buckets[idx]->next;
        if (hashmap.buckets[idx]->value)
        {
            kfree(hashmap.buckets[idx]->value);
        }
        kfree(hashmap.buckets[idx]);
        hashmap.buckets[idx] = temp;
        hashmap.entry_count--;
        return 0;
    }
    temp = hashmap.buckets[idx];
    while (temp != NULL && temp->key != key)
    {
        prev = temp;
        temp = temp->next;
    }
    if (temp == NULL)
    {
        return NOT_EXISTS;
    }
    prev->next = temp->next;
    if (temp->value)
    {
        kfree(temp->value);
    }
    kfree(temp);
    hashmap.entry_count--;
    return 0;
}

static long update_value(uint32_t idx, uint32_t key, uint32_t size, char *src)
{
    hash_entry *temp;
    char *temp_data;

    if (size < 1 || size > MAX_VALUE_SIZE)
    {
        return INVALID;
    }
    if (!hashmap.buckets[idx])
    {
        return NOT_EXISTS;
    }

    for (temp = hashmap.buckets[idx]; temp != NULL; temp = temp->next)
    {
        if (temp->key == key)
        {
            if (temp->size != size)
            {
                if (temp->value)
                {
                    kfree(temp->value);
                }
                temp->value = NULL;
                temp->size = 0;
                temp_data = kzalloc(size, GFP_KERNEL);
                if (!temp_data || copy_from_user(temp_data, src, size))
                {
                    return INVALID;
                }
                temp->size = size;
                temp->value = temp_data;
            }
            else
            {
                if (copy_from_user(temp->value, src, size))
                {
                    return INVALID;
                }
            }
            return 0;
        }
    }
    return NOT_EXISTS;
}

static long delete_value(uint32_t idx, uint32_t key)
{
    hash_entry *temp;
    if (!hashmap.buckets[idx])
    {
        return NOT_EXISTS;
    }
    for (temp = hashmap.buckets[idx]; temp != NULL; temp = temp->next)
    {
        if (temp->key == key)
        {
            if (!temp->value || !temp->size)
            {
                return NOT_EXISTS;
            }
            kfree(temp->value);
            temp->value = NULL;
            temp->size = 0;
            return 0;
        }
    }
    return NOT_EXISTS;
}

static long get_value(uint32_t idx, uint32_t key, uint32_t size, char *dest)
{
    hash_entry *temp;
    if (!hashmap.buckets[idx])
    {
        return NOT_EXISTS;
    }
    for (temp = hashmap.buckets[idx]; temp != NULL; temp = temp->next)
    {
        if (temp->key == key)
        {
            if (!temp->value || !temp->size)
            {
                return NOT_EXISTS;
            }
            if (size > temp->size)
            {  
                return INVALID;
            }
            if (copy_to_user(dest, temp->value, size))
            {
                return INVALID;
            }
            return 0;
        }
    }
    return NOT_EXISTS;
}

#pragma GCC pop_options

static int __init init_hashbrown(void)
{
    major = register_chrdev(0, DEVICE_NAME, &hashbrown_fops);
    if (major < 0)
    {
        return -1;
    }
    hashbrown_class = class_create(THIS_MODULE, CLASS_NAME);
    if (IS_ERR(hashbrown_class))
    {
        unregister_chrdev(major, DEVICE_NAME);
        return -1;
    }
    hashbrown_device = device_create(hashbrown_class, 0, MKDEV(major, 0), 0, DEVICE_NAME);
    if (IS_ERR(hashbrown_device))
    {
        class_destroy(hashbrown_class);
        unregister_chrdev(major, DEVICE_NAME);
        return -1;
    }
    mutex_init(&operations_lock);
    mutex_init(&resize_lock);

    hashmap.size = SIZE_ARR_START;
    hashmap.entry_count = 0;
    hashmap.threshold = GET_THRESHOLD(hashmap.size);
    hashmap.buckets = kzalloc(sizeof(hash_entry *) * hashmap.size, GFP_KERNEL);
    printk(KERN_INFO "HashBrown Loaded! Who doesn't love Hashbrowns!\n");
    return 0;
}

static void __exit exit_hashbrown(void)
{
    device_destroy(hashbrown_class, MKDEV(major, 0));
    class_unregister(hashbrown_class);
    class_destroy(hashbrown_class);
    unregister_chrdev(major, DEVICE_NAME);
    mutex_destroy(&operations_lock);
    mutex_destroy(&resize_lock);
    printk(KERN_INFO "HashBrown Unloaded\n");
}

module_init(init_hashbrown);
module_exit(exit_hashbrown);