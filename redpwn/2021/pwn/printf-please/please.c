#include <stdio.h>
#include <fcntl.h>

int main(void)
{
  char buffer[0x200];
  char flag[0x200];

  setbuf(stdout, NULL);
  setbuf(stdin, NULL);
  setbuf(stderr, NULL);

  memset(buffer, 0, sizeof(buffer));
  memset(flag, 0, sizeof(flag));

  int fd = open("flag.txt", O_RDONLY);
  if (fd == -1) {
    puts("failed to read flag. please contact an admin if this is remote");
    exit(1);
  }

  read(fd, flag, sizeof(flag));
  close(fd);

  puts("what do you say?");

  read(0, buffer, sizeof(buffer) - 1);
  buffer[strcspn(buffer, "\n")] = 0;

  if (!strncmp(buffer, "please", 6)) {
    printf(buffer);
    puts(" to you too!");
  }
}
