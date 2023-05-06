        .text
        .globl  value
        .data
        .align 4
        .type   value, @object
        .size   value, 4
value:
        .long   24564753
        .globl  isGood
        .align 4
        .type   isGood, @object
        .size   isGood, 4
isGood:
        .long   12345
        .section        .rodata
        .align 8
.LC0:
        .string "Hey ! Have you got a password for me ? "
        .text
        .globl  getInput
        .type   getInput, @function
getInput:
.LFB6:
        .cfi_startproc
        endbr64
        pushq   %rbp    #
        .cfi_def_cfa_offset 16
        .cfi_offset 6, -16
        movq    %rsp, %rbp      #,
        .cfi_def_cfa_register 6
        subq    $32, %rsp       #,
# EasyAssembly.c:7: int getInput(void){
        movq    %fs:40, %rax    # MEM[(<address-space-1> long unsigned int *)40B], tmp88
        movq    %rax, -8(%rbp)  # tmp88, D.2854
        xorl    %eax, %eax      # tmp88
# EasyAssembly.c:10:    printf("Hey ! Have you got a password for me ? ");
        leaq    .LC0(%rip), %rdi        #,
        movl    $0, %eax        #,
        call    printf@PLT      #
# EasyAssembly.c:11:    fgets(input, 12, stdin);
        movq    stdin(%rip), %rdx       # stdin, stdin.0_1
        leaq    -20(%rbp), %rax #, tmp85
        movl    $12, %esi       #,
        movq    %rax, %rdi      # tmp85,
        call    fgets@PLT       #
# EasyAssembly.c:12:    return atoi(input);
        leaq    -20(%rbp), %rax #, tmp86
        movq    %rax, %rdi      # tmp86,
        call    atoi@PLT        #
# EasyAssembly.c:13: }
        movq    -8(%rbp), %rcx  # D.2854, tmp89
        xorq    %fs:40, %rcx    # MEM[(<address-space-1> long unsigned int *)40B], tmp89
        je      .L3     #,
        call    __stack_chk_fail@PLT    #
.L3:
        leave
        .cfi_def_cfa 7, 8
        ret
        .cfi_endproc
.LFE6:
        .size   getInput, .-getInput
        .section        .rodata
        .align 8
.LC1:
        .string "Well done ! You can validate with the flag Hero{%d:%d}\n"
        .align 8
.LC2:
        .string "Argh... Try harder buddy you can do it !"
        .text
        .globl  main
        .type   main, @function
main:
.LFB7:
        .cfi_startproc
        endbr64
        pushq   %rbp    #
        .cfi_def_cfa_offset 16
        .cfi_offset 6, -16
        movq    %rsp, %rbp      #,
        .cfi_def_cfa_register 6
        subq    $16, %rsp       #,
# EasyAssembly.c:17:    int input = getInput();
        call    getInput        #
        movl    %eax, -8(%rbp)  # tmp85, input
# EasyAssembly.c:19:    modified = input >> 2;
        movl    -8(%rbp), %eax  # input, tmp89
        sarl    $2, %eax        #, tmp88
        movl    %eax, -4(%rbp)  # tmp88, modified
# EasyAssembly.c:21:    if(modified == 1337404)
        cmpl    $1337404, -4(%rbp)      #, modified
        jne     .L5     #,
# EasyAssembly.c:22:            isGood = 0;
        movl    $0, isGood(%rip)        #, isGood
.L5:
# EasyAssembly.c:24:    if(!isGood)
        movl    isGood(%rip), %eax      # isGood, isGood.1_1
# EasyAssembly.c:24:    if(!isGood)
        testl   %eax, %eax      # isGood.1_1
        jne     .L6     #,
# EasyAssembly.c:25:            printf("Well done ! You can validate with the flag Hero{%d:%d}\n", input, modified);
        movl    -4(%rbp), %edx  # modified, tmp90
        movl    -8(%rbp), %eax  # input, tmp91
        movl    %eax, %esi      # tmp91,
        leaq    .LC1(%rip), %rdi        #,
        movl    $0, %eax        #,
        call    printf@PLT      #
        jmp     .L7     #
.L6:
# EasyAssembly.c:28:            puts("Argh... Try harder buddy you can do it !");
        leaq    .LC2(%rip), %rdi        #,
        call    puts@PLT        #
.L7:
# EasyAssembly.c:30:    return EXIT_SUCCESS;
        movl    $0, %eax        #, _11
# EasyAssembly.c:31: }
        leave
        .cfi_def_cfa 7, 8
        ret
        .cfi_endproc
.LFE7:
        .size   main, .-main
        .ident  "GCC: (Ubuntu 9.3.0-17ubuntu1~20.04) 9.3.0"
        .section        .note.GNU-stack,"",@progbits
        .section        .note.gnu.property,"a"
        .align 8
        .long    1f - 0f
        .long    4f - 1f
        .long    5
0:
        .string  "GNU"
1:
        .align 8
        .long    0xc0000002
        .long    3f - 2f
2:
        .long    0x3
3:
        .align 8
4:
