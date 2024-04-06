#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
  int l, i, j;
  unsigned char input[50];
  unsigned char* output;
  unsigned char b[] = {0x0, 0x28, 0x13, 0x36, 0x11, 0x7a, 0x6e, 0x4, 0x6c, 0x55, 0x5f, 0x39, 0x4, 0x1d, 0x4e, 0x66, 0x6f, 0x6b, 0x42, 0x49, 0x0, 0x52, 0x0, 0x53, 0x1f, 0x0, 0x56, 0x4e, 0x5c};
  char* s = "RS{0h_b0y,I_10v3_f4k3_fl4gs!}";

  printf("Can you guess my favorite flag? > ");
  fgets(input, 50, stdin);
  l = strlen(input);
  if (input[l-1] == '\n') {
    input[l-1] = '\0';
    l--;
  }
  if (l != strlen(s)) {
    printf("Nope! Try again :)\n");
    return -1;
  }
  if (strcmp(input, s) == 0) {
    printf("why would I like a fake flag??\n");
    return -1;
  }
  output = malloc(l+1);
  for (i=0; i <l; i++) {
    output[i] = ' ';
  }
  output[l+1] = 0;

  for (i = 0; i < l; i++) {
    output[(2*i) % l] = input[i] ^ b[i];
  }

  if (strcmp(output, s) != 0) {
    printf("Nope! Try again :)\n");
    return -1;
  }

  printf("Yeah how'd you know?\n");

  return 0;
}
