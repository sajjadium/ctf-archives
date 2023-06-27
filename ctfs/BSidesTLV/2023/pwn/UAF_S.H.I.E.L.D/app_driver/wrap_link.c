#include <assert.h>
#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/types.h>

#include "uaf_shield_ioctl.h"
#define PTR_MASK ((1ull << 47) - 1)

void* __real_malloc(size_t size);
void* __real_realloc(void*, size_t);
void __real_free(void* size);

static int fd;

__attribute__((constructor)) static void open_fd() {
  fd = open("/dev/" DEV, O_RDWR);
}

void* ioctl_malloc(void* ptr, size_t size) {
  if (ptr != NULL) {
    alloc_ptr_t aptr = {0};
    aptr.virt_in = (uint64_t)ptr;
    aptr.alloc_size = (uint64_t)size;
    int res = ioctl(fd, IOCTL_ALLOC_PTR, &aptr);
    if (res < 0) {
      printf("Error ioctl IOCTL_ALLOC_PTR\n");
      return NULL;
    }
    ptr = (void*)aptr.virt_out;
  }
  return ptr;
}

void* __wrap_malloc(size_t size) {
  void* ptr = NULL;
  ptr = __real_malloc(size);
  ptr = ioctl_malloc(ptr, size);
  return ptr;
}

void* ioctl_free(void* ptr) {
  free_ptr_t aptr = {0};
  aptr.virt_in = (uint64_t)ptr;
  int res = ioctl(fd, IOCTL_FREE_PTR, &aptr);
  if (res < 0) {
    printf("Error ioctl IOCTL_ALLOC_PTR\n");
    return NULL;
  }
  return (void*)aptr.virt_out;
}

void __wrap_free(void* ptr) {
  if (ptr == NULL) {
    __real_free(ptr);
    return;
  }
  ptr = ioctl_free(ptr);
  __real_free(ptr);
}

void* __wrap_realloc(void* ptr, size_t size) {
  free_ptr_t aptr = {0};
  if (ptr == NULL) {
    return __wrap_malloc(size);
  }
  ptr = __real_realloc(ioctl_free(ptr), size);
  return ioctl_malloc(ptr, size);
}