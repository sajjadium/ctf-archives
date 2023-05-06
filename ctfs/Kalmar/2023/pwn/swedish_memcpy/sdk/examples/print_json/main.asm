[org 0x0]
[bits 64]

get_program_info:
    lea rdi, [rel buffer]
    mov rcx, 211 ; Program data JSON size
    mov rdx, 0 ; Program data JSON is at offset 0
    mov rax, 3 ; Get data
    int 0x0
print_buffer:
    lea rsi, [rel buffer]
print_on_screen:
    mov rax, 1
    int 0x0

    mov rax, 0
    int 0x0

buffer:
    
