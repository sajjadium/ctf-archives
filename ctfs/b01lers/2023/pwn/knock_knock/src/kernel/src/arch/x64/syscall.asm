%include "asm_def.asm"

global syscall_entry

extern rust_syscall_entry

section .text
bits 64
syscall_entry:
	; kernel stack pointer should be 16 byte aligned
	; iretq clears gs_base msr, so we have to keep it in gs_base_k, and use swapgs to access it

	mov r10, rsp							; save caller rsp in register

	swapgs
	mov rsp, [gs:gs_data.call_rsp]			; load kernel rsp
	swapgs
	sti

	; all values on stack will be part of the rust SyscallVals struct

	push rcx		; save return rip
	push r11		; save old flags
	push r10		; save caller rsp
	push rbp		; save rbp


	push r15		; push args on stack
	push r14
	push r13
	push r12
	push r9
	push r8
	push rdi
	push rsi
	push rdx
	push rbx

	mov rcx, rax	; push options
	shr rcx, 32
	push rcx

	shl rax, 32		; cant use and because it messes things up
	shr rax, 32

	mov rdi, rax	; arg1: sycall number

	mov rsi, rsp	; arg2: reference to syscall vals on stack
	sub rsp, 8		; align stack

	mov rax, rust_syscall_entry
	call rax

	add rsp, 16		; put stack pointer to right place from earlier alignmant, and ignore options on stack

	mov rax, 0
	pop rbx
	pop rdx
	pop rsi
	pop rdi
	pop r8
	pop r9
	pop r12
	pop r13
	pop r14
	pop r15

	pop rbp			; retrieve old rbp
	pop r10			; retrieve old rsp
	pop r11			; retrieve old flags
	pop rcx			; retrieve old rcx

	mov rsp, r10	; restore old rsp

	o64 sysret
