#include "qemu/osdep.h"
#include "hw/pci/pci_device.h"
#include "hw/qdev-properties.h"
#include "qemu/module.h"
#include "sysemu/kvm.h"
#include "qom/object.h"
#include "qapi/error.h"

#include "hw/char/note_service.h"
#include "qemu/queue.h"

#define PAGE_SIZE 0x1000

typedef struct NoteEntry {
	uint64_t id;
	uint64_t size;
	uint8_t * content;
	QTAILQ_ENTRY(NoteEntry) next;
} NoteEntry;

typedef struct NoteCmdHdr {
	uint32_t cmd_type;
	uint32_t res;
	uint32_t note_id;
	uint32_t note_size;
	uint32_t encrypt_offset;
	uint32_t new_note_id;
	uint64_t note_addr;
} NoteCmdHdr;

typedef struct PCINoteDevState {
	PCIDevice parent_obj;

	MemoryRegion mmio;

	uint32_t reg[0x20];
	QTAILQ_HEAD(, NoteEntry) notes;
} PCINoteDevState;

OBJECT_DECLARE_SIMPLE_TYPE(PCINoteDevState, PCI_NOTE_DEV)

static inline dma_addr_t note_addr64(uint32_t low, uint32_t high)
{
    if (sizeof(dma_addr_t) == 4) {
        return low;
    } else {
        return low | (((dma_addr_t)high << 16) << 16);
    }
}


static uint64_t pci_notedev_mmio_read(void *opaque, hwaddr addr, unsigned size);
static void pci_notedev_mmio_write(void *opaque, hwaddr addr, uint64_t val, unsigned size);
static void pci_notedev_reset(PCINoteDevState *ms);
static void do_command(PCINoteDevState *ms);


static const MemoryRegionOps pci_notedev_mmio_ops = {
	.read       = pci_notedev_mmio_read,
	.write      = pci_notedev_mmio_write,
	.endianness = DEVICE_LITTLE_ENDIAN,
	.impl = {
		.min_access_size = 1,
		.max_access_size = 4,
	},
};

static void pci_notedev_realize(PCIDevice *pci_dev, Error **errp) {
	PCINoteDevState *s = PCI_NOTE_DEV(pci_dev);

	memory_region_init_io(&s->mmio, OBJECT(s), &pci_notedev_mmio_ops, s, "note-service-mmio", 0x100);
	pci_register_bar(pci_dev, 0, PCI_BASE_ADDRESS_SPACE_MEMORY, &s->mmio);
	s->mmio.disable_reentrancy_guard = true;

	bzero(&s->reg, sizeof(s->reg));
	QTAILQ_INIT(&s->notes);
}

static void pci_notedev_uninit(PCIDevice *pci_dev) {
	PCINoteDevState *ms = PCI_NOTE_DEV(pci_dev);

	pci_notedev_reset(ms);
}

static void notedev_reset(DeviceState *s) {
	PCINoteDevState *ms = PCI_NOTE_DEV(s);

	pci_notedev_reset(ms);
}

static void pci_notedev_reset(PCINoteDevState *ms) {
	NoteEntry *note;
	bzero(&ms->reg, sizeof(ms->reg));
	for (;;) {
        note = QTAILQ_FIRST(&ms->notes);
        if (note == NULL) {
            break;
        }
		QTAILQ_REMOVE(&ms->notes, note, next);

		if (note->content) {
			g_free(note->content);
		}
		g_free(note);
    }
}

static void pci_notedev_class_init(ObjectClass *klass, void *data) {
	DeviceClass *dc = DEVICE_CLASS(klass);
	PCIDeviceClass *k = PCI_DEVICE_CLASS(klass);

	k->realize = pci_notedev_realize;
	k->exit = pci_notedev_uninit;
	k->vendor_id = NOTE_PCI_VENDOR_ID;
	k->device_id = NOTE_PCI_DEVICE_ID;
	k->revision = 0x00;
	k->class_id = PCI_CLASS_OTHERS;
	dc->desc = "ISITDTU CTF 2023 Challenge : Note service as a QEMU device";
	set_bit(DEVICE_CATEGORY_MISC, dc->categories);
	dc->reset = notedev_reset;
}

static const TypeInfo pci_notedev_info = {
	.name          = TYPE_PCI_NOTE_DEV,
	.parent        = TYPE_PCI_DEVICE,
	.instance_size = sizeof(PCINoteDevState),
	.class_init    = pci_notedev_class_init,
	.interfaces = (InterfaceInfo[]) {
		{ INTERFACE_CONVENTIONAL_PCI_DEVICE },
		{ },
	},
};

static void pci_notedev_register_types(void) {
	type_register_static(&pci_notedev_info);
}

type_init(pci_notedev_register_types)

static uint64_t pci_notedev_mmio_read(void *opaque, hwaddr reg, unsigned size) {
	PCINoteDevState *ms = opaque;
	uint32_t ret;
	switch (reg) {
		case 0x00:
			do_command(ms);
			ret = 0;
			break;
		case 0x04:
			ret = ms->reg[REG_LOW_CMD_CHAIN_ADDR];
			break;
		case 0x08:
			ret = ms->reg[REG_HIGH_CMD_CHAIN_ADDR];
			break;
		default:
			uint32_t idx = reg / 4;
			if (idx < sizeof(ms->reg)) {
				ret = ms->reg[idx];
			}
			break;
	}

	return ret;
}

static void pci_notedev_mmio_write(void *opaque, hwaddr reg, uint64_t val, unsigned size) {
	PCINoteDevState *ms = opaque;
	switch (reg) {
		case 0x00:
			do_command(ms);
			break;
		case 0x04:
			ms->reg[REG_LOW_CMD_CHAIN_ADDR] = val & 0xfffffff0;
			break;
		case 0x08:
			ms->reg[REG_HIGH_CMD_CHAIN_ADDR] = val;
			break;
		default:
			uint32_t idx = reg / 4;
			if (idx < sizeof(ms->reg)) {
				ms->reg[idx] = val;
			}
			break;
	}
}

