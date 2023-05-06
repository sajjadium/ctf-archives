global start
extern long_mode_start
extern KERNEL_LMA

global PML4_table
global PDP_table

global stack_bottom
global stack_top

section .boot_text
bits 32

; TODO: use mb2.asm file instead of putting in here
; I did this because the linker refused to link with multiboot_header section and I don't know why

hstart:
	dd 0xe85250d6
	dd 0			; Arhitecture
	dd hend - hstart	; Header Length
	dd 0x100000000 - (0xe85250d6 + 0 + (hend - hstart))

	dw 0
	dw 0
	dd 8			; End Tag
hend:

start:
	mov esp, stack_top	; initalize stack

	cmp eax, 0x36d76289	; check for multiboot
	jne .no_multiboot

	push ebx		; push mb2 table

; check for CPUID
	pushfd			; put flags in eax
	pop eax

	mov ecx, eax		; copy flags to ecx for comparison

	xor eax, 1 << 21	; flip 21st flag bit

	push eax		; put modified value back to flags
	popfd

	pushfd			; pull modified value back out
	pop eax

	push ecx		; restore old flags
	popfd

	cmp eax, ecx		; compare modified and original to determine if supported, jump if failed
	je .no_CPUID

; check if long mode supported
	mov eax, 0x80000000	; get highest function calling parameter for cpuid
	cpuid

	cmp eax, 0x80000001	; if less, extended long mode info is not supported, jump to error
	jb .no_long_mode

	mov eax, 0x80000001	; get extended info
	cpuid

	test edx, 1 << 29	; 29th bit says if long mode is supported, error if failed
	jz .no_long_mode

; map kernel pages, kernel is at 0xffffff8000000000
	mov eax, PDP_table	; set up first entry of PML4 table
	or eax, 0b11		; set exists and writable bits
	mov [PML4_table], eax
	mov [PML4_table + 511 * 8], eax

	;mov eax, PD_table	; do same with pdp table
	;or eax, 0b11
	;mov [PDP_table], eax
	;mov [PDP_table_2 + 511 * 8], eax

	mov ecx, 0		; zero counter
	mov eax, 0b10000011	; huge, writable, and present bits for each entry
	mov edx, 0
.map_PD_table:
	mov [PDP_table + ecx * 8], eax
	mov [PDP_table + 2 + ecx * 8], edx
	add edx, 0x00004000		; 1gib offset between page mappings

	inc ecx
	cmp ecx, 512
	jl .map_PD_table	; map all 512 pages

; enable paging
	mov eax, PML4_table	; move PML4 address to proper register
	mov cr3, eax

	mov eax, cr4		; enable PAE bit
	or eax, 1 << 5
	mov cr4, eax

	mov ecx, 0xc0000080	; set long mode bit in EFER model specific register
	rdmsr
	or eax, 1 << 8
	wrmsr

	mov eax, cr0		; set paging bit in cr0
	or eax, 1 << 31
	mov cr0, eax

; load 64 bit gdt and start long mode code
	lgdt [gdt64.pointer]
	jmp gdt64.code:long_mode_start

; Not loaded with multiboot
.no_multiboot:
	mov eax, 0x4f424f4d	; NM for no multiboot
	jmp .error

; CPUID not supported
.no_CPUID:
	mov eax, 0x4f504f43	; CP for no CPUID
	jmp .error

; Processor does not support long mode
.no_long_mode:
	mov eax, 0x4f4d4f4c	; LM for long mode
	jmp .error

; Print for debug and cuase slight pause
.debug:
	push ecx
	mov dword [0xb8000], 0x1f421f44	; DB for debug
	mov ecx, 0
.debug_loop:
	inc ecx
	cmp ecx, 0x0fffffff
	jl .debug_loop
	pop ecx
	ret

; Error Occured, error code and color in EAX
.error:
	mov dword [0xb8000], 0x0f520f45		; ER
	mov dword [0xb8004], 0x0f4f0f52		; OR
	mov dword [0xb8008], 0x0f3a0f52		; R:
	mov dword [0xb800c], 0x0f20		; space
	mov dword [0xb800e], eax
	hlt

section .boot_bss
align 4096
PML4_table:
	resb 4096
stack_bottom:
	resb 65536
stack_top:
PDP_table:
	resb 4096

section .boot_rodata
gdt64:		; 64 bit global descriptor table
	dq 0
.code equ $ - gdt64
	dq (1 << 43) | (1 << 44) | (1 << 47) | (1 << 53)
.pointer:	; data structure to pass to lgdt
	dw .pointer - gdt64 - 1
	dq gdt64
