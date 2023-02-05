
.intel_syntax noprefix

.section .data
.global fp_mul_counter
.hidden fp_mul_counter
fp_mul_counter: .quad 0
.global fp_sq_counter
.hidden fp_sq_counter
fp_sq_counter: .quad 0
.global fp_inv_counter
.hidden fp_inv_counter
fp_inv_counter: .quad 0
.global fp_sqt_counter
.hidden fp_sqt_counter
fp_sqt_counter: .quad 0

.section .text

.fp_copy:
    cld
    mov ecx, 8
    rep movsq
    ret


.global fp_eq
fp_eq:
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


.global fp_set
fp_set:
    push rdi
    call uint_set
    pop rdi
    mov rsi, rdi
    jmp fp_enc


.global fp_add2
fp_add2:
    mov rdx, rdi
    /* jmp fp_add3 */

.global fp_add3
fp_add3:
    push r12
    push r13

.macro REDONCE, r0, r1, r2, r3, r4, r5, r6, r7
    cmp \r7, [rip + p + 56]
    jb 0f
    ja 1f
    cmp \r6, [rip + p + 48]
    jb 0f
    ja 1f
    cmp \r5, [rip + p + 40]
    jb 0f
    ja 1f
    cmp \r4, [rip + p + 32]
    jb 0f
    ja 1f
    cmp \r3, [rip + p + 24]
    jb 0f
    ja 1f
    cmp \r2, [rip + p + 16]
    jb 0f
    ja 1f
    cmp \r1, [rip + p +  8]
    jb 0f
    ja 1f
    cmp \r0, [rip + p +  0]
    jb 0f
1:  sub \r0, [rip + p +  0]
    sbb \r1, [rip + p +  8]
    sbb \r2, [rip + p + 16]
    sbb \r3, [rip + p + 24]
    sbb \r4, [rip + p + 32]
    sbb \r5, [rip + p + 40]
    sbb \r6, [rip + p + 48]
    sbb \r7, [rip + p + 56]
0:
.endm

.macro STOREREGS, m, r0, r1, r2, r3, r4, r5, r6, r7
    mov [\m +  0], \r0
    mov [\m +  8], \r1
    mov [\m + 16], \r2
    mov [\m + 24], \r3
    mov [\m + 32], \r4
    mov [\m + 40], \r5
    mov [\m + 48], \r6
    mov [\m + 56], \r7
.endm

    mov  r8,  [rsi +  0]
    mov  r9,  [rsi +  8]
    mov  r10, [rsi + 16]
    mov  r11, [rsi + 24]
    mov  r12, [rsi + 32]
    mov  r13, [rsi + 40]
    mov  rax, [rsi + 48]
    mov  rcx, [rsi + 56]

    add r8,  [rdx +  0]
    adc r9,  [rdx +  8]
    adc r10, [rdx + 16]
    adc r11, [rdx + 24]
    adc r12, [rdx + 32]
    adc r13, [rdx + 40]
    adc rax, [rdx + 48]
    adc rcx, [rdx + 56]

    REDONCE        r8, r9, r10, r11, r12, r13, rax, rcx
    STOREREGS rdi, r8, r9, r10, r11, r12, r13, rax, rcx

    pop r13
    pop r12
    ret


.global fp_sub2
fp_sub2:
    mov rdx, rdi
    xchg rsi, rdx
    /* jmp fp_sub3 */

.global fp_sub3
fp_sub3:
    push r12
    push r13

    mov r8,  [rsi +  0]
    mov r9,  [rsi +  8]
    mov r10, [rsi + 16]
    mov r11, [rsi + 24]
    mov r12, [rsi + 32]
    mov r13, [rsi + 40]
    mov rax, [rsi + 48]
    mov rcx, [rsi + 56]

    sub r8,  [rdx +  0]
    sbb r9,  [rdx +  8]
    sbb r10, [rdx + 16]
    sbb r11, [rdx + 24]
    sbb r12, [rdx + 32]
    sbb r13, [rdx + 40]
    sbb rax, [rdx + 48]
    sbb rcx, [rdx + 56]

    test rcx, rcx
    jns 0f

