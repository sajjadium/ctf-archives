[org 0x0]
[bits 64]
entry:
    lea rsi, [rel buffer]
    mov rax, 1
    int 0x0
    mov rax, 0
    int 0x0

buffer:
    db "Hello, world!", 0
