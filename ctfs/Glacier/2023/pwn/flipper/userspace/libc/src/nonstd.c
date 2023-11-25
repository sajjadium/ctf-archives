#include "nonstd.h"
#include "sys/syscall.h"
#include "../../../common/include/kernel/syscall-definitions.h"
#include "stdlib.h"

int createprocess(const char* path, int sleep)
{
  return __syscall(sc_createprocess, (long) path, sleep, 0x00, 0x00, 0x00);
}

int flipBit(const void* address, int bit_num)
{
    return __syscall(sc_flip_bit, (long) address, bit_num, 0, 0, 0);
}


extern int main();

void _start()
{
  exit(main());
}