1:  add r8,  [rip + p +  0]
    adc r9,  [rip + p +  8]
    adc r10, [rip + p + 16]
    adc r11, [rip + p + 24]
    adc r12, [rip + p + 32]
    adc r13, [rip + p + 40]
    adc rax, [rip + p + 48]
    adc rcx, [rip + p + 56]

0:  STOREREGS rdi, r8, r9, r10, r11, r12, r13, rax, rcx

    pop r13
    pop r12
    ret


/* Montgomery arithmetic */

.global fp_enc
fp_enc:
    lea rdx, [rip + r_squared_mod_p]
    jmp fp_mul3

.global fp_dec
fp_dec:
    lea rdx, [rip + uint_1]
    jmp fp_mul3

.global fp_mul2
fp_mul2:
    mov rdx, rdi
    /* jmp fp_mul3 */

.global fp_mul3
fp_mul3:
                                        mov rcx, [rip + fp_mul_counter]
                                        jrcxz 0f
                                        incq [rcx]
                                        0:
    push r12
    push r13
    push r14
    push r15
    push rbx
    push rbp

    push rdi

    mov rdi, rsi
    mov rsi, rdx

.macro MULSTEP, m, r0, r1, r2, r3, r4, r5, r6, r7, r8, want_carry

    xor eax, eax /* clear flags */

    mulx rbx, rax, [\m +  0]
    adcx \r0, rax
    adox \r1, rbx

    mulx rbp, rax, [\m +  8]
    adcx \r1, rax
    adox \r2, rbp

    mulx rbx, rax, [\m + 16]
    adcx \r2, rax
    adox \r3, rbx

    mulx rbp, rax, [\m + 24]
    adcx \r3, rax
    adox \r4, rbp

    mulx rbx, rax, [\m + 32]
    adcx \r4, rax
    adox \r5, rbx

    mulx rbp, rax, [\m + 40]
    adcx \r5, rax
    adox \r6, rbp

    mulx rbx, rax, [\m + 48]
    adcx \r6, rax
    adox \r7, rbx

    mulx rbp, rax, [\m + 56]
    adcx \r7, rax
    adox \r8, rbp

    .if \want_carry
        mov eax, 0
        adcx \r8, rax
    .else
        adc \r8, 0
    .endif

.endm

.macro REDSTEP, r0, r1, r2, r3, r4, r5, r6, r7, r8, want_carry
    mov rdx, \r0
    mulx rax, rdx, [rip + inv_min_p_mod_r]
    MULSTEP rip + p, \r0, \r1, \r2, \r3, \r4, \r5, \r6, \r7, \r8, \want_carry
.endm

.macro MULREDSTEP, k, r0, r1, r2, r3, r4, r5, r6, r7, r8
    mov rdx, [rdi + 8*\k]
    MULSTEP rsi, \r0, \r1, \r2, \r3, \r4, \r5, \r6, \r7, \r8, 0
    REDSTEP      \r0, \r1, \r2, \r3, \r4, \r5, \r6, \r7, \r8, 0
.endm

    xor r8,  r8
    xor r9,  r9
    xor r10, r10
    xor r11, r11
    xor r12, r12
    xor r13, r13
    xor r14, r14
    xor r15, r15
    xor ecx, ecx

    MULREDSTEP 0, r8,  r9,  r10, r11, r12, r13, r14, r15, rcx
    MULREDSTEP 1, r9,  r10, r11, r12, r13, r14, r15, rcx, r8
    MULREDSTEP 2, r10, r11, r12, r13, r14, r15, rcx, r8,  r9
    MULREDSTEP 3, r11, r12, r13, r14, r15, rcx, r8,  r9,  r10
    MULREDSTEP 4, r12, r13, r14, r15, rcx, r8,  r9,  r10, r11
    MULREDSTEP 5, r13, r14, r15, rcx, r8,  r9,  r10, r11, r12
    MULREDSTEP 6, r14, r15, rcx, r8,  r9,  r10, r11, r12, r13
    MULREDSTEP 7, r15, rcx, r8,  r9,  r10, r11, r12, r13, r14

    /* final reduction */

    pop       rdi
    REDONCE        rcx, r8,  r9,  r10, r11, r12, r13, r14
    STOREREGS rdi, rcx, r8,  r9,  r10, r11, r12, r13, r14

    pop rbp
    pop rbx
    pop r15
    pop r14
    pop r13
    pop r12
    ret


