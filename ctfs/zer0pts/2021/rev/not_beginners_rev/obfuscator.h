#define DEF_ARG(func, T, var)                   \
  T __obfuscated_##func##var
#define DEF_FUNC(func, body) {                  \
  goto __obfuscated_##func##skip;                       \
__obfuscated_##func: body;                              \
  __obfuscated_##func##skip:;                           \
  }
#define ARG(func, var) __obfuscated_##func##var
#define CALL(func)                                                \
  ({                                                              \
    __label__ r;                                                  \
    __stack_shadow[__stack_depth++] = &&r;                        \
    goto __obfuscated_##func;                                     \
  r:                                                              \
    __return_value;                                               \
  })
#define RET(val)                                                        \
  __return_value = (void*)(val); goto *__stack_shadow[--__stack_depth]
#define STACK_MAX 0x100

int __stack_depth = 0;
void *__return_value = NULL;
void *__stack_shadow[STACK_MAX];
