#ifndef __ENCRYPTOR_H__
#define __ENCRYPTOR_H__

#include <string.h>
#include <stdlib.h>
#include <openssl/evp.h>
#include <openssl/aes.h>

#define PATH_KEY "/secret.key"
#define LEN_KEY  0x10
#define LEN_PATH 0x100

int encrypt(int size, char *input, char *key, char **output);

#endif
