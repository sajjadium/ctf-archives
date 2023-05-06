#include <stdio.h>
#include <stdlib.h>

// #define WARMCACHE 30
// #define NUMTESTS 100

//extern void jump64divsteps2 (unsigned long long count, unsigned long long delta, unsigned long long f, unsigned long long g, unsigned long long *h);
//extern void muls64xs512 (unsigned long long *b, unsigned long long *f, unsigned long long *g, unsigned long long k);
extern int jump64divsteps2_s511  (long long count, long long delta, long long *f, long long *g, long long *h);
extern void muls64xs64 (long long *mat1, long long *mat2, long long *mat3);
extern void muls128xs128 (long long *mat1, long long *mat2, long long *mat3);
extern void muls256xs256 (long long *mat1, long long *mat2, long long *mat3);
//extern void norm64_511 (unsigned long long *a, unsigned long long *b);
//extern void muls64x511 (unsigned long long *a, unsigned long long *b, unsigned long long *c, unsigned long long *d);
extern void norm500_511 (long long *a, long long count);
extern void fpmul2x2_511 (unsigned long long *mat1, unsigned long long *mat2, unsigned long long *mat3);
extern void fpmul2x2_511_half (long long *mat1, long long *mat2, long long *mat3);
extern void fpmul2x2_511_quarter (long long *mat1, long long *mat2, long long *mat3);

extern void fpmul511 (long long *f, long long *g, long long *h, long long *M);
extern void fpcneg511 (long long *b, long long f);
extern unsigned long long cpucycles(void);

// void qsort(void *base, size_t nitems, size_t size, int (*compar)(const void *, const void*));
// int cmpfunc (const void * a, const void * b) {
//    return ( *(int*)a - *(int*)b );
// }

// int times[NUMTESTS];

//void print64 (unsigned long long *b) {
//  printf ("add64([\n 0x%016llx, 0x%016llx, 0x%016llx, 0x%016llx, 0x%016llx, 0x%016llx, 0x%016llx, 0x%016llx\n ])\n",b[0],b[1],b[2],b[3],b[4],b[5],b[6],b[7]);
//}

