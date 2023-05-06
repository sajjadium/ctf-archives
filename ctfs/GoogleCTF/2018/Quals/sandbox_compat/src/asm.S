BITS 32

	;; small gadget to restore esp and return to caller
	jmp	trampoline
	mov	esp, ebx
	ret	

	;; trampoline to 64-bit code
	;; there is a NOP at 0xffffffff, followed by kernel entry
trampoline:
	jmp	dword 0x33:0xffffffff
