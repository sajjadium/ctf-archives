#ifndef __APPLET_HEADER__
#define __APPLET_HEADER__

#include <stdint.h>

#define APPLET_ID uint64_t
#define APPLET_TASK_ID uint64_t

#define APPLET_TASK_NIL 0xffffffffffffffff

#define APPLET_TASK_CNT_MAX 0x20

#define APPLET_SIZE_MAX 0x1000
#define APPLET_ARG_SIZE_MAX 0x1000
#define APPLET_RES_SIZE_MAX 0x1000
#define APPLET_STORAGE_SIZE 0x1000

#define APPLET_REG_CNT 0x10
#define APPLET_CONTEXT_MEMORY_SIZE 0x5000

#define DIGEST_SIZE 0x20
#define SIGNATURE_SIZE 0x100

//Exactly same as HYPER_... series of structure
typedef struct DEVICE_APPLET {
  uint64_t codeLen;
  uint8_t code[APPLET_SIZE_MAX];
  uint8_t authoritySignature[SIGNATURE_SIZE];
} DEVICE_APPLET;

typedef struct DEVICE_APPLET_INVOKE {
  DEVICE_APPLET applet;
  APPLET_TASK_ID task;
  APPLET_ID caller;
  uint64_t dataLen;
  uint8_t data[APPLET_ARG_SIZE_MAX];
  uint8_t storage[APPLET_STORAGE_SIZE];
} DEVICE_APPLET_INVOKE;

typedef struct DEVICE_APPLET_CONTEXT {
  APPLET_TASK_ID task;
  uint64_t regs[APPLET_REG_CNT];
  uint8_t memory[APPLET_CONTEXT_MEMORY_SIZE];
} DEVICE_APPLET_CONTEXT;

typedef struct DEVICE_APPLET_RESUME {
  DEVICE_APPLET_CONTEXT context;
  uint64_t resLen;
  uint8_t res[APPLET_RES_SIZE_MAX];
} DEVICE_APPLET_RESUME;

typedef struct DEVICE_APPLET_RES {
  APPLET_TASK_ID task;
  uint64_t resLen;
  uint8_t res[APPLET_RES_SIZE_MAX];
  uint8_t storage[APPLET_STORAGE_SIZE];
} DEVICE_APPLET_RES;

#endif
