#include <err.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <unistd.h>

asm("pop %eax; int3; ret");

// Defined in a separate source file for simplicity.
void init_visualize(char* buff);
void visualize(char* buff);
void safeguard();

// This is what you need to do to get the first flag
// void print_flag() {
//   asm volatile("mov $1, %%eax; mov $0x31337, %%edi; mov $0x1337, %%esi; int3" ::: "eax");
// }

int show_color = 0;

int prompt(char *prompt, int def) {
  char buff[32];

  printf("%s", prompt);
  fgets(buff, sizeof(buff), stdin);
  if (buff[0] == 'Y' || buff[0] == 'y')
    return 1;
  else if (buff[0] == 'N' || buff[0] == 'n')
    return 0;
  else
    return def;
}

void vuln() {
  int secret = 0xdeadbeef;
  char padding[16];
  char buff[32];

  show_color = prompt("Do you want color in the visualization? (Y/n) ", 1);

  memset(buff, 0, sizeof(buff)); // Zero-out the buffer.
  memset(padding, 0xFF, sizeof(padding)); // Zero-out the padding.

  // Initializes the stack visualization. Don't worry about it!
  init_visualize(buff); 

  // Prints out the stack before modification
  visualize(buff);

  printf("Input some text: ");

  gets(buff); // This is a vulnerable call!

  // Prints out the stack after modification
  visualize(buff); 

  // Check if secret has changed.
  if (secret == 0x67616c66) {
    puts("You did it! Congratuations!");
    // print_flag(); // Print out the flag. You deserve it. (not anymore)
    printf("Returning to address: %p\n", (&secret)[4]);
    return;
  } else if (secret != 0xdeadbeef) {
    puts("Wow you overflowed the secret value! Now try controlling the value of it!");
  } else {
    puts("Maybe you haven't overflowed enough characters? Try again?");
  }

  exit(0);
}

int main(int argc, char **argv) {
  setbuf(stdout, NULL);
  setbuf(stdin, NULL);
  safeguard();
  vuln();
}
