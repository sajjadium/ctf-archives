#include <unistd.h>
#include <stdio.h>
#include <seccomp.h>

#define SYS_FILTER_FAIL 2
#define SUCCESS 0

#define WHITELIST_SYSCALL(syscall) \
  if (seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(syscall), 0)) goto err;

void init_filter() 
{
  static bool init = false;
  if (init) 
    return;

  scmp_filter_ctx ctx;

  if (!(ctx = seccomp_init(SCMP_ACT_KILL_PROCESS)))
    goto err;

  WHITELIST_SYSCALL(openat);
  WHITELIST_SYSCALL(read);
  WHITELIST_SYSCALL(write);
  WHITELIST_SYSCALL(sendfile);
  WHITELIST_SYSCALL(exit_group);
  
  if (seccomp_load(ctx))
    goto err;

  seccomp_release(ctx);
  
  init = true;
  return;
err:
  exit(SYS_FILTER_FAIL);
}
#undef WHITELIST_SYSCALL

#define BFSZ 208 
int main() 
{
  char bf[BFSZ];
  
  setvbuf(stdout, nullptr, _IONBF, 0);
  init_filter();

  puts("name your moose: ");
  read(STDIN_FILENO, bf, BFSZ+152);
  puts("your mooses name is:");
  puts(bf);
  puts("congrats!");

  return SUCCESS;
}
