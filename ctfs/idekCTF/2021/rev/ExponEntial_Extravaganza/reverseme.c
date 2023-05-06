#include <stdio.h>
#include <string.h>
#include <math.h>

int main(int argc, char** argv) {
  if(argc != 2){
    printf("Usage: ./reverseme password\n");
    return 1;
  }
  if(strlen(argv[1])!=14){
    printf("Incorrect Length\n");
    return 1;
  }
  if(*argv[1] != 112){//Not enough precision
    printf("Password Incorrect\n");
    return 1;
  }
  double magic_numbers[7] ={-68822144.50341525673866271972656250000000000000000000000000, 56777293.39031631499528884887695312500000000000000000000000, -3274524.75536667229607701301574707031250000000000000000000, -85761.51255339206545613706111907958984375000000000000000, 8443.33244327564352715853601694107055664062500000000000, -166.67369627952575683593750000000000000000000000000000, 1.00000000000000000000000000000000000000000000000000, };
  for(int i = 0; i < 6;i++){
    double foo=1.0,bar=0.0;
    for(int j=0;j<7;j++){
      bar += magic_numbers[j] * foo;
      foo *= (float)log(*(float*)((unsigned long)argv[1]+2*i));
    }
    if((int)(100000*bar) != 0){
      printf("Password Incorrect\n");
      return 1;
    }
  }
  printf("Password Correct\n");
  return 0;
}