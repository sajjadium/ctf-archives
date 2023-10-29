; This is an example user programm for Dasdorf super-secure (TM) OS (aka DAS SOS).
;
; It uses the Intel assembly syntax and can be compiled on x86-based machines
; using the following command:
; nasm -f bin -o example_user_program example_user

[org 0x10000000000] ; The user program will always be loaded at this address by DAS SOS.
[bits 64]           ; We're in long mode.

%define SYSCALL_EXIT    0
%define SYSCALL_PUTS    4

[section .text]
main:
    mov rdi, example_string     ; Move the address of the string to the function parameter register.
    call puts                   ; print it!

    call exit


; A simple puts implementation calling the syscall.
; Parameters:
;   - rdi: Address of the string to print.
puts:
    push rbp
    mov rbp, rsp

    mov rax, SYSCALL_PUTS       ; Syscall # = puts
    mov rdi, example_string     ; The string to print.
    syscall

    leave
    ret


; Call the exit syscall.
; Parameters: none
exit:
    mov rax, SYSCALL_EXIT       ; Syscall #0 = exit
    syscall
    jmp exit                    ; Should not be called.

[section .data]
example_string:
    db "Hello, World!", 0xa, 0x0 ; Make sure to have the 0-byte as end of string.
