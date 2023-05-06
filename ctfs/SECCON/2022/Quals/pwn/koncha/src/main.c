#include <stdio.h>
#include <unistd.h>

int main() {
  char name[0x30], country[0x20];

  /* Ask name (accept whitespace) */
  puts("Hello! What is your name?");
  scanf("%[^\n]s", name);
  printf("Nice to meet you, %s!\n", name);

  /* Ask country */
  puts("Which country do you live in?");
  scanf("%s", country);
  printf("Wow, %s is such a nice country!\n", country);

  /* Painful goodbye */
  puts("It was nice meeting you. Goodbye!");
  return 0;
}

__attribute__((constructor))
void setup(void) {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  alarm(180);
}
