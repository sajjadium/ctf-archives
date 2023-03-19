global long_mode_start
extern _start

extern PML4_table

extern __KERNEL_VMA

section .boot_text
bits 64
long_mode_start:
; zero all segment registers
	mov ax, 0
	mov ss, ax
	mov ds, ax
	mov es, ax
	mov fs, ax
	mov gs, ax

; jmp to higher half
	mov rax, higher_half_start
	jmp rax

section .text
higher_half_start:

; adjust stack pointer to higher half address space
	mov rax, __KERNEL_VMA
	add rsp, rax

; adjust mb2 information pointer to be in higher half address space, and move to first argument
	mov edi, dword [rsp]
	add rsp, 4
	add rdi, rax

; unmap lower half
	mov qword [PML4_table], 0

; force tlb flush
	mov rax, cr3
	mov cr3, rax

; call rust entry point
	call _start

; print okay
.okay:
	mov rax, 0x2f592f412f4b2f4f
    	mov qword [0xb8000], rax
	hlt
