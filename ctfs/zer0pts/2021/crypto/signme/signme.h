#ifndef SIGNME_H
#define SIGNME_H

#include <cstdint>
#include <gmp.h>
#include <gmpxx.h>

#define SECURITY_PARAMETER (1024)

extern gmp_randstate_t rstate;

typedef struct {
  mpz_t p;
  mpz_t q;
  mpz_t n;
  mpz_t e;
  mpz_t d;
} PrivateKey;

typedef struct {
  mpz_t e;
  mpz_t n;
} PublicKey;

void generate_keypair(PublicKey*, PrivateKey*);
void generate_signature(mpz_t, mpz_t, PrivateKey*);
int validate_signature(mpz_t, mpz_t, PublicKey*);

#endif
