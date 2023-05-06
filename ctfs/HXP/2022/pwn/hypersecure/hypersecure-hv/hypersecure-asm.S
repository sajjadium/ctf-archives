#include <linux/linkage.h>
#include <asm/asm.h>

/*
	RDI contains the VMCB
	RSI contains the hypersecure_VM_REGS
*/
SYM_FUNC_START(__hypersecure_run)

// save host registers on the stack
push %rbx
push %rcx
push %rdx
push %rdi
push %rsi
push %rbp
push %r8
push %r9
push %r10
push %r11
push %r12
push %r13
push %r14
push %r15

// Save vm regs base
push %rsi

// Save vmcb
push %rdi

// use rax as base for vm context
mov %rsi, %rax

// load other registers
mov 0x0(%rax), %rbx
mov 0x8(%rax), %rcx
mov 0x10(%rax), %rdx
mov 0x18(%rax), %rdi
mov 0x20(%rax), %rsi
mov 0x28(%rax), %rbp
mov 0x30(%rax), %r8
mov 0x38(%rax), %r9
mov 0x40(%rax), %r10
mov 0x48(%rax), %r11
mov 0x50(%rax), %r12
mov 0x58(%rax), %r13
mov 0x60(%rax), %r14
mov 0x68(%rax), %r15

// pop vmcb into rax
pop %rax

// run vm
clgi
vmrun
stgi

pop %rax

mov %rbx, 0x0(%rax)
mov %rcx, 0x8(%rax)
mov %rdx, 0x10(%rax)
mov %rdi, 0x18(%rax)
mov %rsi, 0x20(%rax)
mov %rbp, 0x28(%rax)
mov %r8,  0x30(%rax)
mov %r9,  0x38(%rax)
mov %r10, 0x40(%rax)
mov %r11, 0x48(%rax)
mov %r12, 0x50(%rax)
mov %r13, 0x58(%rax)
mov %r14, 0x60(%rax)
mov %r15, 0x68(%rax)

// restore host registers
pop %r15
pop %r14
pop %r13
pop %r12
pop %r11
pop %r10
pop %r9
pop %r8
pop %rbp
pop %rsi
pop %rdi
pop %rdx
pop %rcx
pop %rbx

ret 
SYM_FUNC_END(__hypersecure_run)
