// WARNING: You are looking for a different types.h - this one is just for the exe2minixfs tool!
#ifdef EXE2MINIXFS
#pragma once

#define ArchThreads

#include <stdint.h>
#include <string.h>
#include <sys/types.h>

#define ustl std

#include "../../common/include/console/debug.h"

typedef int8_t int8;
typedef uint8_t uint8;

typedef int16_t int16;
typedef uint16_t uint16;

typedef int32_t int32;
typedef uint32_t uint32;

typedef uint64_t uint64;
typedef int64_t int64;

typedef void* pointer;

typedef uint64_t l_off_t;

class FileSystemInfo;

size_t atomic_add(size_t& x,size_t y);

#endif
