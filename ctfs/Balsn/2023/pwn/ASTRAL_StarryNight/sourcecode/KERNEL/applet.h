#ifndef __APPLET_HEADER__
#define __APPLET_HEADER__

#include <stddef.h>
#include "const.h"
#include "memory.h"
#include "kernel.h"
#include "appletStructs.h"
#include "hypercall.h"

#define APPLET_INVOKE_INTERRUPT 0x01
#define APPLET_RES_INTERRUPT 0x02

typedef struct S_APPLET_TASK {
  uint64_t idx;
  APPLET_TASK_ID caller;
  APPLET_STATUS status;
  uint64_t argLen;
  uint8_t *arg;
  uint64_t resLen;
  uint8_t *res;
  APPLET_CONTEXT context;
  uint64_t callResLen;
  uint8_t *callRes;
  uint64_t storage;
  uint64_t codeLen;
  uint64_t code;
  uint64_t authoritySignature;
} S_APPLET_TASK;

typedef struct S_APPLET {
  APPLET_ID id;
  uint64_t taskCnt;
  uint64_t codeLen;
  union {
    uint8_t *code;
    uint64_t (*nativeFn)(APPLET_TASK_ID task, APPLET_INPOUT *arg);
  };
  uint8_t *storage;
  uint8_t userNonce[SIGNATURE_SIZE];
  uint8_t userPubkeyN[SIGNATURE_SIZE];
  uint8_t userPubkeyE[SIGNATURE_SIZE];
  uint8_t authoritySignature[SIGNATURE_SIZE];
} S_APPLET;

typedef struct S_APPLET_STATE {
  S_APPLET applets[APPLET_CNT_MAX + APPLET_NATIVE_CNT_MAX];
  S_APPLET_TASK tasks[APPLET_TASK_CNT_MAX];
} S_APPLET_STATE;

extern S_APPLET_STATE g_applet;

uint64_t initAppletStorage();
uint64_t findAppletIdx(uint64_t id, uint64_t *idx);
uint64_t digestGenerateHelper(uint64_t codeLen, uint8_t *code, uint8_t *n, uint8_t *e, uint8_t *nonce, uint8_t *digest);
uint64_t kAppletRegister(APPLET_REGISTER_REQ *req, APPLET_ID *id);
uint64_t kAppletUnregister(APPLET_UNREGISTER_REQ *req);
uint64_t kAppletInvokeUtil(APPLET_TASK_ID task);
uint64_t kAppletInvoke(APPLET_INVOKE_REQ *req, APPLET_RECEIPT *receipt, APPLET_TASK_ID caller);
uint64_t kAppletResult(APPLET_RECEIPT *receipt, APPLET_RESULT *result);
uint64_t kAppletRecycle(APPLET_RECEIPT *receipt);
uint64_t kAppletStorage(APPLET_STORAGE_REQ *req, APPLET_STORAGE *res);
uint64_t kAppletResume(APPLET_TASK_ID caller, APPLET_TASK_ID callee);
void kAppletInterrupt(uint8_t type, uint8_t *req);
uint64_t appletBuiltinTime(APPLET_TASK_ID task, APPLET_INPOUT *arg);
uint64_t appletBuiltinRand(APPLET_TASK_ID task, APPLET_INPOUT *arg);
uint64_t appletBuiltinValidatePreimage(APPLET_TASK_ID task, APPLET_INPOUT *arg);
uint64_t appletBuiltinFlag(APPLET_TASK_ID task, APPLET_INPOUT *arg);

#endif
