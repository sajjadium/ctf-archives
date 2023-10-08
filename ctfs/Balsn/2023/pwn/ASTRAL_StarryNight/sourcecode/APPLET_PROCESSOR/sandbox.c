#include "sandbox.h"

struct sock_filter seccompfilter[]={
  BPF_STMT(BPF_LD | BPF_W | BPF_ABS, ArchField),
  BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, AUDIT_ARCH_X86_64, 1, 0),
  BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),
  BPF_STMT(BPF_LD | BPF_W | BPF_ABS, SyscallNum),
  BPF_JUMP(BPF_JMP | BPF_JGE | BPF_K, 0x40000000, 0, 1),
  BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),
  Allow(poll),
  Allow(read),
  Allow(write),
  Allow(newfstatat),
  Allow(futex),
  Allow(getrandom),
  Allow(brk),
  Allow(mmap),
  Allow(mprotect),
  Allow(nanosleep),
  Allow(exit),
  Allow(exit_group),
  BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_openat, 0, 1),
  BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ERRNO | 0xffff),
  BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),
};

struct sock_fprog filterprog={
  .len=sizeof(seccompfilter)/sizeof(struct sock_filter),
  .filter=seccompfilter
};

void applySeccomp(){
  if(prctl(PR_SET_NO_NEW_PRIVS,1,0,0,0)){
    printError("applySeccomp::PR_SET_NO_NEW_PRIVS failed");
  }
  if(prctl(PR_SET_SECCOMP,SECCOMP_MODE_FILTER,&filterprog)==-1){
    printError("applySeccomp::PR_SET_SECCOMP failed");
  }
  return;
}
