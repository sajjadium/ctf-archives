#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/miscdevice.h>
#include <linux/init.h>
#include <linux/slab.h>
#include <linux/fs.h>
#include <linux/list.h>
#include <linux/idr.h>
#include <asm/uaccess.h>

#define CSAW_IOCTL_BASE     0x77617363
#define CSAW_ALLOC_CHANNEL  CSAW_IOCTL_BASE+1
#define CSAW_OPEN_CHANNEL   CSAW_IOCTL_BASE+2
#define CSAW_GROW_CHANNEL   CSAW_IOCTL_BASE+3
#define CSAW_SHRINK_CHANNEL CSAW_IOCTL_BASE+4
#define CSAW_READ_CHANNEL   CSAW_IOCTL_BASE+5
#define CSAW_WRITE_CHANNEL  CSAW_IOCTL_BASE+6
#define CSAW_SEEK_CHANNEL   CSAW_IOCTL_BASE+7
#define CSAW_CLOSE_CHANNEL  CSAW_IOCTL_BASE+8

struct ipc_channel {
    struct kref ref;
    int id;
    char *data;
    size_t buf_size;
    loff_t index;
};

static struct idr ipc_idr;

struct ipc_state {
    struct ipc_channel *channel;
    struct mutex lock;
};

struct alloc_channel_args {
    size_t buf_size;
    int id;
};

struct open_channel_args {
    int id;
};

struct grow_channel_args {
    int id;
    size_t size;
};

struct shrink_channel_args {
    int id;
    size_t size;
};

struct read_channel_args {
    int id;
    char *buf;
    size_t count;
};

struct write_channel_args {
    int id;
    char *buf;
    size_t count;
};

struct seek_channel_args {
    int id;
    loff_t index;
    int whence;
};

struct close_channel_args {
    int id;
};

static void ipc_channel_get ( struct ipc_channel *channel )
{
    kref_get(&channel->ref);
}

static void ipc_channel_destroy ( struct kref *ref )
{
    struct ipc_channel *channel = container_of(ref, struct ipc_channel, ref);

    idr_remove(&ipc_idr, channel->id);

    kfree(channel->data);
    kfree(channel);
}

static void ipc_channel_put ( struct ipc_state *state, struct ipc_channel *channel )
{
    kref_put(&channel->ref, ipc_channel_destroy);
}

static int csaw_open ( struct inode *inode, struct file *file )
{
    struct ipc_state *state;

    state = kzalloc(sizeof(*state), GFP_KERNEL);
    if ( state == NULL )
        return -ENOMEM;

    mutex_init(&state->lock);

    file->private_data = state;

    return 0;
}

int alloc_new_ipc_channel ( size_t buf_size, struct ipc_channel **out_channel )
{
    int id;
    char *data;
    struct ipc_channel *channel;

    if ( ! buf_size )
        return -EINVAL;

    channel = kzalloc(sizeof(*channel), GFP_KERNEL);
    if ( channel == NULL )
        return -ENOMEM;

    data = kzalloc(buf_size, GFP_KERNEL);
    if ( data == NULL )
    {
        kfree(channel);
        return -ENOMEM;
    }

    kref_init(&channel->ref);

    channel->data = data;
    channel->buf_size = buf_size;

    id = idr_alloc(&ipc_idr, channel, 1, 0, GFP_KERNEL);
    if ( id < 0 )
    {
        kfree(data);
        kfree(channel);
        return id;
    }

    channel->id = id;
    *out_channel = channel;

    return 0;
}

static struct ipc_channel *get_channel_by_id ( struct ipc_state *state, int id )
{
    struct ipc_channel *channel;

    channel = idr_find(&ipc_idr, id);
    if ( channel )
        ipc_channel_get(channel);

    if ( channel )
        return channel;
    else
        return ERR_PTR(-EINVAL);
}

static int realloc_ipc_channel ( struct ipc_state *state, int id, size_t size, int grow )
{
    struct ipc_channel *channel;
    size_t new_size;
    char *new_data;

    channel = get_channel_by_id(state, id);
    if ( IS_ERR(channel) )
        return PTR_ERR(channel);

    if ( grow )
        new_size = channel->buf_size + size;
    else
        new_size = channel->buf_size - size;

    new_data = krealloc(channel->data, new_size + 1, GFP_KERNEL);
    if ( new_data == NULL )
        return -EINVAL;

    channel->data = new_data;
    channel->buf_size = new_size;

    ipc_channel_put(state, channel);

    return 0;
}

static ssize_t read_ipc_channel ( struct ipc_state *state, char __user *buf, size_t count )
{
    struct ipc_channel *channel;
    loff_t *pos;

    if ( ! state->channel )
        return -ENXIO;

    channel = state->channel;
    pos = &channel->index;

    if ( (count + *pos) > channel->buf_size )
        return -EINVAL;

    if ( copy_to_user(buf, channel->data + *pos, count) )
        return -EINVAL;

    return count;
}

static ssize_t write_ipc_channel ( struct ipc_state *state, const char __user *buf, size_t count )
{
    struct ipc_channel *channel;
    loff_t *pos;

    if ( ! state->channel )
        return -ENXIO;

    channel = state->channel;
    pos = &channel->index;

    if ( (count + *pos) > channel->buf_size )
        return -EINVAL;

    if ( strncpy_from_user(channel->data + *pos, buf, count) < 0 )
        return -EINVAL;

    return count;
}

static loff_t seek_ipc_channel ( struct ipc_state *state, loff_t offset, int whence )
{
    loff_t ret = -EINVAL;
    struct ipc_channel *channel = state->channel;

    if ( ! channel )
        return -ENXIO;

    switch ( whence )
    {
        case SEEK_SET:
            if ( offset < channel->buf_size )
            {
                channel->index = offset;
                ret = offset;
            }
            break;

        case SEEK_CUR:
            ret = channel->index;
            break;
    }

    return ret;
}

