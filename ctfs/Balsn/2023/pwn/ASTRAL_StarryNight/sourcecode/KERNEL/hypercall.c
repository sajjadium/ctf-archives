#include "hypercall.h"

uint64_t hypercall(uint64_t port, uint64_t data) {
  HYPERCALL_REGS args = {.A1 = port, .A2 = data, .R1 = 0};
  asm(
    "mov rax, %[args];"
    "push rax;"
    "mov dx,  [rax + 0x00];"
    "mov eax, [rax + 0x08];"
    "out dx, eax;"
    "in eax, dx;"
    "pop rdi;"
    "mov [rdi + 0x10], eax;"
    :
    : [args] "r" (&args)
    : "rax", "rdi", "rdx"
  );
  return args.R1;
}

uint64_t hp_rand(uint64_t *rand) {
  HYPER_RAND randArgs;
  uint64_t physAddr;
  if (getPhysAddr((uint64_t)&randArgs, 0, &physAddr) == FAIL) panic("hp_rand failed");
  if (hypercall(HP_RAND, physAddr) == HP_FAIL) return FAIL;
  *rand = randArgs.rand;
  return SUCCESS;
}

uint64_t hp_time(uint64_t *time) {
  HYPER_TIME timeArgs;
  uint64_t physAddr;
  if (getPhysAddr((uint64_t)&timeArgs, 0, &physAddr) == FAIL) panic("hp_time failed");
  if (hypercall(HP_TIME, physAddr) == HP_FAIL) return FAIL;
  *time = timeArgs.timestamp;
  return SUCCESS;
}

uint64_t hp_read(uint64_t fd, uint64_t paddr, uint64_t size) {
  HYPER_READ readArgs = {.fd = fd, .paddr = paddr, .size = size};
  uint64_t physAddr;
  if (getPhysAddr((uint64_t)&readArgs, 0, &physAddr) == FAIL) panic("hp_read failed");
  if (hypercall(HP_READ, physAddr) == HP_FAIL) return FAIL;
  return SUCCESS;
}

uint64_t hp_write(uint64_t fd, uint64_t paddr, uint64_t size) {
  HYPER_READ writeArgs = {.fd = fd, .paddr = paddr, .size = size};
  uint64_t physAddr;
  if (getPhysAddr((uint64_t)&writeArgs, 0, &physAddr) == FAIL) panic("hp_read failed");
  if (hypercall(HP_WRITE, physAddr) == HP_FAIL) return FAIL;
  return SUCCESS;
}

void __attribute__((noreturn)) hp_exit(uint64_t status) {
  uint64_t physAddr;
  if (getPhysAddr((uint64_t)&status, 0, &physAddr) == FAIL) panic("hp_read failed");
  hypercall(HP_EXIT, physAddr);
  while(1); //surpress warning
}

uint64_t hp_digestGenerate(uint64_t dataLen, uint8_t *data, uint8_t *digest) {
  HYPER_DIGEST digestReq;
  uint64_t physAddr;
  digestReq.dataLen = dataLen;
  memcpy((uint64_t)digestReq.data, (uint64_t)data, dataLen);
  if (getPhysAddr((uint64_t)&digestReq, 0, &physAddr) == FAIL) panic("hp_digestGenerate failed");
  if (hypercall(HP_DIGEST_GENERATE, physAddr) == HP_FAIL) return FAIL;
  memcpy((uint64_t)digest, (uint64_t)digestReq.digest, DIGEST_SIZE);
  return SUCCESS;
}

uint64_t hp_signatureValidate(uint8_t *digest, uint8_t *n, uint8_t *e, uint8_t *signature) {
  HYPER_SIGNATURE signatureReq;
  uint64_t physAddr;
  memcpy((uint64_t)signatureReq.digest, (uint64_t)digest, DIGEST_SIZE);
  memcpy((uint64_t)signatureReq.pubkeyN, (uint64_t)n, SIGNATURE_SIZE);
  memcpy((uint64_t)signatureReq.pubkeyE, (uint64_t)e, SIGNATURE_SIZE);
  memcpy((uint64_t)signatureReq.signature, (uint64_t)signature, SIGNATURE_SIZE);
  if (getPhysAddr((uint64_t)&signatureReq, 0, &physAddr) == FAIL) panic("hp_signatureValidate failed");
  if (hypercall(HP_SIGNATURE_VALIDATE, physAddr) == HP_FAIL) return FAIL;
  return SUCCESS;
}

