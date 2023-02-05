
#include <string.h>
#include <assert.h>

#include "uint.h"
#include "fp.h"
#include "mont.h"
#include "csidh.h"
#include "rng.h"

__attribute__((visibility("default")))
const public_key base = {0}; /* A = 0 */

/* TODO still wastes quite a bit of randomness */
__attribute__((visibility("default")))
void csidh_private(private_key *priv)
{
    memset(&priv->e, 0, sizeof(priv->e));
    for (size_t i = 0; ; ) {
        uint8_t buf[64];
        randombytes(buf, sizeof(buf));
        for (size_t j = 0; j < 2*sizeof(buf); ++j) {
            int8_t v = (buf[j/2] >> j%2*4 & 0xf);
            v = (int8_t) (v << 4) >> 4;
            if (v <= MAX_EXPONENT && v >= -MAX_EXPONENT) {
                priv->e[i++] = v;
                if (i >= NUM_PRIMES)
                    return;
            }
        }
    }
}

static bool validate_rec(bool *is_supersingular, uint *order, uint8_t *seen, proj *P, proj const *A, size_t lower, size_t upper)
{
    assert(lower < upper);

    if (upper - lower == 1) {

        const size_t i = lower;

        if (seen[i/8] & 1<<i%8)
            return false;

        /* now P is [(p+1) / l_lower] times the original random point */
        /* we only gain information if this multiple is non-zero */

        if (!is_infinity(P)) {

            uint tmp;
            uint_set(&tmp, primes[i]);
            xMUL(P, A, P, &tmp);

            if (!is_infinity(P)) {
                /* order does not divide p+1. */
                *is_supersingular = false;
                return true;
            }

            uint_mul3_64(order, order, primes[i]);
            seen[i/8] |= 1<<i%8;

            if (uint_sub3(&tmp, &four_sqrt_p, order)) { /* returns borrow */
                /* order > 4 sqrt(p), hence definitely supersingular */
                *is_supersingular = true;
                return true;
            }
        }

        /* inconclusive */
        return false;
    }

    /* TODO split according to non-seen primes rather than blindly */
    size_t mid = lower + (upper - lower + 1) / 2;

    uint cl = uint_1, cu = uint_1, *cc = &cu;
    for (size_t i = lower; i < upper; cc = ++i < mid ? &cu : &cl)
        if (~seen[i/8] & 1<<i%8)
            uint_mul3_64(cc, cc, primes[i]);

    proj Q;

    xMUL(&Q, A, P, &cu);
    xMUL( P, A, P, &cl);

    /* start with the right half; bigger primes help more */
    return validate_rec(is_supersingular, order, seen, &Q, A, mid, upper)
        || validate_rec(is_supersingular, order, seen,  P, A, lower, mid);
}

bool validate_basic(public_key const *in)
{
    /* make sure A < p */
    uint dummy;
    if (!uint_sub3(&dummy, &in->A, &p)) /* returns borrow */
        return false;

    /* make sure the curve is nonsingular: A != 2 */
    uint pm2;
    uint_set(&pm2, 2);
    if (uint_eq(&in->A, &pm2))
        return false;

    /* make sure the curve is nonsingular: A != -2 */
    uint_sub3(&pm2, &uint_0, &pm2);
    if (uint_eq(&in->A, &pm2))
        return false;

    return true;
}

/* includes public-key validation. */
/* totally not constant-time. */
__attribute__((visibility("default")))
bool csidh(public_key *out, public_key const *in, private_key const *priv)
{

    if (!validate_basic(in))
        goto invalid;

    int8_t es[NUM_PRIMES];
    memcpy(es, priv->e, sizeof(es));

    proj A;
    fp_enc(&A.x, &in->A);
    A.z = fp_1;

    uint order = uint_1;
    uint8_t seen[(NUM_PRIMES+7)/8] = {0}; /* packed bool */

    fp elligator_rand = first_elligator_rand;
    if (!fp_eq(&A.x, &fp_0))
        fp_mul2(&elligator_rand, &A.x);

    for (bool twist = false; ; ) {

        #define BATCH_SIZE 16

        uint8_t batch[(NUM_PRIMES+7)/8] = {0}; /* packed bool */
        {
            size_t sz = 0;
            for (size_t i = 0; i < NUM_PRIMES && sz < BATCH_SIZE; ++i) {
                if (twist ? (es[i] < 0) : (es[i] > 0)) {
                    batch[i/8] |= 1<<i%8;
                    ++sz;
                }
            }
            if (!sz) {
                if (twist) break;
                twist = true;
                continue;
            }
        }


        uint k = p_cofactor;
        for (size_t i = 0; i < NUM_PRIMES; ++i)
            if (~batch[i/8] & 1<<i%8)
                uint_mul3_64(&k, &k, primes[i]);

        assert(is_affine(&A));

        proj P = {elligator_rand, fp_1};
        if (is_twist(&P.x, &A.x) != twist) {
            fp_add2(&P.x, &A.x);
            fp_sub3(&P.x, &fp_0, &P.x);
        }

        xMUL(&P, &A, &P, &k);


        for (size_t i = NUM_PRIMES-1; i < NUM_PRIMES; --i) {

            if (~batch[i/8] & 1<<i%8) continue;

            uint cof = uint_1;
            for (size_t j = 0; j < i; ++j)
                if (batch[j/8] & 1<<j%8)
                    uint_mul3_64(&cof, &cof, primes[j]);

            if (uint_len(&cof) > (cost_ratio_inv_mul >> !is_affine(&A)))
                affinize(&A, &P);

            proj K;
            xMUL(&K, &A, &P, &cof);

            if (is_infinity(&K))
                continue;

            bool want = !(seen[i/8] & (1 << i%8));

            xISOG(&A, &P, &K, primes[i], want);

            if (want) {
                if (!is_infinity(&K)) goto invalid;
                uint_mul3_64(&order, &order, primes[i]);
                seen[i/8] |= 1 << i%8;
            }

            es[i] -= twist ? -1 : 1;

        }

        assert(!is_infinity(&A));

        fp_random(&elligator_rand);
        if (!fp_eq(&A.x, &fp_0)) {
            fp_sq1(&elligator_rand);
            fp_sub2(&elligator_rand, &fp_1);
            proj t = A;
            fp_mul2(&t.z, &elligator_rand);
            affinize(&A, &t);
            elligator_rand = t.x;
        }
        else
            affinize(&A, NULL);

    }

    /* public-key validation */
    {
        uint tmp;
        proj P;
        bool is_supersingular = uint_sub3(&tmp, &four_sqrt_p, &order); /* returns borrow */

        if (!is_supersingular) do {
            /* this happens only extremely rarely. */

            fp_random(&P.x);
            P.z = fp_1;

            xMUL(&P, &A, &P, &p_cofactor);
            xMUL(&P, &A, &P, &order);

        } while (!validate_rec(&is_supersingular, &order, seen, &P, &A, 0, NUM_PRIMES));

        if (!is_supersingular) {
invalid:
            randombytes(&out->A, sizeof(out->A));
            return false;
        }
    }

    assert(is_affine(&A));
    fp_dec(&out->A, &A.x);

    return true;

}

