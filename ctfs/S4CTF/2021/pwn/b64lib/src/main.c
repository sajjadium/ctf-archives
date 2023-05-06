#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <base64.h>

#define BUFFER_SIZE 0x40

int cnt;

__attribute__((constructor))
void setup(void) {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  alarm(60);
}

void readline(const char *msg, char *buf, int size) {
  int s;

  if (msg) printf("%s", msg);
  if ((s = read(0, buf, size)) <= 0) exit(0);

  if (buf[s-1] == '\n') buf[s-1] = 0;
  else if (s < size) buf[s] = 0;
}

int readint(void) {
  char buf[16];
  readline(NULL, buf, 15);
  return atoi(buf);
}

int menu() {
  puts("1. Encode");
  puts("2. Decode");
  puts("x. Exit");
  printf("> ");
  return readint();
}

int main(void) {
  int choice;
  void (*b64func[])(const char*, char*, int) = {b64encode, b64decode};
  char input[BUFFER_SIZE], output[BUFFER_SIZE];
  memset(input, 0, BUFFER_SIZE);
  memset(output, 0, BUFFER_SIZE);

  for(cnt = 0; cnt < 10; cnt++) {
    // read user input
    choice = menu();
    if (choice < 1 || choice > 2) break;

    // encode | decode
    readline("Input: ", input, BUFFER_SIZE);
    b64func[choice-1](input, output, strlen(input));

    // show result
    if (b64chkerr()) {
      printf("Error: %s\n", b64errmsg());
    } else {
      printf("Output: %s\n", output);
    }
  }

  puts("Bye!");
}
