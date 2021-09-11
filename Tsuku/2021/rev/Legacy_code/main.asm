	.arch i286,jumps
	.code16
	.att_syntax prefix
	.section	.rodata

.LC0:
	.string	"PC%d%.0f\n"
	.text
	.global	main
	.type	main, @function

main:
	enterw	$24-2,	$0
	movw	$9,	-2(%bp)
	movw	$0,	-6(%bp)
	movw	$0,	-4(%bp)
	movw	$0x28A4, -10(%bp)
	movw	$0x4448, -8(%bp)
	movw	$0xE148, -14(%bp)
	movw	$0x3EBA, -12(%bp)

	.arch pentium
	finit
	fld	-10(%bp)
	fld	-14(%bp)
	faddp	%st(0), %st(1)
	fstp	-6(%bp)
	fwait
	.arch i286

	movw	-6(%bp),	%ax
	movw	-4(%bp),	%dx
	leaw	-22(%bp),	%cx
	pushw	%dx
	pushw	%ax
	pushw	%cx
	pushw	%ss
	popw	%ds
	call	__extendsfdf2
	addw	$6,	%sp
	movw	-22(%bp),	%cx
	movw	-20(%bp),	%ax
	movw	-18(%bp),	%dx
	movw	-16(%bp),	%bx
	pushw	%bx
	pushw	%dx
	pushw	%ax
	pushw	%cx
	pushw	-2(%bp)
	pushw	$.LC0
	pushw	%ss
	popw	%ds
	call	printf
	addw	$12,	%sp
	movw	$0,	%ax
	movw	%ax,	%ax
	movw	%ax,	%ax
	leavew
	pushw	%ss
	popw	%ds
	ret
	.size	main, .-main
	.ident	"GCC: (GNU) 6.3.0"
