#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <seccomp.h>
#include <sys/random.h>

const int blacklist[] = {
  SCMP_SYS(open), SCMP_SYS(openat),
  SCMP_SYS(execve), SCMP_SYS(execveat),
};

void fatal(const char *msg) {
  printf("[-] %s\n", msg);
  exit(1);
}

void rndstr(unsigned char *name, int len) {
  if (getrandom(name, len, 0) != len)
    fatal("Failed to generate name");
  while(len--) {
    if (name[len] < 107) {
      name[len] = 'A' + (name[len] % 26);
    } else if (name[len] < 214) {
      name[len] = 'a' + (name[len] % 26);
    } else {
      name[len] = '0' + (name[len] % 10);
    }
  }
}


int fscmp(const char *authdir, const char *filename, const char *data) {
  int fd, n;
  char buf[0x100];

  snprintf(buf, sizeof(buf), "%s/%s", authdir, filename);
  if ((fd = open(buf, O_RDONLY)) < 0)
    return 1;

  memset(buf, 0, sizeof(buf));
  n = read(fd, buf, sizeof(buf));
  close(fd);
  if (n < 0) return 1;
  else buf[n] = 0;

  return strncmp(buf, data, strlen(buf) + 1);
}

void sandboxify(void) {
  int i;
  scmp_filter_ctx ctx;

  ctx = seccomp_init(SCMP_ACT_ALLOW);
  if (ctx == NULL) fatal("Failed to initialize seccomp");

  for(i = 0; i < sizeof(blacklist) / sizeof(int); i++) {
    if (seccomp_rule_add(ctx, SCMP_ACT_KILL, blacklist[i], 0) < 0)
      fatal("Failed to add a rule");
  }

  if (seccomp_load(ctx) < 0)
    fatal("Failed to install seccomp");

  seccomp_release(ctx);
}
