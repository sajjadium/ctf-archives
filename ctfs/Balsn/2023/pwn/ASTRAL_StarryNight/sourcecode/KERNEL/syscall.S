.globl syscallEntry, kernelStack, userStack
.extern syscallHandler
.intel_syntax noprefix

syscallEntry:
  mov [rip + userStack], rsp
  mov rsp, [rip + kernelStack]
  push rdi
  push rsi
  push rbx
  push rdx
  push rcx
  push rbp
  push r8
  push r9
  push r10
  push r11
  push r12
  push r13
  push r14
  push r15
  mov rcx, r10
  call syscallHandler
  pop r15
  pop r14
  pop r13
  pop r12
  pop r11
  pop r10
  pop r9
  pop r8
  pop rbp
  pop rcx
  pop rdx
  pop rbx
  pop rsi
  pop rdi
  mov rsp, [rip + userStack]
  .byte 0x48
  sysretq
