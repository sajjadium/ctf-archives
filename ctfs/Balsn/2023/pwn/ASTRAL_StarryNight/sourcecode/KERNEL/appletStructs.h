#ifndef __APPLETSTRUCTS_HEADER__
#define __APPLETSTRUCTS_HEADER__

#include <stddef.h>

#define APPLET_SIZE_MAX 0x1000
#define APPLET_ARG_SIZE_MAX 0x1000
#define APPLET_RES_SIZE_MAX 0x1000
#define APPLET_STORAGE_SIZE 0x1000

#define APPLET_CNT_MAX 0x20
#define APPLET_NATIVE_CNT_MAX 0x20
#define APPLET_TASK_CNT_MAX 0x20

#define APPLET_NONCE_SIZE 0x08

#define APPLET_NIL 0
#define TASK_NIL 0xffffffffffffffff
#define APPLET_IDX_NIL 0xffffffffffffffff

#define APPLET_ID uint64_t
#define APPLET_TASK_ID uint64_t

#define APPLET_REG_CNT 0x10
#define APPLET_CONTEXT_MEMORY_SIZE 0x5000

#define APPLET_SEG_SHIFT 32
#define APPLET_SEG_SIZE_MAX 0x1000
#define APPLET_SEG_OFFSET_MASK 0xffffffff
#define APPLET_ADDR_MAX 0x500000000

#define APPLET_SEG_OFFSET(addr) (((uint64_t)(addr)) & APPLET_SEG_OFFSET_MASK)
#define APPLET_SEG_IDX(addr) (((uint64_t)(addr)) >> APPLET_SEG_SHIFT)

typedef struct APPLET_CODE {
  uint8_t *code;
  uint64_t codeLen;
} APPLET_CODE;

typedef struct APPLET_INPOUT {
  uint8_t *data;
  uint64_t dataLen;
} APPLET_INPOUT;

typedef struct APPLET_REGISTER_REQ {
  APPLET_CODE applet;
  //NOTE : userNonce is used by user on unregister, signed along with applet itself
  uint8_t userNonce[SIGNATURE_SIZE];
  uint8_t userPubkeyN[SIGNATURE_SIZE];
  uint8_t userPubkeyE[SIGNATURE_SIZE];
  //NOTE : authority signature should be verified by processor everytime
  uint8_t authoritySignature[SIGNATURE_SIZE];
} APPLET_REGISTER_REQ;

typedef struct APPLET_UNREGISTER_REQ {
  APPLET_ID id;
  //NOTE : user signature is used by kernel to ensure users can't unreg, processor doesn't care about this
  uint8_t userSignature[SIGNATURE_SIZE];
} APPLET_UNREGISTER_REQ;

typedef struct APPLET_INVOKE_REQ {
  APPLET_ID id;
  APPLET_INPOUT arg;
} APPLET_INVOKE_REQ;

typedef struct APPLET_RECEIPT {
  APPLET_TASK_ID task;
} APPLET_RECEIPT;

typedef enum APPLET_STATUS {
  APPLET_NOTFOUND = 1,
  APPLET_PENDING = 2,
  APPLET_PROCESSING = 3,
  APPLET_DONE = 4
} APPLET_STATUS;

typedef struct APPLET_RESULT {
  APPLET_STATUS status;
  APPLET_INPOUT res;
} APPLET_RESULT;

typedef struct APPLET_STORAGE_REQ {
  APPLET_ID id;
} APPLET_STORAGE_REQ;

typedef struct APPLET_STORAGE {
  uint8_t storage[APPLET_STORAGE_SIZE];
} APPLET_STORAGE;

typedef struct APPLET_CONTEXT {
  uint64_t regs[APPLET_REG_CNT];
  uint8_t *memory;
} APPLET_CONTEXT;

#endif
