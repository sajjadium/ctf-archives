section .data

msg: db "Welcome to my ISP!", 0xa, "Enter a 39-bit number in binary: "
len: equ $-msg

input: times 40 db 0
output: times 40 db 0xa
num: dq 0

flag: db "<REDACTED>"
flaglen: equ $-flag

section .text

global _start

_start:
    call get_input
    mov rax, 001101011101010001100001000101111011111b
    call f
    mov rax, 101000000011010111111010100110101011010b
    call g
    mov rax, 010110001000001011010111000000100011110b
    call f
    mov rax, 100111011010011101111111100100101110110b
    call g
    mov rax, 011010111001101000110011101000110011100b
    call f
    mov rax, 000010011110110100000010001011000111011b
    call g
    mov rax, 111110010001001100001110100111111111010b
    call g
    mov rax, 011110000001011100011010000000000110101b
    call f
    mov rax, 001111001001100010011001000100111001110b
    call g
    mov rax, 001111100111100000001111000100011110100b
    call f
    mov rax, 001110010001001001100011001110111001101b
    call f
    mov rax, 011010010111001001011001011000010001110b
    call g
    mov rax, 110001111001101010111000000100011110111b
    call g
    mov rax, 110101000110000000011000110011111100111b
    call g
    mov rax, 110011110101101100000100101010001110011b
    call f
    mov rax, 010001001011000011101101001001111110010b
    call g
    mov rax, 100110001101111110111110010001101010101b
    call f
    mov rax, 100110000100111101010000111110010101100b
    call f
    mov rax, 100101100011011011100001111110010100000b
    call f
    mov rax, 100011100000111111000001101000000011101b
    call f
    mov rax, [num]
    call print_number
    mov rax, [num]
    mov rbx, 100110011101000011101101111110011101011b
    cmp rax, rbx
    jne l0
    call print_flag
l0:
    call exit

get_input:
    sub rsp, 8
    mov rax, 1
    mov rdi, 1
    mov rsi, msg
    mov rdx, len
    syscall
    mov rax, 0
    mov rdi, 0
    lea rsi, [input]
    mov rdx, 39
    syscall
    mov rcx, 0
    mov r8, 0
l1:
    shl rcx, 1
    movzx rax, byte [input + r8]
    cmp rax, 0x31
    jne l2
    add rcx, 1
l2:
    add r8, 1
    cmp r8, 39
    jl l1
    mov [num], rcx
    add rsp, 8
    ret

f: ; What does this function do???
    sub rsp, 8
    mov r14, 127
    mov r15, rax
    mov r8, [num]
    shr r8, 31
    sub r8, r14
    mov r10, r15
    shr r10, 31
    sub r10, r14
    mov r9, 1
    shl r9, 31
    mov rbx, [num]
    mov eax, ebx
    btr rax, 31
    or r9, rax
    mov r11, 1
    shl r11, 31
    mov rbx, r15
    mov eax, ebx
    btr rax, 31
    or r11, rax
    cmp r8, r10
    je l6
    jl l4
    mov rcx, r8
    sub rcx, r10
    mov r10, r8
    cmp rcx, 32
    jg l3
    shr r11, cl
    mov r10, r8
    jmp l6
l3:
    mov r11, 0
    jmp l6
l4:
    mov rcx, r10
    sub rcx, r8
    mov r8, r10
    cmp rcx, 32
    jg l5
    shr r9, cl
    jmp l6
l5:
    mov r9, 0
l6:
    mov r12, r8
    mov r13, r9
    add r13, r11
    bt r13, 32
    jnc l7
    shr r13, 1
    add r12, 1
l7:
    btr r13, 31
    add r12, r14
    cmp r12, 0
    jl l8
    cmp r12, 256
    jge l8
    jmp l9
l8:
    call exit
l9:
    mov rax, r12
    shl rax, 31
    or rax, r13
    mov [num], rax
    add rsp, 8
    ret

g: ; Or this one???
    sub rsp, 8
    mov r14, 127
    mov r15, rax
    mov r8, [num]
    shr r8, 31
    sub r8, r14
    mov r10, r15
    shr r10, 31
    sub r10, r14
    mov r9, 1
    shl r9, 31
    mov rbx, [num]
    mov eax, ebx
    btr rax, 31
    or r9, rax
    mov r11, 1
    shl r11, 31
    mov rbx, r15
    mov eax, ebx
    btr rax, 31
    or r11, rax
    mov r12, r8
    add r12, r10
    mov rax, r9
    mul r11d
    shl rdx, 32
    mov r13, rdx
    or r13, rax
    bt r13, 63
    jnc l10
    shr r13, 1
    add r12, 1
l10:
    shr r13, 31
    btr r13, 31
    add r12, r14
    cmp r12, 0
    jl l11
    cmp r12, 256
    jge l11
    jmp l12
l11:
    call exit
l12:
    mov rax, r12
    shl rax, 31
    or rax, r13
    mov [num], rax
    add rsp, 8
    ret

print_number:
    sub rsp, 8
    mov r8, 0
l13:
    mov byte [output + r8], 0x30
    bt rax, 38
    jnc l14
    mov byte [output + r8], 0x31
l14:
    shl rax, 1
    add r8, 1
    cmp r8, 39
    jl l13
    mov rax, 1
    mov rdi, 1
    mov rsi, output
    mov rdx, 40
    syscall
    add rsp, 8
    ret

print_flag:
    sub rsp, 8
    mov rax, 1
    mov rdi, 1
    mov rsi, flag
    mov rdx, flaglen
    syscall
    add rsp, 8
    ret

exit:
    mov rax, 60
    mov rdi, 0
    syscall
