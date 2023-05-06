	.file	"main.c"
	.text
	.section	.rodata
.LC0:
	.string	"Enter your password:"
.LC1:
	.string	"\n Your password is:"
	.text
	.globl	main
	.type	main, @function
main:
.LFB0:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$96, %rsp
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	leaq	.LC0(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-64(%rbp), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	gets@PLT
	movl	$5, -84(%rbp)
	jmp	.L2
.L3:
	movl	-84(%rbp), %eax
	cltq
	movzbl	-64(%rbp,%rax), %eax
	xorl	$15, %eax
	movl	%eax, %edx
	movl	-84(%rbp), %eax
	cltq
	movb	%dl, -32(%rbp,%rax)
	addl	$1, -84(%rbp)
.L2:
	cmpl	$8, -84(%rbp)
	jle	.L3
	movl	$0, -80(%rbp)
	jmp	.L4
.L5:
	movl	-80(%rbp), %eax
	cltq
	movzbl	-64(%rbp,%rax), %eax
	xorl	$5, %eax
	movl	%eax, %edx
	movl	-80(%rbp), %eax
	cltq
	movb	%dl, -32(%rbp,%rax)
	addl	$1, -80(%rbp)
.L4:
	cmpl	$4, -80(%rbp)
	jle	.L5
	movl	$9, -76(%rbp)
	jmp	.L6
.L7:
	movl	-76(%rbp), %eax
	cltq
	movzbl	-64(%rbp,%rax), %eax
	xorl	$37, %eax
	movl	%eax, %edx
	movl	-76(%rbp), %eax
	cltq
	movb	%dl, -32(%rbp,%rax)
	addl	$1, -76(%rbp)
.L6:
	cmpl	$11, -76(%rbp)
	jle	.L7
	movl	$12, -72(%rbp)
	jmp	.L8
.L9:
	movl	-72(%rbp), %eax
	cltq
	movzbl	-64(%rbp,%rax), %eax
	movsbl	%al, %eax
	notl	%eax
	negl	%eax
	movl	%eax, %edx
	movl	-72(%rbp), %eax
	cltq
	movb	%dl, -32(%rbp,%rax)
	addl	$1, -72(%rbp)
.L8:
	cmpl	$16, -72(%rbp)
	jle	.L9
	movl	$17, -68(%rbp)
	jmp	.L10
.L11:
	movl	-68(%rbp), %eax
	cltq
	movzbl	-64(%rbp,%rax), %eax
	movsbl	%al, %eax
	notl	%eax
	movl	%eax, %edx
	movl	$0, %eax
	subl	%edx, %eax
	sall	$2, %eax
	movl	%eax, %edx
	movl	-68(%rbp), %eax
	cltq
	movb	%dl, -32(%rbp,%rax)
	addl	$1, -68(%rbp)
.L10:
	cmpl	$23, -68(%rbp)
	jle	.L11
	leaq	.LC1(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-32(%rbp), %rax
	movq	%rax, %rdi
	call	puts@PLT
	movl	$0, %eax
	movq	-8(%rbp), %rdx
	subq	%fs:40, %rdx
	je	.L13
	call	__stack_chk_fail@PLT
.L13:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	main, .-main
	.ident	"GCC: (GNU) 11.1.0"
	.section	.note.GNU-stack,"",@progbits
