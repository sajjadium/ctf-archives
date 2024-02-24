#ifndef QEMU_VIRTIO_NOTE_H
#define QEMU_VIRTIO_NOTE_H

#include "exec/hwaddr.h"
#include "hw/virtio/virtio.h"
#include "sysemu/rng.h"
#include "standard-headers/linux/virtio_rng.h"
#include "qom/object.h"

#define NOTE_SZ           0x40
#define N_NOTES           0x10
#define TYPE_VIRTIO_NOTE  "virtio-note-device"
#define VIRTIO_NOTE(obj) \
        OBJECT_CHECK(VirtIONote, (obj), TYPE_VIRTIO_NOTE)

typedef enum {
    READ,
    WRITE
} operation;

typedef struct req_t {
    unsigned int idx;
    hwaddr addr;
    operation op;
} req_t;

typedef struct VirtIONote {
    VirtIODevice parent_obj;
    VirtQueue *vnq;
    char *notes[N_NOTES];
} VirtIONote;

#endif
