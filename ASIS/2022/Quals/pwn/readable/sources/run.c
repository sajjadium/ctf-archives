#include <linux/audit.h>
#include <linux/filter.h>
#include <linux/seccomp.h>
#include <linux/unistd.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mount.h>
#include <sys/prctl.h>
#include <sys/ptrace.h>
#include <sys/syscall.h>
#include <unistd.h>

#define syscall_nr (offsetof(struct seccomp_data, nr))
#define arch_nr (offsetof(struct seccomp_data, arch))
#define ARCH_NR AUDIT_ARCH_X86_64

#define VALIDATE_ARCHITECTURE                             \
  BPF_STMT(BPF_LD + BPF_W + BPF_ABS, arch_nr),            \
      BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, ARCH_NR, 1, 0), \
      BPF_STMT(BPF_RET + BPF_K, SECCOMP_RET_KILL)

#define EXAMINE_SYSCALL BPF_STMT(BPF_LD + BPF_W + BPF_ABS, syscall_nr)

#define DISALLOW_SYSCALL(name)                            \
  BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, __NR_##name, 0, 1), \
      BPF_STMT(BPF_RET + BPF_K, SECCOMP_RET_KILL)

#define ALLOW_SYSCALLS BPF_STMT(BPF_RET + BPF_K, SECCOMP_RET_ALLOW)

static int install_filter() {
  struct sock_filter filter[] = {
      VALIDATE_ARCHITECTURE,
      EXAMINE_SYSCALL,
      DISALLOW_SYSCALL(ptrace),
      DISALLOW_SYSCALL(process_vm_readv),
      DISALLOW_SYSCALL(process_vm_writev),
      ALLOW_SYSCALLS,
  };
  struct sock_fprog prog = {
      .len = (unsigned short)(sizeof(filter) / sizeof(filter[0])),
      .filter = filter,
  };

  if (prctl(PR_SET_SECCOMP, 2, &prog)) {
    perror("prctl(PR_SET_SECCOMP)");
    exit(1);
  }
  return 0;
}

int main(char **) {
  install_filter();
  if (umount("/proc")) {
    perror("could not umount procfs");
    exit(1);
  }
  if (setgid(1000) || setuid(1000)) {
    perror("could not drop privs");
    exit(1);
  }

  char *args = NULL;
  execve("/tmp/exploit",&args,&args);
  return 1;
}
