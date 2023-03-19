%ifndef ASM_DEF_ASM
%define ASM_DEF_ASM


;extern c_asmprint


%define PICM_OFFSET 32
%define PICS_OFFSET 40

%define EXC_DIVIDE_BY_ZERO 0
%define EXC_DEBUG 1
%define EXC_NON_MASK_INTERRUPT 2
%define EXC_BREAKPOINT 3
%define EXC_OVERFLOW 4
%define EXC_BOUND_RANGE_EXCEED 5
%define EXC_INVALID_OPCODE 6
%define EXC_DEVICE_UNAVAILABLE 7
%define EXC_DOUBLE_FAULT 8
%define EXC_NONE_9 9
%define EXC_INVALID_TSS 10
%define EXC_SEGMENT_NOT_PRESENT 11
%define EXC_STACK_SEGMENT_FULL 12
%define EXC_GENERAL_PROTECTION_FAULT 13
%define EXC_PAGE_FAULT 14
%define EXC_NONE_15 15
%define EXC_X87_FLOATING_POINT 16
%define EXC_ALIGNMENT_CHECK 17
%define EXC_MACHINE_CHECK 18
%define EXC_SIMD_FLOATING_POINT 19
%define EXC_VIRTUALIZATION 20
%define EXC_NONE_21 21
%define EXC_NONE_22 22
%define EXC_NONE_23 23
%define EXC_NONE_24 24
%define EXC_NONE_25 25
%define EXC_NONE_26 26
%define EXC_NONE_27 27
%define EXC_NONE_28 28
%define EXC_NONE_29 29
%define EXC_SECURITY 30
%define EXC_NONE_31 31

%define IRQ_TIMER PICM_OFFSET
%define IRQ_KEYBOARD (PICM_OFFSET + 1)
%define IRQ_SERIAL_PORT_2 (PICM_OFFSET + 3)
%define IRQ_SERIAL_PORT_1 (PICM_OFFSET + 4)
%define IRQ_PARALLEL_PORT_2_3 (PICM_OFFSET + 5)
%define IRQ_FLOPPY_DISK (PICM_OFFSET + 6)
%define IRQ_PARALLEL_PORT_1 (PICM_OFFSET + 7)

%define IRQ_CLOCK (PICS_OFFSET)
%define IRQ_ACPI (PICS_OFFSET + 1)
%define IRQ_NONE_1 (PICS_OFFSET + 2)
%define IRQ_NONE_2 (PICS_OFFSET + 3)
%define IRQ_MOUSE (PICS_OFFSET + 4)
%define IRQ_CO_PROCESSOR (PICS_OFFSET + 5)
%define IRQ_PRIMARY_ATA (PICS_OFFSET + 6)
%define IRQ_SECONDARY_ATA (PICS_OFFSET + 7)

%define INT_SCHED 128
%define IPI_PROCESS_EXIT 129
%define IPI_PANIC 130

%define DEBUGCON_PORT 0xe9

%macro nsprintax 0
	mov al, 0x61
	out DEBUGCON_PORT, al
	mov al, 0x0a
	out DEBUGCON_PORT, al
%endmacro

%macro nsprint 0
	push rax
	mov al, 0x61
	out DEBUGCON_PORT, al
	mov al, 0x0a
	out DEBUGCON_PORT, al
	pop rax
%endmacro


struc registers
	.rax resq 1
	.rbx resq 1
	.rcx resq 1
	.rdx resq 1
	.rbp resq 1
	.rsp resq 1
	.rdi resq 1
	.rsi resq 1
	.r8 resq 1
	.r9 resq 1
	.r10 resq 1
	.r11 resq 1
	.r12 resq 1
	.r13 resq 1
	.r14 resq 1
	.r15 resq 1
	.rflags resq 1
	.rip resq 1
	.cs resw 1
	.ss resw 1
endstruc

struc int_data
	.rip resq 1
	.cs resq 1
	.rflags resq 1
	.rsp resq 1
	.ss resq 1
endstruc

; structure that a pointer is stored in the gs_base msr
struc gs_data
	.self_addr resq 1
	.call_rsp resq 1
	; nothing else matters for assembly
endstruc


section .text
bits 64
asmprint:
	push rax
	push rcx
	push rdx
	push rdi
	push rsi
	push r8
	push r9
	push r10
	push r11
	;call c_asmprint
	pop r11
	pop r10
	pop r9
	pop r8
	pop rsi
	pop rdi
	pop rdx
	pop rcx
	pop rax
	ret


%endif
