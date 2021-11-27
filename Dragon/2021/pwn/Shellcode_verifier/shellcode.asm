[BITS 64]

section .text
global call_shellcode

call_shellcode:
    push rbp
    push rbx
    push r15
    push r14
    push r13
    push r12

    push rdi

    xor eax, eax
    xor ebx, ebx
    xor ecx, ecx
    xor edx, edx
    xor esi, esi
    xor edi, edi
    xor ebp, ebp
    xor r8, r8
    xor r9, r9
    xor r10, r10
    xor r11, r11
    xor r12, r12
    xor r13, r13
    xor r14, r14
    xor r15, r15

    call [rsp]

    pop rdi

    pop r12
    pop r13
    pop r14
    pop r15
    pop rbx
    pop rbp
    ret

section .note.GNU-stack noalloc noexec nowrite progbits
