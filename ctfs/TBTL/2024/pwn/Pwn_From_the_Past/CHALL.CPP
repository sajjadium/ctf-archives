// Built using Borland C++ 3.0 -- still the best IDE produced by humankind.
// https://winworldpc.com/download/52dfb385-9ba2-11e9-ab10-fa163e9022f0
//
// bcc -v CHALL.CPP 
//

#include <stdio.h>

int main() {
  char name[32];
  FILE *input = fopen("input.txt", "rt");
  FILE *output = fopen("output.txt", "wt");

  if (!input) {
    printf("Error opening input file!");
    return 1;
  }
  if (!output) {
    printf("Error opening input file!");
    return 1;
  }

  fscanf(input, "%[^ ]s", name);
  fprintf(output, "Hello %s\n", name);
  
  fclose(input);
  fclose(output);
  
  return 0;
}