static int close_ipc_channel ( struct ipc_state *state, int id )
{
    struct ipc_channel *channel;

    channel = get_channel_by_id(state, id);
    if ( IS_ERR(channel) )
        return PTR_ERR(channel);

    if ( state->channel == channel )
    {
        state->channel = NULL;
        ipc_channel_put(state, channel);
    }

    ipc_channel_put(state, channel);

    return 0;
}

static long csaw_ioctl ( struct file *file, unsigned int cmd, unsigned long arg )
{
    long ret = 0;
    unsigned long *argp = (unsigned long *)arg;
    struct ipc_state *state = file->private_data;

    switch ( cmd )
    {
        case CSAW_ALLOC_CHANNEL:
        {
            struct alloc_channel_args alloc_channel;
            struct ipc_channel *channel;

            if ( copy_from_user(&alloc_channel, argp, sizeof(alloc_channel)) )
                return -EINVAL;

            mutex_lock(&state->lock);

            if ( state->channel )
            {
                ret = -EBUSY;
                goto RET_UNLOCK;
            }

            ret = alloc_new_ipc_channel(alloc_channel.buf_size, &channel);
            if ( ret < 0 )
                goto RET_UNLOCK;

            state->channel = channel;

            if ( ret < 0 )
                alloc_channel.id = 0;
            else
                alloc_channel.id = channel->id;

            if ( copy_to_user(argp, &alloc_channel, sizeof(alloc_channel)) )
            {
                close_ipc_channel(state, channel->id);
                ret = -EINVAL;
            }

            mutex_unlock(&state->lock);

            break;
        }

        case CSAW_OPEN_CHANNEL:
        {
            struct open_channel_args open_channel;
            struct ipc_channel *channel;

            if ( copy_from_user(&open_channel, argp, sizeof(open_channel)) )
                return -EINVAL;

            mutex_lock(&state->lock);

            if ( state->channel )
            {
                ret = -EBUSY;
                goto RET_UNLOCK;
            }

            channel = get_channel_by_id(state, open_channel.id);
            if ( IS_ERR(channel) )
            {
                ret = PTR_ERR(channel);
                goto RET_UNLOCK;
            }

            state->channel = channel;

            ipc_channel_put(state, channel);

            mutex_unlock(&state->lock);

            break;
        }

        case CSAW_GROW_CHANNEL:
        {
            struct grow_channel_args grow_channel;

            if ( copy_from_user(&grow_channel, argp, sizeof(grow_channel)) )
                return -EINVAL;

            mutex_lock(&state->lock);
            ret = realloc_ipc_channel(state, grow_channel.id, grow_channel.size, 1);
            mutex_unlock(&state->lock);

            break;
        }

        case CSAW_SHRINK_CHANNEL:
        {
            struct shrink_channel_args shrink_channel;

            if ( copy_from_user(&shrink_channel, argp, sizeof(shrink_channel)) )
                return -EINVAL;

            mutex_lock(&state->lock);
            ret = realloc_ipc_channel(state, shrink_channel.id, shrink_channel.size, 0);
            mutex_unlock(&state->lock);

            break;
        }

        case CSAW_READ_CHANNEL:
        {
            struct read_channel_args read_channel;

            if ( copy_from_user(&read_channel, argp, sizeof(read_channel)) )
                return -EINVAL;

            mutex_lock(&state->lock);
            ret = read_ipc_channel(state, read_channel.buf, read_channel.count);
            mutex_unlock(&state->lock);

            break;
        }

        case CSAW_WRITE_CHANNEL:
        {
            struct write_channel_args write_channel;

            if ( copy_from_user(&write_channel, argp, sizeof(write_channel)) )
                return -EINVAL;

            mutex_lock(&state->lock);
            ret = write_ipc_channel(state, write_channel.buf, write_channel.count);
            mutex_unlock(&state->lock);

            break;
        }

        case CSAW_SEEK_CHANNEL:
        {
            struct seek_channel_args seek_channel;

            if ( copy_from_user(&seek_channel, argp, sizeof(seek_channel)) )
                return -EINVAL;

            mutex_lock(&state->lock);
            ret = seek_ipc_channel(state, seek_channel.index, seek_channel.whence);
            mutex_unlock(&state->lock);

            break;
        }

        case CSAW_CLOSE_CHANNEL:
        {
            struct close_channel_args close_channel;

            if ( copy_from_user(&close_channel, argp, sizeof(close_channel)) )
                return -EINVAL;

            mutex_lock(&state->lock);
            ret = close_ipc_channel(state, close_channel.id);
            mutex_unlock(&state->lock);

            break;
        }
    }

    return ret;

RET_UNLOCK:
    mutex_unlock(&state->lock);
    return ret;
}

static int csaw_release ( struct inode *inode, struct file *file )
{
    struct ipc_state *state = file->private_data;

    if ( state->channel )
        ipc_channel_put(state, state->channel);

    kfree(state);

    return 0;
}

struct file_operations csaw_fops = {
    owner:          THIS_MODULE,
    open:           csaw_open,
    release:        csaw_release,
    unlocked_ioctl: csaw_ioctl,
};

static struct miscdevice csaw_miscdev = {
    name:   "csaw",
    fops:   &csaw_fops
};

static int __init init_csaw ( void )
{
    idr_init(&ipc_idr);

    misc_register(&csaw_miscdev);

    return 0;
}

static void __exit exit_csaw ( void )
{
    misc_deregister(&csaw_miscdev);

    idr_destroy(&ipc_idr);
}

module_init(init_csaw);
module_exit(exit_csaw);

MODULE_LICENSE("GPL");
