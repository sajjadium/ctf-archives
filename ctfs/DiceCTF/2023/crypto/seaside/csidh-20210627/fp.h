#ifndef FP_H
#define FP_H

#include <stdbool.h>

#include "params.h"

extern const fp fp_0;
extern const fp fp_1;

bool fp_eq(fp const *x, fp const *y);

void fp_set(fp *x, uint64_t y);

void fp_enc(fp *x, uint const *y); /* encode to Montgomery representation */
void fp_dec(uint *x, fp const *y); /* decode from Montgomery representation */

void fp_add2(fp *x, fp const *y);
void fp_sub2(fp *x, fp const *y);
void fp_mul2(fp *x, fp const *y);

void fp_add3(fp *x, fp const *y, fp const *z);
void fp_sub3(fp *x, fp const *y, fp const *z);
void fp_mul3(fp *x, fp const *y, fp const *z);

void fp_sq1(fp *x);
void fp_sq2(fp *x, fp const *y);
void fp_inv(fp *x);
bool fp_issquare(fp *x); /* destroys input! */

void fp_random(fp *x);

#endif
