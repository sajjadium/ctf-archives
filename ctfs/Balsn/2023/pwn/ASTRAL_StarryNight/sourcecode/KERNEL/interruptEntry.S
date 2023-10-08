.globl _interruptStart
.extern kAppletInterrupt, hlt
.intel_syntax noprefix
_interruptStart:
  call kAppletInterrupt
  hlt
  jmp hlt
