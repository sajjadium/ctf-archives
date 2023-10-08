.globl _start, hlt
.extern kernelMain
.intel_syntax noprefix
_start:
  call kernelMain
hlt:
  hlt
  jmp hlt
