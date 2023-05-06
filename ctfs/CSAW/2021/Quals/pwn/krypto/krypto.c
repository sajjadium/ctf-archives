#include <linux/init.h>
#include <linux/module.h>
#include <linux/miscdevice.h>
#include <linux/fs.h>
#include <crypto/rng.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Nick Gregory");
MODULE_DESCRIPTION("/dev/krypto");
MODULE_VERSION("0.1");

#define KRYPTO_RNG_CMD 0x1337

struct rng_params {
    char *buf;
    size_t buf_len;
};

static int krypto_open(struct inode *inode, struct file *file)
{
    struct crypto_rng *rng = NULL;

    rng = crypto_alloc_rng("ansi_cprng", 0, 0);
    if (IS_ERR(rng)) {
        return -ENOMEM;
    }

    // fun fact! the kernel docs don't include this so the example doesn't actually work!
    char seed[32] = {0};
    crypto_rng_reset(rng, seed, sizeof(seed));

    file->private_data = rng;

    return 0;
}

static int krypto_rng(struct file *file, struct rng_params *params)
{
    char *kbuf = NULL;
    int ret = 0;
    size_t len = params->buf_len;

    if (len == 0 || len > 0x1000) {
        return -EINVAL;
    }

    kbuf = kzalloc(len, GFP_KERNEL);
    if (!kbuf) {
        return -ENOMEM;
    }

    ret = crypto_rng_get_bytes(file->private_data, kbuf, len);

    if (ret < 0) {
        goto out_free;
    }

    memcpy(params->buf, kbuf, params->buf_len);

out_free:
    kfree(kbuf);
    return ret;
}

static long krypto_ioctl(struct file *file, unsigned cmd, unsigned long arg)
{
    switch (cmd) {
    case KRYPTO_RNG_CMD:
        return krypto_rng(file, (struct rng_params *)arg);
    default:
        return -EINVAL;
    }
}

static int krypto_release(struct inode *inode, struct file *file)
{
    crypto_free_rng(file->private_data);
    return 0;
}

static struct file_operations krypto_fops = {
    .owner          = THIS_MODULE,
    .open           = krypto_open,
    .release	    = krypto_release,
    .unlocked_ioctl = krypto_ioctl,
};

static struct miscdevice krypto_device = {
    .minor = MISC_DYNAMIC_MINOR,
    .name = "krypto",
    .fops = &krypto_fops,
    .mode = S_IRUGO,
};

static int __init mod_init(void)
{
    return misc_register(&krypto_device);
}

static void __exit mod_exit(void)
{
    misc_deregister(&krypto_device);
}

module_init(mod_init);
module_exit(mod_exit);
