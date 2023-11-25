#pragma once

#include "arch_backtrace.h"

/**
 * Get the pointer where the current function has been called from.
 * @param offset the call depth
 *        0 ... the point where this function has been called
 *        1 ... the point where the calling function has been called from
 *        x ... the point where the x'th function call happened
 * @return the call pointer  in case it could be resolved
 * @return 0 in case the call could not be resolved
 */
pointer getCalledBefore(size_t offset);

