#include <err.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stddef.h>

#define INSN_ENDBR64 (0xF30F1EFA) /* endbr64 */
#define CFI(f)                                              \
  ({                                                        \
    if (__builtin_bswap32(*(uint32_t*)(f)) != INSN_ENDBR64) \
      __builtin_trap();                                     \
    (f);                                                    \
  })

#define KEY_SIZE 0x20
typedef struct {
  char key[KEY_SIZE];
  char buf[KEY_SIZE];
  const char *error;
  int status;
  void (*throw)(int, const char*, ...);
} ctx_t;

void read_member(ctx_t *ctx, off_t offset, size_t size) {
  if (read(STDIN_FILENO, (void*)ctx + offset, size) <= 0) {
    ctx->status = EXIT_FAILURE;
    ctx->error = "I/O Error";
  }
  ctx->buf[strcspn(ctx->buf, "\n")] = '\0';

  if (ctx->status != 0)
    CFI(ctx->throw)(ctx->status, ctx->error);
}

void encrypt(ctx_t *ctx) {
  for (size_t i = 0; i < KEY_SIZE; i++)
    ctx->buf[i] ^= ctx->key[i];
}

int main() {
  ctx_t ctx = { .error = NULL, .status = 0, .throw = err };

  read_member(&ctx, offsetof(ctx_t, key), sizeof(ctx));
  read_member(&ctx, offsetof(ctx_t, buf), sizeof(ctx));

  encrypt(&ctx);
  write(STDOUT_FILENO, ctx.buf, KEY_SIZE);

  return 0;
}
