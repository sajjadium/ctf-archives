#pragma once

#include "types.h"

extern "C" int64 __divdi3(int64 num, int64 den);
extern "C" uint64 __udivdi3(uint64 num, uint64 den);
extern "C" uint64 __umoddi3(uint64 a, uint64 b);
extern "C" uint64 __udivmoddi4(uint64 num, uint64 den, uint64 *rem_p);

