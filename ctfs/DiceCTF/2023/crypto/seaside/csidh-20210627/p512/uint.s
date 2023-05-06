
.intel_syntax noprefix

.section .rodata

.global uint_0
uint_0: .quad 0, 0, 0, 0, 0, 0, 0, 0

.global uint_1
.hidden uint_1
uint_1: .quad 1, 0, 0, 0, 0, 0, 0, 0


.section .text


.global uint_eq
uint_eq:
    xor eax, eax
.set k, 0
.rept 8
    mov rdx, [rdi + 8*k]
    xor rdx, [rsi + 8*k]
    or rax, rdx
    .set k, k+1
.endr
    test rax, rax
    setz al
    movzx eax, al
    ret


.global uint_set
uint_set:
    cld
    mov rax, rsi
    stosq
    xor rax, rax
    mov ecx, 7
    rep stosq
    ret


.global uint_len
uint_len:
    mov ecx, 7
0:  bsr rax, [rdi + 8*rcx]
    jnz 1f
    loop 0b
    bsr rax, [rdi]
    lea rax, [rax + 1]
    cmovz rax, rcx
    ret
1:  shl ecx, 6
    lea rax, [rax + rcx + 1]
    ret

.global uint_bit
uint_bit:
    mov ecx, esi
    and ecx, 0x3f
    shr rsi, 6
    mov rax, [rdi + 8*rsi]
    shr rax, cl
    and rax, 1
    ret


.global uint_add3
uint_add3:
    mov rax, [rsi +  0]
    add rax, [rdx +  0]
    mov [rdi +  0], rax
    .set k, 1
    .rept 7
        mov rax, [rsi + 8*k]
        adc rax, [rdx + 8*k]
        mov [rdi + 8*k], rax
        .set k, k+1
    .endr
    setc al
    movzx eax, al
    ret

.global uint_sub3
uint_sub3:
    mov rax, [rsi +  0]
    sub rax, [rdx +  0]
    mov [rdi +  0], rax
    .set k, 1
    .rept 7
        mov rax, [rsi + 8*k]
        sbb rax, [rdx + 8*k]
        mov [rdi + 8*k], rax
        .set k, k+1
    .endr
    setc al
    movzx eax, al
    ret


.global uint_mul3_64
uint_mul3_64:

    mulx r10, rax, [rsi +  0]
    mov [rdi +  0], rax

    mulx r11, rax, [rsi +  8]
    add  rax, r10
    mov [rdi +  8], rax

    mulx r10, rax, [rsi + 16]
    adcx rax, r11
    mov [rdi + 16], rax

    mulx r11, rax, [rsi + 24]
    adcx rax, r10
    mov [rdi + 24], rax

    mulx r10, rax, [rsi + 32]
    adcx rax, r11
    mov [rdi + 32],rax

    mulx r11, rax, [rsi + 40]
    adcx rax, r10
    mov [rdi + 40],rax

    mulx r10, rax, [rsi + 48]
    adcx rax, r11
    mov [rdi + 48],rax

    mulx r11, rax, [rsi + 56]
    adcx rax, r10
    mov [rdi + 56],rax

    ret


.global uint_random
uint_random:
    test rsi, rsi
    jnz 0f
    mov esi, 64
    jmp randombytes
0:
    push r12    /* x */
    push r13    /* m */
    push rbx    /* bits */
    push rbp    /* mask */

    mov r12, rdi
    mov r13, rsi

    jz 1f
    mov rdi, rsi
    call uint_len
    mov ebx, eax
    mov ebp, 1
    mov ecx, eax
    and ecx, 0x3f
    shl rbp, cl
    dec rbp

    mov rdi, r12
    cld
    mov ecx, 8
    xor eax, eax
    rep stosq

0:
    mov rdi, r12
    mov esi, ebx
    add esi, 7
    shr esi, 3
    call randombytes

    mov ecx, ebx
    shr ecx, 6
    cmp ecx, 8
    je 1f
    and [r12 + 8*rcx], rbp
    1:

    .set k, 7
    .rept 8
        mov rax, [r13 + 8*k]
        cmp [r12 + 8*k], rax
        ja 0b
        jb 2f
        .set k, k-1
    .endr
    jmp 0b
2:  pop rbp
    pop rbx
    pop r13
    pop r12
    ret

