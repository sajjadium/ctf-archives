Added to `arch/x86/entry/syscalls/syscall_64.tbl`
```
1337 64 seccon sys_seccon
```

Added to `kernel/sys.c`:
```c
SYSCALL_DEFINE1(seccon, unsigned long, rip)
{
  asm volatile("xor %%edx, %%edx;"
               "xor %%ebx, %%ebx;"
               "xor %%ecx, %%ecx;"
               "xor %%edi, %%edi;"
               "xor %%esi, %%esi;"
               "xor %%r8d, %%r8d;"
               "xor %%r9d, %%r9d;"
               "xor %%r10d, %%r10d;"
               "xor %%r11d, %%r11d;"
               "xor %%r12d, %%r12d;"
               "xor %%r13d, %%r13d;"
               "xor %%r14d, %%r14d;"
               "xor %%r15d, %%r15d;"
               "xor %%ebp, %%ebp;"
               "xor %%esp, %%esp;"
               "jmp %0;"
               "ud2;"
               : : "rax"(rip));
  return 0;
}
```
