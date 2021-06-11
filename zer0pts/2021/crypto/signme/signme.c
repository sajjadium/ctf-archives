#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include "signme.h"

gmp_randstate_t rstate;

/**
 * Generate a random n-bit prime
 * @param mpz_t    p Prime integer
 * @param uint32_t n Bit length of prime to generate
 */
void _get_prime(mpz_t p, uint32_t n) {
  mpz_t r;
  mpz_init(r);
  do {
    mpz_urandomb(r, rstate, n);
    mpz_setbit(r, n - 1);
    mpz_nextprime(p, r);
  } while(mpz_sizeinbase(p, 2) >= n + 1);
  mpz_clear(r);
}

/**
 * Generate a pair of keys for signature
 * @param PublicKey  pub      Pointer to the public key instance
 * @param PrivateKey priv     Pointer to the private key instance
 */
void generate_keypair(PublicKey *pub, PrivateKey *priv) {
  mpz_t phi, pm, qm;
  mpz_inits(phi, pm, qm, NULL);

  /* Generate private key*/
  mpz_inits(priv->p, priv->q, priv->n, priv->e, priv->d, NULL);
  mpz_set_ui(priv->e, 65537UL);
  _get_prime(priv->p, SECURITY_PARAMETER);
  _get_prime(priv->q, SECURITY_PARAMETER);
  mpz_mul(priv->n, priv->p, priv->q);
  mpz_sub_ui(pm, priv->p, 1UL);
  mpz_sub_ui(qm, priv->q, 1UL);
  mpz_mul(phi, pm, qm);
  mpz_invert(priv->d, priv->e, phi);

  /* Generate public key */
  mpz_init_set(pub->e, priv->e);
  mpz_init_set(pub->n, priv->n);

  /* Cleanup */
  mpz_clears(phi, pm, qm, NULL);
}

/**
 * Sign a message
 * @param mpz_t      sign Signature to be generated
 * @param mpz_t      m    Message
 * @param PrivateKey priv Pointer to an initialized private key
 */
void generate_signature(mpz_t sign, mpz_t m, PrivateKey *priv) {
  mpz_t sp, sq, qi;
  mpz_init2(sp, SECURITY_PARAMETER);
  mpz_init2(sq, SECURITY_PARAMETER);
  mpz_init2(qi, SECURITY_PARAMETER);

  mpz_powm(sp, m, priv->d, priv->p);
  mpz_powm(sq, m, priv->d, priv->q);
  mpz_invert(qi, priv->q, priv->p);
  mpz_sub(sign, sp, sq);
  mpz_mul(sign, sign, qi);
  mpz_mod(sign, sign, priv->p);
  mpz_mul(sign, sign, priv->q);
  mpz_add(sign, sign, sq);
  mpz_mod(sign, sign, priv->n);

  mpz_clears(sp, sq, NULL);
}

/**
 * Validate a signature
 * @param mpz_t     sign Signature of messasge
 * @param mpz_t     m    Message to validate
 * @param PublicKey pub  Pointer to public key
 */
int validate_signature(mpz_t sign, mpz_t m, PublicKey *pub) {
  int r;
  mpz_t w;

  mpz_init(w);
  mpz_powm(w, sign, pub->e, pub->n);
  r = mpz_cmp(w, m);

  mpz_clear(w);
  return r;
}

/**
 * Initialize random state (constructor)
 */
__attribute__((constructor))
void _signme_setup(void) {
  struct timeval tv;
  struct timezone tz;

  if (gettimeofday(&tv, &tz)) {
    perror("gettimeofday");
    exit(1);
  }

  gmp_randinit_lc_2exp_size(rstate, 16);
  gmp_randseed_ui(rstate, tv.tv_sec * 1000000 + tv.tv_usec);
}
/**
 * Cleanup random state (destructor)
 */
__attribute__((destructor))
void _signme_cleanup(void) {
  gmp_randclear(rstate);
}

