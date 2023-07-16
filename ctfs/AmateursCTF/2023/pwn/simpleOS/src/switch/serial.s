    .intel_syntax noprefix
    .section .code16, "awx"
    .code16


    .include "src/switch/macros.s"


    .global serial_init
    .global serial_send16


    .equ COM1, 0x3F8


serial_init:
    pusha

    outb  COM1+1, 0x00
    outb  COM1+3, 0x80
    outb  COM1+0, 0x03
    outb  COM1+1, 0x00
    outb  COM1+3, 0x03
    outb  COM1+2, 0xC7
    outb  COM1+4, 0x0B
    outb  COM1+4, 0x1E
    outb  COM1+0, 0xAE

    inb   COM1+0
    cmp   al,     0xAE
    jz    serial_init_ok

1:  jmp   1b

serial_init_ok:
    outb  COM1+4, 0x0F
    outb  COM1+1, 0x01

    mov   si,    offset serial_init_success
    call  serial_send16

    popa
    ret 


serial_init_fail: .asciz "failed to initialize serial in 16 bit mode"
serial_init_success: .asciz "initialized serial\n"


serial_send16:
    pusha
2:
    inb   COM1+5
    test  al,   0x20
    jz    2b

    lodsb
    test  al,    al
    jz    1f
    mov   dx,    COM1+0
    out   dx,    al
    jmp   2b
1:
    popa
    ret 


    .att_syntax prefix