.global fp_sq1
fp_sq1:
    mov rsi, rdi
    /* jmp fp_sq2 */

.global fp_sq2
fp_sq2:
                                        mov rcx, [rip + fp_sq_counter]
                                        jrcxz 0f
                                        incq [rcx]
                                        0:
    push r12
    push r13
    push r14
    push r15
    push rbx
    push rbp

.macro SQSTEPSTEP r0, r1, u, i, j, iprev
    .if \i != \iprev
        mov rdx, [rsi + 8*\i]
    .endif
    mulx \u, rax, [rsi + 8*\j]
    adcx \r0, rax
    adox \r1, \u
.endm

.macro SQSTEP, i0,i1,i2,i3,i4,i5,i6, j0,j1,j2,j3,j4,j5,j6, r0,r1,r2,r3,r4,r5,r6,r7

    xor eax, eax /* clear flags */

    SQSTEPSTEP \r0, \r1, rbx, \i0, \j0, -1
    SQSTEPSTEP \r1, \r2, rbp, \i1, \j1, \i0
    SQSTEPSTEP \r2, \r3, rbx, \i2, \j2, \i1
    SQSTEPSTEP \r3, \r4, rbp, \i3, \j3, \i2
    SQSTEPSTEP \r4, \r5, rbx, \i4, \j4, \i3
    SQSTEPSTEP \r5, \r6, rbp, \i5, \j5, \i4
    SQSTEPSTEP \r6, \r7, rbx, \i6, \j6, \i5
    adc \r7, 0

.endm

    xor r8,  r8
    xor r9,  r9
    xor r10, r10
    xor r11, r11
    xor r12, r12
    xor r13, r13
    xor r14, r14
    xor r15, r15
    xor ecx, ecx

    /* put the sum of non-square parts on the stack */

    sub rsp, 14*8

    SQSTEP 0,0,0,0,0,0,0, 1,2,3,4,5,6,7, r10, r11, r12, r13, r14, r15, rcx, r8
    mov [rsp +   0], r10
    mov [rsp +   8], r11
    xor r10, r10
    xor r11, r11

    SQSTEP 1,1,1,1,1,1,2, 2,3,4,5,6,7,7, r12, r13, r14, r15, rcx, r8,  r9,  r10
    mov [rsp +  16], r12
    mov [rsp +  24], r13
    xor r12, r12
    xor r13, r13

    SQSTEP 2,2,2,2,6,6,6, 3,4,5,6,3,4,5, r14, r15, rcx, r8,  r9,  r10, r11, r12
    mov [rsp +  32], r14
    mov [rsp +  40], r15
    xor r14, r14

    SQSTEP 3,3,4,7,7,7,7, 4,5,5,3,4,5,6, rcx, r8,  r9,  r10, r11, r12, r13, r14
    STOREREGS rsp + 48, rcx, r8,  r9,  r10, r11, r12, r13, r14

.macro POPADD2, r, a0, a1
    pop rax
    adcx \r, \a0
    adox \r, \a1
.endm

    /* compute the lower half of the square part /*
    /* add the lower half of the non-square part twice */

    xor ecx, ecx /* clear flags */

    mov rdx, [rsi +  0]
    mulx r9,  r8,  rdx
    POPADD2 r9,  rax, rax

    mov rdx, [rsi +  8]
    mulx r11, r10, rdx
    POPADD2 r10, rax, rax
    POPADD2 r11, rax, rax

    mov rdx, [rsi + 16]
    mulx r13, r12, rdx
    POPADD2 r12, rax, rax
    POPADD2 r13, rax, rax

    mov rdx, [rsi + 24]
    mulx r15, r14, rdx
    POPADD2 r14, rax, rax
    POPADD2 r15, rax, rax

    mov eax, 0
    adcx rcx, rax
    adox rcx, rax

.macro SQPUSHADD2, m, r, a0, a1
    mov rdx, \m
    mulx rbx, rax, rdx
    push rbx
    adcx \r, \a0
    adox \r, \a1
