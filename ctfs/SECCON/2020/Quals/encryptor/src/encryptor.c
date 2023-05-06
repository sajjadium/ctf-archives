#include "encryptor.h"

int encrypt(int size, char *input, char *key, char **output) {
  int c_len, pad;
  EVP_CIPHER_CTX *ctx;

  /* assert key is properly set */
  if (strlen(key) != EVP_CIPHER_key_length(EVP_aes_128_ecb()))
    return -1;

  /* initialize AES-128-ECB */
  ctx = EVP_CIPHER_CTX_new();
  if (ctx == NULL)
    return -1;
  EVP_CIPHER_CTX_init(ctx);
  EVP_EncryptInit_ex(ctx, EVP_aes_128_ecb(), NULL, key, NULL);

  /* allocate output buffer */
  c_len = size + EVP_MAX_BLOCK_LENGTH;
  *output = calloc(sizeof(char), c_len);
  if (*output == NULL) {
    EVP_CIPHER_CTX_free(ctx);
    return -1;
  }

  /* encrypt */
  EVP_EncryptUpdate(ctx,
                    (unsigned char*)*output,
                    &c_len,
                    (unsigned char*)input,
                    size);
  EVP_EncryptFinal_ex(ctx, (unsigned char*)(*output + c_len), &pad);

  /* cleanup */
  EVP_CIPHER_CTX_cleanup(ctx);
  EVP_CIPHER_CTX_free(ctx);

  return (c_len + LEN_KEY) & ~0xf;
}
