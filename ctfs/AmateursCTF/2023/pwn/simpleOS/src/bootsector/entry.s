    .intel_syntax noprefix
    .section .bootsector, "awx"
    .code16

    .extern  _zig_entry

    .global  _entry

_entry:
    cli
    xor   ax,    ax
    mov   ds,    ax
    mov   es,    ax
    mov   ss,    ax
    mov   fs,    ax
    mov   gs,    ax
    mov   sp,    0x7C00

    push  ecx
    push  edi
    push  edx

    call  _zig_entry

    .section .stub, "awx"
_stub:
    jmp   _entry