#include"syscall.h"

uint64_t syscall(uint64_t a1, uint64_t a2, uint64_t a3, uint64_t a4, uint64_t a5, uint64_t a6, uint64_t a7) {
  SYSCALL_REGS args = {
    .A1 = a1,
    .A2 = a2,
    .A3 = a3,
    .A4 = a4,
    .A5 = a5,
    .A6 = a6,
    .A7 = a7,
    .R1 = 0
  };
  asm(
    "mov rax, %[args];"
    "push rax;"
    "mov rdi, [rax + 0x08];"
    "mov rsi, [rax + 0x10];"
    "mov rdx, [rax + 0x18];"
    "mov r10, [rax + 0x20];"
    "mov r8,  [rax + 0x28];"
    "mov r9,  [rax + 0x30];"
    "mov rax, [rax + 0x00];"
    "syscall;"
    "pop rdi;"
    "mov [rdi + 0x38], rax;"
    :
    : [args] "r" (&args)
    : "rax", "rdi", "rsi", "rdx", "r10", "r8", "r9"
  );
  return args.R1;
}

uint64_t read(uint32_t fd, uint8_t *buffer, uint64_t size) {
  return syscall4(SYS_READ, fd, buffer, size);
}

uint64_t write(uint32_t fd, uint8_t *buffer, uint64_t size) {
  return syscall4(SYS_WRITE, fd, buffer, size);
}

void *mmap(void *addr, uint64_t size, uint64_t prot, uint64_t flag, uint64_t fd, uint64_t off) {
  return (void*)syscall7(SYS_MMAP, addr, size, prot, flag, fd, off); 
}

uint64_t munmap(void *addr, uint64_t len) {
  return syscall3(SYS_MUNMAP, addr, len);
}

void __attribute__((noreturn)) exit(uint64_t status) {
  syscall2(SYS_EXIT, status);
  while(1); //surpress warning
}

uint64_t appletRegister(APPLET_REGISTER_REQ *req, APPLET_ID *id) {
  return (APPLET_ID)syscall3(SYS_APPLET_REGISTER, req, id);
}

uint64_t appletUnregister(APPLET_UNREGISTER_REQ *req) {
  return syscall2(SYS_APPLET_UNREGISTER, req);
}

uint64_t appletInvoke(APPLET_INVOKE_REQ *req, APPLET_RECEIPT *receipt) {
  return syscall3(SYS_APPLET_INVOKE, req, receipt);
}

uint64_t appletResult(APPLET_RECEIPT *receipt, APPLET_RESULT *result) {
  return syscall3(SYS_APPLET_RESULT, receipt, result);
}

uint64_t appletStorage(APPLET_STORAGE_REQ *req, APPLET_STORAGE *storage) {
  return syscall3(SYS_APPLET_STORAGE, req, storage);
}
