%include "asm_def.asm"

extern eoi
extern rust_int_handler

%macro save_regs 0
	; rsp, rflags, and rip are set on interrupt stack frame
	sub rsp, registers_size
	mov [rsp + registers.rax], rax
	mov [rsp + registers.rbx], rbx
	mov [rsp + registers.rcx], rcx
	mov [rsp + registers.rdx], rdx
	mov [rsp + registers.rbp], rbp
	mov [rsp + registers.rdi], rdi
	mov [rsp + registers.rsi], rsi
	mov [rsp + registers.r8], r8
	mov [rsp + registers.r9], r9
	mov [rsp + registers.r10], r10
	mov [rsp + registers.r11], r11
	mov [rsp + registers.r12], r12
	mov [rsp + registers.r13], r13
	mov [rsp + registers.r14], r14
	mov [rsp + registers.r15], r15
%endmacro

; first arg is pointer to int_data structure
%macro save_int_data_regs 1
	; move data from stack frame into registers
	mov rax, [%1 + int_data.rip]
	mov [rsp + registers.rip], rax
	mov rax, [%1 + int_data.cs]
	mov [rsp + registers.cs], ax
	mov rax, [%1 + int_data.rflags]
	mov [rsp + registers.rflags], rax
	mov rax, [%1 + int_data.rsp]
	mov [rsp + registers.rsp], rax
	mov rax, [%1 + int_data.ss]
	mov [rsp + registers.ss], ax
%endmacro

; registers data structure should be on stack
%macro load_old_regs 0
	mov rax, [rsp + registers.rax]
	mov rbx, [rsp + registers.rbx]
	mov rcx, [rsp + registers.rcx]
	mov rdx, [rsp + registers.rdx]
	mov rbp, [rsp + registers.rbp]
	mov rdi, [rsp + registers.rdi]
	mov rsi, [rsp + registers.rsi]
	mov r8, [rsp + registers.r8]
	mov r9, [rsp + registers.r9]
	mov r10, [rsp + registers.r10]
	mov r11, [rsp + registers.r11]
	mov r14, [rsp + registers.r14]
	mov r15, [rsp + registers.r15]
%endmacro

%macro make_asm_int_handler 1
global int_handler_ %+ %1
int_handler_ %+ %1 %+ :
	save_regs

	; get location of interrupt stack frame data structure
	mov r15, rsp
	add r15, registers_size

	save_int_data_regs r15

	; call rust function
	mov rdi, %1
	mov rsi, rsp
	mov rdx, 0
	mov rax, rust_int_handler
	; FIXME: stack might not be aligned
	call rax
	
	load_old_regs

	add rsp, registers_size
	iretq
%endmacro

%macro make_asm_int_handler_e 1
global int_handler_ %+ %1
int_handler_ %+ %1 %+ :
	save_regs

	; get location of interrupt stack frame data structure
	mov r15, rsp
	add r15, registers_size

	; get error code
	mov rdx, [r15]
	add r15, 8

	save_int_data_regs r15

	; call rust function
	mov rdi, %1
	mov rsi, rsp
	mov rax, rust_int_handler
	; FIXME: stack might not be aligned
	call rax
	
	load_old_regs

	add rsp, registers_size
	add rsp, 8

	mov qword [rsp + int_data.cs], 0x23
	mov qword [rsp + int_data.ss], 0x1b

	iretq
%endmacro

%macro make_asm_irq_handler 1
global int_handler_ %+ %1
int_handler_ %+ %1 %+ :
	save_regs

	; get location of interrupt stack frame data structure
	mov r15, rsp
	add r15, registers_size

	save_int_data_regs r15

	; call rust function
	mov rdi, %1
	mov rsi, rsp
	mov rdx, 0
	mov rax, rust_int_handler
	; FIXME: stack might not be aligned
	call rax

	; send eoi
	mov rdi, %1
	mov rcx, eoi
	call rcx

	load_old_regs

	add rsp, registers_size
	iretq
%endmacro

section .text
bits 64
make_asm_int_handler 0
make_asm_int_handler 1
make_asm_int_handler 2
make_asm_int_handler 3
make_asm_int_handler 4
make_asm_int_handler 5
make_asm_int_handler 6
make_asm_int_handler 7
make_asm_int_handler_e 8
make_asm_int_handler 9
make_asm_int_handler_e 10
make_asm_int_handler_e 11
make_asm_int_handler_e 12
make_asm_int_handler_e 13
make_asm_int_handler_e 14
make_asm_int_handler 15
make_asm_int_handler 16
make_asm_int_handler_e 17
make_asm_int_handler 18
make_asm_int_handler 19
make_asm_int_handler 20
make_asm_int_handler 21
make_asm_int_handler 22
make_asm_int_handler 23
make_asm_int_handler 24
make_asm_int_handler 25
make_asm_int_handler 26
make_asm_int_handler 27
make_asm_int_handler 28
make_asm_int_handler 29
make_asm_int_handler_e 30
make_asm_int_handler 31
make_asm_irq_handler 32
make_asm_irq_handler 33
make_asm_irq_handler 34
make_asm_irq_handler 35
make_asm_irq_handler 36
make_asm_irq_handler 37
make_asm_irq_handler 38
make_asm_irq_handler 39
make_asm_irq_handler 40
make_asm_irq_handler 41
make_asm_irq_handler 42
make_asm_irq_handler 43
make_asm_irq_handler 44
make_asm_irq_handler 45
make_asm_irq_handler 46
make_asm_irq_handler 47
