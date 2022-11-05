#include "util.h"
#ifndef FUSE_USE_VERSION
#define FUSE_USE_VERSION 31
#endif
#include "fuse.h"
#include <stdarg.h>
#include <stddef.h>
#include <execinfo.h>
#include <unistd.h>

void err_exit(const char* msg, ...) {
  char buf[128] = "\033[1;91m[-]\033[0m \033[91mmyfuse fatal error:\033[0m ";
  va_list arg;
  va_start(arg, msg);
  strncat(buf, msg, 127);
  strncat(buf, "\n", 127);
  vfprintf(stderr, buf, arg);
  va_end(arg);

  void* array[10];
  size_t size;

  // get void*'s for all entries on the stack
  size = backtrace(array, 10);

  // print out all the frames to stderr
  fprintf(stderr, "back trace:\n");
  backtrace_symbols_fd(array, size, STDERR_FILENO);

  exit(1);
}

void myfuse_debug_log(const char* msg, ...) {
#ifdef VERBOSE
  char buf[128] = "\033[1;92m[+]\033[0m \033[92mmyfuse debug log:\033[0m ";
  va_list arg;
  va_start(arg, msg);
  strncat(buf, msg, 127);
  strncat(buf, "\n", 127);
  vfprintf(stdout, buf, arg);
  va_end(arg);
#endif
}

void myfuse_log(const char* msg, ...) {
  char buf[128] = "\033[1;92m[+]\033[0m \033[92mmyfuse log:\033[0m ";
  va_list arg;
  va_start(arg, msg);
  strncat(buf, msg, 127);
  strncat(buf, "\n", 127);
  vfprintf(stdout, buf, arg);
  va_end(arg);
}

void myfuse_nonfatal(const char* msg, ...) {
  char buf[128] = "\033[1;93m[!]\033[0m \033[93mmyfuse nonfatal error:\033[0m ";
  va_list arg;
  va_start(arg, msg);
  strncat(buf, msg, 127);
  strncat(buf, "\n", 127);
  vfprintf(stderr, buf, arg);
  va_end(arg);
}

#ifdef __GNUC__
#pragma weak fuse_get_context
#endif
struct myfuse_state* get_myfuse_state() {
  return (struct myfuse_state*)fuse_get_context()->private_data;
}

void get_current_timespec(struct timespec* t) { timespec_get(t, TIME_UTC); }
