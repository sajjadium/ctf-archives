#ifndef _SECMSG_H
#define _SECMSG_H

#define CMD_ADD_MESSAGE 0x11111111
#define CMD_READ_MESSAGE 0x22222222
#define CMD_DELETE_MESSAGE 0x33333333

#define N_MAX_MESSAGES 32
#define MESSAGE_MIN_SZ 0x20
#define MESSAGE_MAX_SZ 0x300

#define MIN_LIFETIME 1000
#define MAX_LIFETIME 5000

#define DEVICE_NAME "secmsg_storage"
#define CLASS_NAME  DEVICE_NAME

struct secure_message {
    struct work_struct work;
    uint32_t lifetime;
    uint32_t consumed;
    uint32_t content_size;
    char content[];
};

struct params {
    void __user *buf;
    uint32_t lifetime;
    uint32_t len;
    uint32_t idx;
};

struct chrdev_info {
	unsigned int major;
	struct cdev cdev;
	struct class *class;
};

#endif
