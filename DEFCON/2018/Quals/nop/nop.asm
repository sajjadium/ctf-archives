bits 32

section .text
global _start

_start:
    mov eax, 0x05
    int 0x80

