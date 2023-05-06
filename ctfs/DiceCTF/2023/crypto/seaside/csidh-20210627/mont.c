
#include <string.h>
#include <assert.h>

#include "params.h"
#include "uint.h"
#include "fp.h"
#include "mont.h"
#include "rng.h"

uint64_t *xmul_counters = NULL;  /* array indexed by bit length */
uint64_t *isog_counters = NULL;  /* array indexed by degree */


bool is_infinity(proj const *P)
{
    return fp_eq(&P->z, &fp_0);
}

bool is_affine(proj const *P)
{
    return fp_eq(&P->z, &fp_1);
}

void affinize(proj *P, proj *Q)
{
    if (!Q) {
        if (is_infinity(P)) {
            P->x = fp_1;
            P->z = fp_0;
        }
        else if (!is_affine(P)) {
            fp_inv(&P->z);
            fp_mul2(&P->x, &P->z);
            P->z = fp_1;
        }
    }
    else if (is_affine(P))
        affinize(Q, NULL);
    else if (is_affine(Q))
        affinize(P, NULL);
    else if (is_infinity(P) || is_infinity(Q)) {
        affinize(P, NULL);
        affinize(Q, NULL);
    }
    else {
        /* batch inversions */
        fp t;
        fp_mul3(&t, &P->z, &Q->z);
        fp_inv(&t);
        fp_mul2(&Q->z, &t);
        fp_mul2(&P->x, &Q->z);
        fp_mul2(&P->z, &t);
        fp_mul2(&Q->x, &P->z);
        P->z = Q->z = fp_1;
    }
}


void xDBL(proj *Q, proj const *P, proj const *A)
{
    fp a, b, c;
    fp_add3(&a, &P->x, &P->z);
    fp_sq1(&a);
    fp_sub3(&b, &P->x, &P->z);
    fp_sq1(&b);
    fp_sub3(&c, &a, &b);
    fp_add2(&b, &b); fp_add2(&b, &b);
    if (!is_affine(A))
        fp_mul2(&b, &A->z);
    fp_mul3(&Q->x, &a, &b);
    fp_add3(&a, &A->z, &A->z);
    fp_add2(&a, &A->x);
    fp_mul2(&a, &c);
    fp_add2(&a, &b);
    fp_mul3(&Q->z, &a, &c);
}

void xADD(proj *S, proj const *P, proj const *Q, proj const *PQ)
{
    fp a, b, c, d;
    fp_add3(&a, &P->x, &P->z);
    fp_sub3(&b, &P->x, &P->z);
    fp_add3(&c, &Q->x, &Q->z);
    fp_sub3(&d, &Q->x, &Q->z);
    fp_mul2(&a, &d);
    fp_mul2(&b, &c);
    fp_add3(&S->x, &a, &b);
    fp_sub3(&S->z, &a, &b);
    fp_sq1(&S->x);
    fp_sq1(&S->z);
    if (!is_affine(PQ))
        fp_mul2(&S->x, &PQ->z);
    fp_mul2(&S->z, &PQ->x);
}

void xDBLADD(proj *R, proj *S, proj const *P, proj const *Q, proj const *PQ, proj const *A)
{
    fp a, b, c, d;

    fp_add3(&a, &Q->x, &Q->z);
    fp_sub3(&b, &Q->x, &Q->z);
    fp_add3(&c, &P->x, &P->z);
    fp_sub3(&d, &P->x, &P->z);
    fp_sq2(&R->x, &c);
    fp_sq2(&S->x, &d);
    fp_mul2(&c, &b);
    fp_mul2(&d, &a);
    fp_sub3(&b, &R->x, &S->x);
    fp_add3(&a, &A->z, &A->z);
    if (!is_affine(A))
        fp_mul3(&R->z, &S->x, &a);
    else
        fp_add3(&R->z, &S->x, &S->x);
    fp_add3(&S->x, &A->x, &a);
    fp_add2(&R->z, &R->z);
    fp_mul2(&R->x, &R->z);
    fp_mul2(&S->x, &b);
    fp_sub3(&S->z, &c, &d);
    fp_add2(&R->z, &S->x);
    fp_add3(&S->x, &c, &d);
    fp_mul2(&R->z, &b);
    fp_sq1(&S->x);
    fp_sq1(&S->z);
    if (!is_affine(PQ))
        fp_mul2(&S->x, &PQ->z);
    fp_mul2(&S->z, &PQ->x);
}


/* Montgomery ladder. */
/* P must not be the unique point of order 2. */
/* not constant-time! */
void xMUL(proj *Q, proj const *A, proj const *P, uint const *k)
{
    size_t i = uint_len(k);
    if (xmul_counters) ++xmul_counters[i];

    proj R = *P;
    const proj Pcopy = *P; /* in case Q = P */

    Q->x = fp_1;
    Q->z = fp_0;

    while (i --> 0) {

        const bool bit = uint_bit(k, i);

        if (bit) { proj T = *Q; *Q = R; R = T; } /* not constant-time */

        xDBLADD(Q, &R, Q, &R, &Pcopy, A);

        if (bit) { proj T = *Q; *Q = R; R = T; } /* not constant-time */

    }
}


