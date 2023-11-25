#include "libgcc.h"
#include "kprintf.h"
#include "assert.h"

int64 __divdi3(int64 num, int64 den)
{
  int minus = 0;
  int64 v;

  if ( num < 0 )
  {
    num = -num;
    minus = 1;
  }
  if ( den < 0 )
  {
    den = -den;
    minus ^= 1;
  }

  v = __udivmoddi4(num, den, 0);
  if ( minus )
    v = -v;

  return v;
}


uint64 __udivdi3(uint64 num, uint64 den)
{
  return __udivmoddi4(num, den, 0);
}

uint64 __umoddi3(uint64 a, uint64 b)
{
  uint64 r;
  __udivmoddi4(a, b, &r);
  return r;
}

uint64 __udivmoddi4(uint64 num, uint64 den, uint64 *rem_p)
{
  uint64 quot = 0, qbit = 1;
  assert(den && "division by zero");

  while ( (int64)den >= 0 )
  {
    den <<= 1;
    qbit <<= 1;
  }

  while ( qbit )
  {
    if ( den <= num )
    {
      num -= den;
      quot += qbit;
    }
    den >>= 1;
    qbit >>= 1;
  }

  if ( rem_p )
    *rem_p = num;

  return quot;
}
