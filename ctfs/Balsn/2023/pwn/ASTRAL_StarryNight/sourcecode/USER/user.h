#ifndef __USER_HEADER__
#define __USER_HEADER__

#include <stddef.h>
#include <stdint.h>
#include "lib.h"
#include "syscall.h"
#include "applet.h"

#define SUCCESS 0
#define FAIL 0xffffffffffffffff

typedef struct ACTIVITY_STAT {
  uint64_t registerCnt;
  uint64_t invokeCnt;
  uint64_t unregisterCnt;
  uint64_t inspectCnt;
  uint64_t resultCnt;
} ACTIVITY_STAT;

typedef struct USER {
  uint64_t usernameLen;
  uint64_t passwordLen;
  uint8_t username[0x100];
  uint8_t password[0x100];
  ACTIVITY_STAT stat;
} USER;

void __attribute__((noreturn)) userMain();

#endif
