/*
 * This is a demo program to show how to interact with ATOMS.
 * Don't waste time on finding bugs here ;)
 *
 * Copyright (c) 2020 david942j
 */

#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/mman.h>

#include <linux/atoms.h>

#define DEV_PATH "/dev/atoms"
#define TOKEN 0xdeadbeef

static void child_work() {
  int fd = open(DEV_PATH, O_RDWR);
  assert(fd >= 0);
  assert(ioctl(fd, ATOMS_USE_TOKEN, TOKEN) == 0);
  void *ptr = mmap(0, 0x1000, PROT_READ, MAP_SHARED, fd, 0);
  assert(ptr != MAP_FAILED);
  printf("[child] Message from parent: %s\n", (char*) ptr);
  assert(ioctl(fd, ATOMS_RELEASE) == 0);
  munmap(ptr, 0x1000);
  close(fd);
}

static void parent_work() {
  int fd = open(DEV_PATH, O_RDWR);
  assert(fd >= 0);
  assert(ioctl(fd, ATOMS_USE_TOKEN, TOKEN) == 0);
  struct atoms_ioctl_alloc arg = {
    .size = 0x1000,
  };
  assert(ioctl(fd, ATOMS_ALLOC, &arg) == 0);
  void *ptr = mmap(0, 0x1000, PROT_WRITE, MAP_SHARED, fd, 0);
  assert(ptr != MAP_FAILED);
  strcpy((char*)ptr, "the secret message left by parent");
  munmap(ptr, 0x1000);
  close(fd);
  puts("[parent] Message left.");
}

int main(int argc, char *argv[]) {
  if (argc == 1) {
    parent_work();
    char * newarg[] = { argv[0], "child", NULL };
    execv(argv[0], newarg);
  } else {
    child_work();
  }
  return 0;
}
