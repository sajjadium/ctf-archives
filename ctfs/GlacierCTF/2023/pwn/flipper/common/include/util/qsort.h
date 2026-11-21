#pragma once

#include "types.h"

void qsort(void* base, size_t nitems, size_t size, int (*compar)(const void *, const void*));
