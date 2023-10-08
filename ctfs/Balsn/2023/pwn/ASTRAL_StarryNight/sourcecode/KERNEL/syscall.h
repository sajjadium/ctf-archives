#ifndef __SYSCALL_HEADER__
#define __SYSCALL_HEADER__

#include <stdint.h>
#include <stdbool.h>
#include "const.h"
#include "kernel.h"
#include "panic.h"
#include "memory.h"
#include "applet.h"
#include "hypercall.h"

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
#define MAP_FIXED 0x10
#define MAP_ANONYMOUS 0x20
#define MAP_MASK 0x32

#define PROT_READ 0x01
#define PROT_WRITE 0x02
#define PROT_MASK 0x03

#define STDIN_FILENO 0
#define STDOUT_FILENO 1

uint64_t syscallHandler(uint64_t a1, uint64_t a2, uint64_t a3, uint64_t a4, uint64_t a5, uint64_t a6);
uint64_t sys_read(uint64_t fd, uint64_t ubuf, uint64_t size);
uint64_t sys_write(uint64_t fd, uint64_t ubuf, uint64_t size);
uint64_t sys_mmap(uint64_t vaddr, uint64_t size, uint64_t prot, uint64_t flag, uint64_t fd, uint64_t off);
uint64_t sys_munmap(uint64_t vaddr, uint64_t size);
void __attribute__((noreturn)) sys_exit(uint64_t status);
uint64_t sys_appletRegister(uint64_t ureq, uint64_t ures);
uint64_t sys_appletUnregister(uint64_t ureq);
uint64_t sys_appletInvoke(uint64_t ureq, uint64_t ures);
uint64_t sys_appletResult(uint64_t ureq, uint64_t ures);
uint64_t sys_appletInspectStorage(uint64_t ureq, uint64_t ures);
uint64_t sys_flag();

#endif
