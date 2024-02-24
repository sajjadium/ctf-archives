#include "qemu/osdep.h"
#include "hw/virtio/virtio-pci.h"
#include "hw/virtio/virtio-note.h"
#include "hw/qdev-properties.h"
#include "qapi/error.h"
#include "qemu/module.h"
#include "qom/object.h"

typedef struct VirtIONotePCI VirtIONotePCI;

#define TYPE_VIRTIO_NOTE_PCI "virtio-note-pci-base"
DECLARE_INSTANCE_CHECKER(VirtIONotePCI, VIRTIO_NOTE_PCI,
                         TYPE_VIRTIO_NOTE_PCI)

struct VirtIONotePCI {
    VirtIOPCIProxy parent_obj;
    VirtIONote vdev;
};

static Property virtio_note_properties[] = {
    DEFINE_PROP_BIT("ioeventfd", VirtIOPCIProxy, flags,
                    VIRTIO_PCI_FLAG_USE_IOEVENTFD_BIT, true),
    DEFINE_PROP_UINT32("vectors", VirtIOPCIProxy, nvectors,
                       DEV_NVECTORS_UNSPECIFIED),
    DEFINE_PROP_END_OF_LIST(),
};

static void virtio_note_pci_realize(VirtIOPCIProxy *vpci_dev, Error **errp)
{
    VirtIONotePCI *vrng = VIRTIO_NOTE_PCI(vpci_dev);
    DeviceState *vdev = DEVICE(&vrng->vdev);

    if (vpci_dev->nvectors == DEV_NVECTORS_UNSPECIFIED) {
        vpci_dev->nvectors = 1;
    }

    if (!qdev_realize(vdev, BUS(&vpci_dev->bus), errp)) {
        return;
    }
}

static void virtio_note_pci_class_init(ObjectClass *klass, void *data)
{
    DeviceClass *dc = DEVICE_CLASS(klass);
    VirtioPCIClass *k = VIRTIO_PCI_CLASS(klass);
    PCIDeviceClass *pcidev_k = PCI_DEVICE_CLASS(klass);

    k->realize = virtio_note_pci_realize;
    set_bit(DEVICE_CATEGORY_MISC, dc->categories);

    pcidev_k->vendor_id = 0xb105;
    pcidev_k->device_id = 0x1337;
    pcidev_k->revision = VIRTIO_PCI_ABI_VERSION;
    pcidev_k->class_id = PCI_CLASS_OTHERS;
    device_class_set_props(dc, virtio_note_properties);
}

static void virtio_note_initfn(Object *obj)
{
    VirtIONotePCI *dev = VIRTIO_NOTE_PCI(obj);

    virtio_instance_init_common(obj, &dev->vdev, sizeof(dev->vdev),
                                TYPE_VIRTIO_NOTE);
}

static const VirtioPCIDeviceTypeInfo virtio_note_pci_info = {
    .base_name             = TYPE_VIRTIO_NOTE_PCI,
    .generic_name          = "virtio-note-pci",
    .transitional_name     = "virtio-note-pci-transitional",
    .non_transitional_name = "virtio-note-pci-non-transitional",
    .instance_size = sizeof(VirtIONotePCI),
    .instance_init = virtio_note_initfn,
    .class_init    = virtio_note_pci_class_init,
};

static void virtio_rng_pci_register(void)
{
    virtio_pci_types_register(&virtio_note_pci_info);
}

type_init(virtio_rng_pci_register)