.endm

    /* reduce everything up to the middle */
    /* add the upper half of the square part */

    mov rdx, [rsi + 32]
    mulx rbx, rax, rdx
    push rbx
    add rcx, rax    /* no carry or overflow */

    REDSTEP r8,  r9,  r10, r11, r12, r13, r14, r15, rcx, 1
    POPADD2 r8,  r8,  rax

    REDSTEP r9,  r10, r11, r12, r13, r14, r15, rcx, r8,  1
    SQPUSHADD2 [rsi + 40], r9,  r9,  rax

    REDSTEP r10, r11, r12, r13, r14, r15, rcx, r8,  r9,  1
    POPADD2 r10, r10, rax

    REDSTEP r11, r12, r13, r14, r15, rcx, r8,  r9,  r10, 1
    SQPUSHADD2 [rsi + 48], r11, r11, rax

    REDSTEP r12, r13, r14, r15, rcx, r8,  r9,  r10, r11, 1
    POPADD2 r12, r12, rax

    REDSTEP r13, r14, r15, rcx, r8,  r9,  r10, r11, r12, 1
    SQPUSHADD2 [rsi + 56], r13, r13, rax

    REDSTEP r14, r15, rcx, r8,  r9,  r10, r11, r12, r13, 1
    POPADD2 r14, r14, rax

    REDSTEP r15, rcx, r8,  r9,  r10, r11, r12, r13, r14, 0

    /* add the upper half of the non-square part twice */

    xor edx, edx /* clear flags */

    POPADD2 rcx, rax, rax
    POPADD2 r8,  rax, rax
    POPADD2 r9,  rax, rax
    POPADD2 r10, rax, rax
    POPADD2 r11, rax, rax
    POPADD2 r12, rax, rax
    POPADD2 r13, rax, rax

    adcx r14, rdx
    adox r14, rdx

    /* final reduction */

    REDONCE        rcx, r8,  r9,  r10, r11, r12, r13, r14
    STOREREGS rdi, rcx, r8,  r9,  r10, r11, r12, r13, r14

    pop rbp
    pop rbx
    pop r15
    pop r14
    pop r13
    pop r12
    ret


.global fp_inv
fp_inv:
                                        mov rcx, [rip + fp_inv_counter]
                                        jrcxz 0f
                                        incq [rcx]
                                        0:
    mov rsi, rdi
    jmp fpinv511


/* destroys input! */
.global fp_issquare
fp_issquare:
                                        mov rcx, [rip + fp_sqt_counter]
                                        jrcxz 0f
                                        incq [rcx]
                                        0:
.set k, 7
.rept 8
    pushq [rip + p + 8*k]
    .set k, k-1
.endr

    mov rsi, rsp
    mov cl, 1  /* result */

.l0p:

    .set k, 0
    .set v, 1
    .rept 8
        cmpq [rdi + 8*k], v
        jnz 1f
        .set k, k+1
        .set v, 0
    .endr
        jmp .l0pbrk
        1:

        testq [rdi], 1
        jz .shift

    .set k, 7
    .rept 8
        mov rax, [rdi + 8*k]
        cmp rax, [rsi + 8*k]
        ja .reduce
        .if k != 0
        jb .recip
        .endif
        .set k, k-1
    .endr

    .recip:
        mov al, [rdi]
        and al, [rsi]
        and al, 3
        cmp al, 3
        sete al
        xor cl, al
        xchg rdi, rsi

    .reduce:
        mov rax, [rsi +  0]
        sub [rdi +  0], rax
    .set k, 1
    .rept 7
        mov rax, [rsi + 8*k]
        sbb [rdi + 8*k], rax
        .set k, k+1
    .endr

    .shift:
        mov eax, [rsi]
        and eax, 7
        popcnt eax, eax
        test eax, 1
        setz al
        xor cl, al
        shrq [rdi + 56]
        rcrq [rdi + 48]
        rcrq [rdi + 40]
        rcrq [rdi + 32]
        rcrq [rdi + 24]
        rcrq [rdi + 16]
        rcrq [rdi +  8]
        rcrq [rdi +  0]
        jmp .l0p

.l0pbrk:
    movzx eax, cl
    add rsp, 64
    ret


.global fp_random
fp_random:
    lea rsi, [rip + p]
    jmp uint_random

