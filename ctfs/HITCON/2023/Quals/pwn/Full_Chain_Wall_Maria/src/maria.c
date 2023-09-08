#include "hw/hw.h"
#include "hw/pci/msi.h"
#include "hw/pci/pci.h"
#include "qapi/visitor.h"
#include "qemu/main-loop.h"
#include "qemu/module.h"
#include "qemu/osdep.h"
#include "qom/object.h"

#define TYPE_PCI_MARIA_DEVICE "maria"
#define MARIA_MMIO_SIZE 0x10000

#define BUFF_SIZE 0x2000

typedef struct {
    PCIDevice pdev;
    struct {
		uint64_t src;
        uint8_t off;
	} state;
    char buff[BUFF_SIZE];
    MemoryRegion mmio;
} MariaState;

DECLARE_INSTANCE_CHECKER(MariaState, MARIA, TYPE_PCI_MARIA_DEVICE)

static uint64_t maria_mmio_read(void *opaque, hwaddr addr, unsigned size) {
    MariaState *maria = (MariaState *)opaque;
    uint64_t val = 0;
    switch (addr) {
        case 0x00:
            cpu_physical_memory_rw(maria->state.src, &maria->buff[maria->state.off], BUFF_SIZE, 1);
            val = 0x600DC0DE;
            break;
        case 0x04:
            val = maria->state.src;
            break;
        case 0x08:
            val = maria->state.off;
            break;
        default:
            val = 0xDEADC0DE;
            break;
    }
    return val;
}

static void maria_mmio_write(void *opaque, hwaddr addr, uint64_t val, unsigned size) {
    MariaState *maria = (MariaState *)opaque;
    switch (addr) {
        case 0x00:
            cpu_physical_memory_rw(maria->state.src, &maria->buff[maria->state.off], BUFF_SIZE, 0);
            break;
        case 0x04:
            maria->state.src = val;
            break;
        case 0x08:
            maria->state.off = val;
            break;
        default:
            break;
    }
}

static const MemoryRegionOps maria_mmio_ops = {
    .read = maria_mmio_read,
    .write = maria_mmio_write,
    .endianness = DEVICE_NATIVE_ENDIAN,
    .valid = {
        .min_access_size = 4,
        .max_access_size = 4,
    },
    .impl = {
        .min_access_size = 4,
        .max_access_size = 4,
    },
};

static void pci_maria_realize(PCIDevice *pdev, Error **errp) {
    MariaState *maria = MARIA(pdev);
    memory_region_init_io(&maria->mmio, OBJECT(maria), &maria_mmio_ops, maria, "maria-mmio", MARIA_MMIO_SIZE);
    pci_register_bar(pdev, 0, PCI_BASE_ADDRESS_SPACE_MEMORY, &maria->mmio);
}

static void maria_instance_init(Object *obj) {
    MariaState *maria = MARIA(obj);
    memset(&maria->state, 0, sizeof(maria->state));
    memset(maria->buff, 0, sizeof(maria->buff));
}

static void maria_class_init(ObjectClass *class, void *data) {
    DeviceClass *dc = DEVICE_CLASS(class);
    PCIDeviceClass *k = PCI_DEVICE_CLASS(class);

    k->realize = pci_maria_realize;
    k->vendor_id = PCI_VENDOR_ID_QEMU;
    k->device_id = 0xDEAD;
    k->revision = 0x0;
    k->class_id = PCI_CLASS_OTHERS;

    set_bit(DEVICE_CATEGORY_MISC, dc->categories);
}

static void pci_maria_register_types(void) {
    static InterfaceInfo interfaces[] = {
        { INTERFACE_CONVENTIONAL_PCI_DEVICE },
        { },
    };
    static const TypeInfo maria_info = {
        .name = TYPE_PCI_MARIA_DEVICE,
        .parent = TYPE_PCI_DEVICE,
        .instance_size = sizeof(MariaState),
        .instance_init = maria_instance_init,
        .class_init = maria_class_init,
        .interfaces = interfaces,
    };

    type_register_static(&maria_info);
}

type_init(pci_maria_register_types)
