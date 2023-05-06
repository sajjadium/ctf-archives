#include <stdio.h>
#include <stdlib.h>

extern void fpmul511 (unsigned long long *x, unsigned long long *y, unsigned long long *r, unsigned long long *M);
extern void fpadd511 (unsigned long long *x, unsigned long long *y, unsigned long long *r);

void fpmul2x2_511 (unsigned long long *m1, unsigned long long *m2, unsigned long long *m3) {

  unsigned long long t0[8], t1[8];

  unsigned long long M1[8] = {
  0x1b81b90533c6c87b, 0xc2721bf457aca835, 0x516730cc1f0b4f25,
  0xa7aac6c567f35507, 0x5afbfcc69322c9cd, 0xb42d083aedc88c42,
  0xfc8ab0d15e3e4c4a, 0x65b48e8f740f89bf};

// u:
  fpmul511(m1,m2,t0,M1);
  fpmul511(m1+8,m2+16,t1,M1);
  fpadd511(t0,t1,m3);
// v:
  fpmul511(m1,m2+8,t0,M1);
  fpmul511(m1+8,m2+24,t1,M1);
  fpadd511(t0,t1,m3+8);
// q:
  fpmul511(m1+16,m2,t0,M1);
  fpmul511(m1+24,m2+16,t1,M1);
  fpadd511(t0,t1,m3+16);
// r:
  fpmul511(m1+16,m2+8,t0,M1);
  fpmul511(m1+24,m2+24,t1,M1);
  fpadd511(t0,t1,m3+24);

}
 