uint64_t hp_appletRegisterValidate(uint64_t codeLen, uint8_t *code, uint8_t *authoritySignature) {
  HYPER_APPLET applet;
  uint64_t physAddr;
  applet.codeLen = codeLen;
  memcpy((uint64_t)applet.code, (uint64_t)code, codeLen);
  memset((uint64_t)&applet.code[codeLen], '\0', APPLET_SIZE_MAX - codeLen);
  memcpy((uint64_t)applet.authoritySignature, (uint64_t)authoritySignature, SIGNATURE_SIZE);
  if (getPhysAddr((uint64_t)&applet, 0, &physAddr) == FAIL) panic("hp_appletRegisterValidate failed");
  if (hypercall(HP_APPLET_REGISTER_VALIDATE, physAddr) == HP_FAIL) return FAIL;
  return SUCCESS;
}

uint64_t hp_appletInvoke(APPLET_ID caller, APPLET_TASK_ID task, uint64_t codeLen, uint64_t code, uint64_t authoritySignature, uint64_t dataLen, uint8_t *data, uint64_t storage) {
  HYPER_APPLET_INVOKE invokeReq;
  uint64_t physAddr;
  invokeReq.applet.codeLen = codeLen;
  invokeReq.task = task;
  invokeReq.caller = caller;
  memcpy((uint64_t)invokeReq.applet.code, code, codeLen);
  memset((uint64_t)&invokeReq.applet.code[codeLen], '\0', APPLET_SIZE_MAX - codeLen);
  memcpy((uint64_t)invokeReq.applet.authoritySignature, authoritySignature, SIGNATURE_SIZE);
  invokeReq.dataLen = dataLen;
  memcpy((uint64_t)invokeReq.data, (uint64_t)data, dataLen);
  memset((uint64_t)&invokeReq.data[dataLen], '\0', APPLET_ARG_SIZE_MAX - dataLen);
  memcpy((uint64_t)invokeReq.storage, storage, APPLET_STORAGE_SIZE);
  if (getPhysAddr((uint64_t)&invokeReq, 0, &physAddr) == FAIL) panic("hp_appletInvoke failed");
  return hypercall(HP_APPLET_INVOKE, physAddr);
}

uint64_t hp_appletResume(APPLET_TASK_ID task, APPLET_CONTEXT *context, uint64_t callResLen, uint8_t *callRes) {
  HYPER_APPLET_RESUME resumeReq;
  uint64_t physAddr;
  resumeReq.context.task = task;
  memcpy((uint64_t)resumeReq.context.regs, (uint64_t)context->regs, sizeof(uint64_t) * APPLET_REG_CNT);
  memcpy((uint64_t)resumeReq.context.memory, (uint64_t)context->memory, APPLET_CONTEXT_MEMORY_SIZE);
  resumeReq.resLen = callResLen;
  memcpy((uint64_t)resumeReq.res, (uint64_t)callRes, callResLen);
  memset((uint64_t)&resumeReq.res[callResLen], '\0', APPLET_RES_SIZE_MAX - callResLen);
  if (getPhysAddr((uint64_t)&resumeReq, 0, &physAddr) == FAIL) panic("hp_appletResume failed");
  return hypercall(HP_APPLET_RESUME, physAddr);
}

uint64_t hp_appletspaceFlag() {
  if (hypercall(HP_APPLETSPACE_FLAG, 9) == HP_FAIL) return FAIL;
  return SUCCESS;
}

uint64_t hp_userspaceFlag() {
  if (hypercall(HP_USERSPACE_FLAG, 0) == HP_FAIL) return FAIL;
  return SUCCESS;
}
