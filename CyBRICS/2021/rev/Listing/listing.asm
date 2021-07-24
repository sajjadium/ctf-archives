BITS 64
global check
section .text
check:
    mov rbp, rsp
    sub rsp, 0x100
    VMOVDQA ymm0, [rdi]
    and rsp, 0xffffffffffffff00
    mov rax, 0xfeca50051345b0b0
    push rax
    push rax
    push rax
    push rax
    VMOVDQA ymm1, [rsp]
    VPXOR ymm2, ymm1, ymm0
    mov rax, 0x0100030205040706
    push rax
    mov rax, 0x09080b0a0c0d0f0e
    push rax
    mov rax, 0x1110131215141716
    push rax
    mov rax, 0x19181b1a1c1d1f1e
    push rax
    VMOVDQA ymm3, [rsp]
    VPSHUFB ymm4, ymm2, ymm3
    mov rax, 0xd1d3762335619aab
    push rax
    mov rax, 0xd5d52327356583f8
    push rax
    mov rax, 0xc9d36127336c85b9
    push rax
    mov rax,0xd5d622713161cbf8 
    push rax
    VMOVDQA ymm0, [rsp]
    VPCMPEQQ  ymm1, ymm4, ymm0
    VMOVDQA [rsp], ymm1
    pop rax
    cmp rax, 0xffffffffffffffff
    jnz fail
    pop rax
    cmp rax, 0xffffffffffffffff
    jnz fail
    pop rax
    cmp rax, 0xffffffffffffffff
    jnz fail
    pop rax
    cmp rax, 0xffffffffffffffff
    jnz fail
    mov rax, 1
    jmp fin
fail:
    xor rax, rax
fin:
    mov rsp, rbp
    ret

    
