.globl panic
.extern hlt
.intel_syntax noprefix
panic:
  mov eax, edi
  mov dx, 0x8002
  out dx, eax
  jmp hlt
