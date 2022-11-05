#pragma once
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

void err_exit(const char* msg, ...);

void myfuse_debug_log(const char* msg, ...);

void myfuse_log(const char* msg, ...);

void myfuse_nonfatal(const char* msg, ...);

struct myfuse_state* get_myfuse_state()
    // weak symbol to make the test suite can rewrite the get_myfuse_state
    // to provide state with no need to start a fuse runtime
    __attribute__((weak));

#define MYFUSE_STATE (get_myfuse_state())

#define ROUNDUP(x, align) (((x) + align - 1) & ~(align - 1))
#define ROUNDDOWN(x, align) (((x)) & ~(align - 1))

#ifdef DEBUG
#define DEBUG_TEST(statements) \
  do {                         \
    statements                 \
  } while (0)
#else
#define DEBUG_TEST(statements)
#endif

void get_current_timespec(struct timespec* t);
