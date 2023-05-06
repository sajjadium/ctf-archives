#include <stdio.h>
#include <string.h>

int main(void)
{
  char your_reassuring_and_comforting_we_will_arrive_safely_in_libc[32];

  setbuf(stdout, NULL);
  setbuf(stdin, NULL);
  setbuf(stderr, NULL);

  puts("that board meeting was a *smashing* success! rob loved the challenge!");
  puts("in fact, he loved it so much he sponsored me a business trip to this place called 'libc'...");
  puts("where is this place? can you help me get there safely?");

  // please i cant afford the medical bills if we crash and segfault
  gets(your_reassuring_and_comforting_we_will_arrive_safely_in_libc);

  puts("phew, good to know. shoot! i forgot!");
  printf("rob said i'd need this to get there: %llx\n", printf);
  puts("good luck!");
}