static NoteEntry * search_for_notes(PCINoteDevState * ms, uint64_t id) {
	NoteEntry *note;
	QTAILQ_FOREACH(note, &ms->notes, next) {
		if (note->id == id) {
			return note;
		}
	}
	return NULL;
}

static void do_command(PCINoteDevState *ms){
	uint32_t cnt = 0;
	uint32_t res = 0;
	NoteCmdHdr hdr;
	NoteEntry * note = NULL;
	dma_addr_t cmd_chain_addr = note_addr64(ms->reg[REG_LOW_CMD_CHAIN_ADDR], ms->reg[REG_HIGH_CMD_CHAIN_ADDR]);
	

	for (cnt = 0; cnt < 0x20; ++cnt) {
		memset(&hdr, 0, sizeof hdr);
		cpu_physical_memory_rw(cmd_chain_addr, &hdr, sizeof(NoteCmdHdr), 0);
		le32_to_cpus(&hdr.cmd_type);
		le32_to_cpus(&hdr.note_id);
		le32_to_cpus(&hdr.note_size);
		le32_to_cpus(&hdr.encrypt_offset);
		le32_to_cpus(&hdr.new_note_id);
		le64_to_cpus(&hdr.note_addr);
		hdr.note_size &= 0xfff;
		hdr.encrypt_offset &= 0xfff;
		res = NOTE_SUCCESS;
		switch (hdr.cmd_type) {
			case CMD_SUBMIT_NOTE:
				note = g_malloc(sizeof(NoteEntry));
				note->id = hdr.note_id;
				note->size = hdr.note_size;
				note->content = g_malloc(note->size);
				memset(note->content, 0, note->size);

				cpu_physical_memory_rw(hdr.note_addr, note->content, note->size, 0);

				QTAILQ_INSERT_TAIL(&ms->notes, note, next);

				break;

			case CMD_DELETE_NOTE:
				note = search_for_notes(ms, hdr.note_id);
				if (note == NULL) {
					res = NOTE_FAIL;
					break;
				}

				QTAILQ_REMOVE(&ms->notes, note, next);
				if (note->content) {
					g_free(note->content);
				}
				g_free(note);

				break;

			case CMD_READ_NOTE:
				note = search_for_notes(ms, hdr.note_id);
				if (note == NULL) {
					res = NOTE_FAIL;
					break;
				}
				uint32_t size = hdr.note_size;
				
				if (size > note->size) {
					size = note->size;
				}

				cpu_physical_memory_rw(hdr.note_addr, note->content, size, 1);

				break;

			case CMD_EDIT_NOTE:
				note = search_for_notes(ms, hdr.note_id);
				if (note == NULL) {
					res = NOTE_FAIL;
					break;
				}
				
				if (hdr.note_size <= note->size) {
					cpu_physical_memory_rw(hdr.note_addr, note->content, hdr.note_size, 0);
				}
				else {
					g_free(note->content);
					note->size = hdr.note_size;
					note->content = g_malloc(note->size);
					memset(note->content, 0, note->size);
					cpu_physical_memory_rw(hdr.note_addr, note->content, note->size, 0);
				}
				break;
			
			case CMD_DUPLICATE_NOTE:
				NoteEntry *dup_note = search_for_notes(ms, hdr.note_id);
				if (dup_note == NULL) {
					res = NOTE_FAIL;
					break;
				}
				note = g_malloc(sizeof(NoteEntry));
				note->id = hdr.new_note_id;
				note->size = hdr.note_size;
				note->content = g_malloc(note->size);
				memset(note->content, 0, note->size);
				
				cpu_physical_memory_rw(hdr.note_addr, note->content, note->size, 0);
				
				uint32_t size_to_copy = dup_note->size;
				if (size_to_copy > note->size) {
					size_to_copy = note->size;
				}

				memcpy(note->content, dup_note->content, size_to_copy);
				QTAILQ_INSERT_TAIL(&ms->notes, note, next);
				break;

			case CMD_ENCRYPT_NOTE:
				note = search_for_notes(ms, hdr.note_id);
				if (note == NULL) {
					res = NOTE_FAIL;
					break;
				}

				if (hdr.encrypt_offset >= note->size) {
					res = NOTE_FAIL;
					break;
				}

				uint32_t size_to_encrypt = note->size;
				if (size_to_copy > hdr.note_size) {
					size_to_copy = hdr.note_size;
				}

				if (size_to_copy + hdr.encrypt_offset >= note->size) {
					size_to_copy = note->size - hdr.encrypt_offset;
				}

				uint8_t * secret = g_malloc(hdr.note_size);
				memset(secret, 0, hdr.note_size);

				cpu_physical_memory_rw(hdr.note_addr, secret, hdr.note_size, 0);
				
				

				for (uint32_t i = 0; i < size_to_encrypt; ++i) {
					note->content[i + hdr.encrypt_offset] ^= secret[i];
				}
				break;
			
			case CMD_RESET:
				res = NOTE_RESET;
				res = cpu_to_le32(res);
				cpu_physical_memory_rw(cmd_chain_addr + 4, &res, 4, 0);
				pci_notedev_reset(ms);
				return;
		}
		
		res = cpu_to_le32(res);
		cpu_physical_memory_rw(cmd_chain_addr + 4, &res, 4, 0);
		if (hdr.cmd_type == CMD_END_CHAIN) {
			break;
		}
		cmd_chain_addr += sizeof(NoteCmdHdr);
	}	

}
