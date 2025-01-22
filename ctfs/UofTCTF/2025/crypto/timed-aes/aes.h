#include <stdlib.h>

// expects 16 byte of key and 16 byte of msg and 16 byte space for enc
void aesBlockEncrypt(u_int8_t *key, const u_int8_t *msg, u_int8_t *enc);
void aesBlockDecrypt(u_int8_t *key, const u_int8_t *enc, u_int8_t *msg);
void keyExpand(u_int8_t *key, u_int8_t *exp);