#include "sched.h"
#include "sys/syscall.h"
#include "../../../common/include/kernel/syscall-definitions.h"

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
int sched_yield(void)
{
  return __syscall(sc_sched_yield, 0x00, 0x00, 0x00, 0x00, 0x00);
}
