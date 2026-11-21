#include "../../common/include/kernel/syscall-definitions.h"


/* the result should be 1237619379 for size of 100 */
#define ARRAY_SIZE 100
#define POS(x,y) (x*ARRAY_SIZE+y)

typedef unsigned int uint32;


uint32 axa[ARRAY_SIZE][ARRAY_SIZE];
uint32 bxb[ARRAY_SIZE][ARRAY_SIZE];
uint32 cxc[ARRAY_SIZE][ARRAY_SIZE];
uint32 prime = 5000011;
uint32 rand = 31337;
uint32 expos = 1;
uint32 sum = 0;

uint32 getRandom()
{
  expos = expos * prime;
  rand = rand + expos;
  rand = rand % 100003;
  return rand;
}

int main(int argc, char** argv)
{
  int x, y, a = 0;


  for (x = 0; x < ARRAY_SIZE; ++x)
  {
    for (y = 0; y < ARRAY_SIZE; ++y)
    {
      axa[x][y]= getRandom();
      bxb[x][y] = getRandom();
      
    }
  }
  for (x=0;x<ARRAY_SIZE;++x)
    for (y=0;y<ARRAY_SIZE;++y)
    {
      cxc[x][y]=0;
      for (a=0;a<ARRAY_SIZE;++a)
        cxc[x][y]+=axa[x][a]*bxb[a][y];
    }
  for (x=0;x<ARRAY_SIZE;++x)
    for (y=0;y<ARRAY_SIZE;++y)
      sum += cxc[x][y];
  
 // printf("Result is %d",sum);
  return sum;
}
