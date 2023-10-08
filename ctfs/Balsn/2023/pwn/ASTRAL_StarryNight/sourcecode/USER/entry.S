.globl _start, hlt
.extern userMain
.intel_syntax noprefix
_start:
  call userMain
hlt:
  hlt
  jmp hlt
