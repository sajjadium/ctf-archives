#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <stdint.h>
#include <sys/mman.h>

// These constants are valuable for exploits
#define STACK_LENGTH 4096
#define STACK_START  NULL
#define CODE_LENGTH 0x500000
#define CODE_START 0x13370000

// The amount of time shellcode is allowed to run
#define TIME 10

// Makes xinetd work better
#define disable_buffering(_fd) setvbuf(_fd, NULL, _IONBF, 0)

int main(int argc, char *argv[])
{
  // Generate a random block of +rwx memory that'll be filled randomly
  uint32_t *random_code = mmap((void*)CODE_START,  CODE_LENGTH,  PROT_READ | PROT_WRITE | PROT_EXEC, MAP_ANONYMOUS | MAP_PRIVATE, 0, 0);

  // Allocate memory for the user to send us a stack - it's just +rw
  uint8_t  *stack       = mmap((void*)STACK_START, STACK_LENGTH, PROT_READ | PROT_WRITE,             MAP_ANONYMOUS | MAP_PRIVATE, 0, 0);

  // Don't buffer output
  disable_buffering(stdout);
  disable_buffering(stderr);

  // Start a timer - after this elapses, the shellcode will be killed
  alarm(TIME);

  // Set the randomness in stone at the outset
  time_t t = time(NULL);

  // Immediately let the user know how much time they have
  printf("The current time is: %ld\n", t);
  printf("You have %d seconds to make this work\n", TIME);

  // Populate the random code block using a predictable RNG
  int i;
  srand(t);
  for(i = 0; i < CODE_LENGTH / 4; i++) {
    random_code[i] = rand();
  }

  // Sleep just for the joke
  sleep(1);
  printf("And to show you we're serious, you have %d seconds.\n\n", TIME - 1);

  // Read user's input
  ssize_t len = read(0, stack, STACK_LENGTH);

  if(len < 0) {
    printf("Error reading!\n");
    exit(1);
  }

  // Make sure they can't read in more code
  close(fileno(stdin));

  asm(
      // Set ESP to the stack the user supplied
      "mov %0, %%esp;"

      // Clear the remaining registers
      "mov $0, %%eax;"
      "mov $0, %%ebx;"
      "mov $0, %%ecx;"
      "mov $0, %%edx;"
      "mov $0, %%esi;"
      "mov $0, %%edi;"
      "mov $0, %%ebp;"

      // Return to the first address on the stack.
      // Ideally, the original execution environment is completely lost now. In
      // reality, there are probably ways to find it, but /shrug
      "ret;"
      : :"r"((int32_t)stack));

  return 0;
}
