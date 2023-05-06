#include <stdio.h>
#include <unistd.h>
#include <seccomp.h>

void gadgets()
{
  __asm__("pop %rdi; ret\n\t");
}

int sandbox()
{
  scmp_filter_ctx ctx;
  ctx = seccomp_init(SCMP_ACT_KILL); // default action: kill
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(mmap), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
  seccomp_load(ctx);
  return 0;
}

int main(int argc, char const *argv[])
{
    char buffer[32];
    gets(buffer);
    return sandbox();
}
