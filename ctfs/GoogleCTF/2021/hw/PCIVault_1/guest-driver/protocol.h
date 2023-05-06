#ifndef PROTOCOL_H
#define PROTOCOL_H

#include <linux/mutex.h>
#include <linux/pci.h>

#include "device.h"

#define MAX_PACKET_SIZE 0x100

extern wait_queue_head_t device_wait_queue;

struct private_data {
  u8 __iomem *hwmem;
  u16 device_max_packet_size;
  char encryption_key[64];
};

int device_init(struct private_data *priv);
int device_do_nop(struct private_data *priv, u32 payload);
int device_select_entry(struct private_data *priv, const char *entry_name);
int device_read_entry(struct private_data *priv, char *buffer);
int device_write_entry(struct private_data *priv, const char *buffer,
                       size_t buffer_sz);
int device_delete_entry(struct private_data *priv);
int device_set_encryption_key(struct private_data *priv);

#endif