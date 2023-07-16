    .intel_syntax noprefix
    .section .mbrsector, "awx"
    .code16

    .extern  _zig_entry
    .extern  _entry_base

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

    push  edx

    mov   di,   offset _entry_base
    mov   si,   0x7C00
    mov   cx,   256
    rep   movsw

    mov   ax,   0x02
    int   0x10

    mov   eax,  offset _zig_entry
    call  eax