/* Montgomery <-> Edwards conversions */

static void mont2edw(proj *d, proj const *A)
{
    /* d = (A-2)/(A+2) */
    fp_sub3(&d->x, &A->x, &A->z);
    fp_sub2(&d->x, &A->z);
    fp_add3(&d->z, &A->x, &A->z);
    fp_add2(&d->z, &A->z);
}

static void edw2mont(proj *A, proj const *d)
{
    /* A = 2*(1+d)/(1-d) */
    fp_add3(&A->x, &d->z, &d->x);
    fp_add2(&A->x, &A->x);
    fp_sub3(&A->z, &d->z, &d->x);
}

/* Montgomery isogeny evaluation [Costello-Hisil, Renes] */

static void montisog_eval_init(proj *Q, const proj *P, const proj *K)
{
    fp t;

    fp_mul3(&Q->x, &P->x, &K->x);
    fp_mul3(&t, &P->z, &K->z);
    fp_sub2(&Q->x, &t);

    fp_mul3(&Q->z, &P->x, &K->z);
    fp_mul3(&t, &P->z, &K->x);
    fp_sub2(&Q->z, &t);
}

static void montisog_eval_consume(proj *Q, const proj *P, const proj *M)
{
    fp t0, t1, t2;

    fp_sub3(&t0, &P->x, &P->z);
    fp_add3(&t1, &M->x, &M->z);
    fp_mul2(&t0, &t1);

    fp_sub3(&t1, &M->x, &M->z);
    fp_add3(&t2, &P->x, &P->z);
    fp_mul2(&t1, &t2);

    fp_add3(&t2, &t0, &t1);
    fp_mul2(&Q->x, &t2);

    fp_sub3(&t2, &t0, &t1);
    fp_mul2(&Q->z, &t2);
}

static void montisog_eval_finish(proj *P, proj *Q)  /* destroys Q */
{
    fp_sq1(&Q->x);
    fp_sq1(&Q->z);
    fp_mul2(&P->x, &Q->x);
    fp_mul2(&P->z, &Q->z);
}

/* Edwards isogeny codomain [Moody-Shumow] */

static void edwisog_curve_init(proj *prod, proj const *K)
{
    fp_sub3(&prod->x, &K->x, &K->z);
    fp_add3(&prod->z, &K->x, &K->z);
}

static void edwisog_curve_consume(proj *prod, proj const *M)
{
    fp Y, Z;

    fp_sub3(&Y, &M->x, &M->z);
    fp_add3(&Z, &M->x, &M->z);

    fp_mul2(&prod->x, &Y);
    fp_mul2(&prod->z, &Z);
}

static void edwisog_curve_finish(proj *d, proj const *prod, uint64_t l)
{

    proj newd = *prod;
    fp_sq1(&newd.x); fp_sq1(&newd.z);   /* ^2 */
    fp_sq1(&newd.x); fp_sq1(&newd.z);   /* ^4 */
    fp_sq1(&newd.x); fp_sq1(&newd.z);   /* ^8 */

    /* square-and-multiply to compute d^l */
    for (uint64_t k = l; k; k >>= 1) {
        if (k & 1) {
            fp_mul2(&newd.x, &d->x);
            fp_mul2(&newd.z, &d->z);
        }
        fp_sq1(&d->x);
        fp_sq1(&d->z);
    }

    *d = newd;
}

/* computes the isogeny with kernel point K of order l */
/* returns the new curve coefficient A and the image of P */
/* optionally also multiplies K by l */
/* (obviously) not constant time in l */
void xISOG(proj *A, proj *P, proj *K, uint64_t l, bool want_multiple)
{
    assert(l >= 3);
    assert(l % 2 == 1);

    if (isog_counters) ++isog_counters[l];

    proj prod, Q;

    montisog_eval_init(&Q, P, K);
    edwisog_curve_init(&prod, K);

    proj M[3] = {*K};
    xDBL(&M[1], K, A);

    for (uint64_t i = 1; i < l / 2; ++i) {

        if (i >= 2)
            xADD(&M[i%3], &M[(i-1)%3], K, &M[(i-2)%3]);

        montisog_eval_consume(&Q, P, &M[i%3]);
        edwisog_curve_consume(&prod, &M[i%3]);
    }

    /* "dummy isogeny" trick [Meyer-Campos-Reith] */
    if (want_multiple) {
        if (l > 3)
            xADD(&M[l/2%3], &M[(l/2-1)%3], K, &M[(l/2-2)%3]);
        xADD(K, &M[l/2%3], &M[(l/2-1)%3], K);
    }

    montisog_eval_finish(P, &Q);

    proj d;
    mont2edw(&d, A);
    edwisog_curve_finish(&d, &prod, l);
    edw2mont(A, &d);
}


bool is_twist(fp const *x, fp const *A)
{
    fp t;
    fp_add3(&t, x, A);  /* x + A */
    fp_mul2(&t, x);     /* x^2 + Ax */
    fp_add2(&t, &fp_1); /* x^2 + Ax + 1 */
    fp_mul2(&t, x);     /* x^3 + Ax^2 + x */
    return !fp_issquare(&t);
}

