;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Sample 32-bit user code that writes "hello\n" to stdout.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

	BITS 32

	mov	esp, 0xbef00000
	sub	esp, 4

	push	0x00000a6f
	push	0x6c6c6568

	;; kernel arguments
	mov	edi, 1		; __NR_write
	mov	esi, 1		; fd
	mov	edx, esp	; buf
	mov	ecx, 6		; size

	;; jmp to trampoline 64-bit kernel
	;; not straightforward because of restricted characters
	mov	eax, 0xdead0000 + done
	push	eax

	xor	eax, eax	;; mov  eax, 0xfffff000
	dec	eax
	shl	eax, 12

	push	eax
	ret

done:
	int	3
