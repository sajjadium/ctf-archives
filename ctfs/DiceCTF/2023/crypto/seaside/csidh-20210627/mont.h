#ifndef MONT_H
#define MONT_H

#include "params.h"

bool is_infinity(proj const *P);
bool is_affine(proj const *P);
void affinize(proj *P, proj *Q);

void xDBL(proj *Q, proj const *P, proj const *A);
void xADD(proj *S, proj const *P, proj const *Q, proj const *PQ);
void xDBLADD(proj *R, proj *S, proj const *P, proj const *Q, proj const *PQ, proj const *A);
void xMUL(proj *Q, proj const *A, proj const *P, uint const *k);

void xISOG(proj *A, proj *P, proj *K, uint64_t l, bool want_multiple);

bool is_twist(fp const *x, fp const *A);

#endif
