// SPDX-License-Identifier: MIT
/*
 * Copyright 2021 Google LLC.
 */

	.text
	.section	socket, "ax", @progbits
	.globl		prog
	.p2align	3
	.type		prog, @function
prog:
	// Your code here
	r0 = 0
	exit
.end:
	.size		prog, .end-prog

	.type		_license, @object
	.section	license, "aw", @progbits
	.globl		_license
_license:
	.asciz		"GPL"
	.size		_license, 4
