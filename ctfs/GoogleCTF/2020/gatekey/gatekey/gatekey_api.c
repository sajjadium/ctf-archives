#include "internal.h"

static void *memcpy(void *dst, const void *src, unsigned long len) {
  asm volatile(
    "rep movsb\n\t"
  : //out
    "+D"(dst),
    "+S"(src),
    "+c"(len)
  : //in
  : //clobber
    "cc", "memory"
  );
  return dst;
}

int gatekey_open(char *path, char *authkey) {
  struct gatekey_args args = {
    .op = GATEKEY_OP_OPEN,
    .path = path
  };
  memcpy(&args.authkey, authkey, 64);
  return gatekey_call(&args);
}

int gatekey_create(char *path, char *authkey_out) {
  struct gatekey_args args = {
    .op = GATEKEY_OP_CREATE,
    .path = path
  };
  int res = gatekey_call(&args);
  memcpy(authkey_out, &args.authkey, 64);
  return res;
}
