    .intel_syntax noprefix

    .section .boot64, "awx"
    .code64

    .extern _start
    .extern gdt64_offset_data
    .extern __e820_memory_map
    .extern __e820_memory_map_len
    .extern identity_map
    .extern __end_of_bootloader

    .global _code_64


    .equ STACK_SIZE, 0x100000 * 4


_code_64:
    cli
    mov ax, offset gdt64_offset_data
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax

    mov rsp, 0x200000

    mov rsi, offset enter_code64
    call serial_send64

    mov rdi, offset __e820_memory_map
    mov rcx, qword ptr [__e820_memory_map_len]
    xor rbx, rbx
    mov rdx, offset __end_of_bootloader
search:
    mov eax, dword ptr [rdi + 16]
    cmp eax, 1
    jz  1f
    cmp eax, 3
    jz  1f
    jmp 2f

1:
    mov rax, qword ptr [rdi + 8]
    cmp rax, STACK_SIZE
    jl  2f
    add rax, qword ptr [rdi]
    mov rsi, rax
    sub rax, STACK_SIZE
    cmp rax, rdx
    jl  2f

    mov rbx, rax
    sub rsi, rax
    jmp 1f

2:
    add rdi, 24
    dec rcx
    jnz search

    mov rsi, offset stack_fail
    call serial_send64
0:  jmp 0b

1:
    lea rdi, [rbx + rsi]
    sub rdi, STACK_SIZE
    mov rcx, STACK_SIZE / 0x1000
setup_stack:
    push rdi
    push rcx
    call identity_map
    pop rcx
    pop rdi
    add rdi, 0x1000
    dec rcx
    jnz setup_stack

    mov rsp, rdi
    mov rsi, rdi
    sub rdi, STACK_SIZE

    call _start


serial_send64:
    push rsi
    push rax
    push rdx
1:
    mov dx, 0x3F8 + 5
    in al, dx
    test al, 0x20
    jz 1b

    lodsb
    test al, al
    jz 2f
    mov dx, 0x3F8
    out dx, al
    jmp 1b
2:
    pop rdx
    pop rax
    pop rsi
    ret


stack_fail: .asciz "failed to setup stack. contact an admin.\n"
enter_code64: .asciz "enter code64\n"


    .att_syntax prefix
    