#ifndef __DEVICE_HEADER__
#define __DEVICE_HEADER__

#define _GNU_SOURCE
#include <stdint.h>
#include <stdbool.h>
#include <unistd.h>
#include <fcntl.h>
#include <poll.h>
#include <errno.h>
#include "util.h"
#include "applet.h"
#include "hypercall.h"


#define DV_READ_FD 0x100
#define DV_WRITE_FD 0x101
#define DV_INTERRUPT_FD 0x102

#define DV_SUCCESS 0
#define DV_BUSY 1
#define DV_FAIL 0xffffffffffffffff

#define DV_SYNC_CODE 0xff

#define DV_APPLET_REGISTER_MSG 0x01
#define DV_APPLET_INVOKE_MSG 0x02
#define DV_APPLET_RESUME_MSG 0x03

#define DV_NO_INTERRUPT 0xf0
#define DV_APPLET_RES_INTERRUPT 0xf1
#define DV_APPLET_INVOKE_INTERRUPT 0xf2
#define DV_APPLET_PROCESSOR_FLAG_INTERRUPT 0xf3

#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define DV_INTERRUPT_DATA_SIZE_MAX MAX(sizeof(HYPER_APPLET_RES), sizeof(HYPER_APPLET_CONTEXT))

#define DV_APPLET_REGISTER_RES uint64_t
#define DV_APPLET_INVOKE_RES uint64_t
#define DV_APPLET_RESUME_RES uint64_t

void launchDevice(char *device, char *timeout);
void dv_sendMsg(uint8_t type, uint8_t *msg, uint64_t size);
void dv_recvMsg(uint8_t type, uint8_t *msg, uint64_t size);
uint8_t dv_recvInterrupt(uint8_t *res);

#endif
