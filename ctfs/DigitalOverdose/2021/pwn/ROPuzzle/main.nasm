section .text
global _start

section .data
msg db '/bin/sh'

section .text

_start:
    push rbp
    mov rbp, rsp
    call get_input
    call exit

get_input:
    push rbp
    mov rbp, rsp
    mov rax, 0x0
    mov rdi, 0x0
    mov rsi, rsp
    mov rdx, 4096
    call syscall_me
    leave
    ret

syscall_me:
    syscall
    ret

exit:
    mov rax, 0x3c
    mov rdi, 0x0
    syscall
    call exit

gadget:
    pop rax
    ret