#include "sys/mman.h"

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
void* mmap(void* start, size_t length, int prot, int flags, int fd,
           off_t offset)
{
  return 0;
}

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
int munmap(void* start, size_t length)
{
  return -1;
}

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
int shm_open(const char* name, int oflag, mode_t mode)
{
  return -1;
}

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
int shm_unlink(const char* name)
{
  return -1;
}

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
int mprotect(void *addr, size_t len, int prot)
{
  return -1;
}