void fpinv511 (long long *g0, long long *f0) {
  long long j, delta;
//  signed long long x;
  signed long long M[8] = {
  0x1b81b90533c6c87b, 0xc2721bf457aca835, 0x516730cc1f0b4f25,
  0xa7aac6c567f35507, 0x5afbfcc69322c9cd, 0xb42d083aedc88c42,
  0xfc8ab0d15e3e4c4a, 0x65b48e8f740f89bf};
//  signed long long M1[1] = {0x66c1301f632e294d};
  
//   unsigned long long R2[8] = {
//     0x36905b572ffc1724, 0x67086f4525f1f27d, 0x4faf3fbfd22370ca,
//     0x192ea214bcc584b1, 0x5dae03ee2f5de3d0, 0x1e9248731776b371,
//     0xad5f166e20e4f52d, 0x4ed759aea6f3917e
//   }; // 2^1024 mod M
   
//   unsigned long long R[8] = {
//     0xc8fc8df598726f0a, 0x7b1bc81750a6af95, 0x5d319e67c1e961b4,
//     0xb0aa7275301955f1, 0x4a080672d9ba6c64, 0x97a5ef8a246ee77b,
//     0x06ea9e5d4383676a, 0x3496e2e117e0ec80
//   }; // 2^512 mod M
  signed long long f[8];
  signed long long g[8] =   {
  0x4c315e480b029aef, 0xeaf9c53c25ccc9b4, 0xea5f3a1404c18e2c,
  0x677a55e3391c85ed, 0x562380923b6e2203, 0x520af26080167eac,
  0x9418c4fd950b99bc, 0x5fa30a96cc2afd71};
  // unsigned long long g0[8];
  
  signed long long b[8] = {0LL, 0LL, 0LL, 0LL, 0LL, 0LL, 0LL, 0LL}; 
  signed long long b2[8] = {0LL, 0LL, 0LL, 0LL, 0LL, 0LL, 0LL, 0LL};
  signed long long b3[16]= {0LL, 0LL, 0LL, 0LL, 0LL, 0LL, 0LL, 0LL};
  signed long long b4[16]= {0LL, 0LL, 0LL, 0LL, 0LL, 0LL, 0LL, 0LL};
  signed long long b5[32];
  signed long long b6[32];
  signed long long b7[32];
  signed long long b8[32];
  signed long long b9[32];
  // unsigned long long scale2_604[8] = {
  //   0x929781a47d552e63, 0x03a6c99956547117, 0xfb73cd1b69c6ec0b,
  //   0x3a573d35c6148671, 0xe079b26d00ae1f14, 0x6cbf1de3fd6ba1f0,
  //   0x5c1f0e37ce826d4d, 0x0bf1629faf86e57b};
//  signed long long scale2_560[8] = {
//  0xec14faf1a15ff91b, 0x2e88db4db5e18cb7, 0x1f6c6cc387c0328c,
//  0xccfe4014d5d6104c, 0x20d877a8667747f2, 0xb01488941f9ab934,
//  0xb740658ee8725d59, 0x4487e978f90af771};
  signed long long scale2_1072[8] = {
  0x354a651b15013ea1, 0x7103685b977c420d, 0x6a816d4220cd53c3,
  0xfea8185f044305f8, 0x81487b538af41a13, 0x8396b6c0ccd90808,
  0x84d981e90782b428, 0x264b7d2c918fafc7};

  for (j=7; j>=0; j--) {
    f[j] = M[j];
    g[j] = g0[j];
  }

  delta = 1;
  
  delta = jump64divsteps2_s511(62,delta,f,g,b);
    
  delta = jump64divsteps2_s511(62,delta,f,g,b2);
    
  muls64xs64(b2,b,b3);
    
  delta = jump64divsteps2_s511(62,delta,f,g,b);
    
  delta = jump64divsteps2_s511(62,delta,f,g,b2);
    
  muls64xs64(b2,b,b4);
  
  muls128xs128(b4,b3,b5);

  // next 248 iterations  
  delta = jump64divsteps2_s511(62,delta,f,g,b);
  
  delta = jump64divsteps2_s511(62,delta,f,g,b2);
  
  muls64xs64(b2,b,b3);

  delta = jump64divsteps2_s511(62,delta,f,g,b);
  
  delta = jump64divsteps2_s511(62,delta,f,g,b2);
  
  muls64xs64(b2,b,b4);
  
  muls128xs128(b4,b3,b6);

  // merge to 503 bits
  muls256xs256(b6,b5,b7);
  // printf("\n");
  // print64(b6); print64(b6+8);
  // printf("\n");
  // print64(b5); print64(b5+8);
  // printf("\n");
  // print64(b7); print64(b7+8);
  // print64(b7+16); print64(b7+24);
  // printf("\n");
  
  norm500_511(b7,4);
  // print64(b7); print64(b7+8);
  // print64(b7+16); print64(b7+24);
  // printf("\n");
  
  // start of second 496 iterations

  // first 248 iterations  
  delta = jump64divsteps2_s511(62,delta,f,g,b);
    
  delta = jump64divsteps2_s511(62,delta,f,g,b2);
    
  muls64xs64(b2,b,b3);
    
  delta = jump64divsteps2_s511(62,delta,f,g,b);
    
  delta = jump64divsteps2_s511(62,delta,f,g,b2);
    
  muls64xs64(b2,b,b4);
  
  muls128xs128(b4,b3,b5);

  // next 248 iterations  
  delta = jump64divsteps2_s511(62,delta,f,g,b);
  
  delta = jump64divsteps2_s511(62,delta,f,g,b2);
  
  muls64xs64(b2,b,b3);

  delta = jump64divsteps2_s511(62,delta,f,g,b);
  
  delta = jump64divsteps2_s511(62,delta,f,g,b2);
  
  muls64xs64(b2,b,b4);
  
  muls128xs128(b4,b3,b6);

  // merge to 503 bits
  muls256xs256(b6,b5,b8);
  norm500_511(b8,4);
  // print64(b8); print64(b8+8);
  // print64(b8+16); print64(b8+24);
  // printf("\n");

  // montgomery arithmetic?
  fpmul2x2_511_half(b8,b7,b9);
  // print64(b9); print64(b9+8);
  // print64(b9+16); print64(b9+24);
  // printf("\n");
  // note scaled by 2^{-512} 
    
  // start of third 496 iterations
  // first 248 iterations  
  delta = jump64divsteps2_s511(62,delta,f,g,b);
    
  delta = jump64divsteps2_s511(62,delta,f,g,b2);
    
  muls64xs64(b2,b,b3);
    
  delta = jump64divsteps2_s511(62,delta,f,g,b);
    
  delta = jump64divsteps2_s511(62,delta,f,g,b2);
    
  muls64xs64(b2,b,b4);
  
  muls128xs128(b4,b3,b5);

  // next 248 iterations  
  delta = jump64divsteps2_s511(62,delta,f,g,b);
  
  delta = jump64divsteps2_s511(62,delta,f,g,b2);
  
  muls64xs64(b2,b,b3);

  delta = jump64divsteps2_s511(62,delta,f,g,b);
  
  delta = jump64divsteps2_s511(62,delta,f,g,b2);
  
  muls64xs64(b2,b,b4);
  
  muls128xs128(b4,b3,b6);

  // merge to 503 bits
  muls256xs256(b6,b5,b7);
  norm500_511(b7,4);

  // montgomery arithmetic?
  fpmul2x2_511_quarter(b7,b9,b8);
  // scaled by 2^{-1024}
    
  // // remaining 20 iterations 
  // jump64divsteps2(20,delta,f[0],g[0],b);
  // 
  // //norm64_511(b+3,b7);
  // //fpmul2x2_511(b7,b8,b9);
  // // this multiplication is scaled by 2^{-64}, scaled by 2^{-1088}
  // muls64x511(b+3,b8,b9,M);
  // // would be scaled by 2^{-1088} 
    
  //  
  fpcneg511(b8+8,f[7]);
//  fpmul511(b8+8,scale2_560,f0,M);
  fpmul511(b8+8,scale2_1072,f0,M);
  // v itself is the inverse scaled by 2^1488
  // scale factor is 2^560
  // three multiplications is 2^{-1536}
  // result should be 2^512 times the inverse
}
