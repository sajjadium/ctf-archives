#ifndef __APPLET_HEADER__
#define __APPLET_HEADER__

#include <stdint.h>

#define DIGEST_SIZE 0x20
#define SIGNATURE_SIZE 0x100

#define APPLET_SIZE_MAX 0x1000
#define APPLET_ARG_SIZE_MAX 0x1000
#define APPLET_RES_SIZE_MAX 0x1000
#define APPLET_STORAGE_SIZE 0x1000

#define APPLET_ID uint64_t
#define APPLET_TASK_ID uint64_t

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
  //NOTE : user signature is used by kernel to ensure 3rd party users can't unreg, processor doesn't care about this
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

#endif
