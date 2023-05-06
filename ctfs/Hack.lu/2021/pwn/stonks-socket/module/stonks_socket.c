#include <net/tcp.h>

MODULE_LICENSE("GPL");

#define OPTION_CALL     0x1337
#define OPTION_PUT      0x1338
#define OPTION_DEBUG    0x1339

struct Hash {
    u64 word1;
    u64 word2;
    u64 word3;
    u64 word4;
    unsigned length;
    u64 rounds;
    u64 key;
};

struct StonksSocket {
    unsigned hash_size;
    u64 hash_rounds;
    u64 hash_key;
    int (*hash_function)(struct iov_iter *msg, struct Hash *hash);
};

int null_hash(struct iov_iter *msg, struct Hash *h) {
    return 0;
}

int secure_hash(struct iov_iter *msg, struct Hash *h) {
    u64 i = 1, j, size;
    char *buf;
    char *hash = (char*)&h->word1;

    // init
    for (i = 0; i < h->length; i++) {
        (&h->word1)[i] = h->key;
    }

    //load data
    while (i) {
        size = h->length * sizeof(u64);
        buf = kmalloc(size, GFP_KERNEL);
        i = copy_from_iter(buf, size, msg);
        for (j = 0; j < i; j++) {
            hash[j] ^= buf[j];
        }
        kfree(buf);
    }

    // hash
    for (i = 0; i < h->rounds; i++) {
        for (j = 0; j < size; j++) {
            hash[j] = hash[(j+8)%size] ^ 0xAC ^ i;
        }
    }
    return size;
}

int stonks_rocket(struct sock *sk, struct msghdr *msg, size_t len, int nonblock, int flags, int *addr_len) {
    int ret, count;
    struct StonksSocket *s_sk = sk->sk_user_data;
    struct Hash hash;
    struct iov_iter iter[2];

    ret = tcp_recvmsg(sk, msg, len, nonblock, flags, addr_len);
    if (ret < 1 || s_sk == NULL) {
        return ret;
    }
    printk(KERN_INFO "stonks_socket: received message, size: %d", ret);

    iter[0] = msg->msg_iter;
    iov_iter_init(&iter[1], WRITE, iter[0].iov, iter[0].count, ret);

    hash.length = s_sk->hash_size;
    hash.rounds = s_sk->hash_rounds;
    hash.key = s_sk->hash_key;
    count = s_sk->hash_function(&iter[1], &hash);

    len = copy_to_iter(&hash.word1, count, &iter[0]);
    ret += count;
    return ret;
}

int stonks_ioctl(struct sock *sk, int cmd, unsigned long arg) {
    int err;
    u64 *sks = (u64*)sk;
    union {
        struct {
            u64 off;
            u64 __user *data;
        };
        struct {
            unsigned size;
            u64 rounds;
            u64 key;
            u64 security;
        };
    } a;
    struct StonksSocket *stonks_sk;

    if (cmd == OPTION_CALL) {
        if (sk->sk_user_data != NULL) {
            return -EINVAL;
        }

        err = copy_from_user(&a, (void*)arg, sizeof(a));

        stonks_sk = kmalloc(sizeof(struct StonksSocket), GFP_KERNEL);
        stonks_sk->hash_size = a.size;
        stonks_sk->hash_rounds = a.rounds;
        stonks_sk->hash_key = a.key;
        if (a.security == 1) {
            stonks_sk->hash_function = secure_hash;
        } else {
            stonks_sk->hash_function = null_hash;
        }
        sk->sk_user_data = stonks_sk;
        sk->sk_prot->recvmsg = stonks_rocket;
        return err;
    } else if (cmd == OPTION_PUT) {
        if (sk->sk_user_data == NULL) {
            return -EINVAL;
        }
        kfree(sk->sk_user_data);
        sk->sk_user_data = NULL;
    } else if (cmd == OPTION_DEBUG) {
        err = copy_from_user(&a, (void*)arg, sizeof(a));
        return put_user(sks[a.off], a.data);
    }
    return tcp_ioctl(sk, cmd, arg);
}

int __init stonks_socket(void)
{
    printk(KERN_INFO "stonks_socket: maximizing profits");
    printk(KERN_INFO "stonks_socket: recvms: %llx", (u64)stonks_rocket);
    tcp_prot.ioctl = stonks_ioctl;
    return 0;
}

void __exit stinks_socket(void)
{
    printk(KERN_INFO "stonks_socket: unloading :( this stinks");
    tcp_prot.ioctl = tcp_ioctl;
}

module_init(stonks_socket);
module_exit(stinks_socket);
