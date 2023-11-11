#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <gmp.h>
#include <unistd.h>

char flag[100];

typedef struct {
  struct {
    mpz_t u; mpz_t p; mpz_t q; mpz_t dp; mpz_t dq;
  } priv;
  struct {
    mpz_t n; mpz_t e;
  } pub;
} rsacrt_t;

/** @fn random_prime
 *  @brief Generate a random prime number.
 *  @param p: `mpz_t` variable to store the prime.
 *  @param nbits: Bit length of the prime.
 */
void random_prime(mpz_t p, int nbits) {
  gmp_randstate_t state;
  gmp_randinit_default(state);
  gmp_randseed_ui(state, rand());
  mpz_urandomb(p, state, nbits);
  mpz_nextprime(p, p);
  gmp_randclear(state);
}

/** @fn rsa_keygen
 *  @brief Generate a key pair for RSA-CRT.
 *  @param rsa: `rsacrt_t` structure to store the key.
 */
void rsa_keygen(rsacrt_t *rsa) {
  mpz_t p1, q1;
  mpz_inits(rsa->pub.n, rsa->pub.e,
            rsa->priv.u, rsa->priv.p, rsa->priv.q, rsa->priv.dp, rsa->priv.dq,
            p1, q1, NULL);

  /* Generate RSA parameters */
  mpz_set_ui(rsa->pub.e, 65537);
  random_prime(rsa->priv.p, 512);
  random_prime(rsa->priv.q, 512);
  mpz_sub_ui(p1, rsa->priv.p, 1);
  mpz_sub_ui(q1, rsa->priv.q, 1);
  mpz_mul(rsa->pub.n, rsa->priv.p, rsa->priv.q);     // n = p * q
  mpz_invert(rsa->priv.dp, rsa->pub.e, p1);          // dp = e^-1 mod p-1
  mpz_invert(rsa->priv.dq, rsa->pub.e, q1);          // dq = e^-1 mod q-1
  mpz_invert(rsa->priv.u, rsa->priv.q, rsa->priv.p); // u = q^-1 mod p
}

/** @fn challenge
 *  @brief Can you solve this?
 *  @param rsa: `rsacrt_t` structure containing a key pair.
 */
void challenge(rsacrt_t *rsa) {
  char buf[0x200];
  gmp_randstate_t state;
  mpz_t x, m, c, cp, cq, mp, mq;
  mpz_inits(x, m, c, cp, cq, mp, mq, NULL);

  /* Generate a random number and encrypt it */
  gmp_randinit_default(state);
  gmp_randseed_ui(state, rand());
  mpz_urandomb(x, state, 512);
  mpz_powm_ui(c, x, 1333, rsa->pub.n); // c = x^1333 mod n

  gmp_printf("n = %Zd\n", rsa->pub.n);
  gmp_printf("c = %Zd\n", c);

  for (;;) {
    /* Input ciphertext */
    printf("c = ");
    if (scanf("%s", buf) != 1
        || mpz_set_str(c, buf, 10) != 0) {
      fputs("Invalid input", stderr);
      exit(0);
    }

    /* Calculate plaintext */
    mpz_mod(cp, c, rsa->priv.p);
    mpz_mod(cq, c, rsa->priv.q);
    mpz_powm(mp, cp, rsa->priv.dp, rsa->priv.p);
    mpz_powm(mq, cq, rsa->priv.dq, rsa->priv.q);
    // m = (((mp - mq) * u mod p) * q + mq) mod n
    mpz_set(m, mp);
    mpz_sub(m, m, mq);
    mpz_mul(m, m, rsa->priv.u);
    mpz_mod(m, m, rsa->priv.p);
    mpz_mul(m, m, rsa->priv.q);
    mpz_add(m, m, mq);
    mpz_mod(m, m, rsa->pub.n);
    gmp_printf("m = %Zd\n", m);

    /* Check plaintext */
    if (mpz_cmp(m, x) == 0) {
      printf("Congratulations!\n"
             "Here is the flag: %s\n", flag);
      break;
    }
  }
}

/**
 * Entry point
 */
int main() {
  rsacrt_t rsa;
  rsa_keygen(&rsa);
  challenge(&rsa);
  return 0;
}

__attribute__((constructor))
void setup(void) {
  int seed;
  int fd;
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);

  // Get random seed
  if ((fd = open("/dev/urandom", O_RDONLY)) == -1 ||
      read(fd, &seed, sizeof(seed)) != sizeof(seed)) {
    perror("setup failed");
    exit(1);
  }
  close(fd);
  srand(seed);

  // Read flag
  if ((fd = open("/flag.txt", O_RDONLY)) == -1 ||
      read(fd, flag, sizeof(flag)) <= 0) {
    perror("flag not found");
    exit(1);
  }
  close(fd);
}
