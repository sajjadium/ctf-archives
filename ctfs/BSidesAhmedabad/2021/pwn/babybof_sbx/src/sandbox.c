#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/prctl.h>
#include <sys/stat.h>
#include <unistd.h>
#include <linux/seccomp.h>
#include <signal.h>

#define RULE_FILENAME "rule.bin"
#define DEBUG(x) puts("[libsandbox.so] "x);

static void __install_seccomp(void) {
  struct stat st;
  if (stat(RULE_FILENAME, &st) == -1) {
    perror("stat");
    exit(1);
  }

  unsigned char *filter = malloc(st.st_size);
  if (filter == NULL) {
    perror("malloc");
    exit(1);
  }

  int fd = open(RULE_FILENAME, O_RDONLY);
  if (fd == -1 || read(fd, filter, st.st_size) != st.st_size) {
    perror(RULE_FILENAME);
    exit(1);
  }

  struct prog {
    unsigned short len;
    unsigned char *filter;
  } rule = {.len = st.st_size >> 3, .filter = filter};

  if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) < 0) {
    perror("prctl(PR_SET_NO_NEW_PRIVS)");
    exit(1);
  }

  if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &rule) < 0) {
    perror("prctl(PR_SET_SECCOMP)");
    exit(1);
  }
}

static void __funeral(int sig) {
  DEBUG("Sandboxed process terminated");
}

static void __watcher(void) {
  int pid = fork();
  if (pid == -1) {
    perror("fork");
    exit(1);
  } else if (pid) {
    return;
  }

  prctl(PR_SET_PDEATHSIG, SIGHUP);
  signal(SIGHUP, __funeral);
  pause();
  exit(0);
}

__attribute__((constructor))
static void __initialize(void) {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  __watcher();
  DEBUG("Setting up sandbox...");
  __install_seccomp();
  DEBUG("Sandbox is successfully setup");
}
