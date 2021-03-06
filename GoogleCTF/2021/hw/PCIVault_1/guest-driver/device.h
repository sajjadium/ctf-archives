#define CONFIG_VERSION 1

#define CMD_GET_KEY 1
#define CMD_SET_KEY 2
#define CMD_GET_VAL 3
#define CMD_SET_VAL 4
#define CMD_DELETE  5
#define CMD_SET_ENCRYPTION_KEY 6
#define CMD_GET_DEVICE_CONFIG 126
#define CMD_SET_HOST_CONFIG 127
#define CMD_EXECUTE 128

#define STATUS_UNKNOWN 0
#define STATUS_OK 1
#define STATUS_IN_PROGRESS 2
#define STATUS_REQ_INIT 3
#define STATUS_ERROR 4
#define STATUS_OOM 5
#define STATUS_NOTFOUND 6
#define STATUS_NOTSUPPORTED 7

typedef unsigned char u8;
typedef unsigned short u16;

struct IoBlock {
    u8 cmd;
    u8 status;
    u16 length;
    u8 iobuf[0x1000 - 4];
};

struct DeviceConfigDescriptor {
    u8 device_config_descriptor_length;
    u8 config_version;
    u8 device_version;
    u8 host_config_descriptor_length;
    u16 max_packet_size;
};

struct HostConfigDescriptor {
    u8 host_config_descriptor_length;
    u8 config_version;
    u16 max_packet_size;
};
