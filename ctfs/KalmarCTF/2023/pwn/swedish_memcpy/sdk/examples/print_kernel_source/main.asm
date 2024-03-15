EFAULT equ -2

[org 0x0]
[bits 64]
entry:
print_kernel_source:
    mov rdx, 212 ; Kernel source start offset
.loop:
    ; Read info
    mov rcx, 1 ; Read one byte at a time
    lea rdi, [rel buffer] ; What we want to print on the screen
    mov rax, 3
    int 0x0
    cmp rax, EFAULT
    je .end

    ; Increment the offset we're reading at
    inc rdx

    lea rsi, [rel buffer]
    mov rax, 1
    int 0x0

    jmp .loop

.end:
    mov rax, 0
    int 0x0

buffer:
    db 0
null_term:
    db 0
