#define HW_NOTE_SERVICE_H

#define TYPE_PCI_NOTE_DEV "note-service"

#define NOTE_PCI_VENDOR_ID 0x7331
#define NOTE_PCI_DEVICE_ID 0x1337

#define REG_NOTE_COMMAND 0
#define REG_LOW_CMD_CHAIN_ADDR 1
#define REG_HIGH_CMD_CHAIN_ADDR 2


#define CMD_SUBMIT_NOTE   0x10
#define CMD_DELETE_NOTE     0x11
#define CMD_READ_NOTE     0x12
#define CMD_EDIT_NOTE     0x13
#define CMD_DUPLICATE_NOTE   0x14
#define CMD_ENCRYPT_NOTE   0x15
#define CMD_END_CHAIN     0x16
#define CMD_RESET     0x17

#define NOTE_SUCCESS    0x00
#define NOTE_RESET    0x01
#define NOTE_FAIL   0xff

