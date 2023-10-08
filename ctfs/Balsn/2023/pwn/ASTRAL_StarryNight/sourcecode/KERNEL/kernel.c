#include "kernel.h"

KERNEL_RUNTIME_CONTEXT g_runtimeContext;
uint64_t kernelStack;
uint64_t userStack;

void registerSyscall() {
  asm(
    "xor rax, rax;"
    "mov rdx, 0x00200008;"
    "mov ecx, %[msr_star];"
    "wrmsr;"
    "mov eax, %[fmask];"
    "xor rdx, rdx;"
    "mov ecx, %[msr_fmask];"
    "wrmsr;"
    "lea rax, [rip + syscallEntry];"
    "mov rdx, rax;"
    "shr rdx, 32;"
    "mov ecx, %[msr_syscall];"
    "wrmsr;"
    :
    : [msr_star] "i" (MSR_STAR),
      [fmask] "i" (0x3f7fd5), [msr_fmask]"i"(MSR_SYSCALL_MASK),
      [msr_syscall]"i"(MSR_LSTAR)
    : "rax", "rdx", "rcx"
  );
  return;
}

void initRuntimeContext(uint64_t kaslr, uint64_t uaslr) {
  g_runtimeContext.kernelMmapBase = kaslr;
  g_runtimeContext.userMmapBase = uaslr;
  return;
}

void __attribute__((noreturn)) startUser(uint64_t rip, uint64_t rsp) {
  asm (
    "mov [rip + kernelStack], rsp;"
    "mov rcx, %[rip];"
    "mov r11, 0x2;"      /* rflags */
    "mov rsp, %[rsp];"
    "xor rax, rax;"
    "xor rbx, rbx;"
    "xor rdx, rdx;"
    "xor rdi, rdi;"
    "xor rsi, rsi;"
    "xor rbp, rbp;"
    "xor r8, r8;"
    "xor r9, r9;"
    "xor r10, r10;"
    "xor r12, r12;"
    "xor r13, r13;"
    "xor r14, r14;"
    "xor r15, r15;"
    "xor rbp, rbp;"
    ".byte 0x48;"
    "sysretq;"
    :
    : [rip] "r" (rip), [rsp] "r" (rsp)
    : "r11", "rcx"
  );
  while(1);
}

void __attribute__((noreturn)) kernelMain(uint64_t kaslr, uint64_t elfImageAddr) {
  uint64_t entry, uaslr, ustack;
  uaslr = genUaslr();
  ustack = genUaslr();
  while (ustack == uaslr) {
    ustack = genUaslr();
  }
  if (ustack < uaslr) {
    uaslr ^= ustack;
    ustack ^= uaslr;
    uaslr ^= ustack;
  }
  initRuntimeContext(kaslr, uaslr);
  initAllocator();
  initAppletStorage();
  registerSyscall();
  if (initUserRuntime(elfImageAddr, uaslr, ustack, &entry) == FAIL) panic("initUserRuntime failed");
  startUser(entry, ustack + USER_STACK_SIZE);
}
