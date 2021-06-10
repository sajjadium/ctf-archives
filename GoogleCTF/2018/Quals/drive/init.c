#define _GNU_SOURCE
#include "util.h"

#include <stdio.h>
#include <sys/prctl.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <err.h>

static pid_t spawn_binary(int exec_fd) {
  pid_t pid = check(fork(), "fork(spawn binary)");
  if (pid == 0) {
    const char * const argv[] = {"foobar", NULL};
    syscall(SYS_execveat, exec_fd, "", argv, NULL, AT_EMPTY_PATH);
    err(1, "execveat(foobar)");
  }
  return pid;
}

static void waitfor(pid_t pid) {
  int wstatus = 0;
  while (1) {
    check(waitpid(pid, &wstatus, WUNTRACED), "waitpid");
    if (WIFEXITED(wstatus) || WIFSIGNALED(wstatus)) {
      return;
    }
  }
}

int main(int argc, char *argv[]) {
  int broker_fd = BROKER_FD;
  int sandbox_fd = SANDBOX_FD;

  make_cloexec(sandbox_fd);
  // Leave the broker fd open for the sandboxees

  while (1) {
    int exec_fd = recv_fd(sandbox_fd);
    pid_t pid = spawn_binary(exec_fd);
    waitfor(pid);
    send_str(sandbox_fd, "OK");
  }

  return 0;
}

