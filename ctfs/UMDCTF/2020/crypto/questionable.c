#include <stdlib.h>
#include <string.h>
#include <openssl/evp.h>
#include <openssl/conf.h>
#include <openssl/err.h>
 
int read_file(char * buffer, FILE *f, int length) {
  int i = 0;
  char c = 0;

  if (f == NULL) 
    return 1;

  for(i = 0; i < length; i++) {
    c = fgetc(f);
    if (feof(f)) 
      break;
    buffer[i] = c;
  }

  return 0;
}

void handleErrors() {
  ERR_print_errors_fp(stderr);
  abort();
}

int encrypt(unsigned char *plaintext, int plaintext_len, unsigned char *key,
            unsigned char *iv, unsigned char *ciphertext) {
  EVP_CIPHER_CTX *ctx;
  int len;
  int ciphertext_len;
  
  if(!(ctx = EVP_CIPHER_CTX_new()))
    handleErrors();

  if(1 != EVP_EncryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key, iv)) 
    handleErrors();

  if(1 != EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len))
    handleErrors();
  ciphertext_len = len;

  if(1 != EVP_EncryptFinal_ex(ctx, ciphertext + len, &len)) 
    handleErrors();
  ciphertext_len += len;

  EVP_CIPHER_CTX_free(ctx);
  return ciphertext_len;
}

int main(int argc, char * argv[]) {
  unsigned char key[32] = {0}, iv[16] = {0}, flag[64] = {0}, ctxt[128] = {0};
  FILE *i = NULL, *f = NULL;
  int result = 0, clen = 0;

  setbuf(stdout, NULL);

  f = fopen("flag.txt", "r");
  i = fopen("/dev/urandom", "r");  
  
  result = read_file(flag, f, 64);
  result = read_file(iv, i, 16);
  
  strncpy(key, "HARCODED KEY CAUSE IM LAZY TODAY", 32);
  clen = encrypt(flag, strlen(flag), key, iv, ctxt);

  printf("Pretty Ciphertext: \n");
  BIO_dump_fp (stdout, (const char *)ctxt, clen);
  
  fclose(f);
  fclose(i);
  
  return 0;
}
