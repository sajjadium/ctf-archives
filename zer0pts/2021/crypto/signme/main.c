#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "signme.h"

void authenticated(void) {
  puts("Thank you for signing my message!");
  system("/bin/sh");
}

void fatal(const char *msg) {
  fputs(msg, stderr);
  exit(1);
}

/**
 * Pad message with PKCS1 v1.5
 */
char* pad_pkcs1_v15(char *msg, int s, int n) {
  mpz_t r;
  char *padded;
  int i, rlen = n - s - 3;

  /* Initialize */
  mpz_init(r);
  padded = (char*)malloc(n);
  memcpy(&padded[3 + rlen], msg, s);

  /* Generate PS */
  msg = (char*)realloc(msg, rlen);
  for(i = 0; i < rlen; i++) {
    do {
      mpz_urandomb(r, rstate, 8);
    } while(mpz_cmp_ui(r, 0) == 0);
    msg[i] = mpz_get_ui(r);
  }

  /* PKCS thing */
  padded[rlen + 2] = '\x00';
  padded[0] = '\x00';
  padded[1] = '\x02';
  memcpy(&padded[2], msg, rlen);

  mpz_clear(r);
  return padded;
}

/**
 * Read message
 */
void get_message(mpz_t m) {
  char *padded, *msg;
  size_t s;

  /* Read message */
  msg = (char*)malloc(SECURITY_PARAMETER / 8);
  
  printf("Message: ");
  if ((s = read(0, msg, SECURITY_PARAMETER / 8)) <= 0)
    fatal("I/O Error\n");
  if (msg[s-1] == '\n') msg[--s] = '\0';

  /* Pad message */
  padded = pad_pkcs1_v15(msg, s, SECURITY_PARAMETER / 8);

  /* Bytes to integer */
  mpz_import(m, 1, 1, SECURITY_PARAMETER / 8, 1, 0, padded);
  free(padded);
  free(msg);
}

/**
 * Entry Point
 */
int main(void) {
  mpz_t m, s;
  PrivateKey priv;
  PublicKey pub;

  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  alarm(60);

  /* Step 0. Key generation */
  generate_keypair(&pub, &priv);
  mpz_inits(s, m, NULL);

  /* Step 1. I'll sign your message */
  get_message(m);
  gmp_printf("m = %Zx\n", m);
  generate_signature(s, m, &priv);
  gmp_printf("pubkey = (%Zx, %Zx)\n", pub.n, pub.e);
  gmp_printf("signature = %Zx\n", s);

  /* Step 2. You'll sign my message */
  mpz_urandomb(m, rstate, SECURITY_PARAMETER);
  gmp_printf("Sign this message: %Zx\n", m);
  printf("Signature: ");
  if (gmp_scanf("%Zx", s) != 1) fatal("I/O Error\n");

  /* Step 3. I'll validate your signature */
  if (validate_signature(s, m, &pub) == 0) {
    authenticated();
  } else {
    puts("Nope.");
  }

  return 0;
}
