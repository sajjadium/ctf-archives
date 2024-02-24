#include "qemu/osdep.h"
#include "hw/hw.h"
#include "hw/virtio/virtio.h"
#include "hw/virtio/virtio-note.h"
#include "qemu/iov.h"
#include "qemu/error-report.h"
#include "standard-headers/linux/virtio_ids.h"
#include "sysemu/runstate.h"

static uint64_t virtio_note_get_features(VirtIODevice *vdev, uint64_t f, Error **errp)
{
    return f;
}

static void virtio_note_set_status(VirtIODevice *vdev, uint8_t status)
{
    if (!vdev->vm_running) {
        return;
    }
    vdev->status = status;
}

static void virtio_note_handle_req(VirtIODevice *vdev, VirtQueue *vq) {
    VirtIONote *vnote = VIRTIO_NOTE(vdev);
    VirtQueueElement *vqe = 0;
    req_t *req = 0;

    while(!virtio_queue_ready(vq)) {
        return;
    }

    if (!runstate_check(RUN_STATE_RUNNING)) {
        return;
    }

    vqe = virtqueue_pop(vq, sizeof(VirtQueueElement));
    if(!vqe) goto end;

    if(vqe->out_sg->iov_len != sizeof(req_t)) goto end;
    req = calloc(1, sizeof(req_t));
    if(!req) goto end;
    if(iov_to_buf(vqe->out_sg, vqe->out_num, 0, req, vqe->out_sg->iov_len) != sizeof(req_t)) goto end;

    if(!vnote->notes[req->idx])
    {
        virtio_error(vdev, "Corrupted note encountered");
        goto end;
    }

    switch(req->op)
    {
        case READ:
            cpu_physical_memory_write(req->addr, vnote->notes[req->idx], NOTE_SZ);
            break;

        case WRITE:
            cpu_physical_memory_read(req->addr, vnote->notes[req->idx], NOTE_SZ);
            break;

        default:
            goto end;
    }

    virtqueue_push(vq, vqe, vqe->out_sg->iov_len);
    virtio_notify(vdev, vq);

end:
    g_free(vqe);
    free(req);
    return;
}

static void virtio_note_device_realize(DeviceState *dev, Error **errp) {
    VirtIODevice *vdev = VIRTIO_DEVICE(dev);
    VirtIONote *vnote = VIRTIO_NOTE(dev);
    virtio_init(vdev, VIRTIO_ID_NOTE, 0);
    vnote->vnq = virtio_add_queue(vdev, 4, virtio_note_handle_req);
    for(int i = 0; i < N_NOTES; i++)
    {
        vnote->notes[i] = calloc(NOTE_SZ, 1);
        if(!vnote->notes[i])
        {
            virtio_error(vdev, "Unable to initialize notes");
            return;
        }
    }
}

static void virtio_note_device_unrealize(DeviceState *dev) {
    VirtIODevice *vdev = VIRTIO_DEVICE(dev);
    VirtIONote *vnote = VIRTIO_NOTE(dev);
    for(int i = 0; i < N_NOTES; i++)
    {
        free(vnote->notes[i]);
        vnote->notes[i] = NULL;
    }
    virtio_cleanup(vdev);
}

static void virtio_note_class_init(ObjectClass *klass, void *data) {
    DeviceClass *dc = DEVICE_CLASS(klass);
    VirtioDeviceClass *vdc = VIRTIO_DEVICE_CLASS(klass);

    set_bit(DEVICE_CATEGORY_MISC, dc->categories);
    vdc->realize = virtio_note_device_realize;
    vdc->unrealize = virtio_note_device_unrealize;
    vdc->get_features = virtio_note_get_features;
    vdc->set_status = virtio_note_set_status;
}

static const TypeInfo virtio_note_info = {
    .name = TYPE_VIRTIO_NOTE,
    .parent = TYPE_VIRTIO_DEVICE,
    .instance_size = sizeof(VirtIONote),
    .class_init = virtio_note_class_init,
};

static void virtio_register_types(void) {
    type_register_static(&virtio_note_info);
}

type_init(virtio_register_types);
