#ifndef __HYPERCALL_HEADER__
#define __HYPERCALL_HEADER__

#include <stdint.h>
#include "const.h"
#include "memory.h"
#include "appletStructs.h"

#define HP_READ                     0x8000
#define HP_WRITE                    0x8001
#define HP_EXIT                     0x8002

#define HP_DIGEST_GENERATE          0x8100
#define HP_SIGNATURE_VALIDATE       0x8101
#define HP_RAND                     0x8102
#define HP_TIME                     0x8103

#define HP_APPLET_REGISTER_VALIDATE 0x8200
#define HP_APPLET_INVOKE            0x8201
#define HP_APPLET_RESUME            0x8202

#define HP_APPLETSPACE_FLAG         0xf0a9
#define HP_USERSPACE_FLAG           0xf1a9
#define HP_KERNELSPACE_FLAG         0xf2a9

#define HP_SUCCESS 0
#define HP_APPLET_PROCESSOR_REJECT 1
#define HP_APPLET_PROCESSOR_BUSY 2
#define HP_FAIL 0xffffffff

typedef struct HYPERCALL_REGS {
  uint64_t A1;
  uint64_t A2;
  uint64_t R1;
} HYPERCALL_REGS;

typedef struct HYPER_RAND {
  uint64_t rand;
} HYPER_RAND;

typedef struct HYPER_TIME {
  uint64_t timestamp;
} HYPER_TIME;

typedef struct HYPER_READ {
  uint64_t fd;
  uint64_t paddr;
  uint64_t size;
} HYPER_READ;

typedef struct HYPER_WRITE {
  uint64_t fd;
  uint64_t paddr;
  uint64_t size;
} HYPER_WRITE;
  
typedef struct HYPER_DIGEST {
  uint64_t dataLen;
  uint8_t data[DIGEST_PAYLOAD_SIZE_MAX];
  uint8_t digest[DIGEST_SIZE];
} HYPER_DIGEST;

typedef struct HYPER_SIGNATURE {
  uint8_t digest[DIGEST_SIZE];
  uint8_t pubkeyN[SIGNATURE_SIZE];
  uint8_t pubkeyE[SIGNATURE_SIZE];
  uint8_t signature[SIGNATURE_SIZE];
} HYPER_SIGNATURE;

typedef struct HYPER_APPLET {
  uint64_t codeLen;
  uint8_t code[APPLET_SIZE_MAX];
  uint8_t authoritySignature[SIGNATURE_SIZE];
} HYPER_APPLET;

typedef struct HYPER_APPLET_INVOKE {
  HYPER_APPLET applet;
  APPLET_TASK_ID task;
  APPLET_ID caller;
  uint64_t dataLen;
  uint8_t data[APPLET_ARG_SIZE_MAX];
  uint8_t storage[APPLET_STORAGE_SIZE];
} HYPER_APPLET_INVOKE;

typedef struct HYPER_APPLET_CONTEXT {
  APPLET_TASK_ID task;
  uint64_t regs[APPLET_REG_CNT];
  uint8_t memory[APPLET_CONTEXT_MEMORY_SIZE];
} HYPER_APPLET_CONTEXT;

typedef struct HYPER_APPLET_RESUME {
  HYPER_APPLET_CONTEXT context;
  uint64_t resLen;
  uint8_t res[APPLET_RES_SIZE_MAX];
} HYPER_APPLET_RESUME;

typedef struct HYPER_APPLET_RES {
  APPLET_TASK_ID task;
  uint64_t resLen;
  uint8_t res[APPLET_RES_SIZE_MAX];
  uint8_t storage[APPLET_STORAGE_SIZE];
} HYPER_APPLET_RES;

uint64_t hypercall(uint64_t port, uint64_t data);
uint64_t hp_rand();
uint64_t hp_time(uint64_t *time);
uint64_t hp_read(uint64_t fd, uint64_t paddr, uint64_t size);
uint64_t hp_write(uint64_t fd, uint64_t paddr, uint64_t size);
void __attribute__((noreturn)) hp_exit(uint64_t status);
uint64_t hp_digestGenerate(uint64_t dataLen, uint8_t *data, uint8_t *digest);
uint64_t hp_signatureValidate(uint8_t *digest, uint8_t *n, uint8_t *e, uint8_t *signature);
uint64_t hp_appletRegisterValidate(uint64_t codeLen, uint8_t *code, uint8_t *authoritySignature);
uint64_t hp_appletInvoke(APPLET_ID caller, APPLET_TASK_ID task, uint64_t codeLen, uint64_t code, uint64_t authoritySignature, uint64_t dataLen, uint8_t *data, uint64_t storage);
uint64_t hp_appletResume(APPLET_TASK_ID task, APPLET_CONTEXT *context, uint64_t callResLen, uint8_t *callRes);
uint64_t hp_appletFetchRes(uint64_t *resLen, uint8_t *res, uint8_t *storage);
uint64_t hp_appletFetchContext(APPLET_CONTEXT *context);
uint64_t hp_appletspaceFlag();
uint64_t hp_userspaceFlag();

#endif
