#ifndef __SYSCALL_HEADER__
#define __SYSCALL_HEADER__

#include <stdint.h>
#include "applet.h"

#define SYS_READ              0x0
#define SYS_WRITE             0x1
#define SYS_MMAP              0x9
#define SYS_MUNMAP            0xb
#define SYS_EXIT              0x3c
#define SYS_APPLET_REGISTER   0xffff0000
#define SYS_APPLET_UNREGISTER 0xffff0001
#define SYS_APPLET_INVOKE     0xffff0002
#define SYS_APPLET_RESULT     0xffff0003
#define SYS_APPLET_STORAGE    0xffff0004
#define SYS_FLAG              0xf1a9f1a9

#define SYS_SUCCESS 0
#define SYS_FAIL 0xffffffffffffffff

#define MAP_PRIVATE 0x02
#define MAP_ANONYMOUS 0x20

#define PROT_READ 0x01
#define PROT_WRITE 0x02

#define STDIN_FILENO 0
#define STDOUT_FILENO 1

typedef struct SYSCALL_REGS {
  uint64_t A1;
  uint64_t A2;
  uint64_t A3;
  uint64_t A4;
  uint64_t A5;
  uint64_t A6;
  uint64_t A7;
  uint64_t R1;
} SYSCALL_REGS;

uint64_t syscall(uint64_t a1, uint64_t a2, uint64_t a3, uint64_t a4, uint64_t a5, uint64_t a6, uint64_t a7);
#define syscall7(a1, a2, a3, a4, a5, a6, a7) syscall((uint64_t)(a1), (uint64_t)(a2), (uint64_t)(a3), (uint64_t)(a4), (uint64_t)(a5), (uint64_t)(a6), (uint64_t)(a7))
#define syscall6(a1, a2, a3, a4, a5, a6) syscall7((a1), (a2), (a3), (a4), (a5), (a6), 0)
#define syscall5(a1, a2, a3, a4, a5) syscall6((a1), (a2), (a3), (a4), (a5), 0)
#define syscall4(a1, a2, a3, a4) syscall5((a1), (a2), (a3), (a4), 0)
#define syscall3(a1, a2, a3) syscall4((a1), (a2), (a3), 0)
#define syscall2(a1, a2) syscall3((a1), (a2), 0)
#define syscall1(a1) syscall2((a1), 0)
uint64_t read(uint32_t fd, uint8_t *buffer, uint64_t size);
uint64_t write(uint32_t fd, uint8_t *buffer, uint64_t size);
void *mmap(void *addr, uint64_t size, uint64_t prot, uint64_t flag, uint64_t fd, uint64_t off);
uint64_t munmap(void *addr, uint64_t len);
void __attribute__((noreturn)) exit(uint64_t status);
uint64_t appletRegister(APPLET_REGISTER_REQ *req, APPLET_ID *id);
uint64_t appletUnregister(APPLET_UNREGISTER_REQ *req);
uint64_t appletInvoke(APPLET_INVOKE_REQ *req, APPLET_RECEIPT *receipt);
uint64_t appletResult(APPLET_RECEIPT *receipt, APPLET_RESULT *result);
uint64_t appletStorage(APPLET_STORAGE_REQ *req, APPLET_STORAGE *storage);

#endif
