.section .rodata
chirp:
    .string "HEY!!!!!! NO STACK SMASHING!!!!!!"
prompt:
    .string "Enter name: "
greeting:
    .string "Hello, "
canary_fname:
    .string "canary.bin"
read_permission:
    .string "rb"
bin_sh:
    .string "/bin/sh"

.data
canary:
    .space 4

.text
    .type shell, @function
shell:
    # here's a free shell function!
    # too bad you can't use it!
    leaq   bin_sh(%rip), %rdi
    call   system
    ret

    .type set_canary, @function
set_canary:
    pushq   %rbp
    movq    %rsp, %rbp
    subq    $16, %rsp

    leaq    canary_fname(%rip), %rdi
    leaq    read_permission(%rip), %rsi
    call    fopen

    movq    %rax, %rcx
    movq    %rcx, (%rsp)    

    leaq    canary(%rip), %rdi
    movq    $8, %rsi
    movq    $1, %rdx

    call    fread

    movq    (%rsp), %rdi
    call    fclose

    leave
    ret

    .globl main
    .type main, @function
main:
    pushq   %rbp
    movq    %rsp, %rbp
    subq    $32, %rsp

    call    set_canary

    movq    canary(%rip), %rax
    movq    %rax, -8(%rbp)

    movq    stdin(%rip), %rdi
    xorq    %rsi, %rsi
    movq    $2, %rdx
    xorq    %rcx, %rcx
    call    setvbuf

    movq    stdout(%rip), %rdi
    xorq    %rsi, %rsi
    movq    $2, %rdx
    xorq    %rcx, %rcx
    call    setvbuf

    leaq    prompt(%rip), %rdi
    xorl    %eax, %eax
    call    printf

    leaq    -32(%rbp), %rdi
    call    gets

    leaq    greeting(%rip), %rdi
    xorl    %eax, %eax
    call    printf

    leaq   -32(%rbp), %rdi
    xorl    %eax, %eax
    call    printf

    movb    $0, (%rsp)
    movq    %rsp, %rdi
    call    puts

    leaq    -8(%rbp), %rdi
    leaq    canary(%rip), %rsi
    movq    $8, %rdx
    call    strncmp
    je      canary_passed

    leaq    chirp(%rip), %rdi
    call    puts

    movl    $134, %edi
    call    exit
    
canary_passed:
    movl    $0, %eax

    leave
    ret

    .size main, .-main
