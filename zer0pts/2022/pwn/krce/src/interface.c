#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>

#define CMD_NEW  0xeb15
#define CMD_EDIT 0xac1ba
#define CMD_SHOW 0x7aba7a
#define CMD_DEL  0x0da1ba

typedef struct {
  unsigned int index;
  unsigned int size;
  char *data;
} request_t;

void fatal(const char *msg)
{
  perror(msg);
  exit(1);
}

void add(int fd)
{
  request_t req;

  printf("index: ");
  if (scanf("%u%*c", &req.index) != 1)
    exit(1);

  printf("size: ");
  if (scanf("%u%*c", &req.size) != 1)
    exit(1);

  if (ioctl(fd, CMD_NEW, &req))
    puts("[-] Something went wrong");
  else
    puts("[+] Successfully created");
}

void edit(int fd)
{
  request_t req;

  printf("index: ");
  if (scanf("%u%*c", &req.index) != 1)
    exit(1);

  printf("size: ");
  if (scanf("%u%*c", &req.size) != 1)
    exit(1);

  printf("data: ");
  req.data = malloc(req.size);
  if (!req.data) {
    puts("[-] Invalid size");
    return;
  }
  for (unsigned int i = 0; i < req.size; i++) {
    if (scanf("%02hhx", &req.data[i]) != 1)
      exit(1);
  }

  if (ioctl(fd, CMD_EDIT, &req))
    puts("[-] Something went wrong");
  else
    puts("[+] Successfully updated");

  free(req.data);
}

void show(int fd)
{
  request_t req;

  printf("index: ");
  if (scanf("%u%*c", &req.index) != 1)
    exit(1);

  printf("size: ");
  if (scanf("%u%*c", &req.size) != 1)
    exit(1);

  req.data = malloc(req.size);
  if (!req.data) {
    puts("[-] Invalid size");
    return;
  }

  if (ioctl(fd, CMD_SHOW, &req) < 0)
    puts("[-] Something went wrong");
  else {
    printf("[+] Data: ");
    for (unsigned int i = 0; i < req.size; i++) {
      printf("%02hhx ", req.data[i]);
    }
    putchar('\n');
  }

  free(req.data);
}

void del(int fd)
{
  request_t req;

  printf("index: ");
  if (scanf("%u%*c", &req.index) != 1)
    exit(1);

  if (ioctl(fd, CMD_DEL, &req) < 0)
    puts("[-] Something went wrong");
  else
    puts("[+] Successfully deleted");
}

int main()
{
  int bufd = open("/dev/buffer", O_RDWR | O_CLOEXEC);
  if (bufd == -1)
    fatal("/dev/buffer");
  if (setregid(1337, 1337) == -1)
    fatal("setregid");
  if (setreuid(1337, 1337) == -1)
    fatal("setreuid");
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);

  puts("1. add");
  puts("2. edit");
  puts("3. show");
  puts("4. delete");
  while (1) {
    int choice;
    printf("> ");
    if (scanf("%d%*c", &choice) != 1)
      exit(1);

    switch (choice) {
    case 1: add(bufd); break;
    case 2: edit(bufd); break;
    case 3: show(bufd); break;
    case 4: del(bufd); break;
    default: return 0;
    }
  }
}
