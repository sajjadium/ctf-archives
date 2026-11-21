#include "backtrace.h"
#include "Thread.h"

pointer getCalledBefore(size_t offset)
{
  // this function calls the backtrace function, so increase the backtrace depth
  offset += 2;
  pointer call_stack[offset];
  call_stack[offset-1] = 0;
  if((size_t)backtrace(call_stack, offset, currentThread, false) == offset)
  {
    return call_stack[offset-1];
  }
  return 0;
}
