.intel_syntax noprefix
#define HOST_RSP 0x00006c14

.globl vmexit_handle
.type vmexit_handle @function

.section .text

.globl vm_entrypoint
.type vm_entrypoint @function

.globl _vmxon
.type _vmxon @function

.globl _vmxoff
.type _vmxoff @function

.globl _vmclear
.type _vmclear @function

.globl _vmptrld
.type _vmptrld @function

.globl _vmptrst
.type _vmptrst @function

.globl _vmlaunch
.type _vmlaunch @function

.globl _vmresume
.type _vmresume @function

.globl _vmwrite
.type _vmwrite @function

.globl check_vmx_error
.type  check_vmx_error @function

.globl fc_status
.type fc_status @function

.globl cr0_fixed0
.type cr0_fixed0 @function

.globl cr0_fixed1
.type cr0_fixed1 @function

.globl cr4_fixed0
.type cr4_fixed0 @function

.globl cr4_fixed1
.type cr4_fixed1 @function

.globl vmcs_revision_id
.type vmcs_revision_id @function

.globl get_vmx_support
.type get_vmx_support @function

.globl _segmentlimit
.type _segmentlimit @function

.global _load_ar
.type _load_ar @function


.globl __readmsr
.type __readmsr @function

.globl _read_cr0
.type _read_cr0 @function

.globl _read_cr3
.type _read_cr4 @function

.globl _read_cr4
.type _read_cr4 @function

.globl _read_dr7
.type _read_dr7 @function

.globl _read_rflags
.type _read_rflags @function

.globl _read_cs
.type _read_cs @function

.globl _read_ss
.type _read_ss @function

.globl _read_ds
.type _read_ds @function

.globl _read_es
.type _read_es @function

.globl _read_fs
.type _read_fs @function

.globl _read_gs
.type _read_gs @function

.globl _read_tr
.type _read_tr @function

.globl _read_ldtr
.type _read_ldtr @function

.globl _sgdt
.type _sgdt @function

.globl _sidt
.type _sidt @function

.macro SAVE_GP
        #push    rax
        push    rcx
        push    rdx
        push    rbx
        push    rbp
        push    rsi
        push    rdi
        push    r8
        push    r9
        push    r10
        push    r11
        push    r12
        push    r13
        push    r14
        push    r15
.endm

.macro RESTORE_GP
        pop     r15
        pop     r14
        pop     r13
        pop     r12
        pop     r11
        pop     r10
        pop     r9
        pop     r8
        pop     rdi
        pop     rsi
        pop     rbp
        pop     rbx
        pop     rdx
        pop     rcx
        #pop     rax
.endm

#define X64_GPR_RAX		    0
#define X64_GPR_RCX		    1
#define X64_GPR_RDX		    2
#define X64_GPR_RBX		    3
#define X64_GPR_RSP		    4
#define X64_GPR_RBP		    5
#define X64_GPR_RSI		    6
#define X64_GPR_RDI		    7
#define X64_GPR_R8			8
#define X64_GPR_R9			9
#define X64_GPR_R10		    10
#define X64_GPR_R11		    11
#define X64_GPR_R12		    12
#define X64_GPR_R13		    13
#define X64_GPR_R14		    14
#define X64_GPR_R15		    15
#define X64_GPR_RIP		    16
#define X64_GPR_RFLAGS		17
#define X64_NGPR			18

.macro SAVE_GUEST_GPRS state
    mov [rax + X64_GPR_RCX*8], rcx
    mov [rax + X64_GPR_RDX*8], rdx
    mov [rax + X64_GPR_RBX*8], rbx
    mov [rax + X64_GPR_RBP*8], rbp
    mov [rax + X64_GPR_RSI*8], rsi
    mov [rax + X64_GPR_RDI*8], rdi
    mov [rax + X64_GPR_R8*8], r8
    mov [rax + X64_GPR_R9*8], r9
    mov [rax + X64_GPR_R10*8], r10
    mov [rax + X64_GPR_R11*8], r11
    mov [rax + X64_GPR_R12*8], r12
    mov [rax + X64_GPR_R13*8], r13
    mov [rax + X64_GPR_R14*8], r14
    mov [rax + X64_GPR_R15*8], r15
    mov [rax + X64_GPR_R15*8], r15
.endm

.macro RESTORE_GUEST_GPRS state
    mov rcx, [rax + X64_GPR_RCX*8]
    mov rdx, [rax + X64_GPR_RDX*8]
    mov rbx, [rax + X64_GPR_RBX*8]
    mov rbp, [rax + X64_GPR_RBP*8]
    mov rsi, [rax + X64_GPR_RSI*8]
    mov rdi, [rax + X64_GPR_RDI*8]
    mov r8,  [rax + X64_GPR_R8*8]
    mov r9,  [rax + X64_GPR_R9*8]
    mov r10, [rax + X64_GPR_R10*8]
    mov r11, [rax + X64_GPR_R11*8]
    mov r12, [rax + X64_GPR_R12*8]
    mov r13, [rax + X64_GPR_R13*8]
    mov r14, [rax + X64_GPR_R14*8]
    mov r15, [rax + X64_GPR_R15*8]
    mov rax, [rax + X64_GPR_RAX*8]
.endm

get_vmx_support:
    push rbx
    mov rax, 1
    cpuid
    shr ecx, 5
    and ecx, 1
    mov eax, ecx
    pop rbx
    ret
.size get_vmx_support, .-get_vmx_support;

_segmentlimit:
    lsl rax, rdi
    ret
.size _segmentlimit, .-_segmentlimit

_load_ar:
    lar eax, edi
    jz load_ar_success
    xor rax, rax
load_ar_success:
    ret

.size _load_ar, .-_load_ar

.set MSR_IA32_VMX_BASIC, 0x480
vmcs_revision_id:
    mov rcx, MSR_IA32_VMX_BASIC
    rdmsr
    ret
.size vmcs_revision_id, .-vmcs_revision_id;

check_vmx_error:
    jc fail_cf
    jz fail_zf
    mov rax, 0
    ret
fail_cf:
    mov rax, -1
    ret
fail_zf:
    mov rax, -2
    ret
.size check_vmx_error, .-check_vmx_error

.set IA32_FEATURE_CONTROL, 0x3a
.set IA32_VMX_CR0_FIXED0, 0x486
.set IA32_VMX_CR0_FIXED1, 0x487
.set IA32_VMX_CR4_FIXED0, 0x488
.set IA32_VMX_CR4_FIXED1, 0x489

_vmxon:
    mov rcx, cr4
    bts rcx, 13
    mov cr4, rcx
    mov rcx, IA32_FEATURE_CONTROL
    rdmsr
    and eax, 0x5
    xor eax, 0x5
    jz good
    mov rax, -2
    ret
good:
    mov r10, cr0
    mov rcx, IA32_VMX_CR0_FIXED1
    rdmsr
    and r10d, eax
    mov rcx, IA32_VMX_CR0_FIXED0
    rdmsr
    or r10d, eax
    mov cr0, r10
    mov r10, cr4
    mov rcx, IA32_VMX_CR4_FIXED1
    rdmsr
    and r10d, eax
    mov rcx, IA32_VMX_CR4_FIXED0
    rdmsr
    or r10d, eax
    mov cr4, r10
    vmxon [rdi]
    jmp check_vmx_error
.size _vmxon, .-_vmxon;

_vmxoff:
    vmxoff
    jmp check_vmx_error
.size _vmxoff, .-_vmxoff;

_vmclear:
    vmclear [rdi]
    jmp check_vmx_error
.size _vmclear, .-_vmclear;

_vmptrld:
    vmptrld [rdi]
    jmp check_vmx_error
.size _vmptrld, .-_vmptrld

_vmptrst:
    vmptrst [rdi]
    jmp check_vmx_error
.size _vmptrst, .-_vmptrst

vm_entrypoint:
    push rax
    mov rax, [rsp+8]
    SAVE_GUEST_GPRS(rax)
    pop rdi
    mov [rax + X64_GPR_RAX*8], rdi
    pop rax
    RESTORE_GP
    xor rax, rax
    ret
.size vm_entrypoint, .-vm_entrypoint

_vmlaunch:
    SAVE_GP
    mov rax, rdi
    push rax
    mov rbx, HOST_RSP
    mov rsi, rsp
    vmwrite rbx, rsi
    mov rax, rdi
    RESTORE_GUEST_GPRS(rax)
    vmlaunch
    pop rax
    RESTORE_GP
    xor rax, rax
    jmp check_vmx_error
.size _vmlaunch, .-_vmlaunch

_vmresume:
  # save host GPRs
  SAVE_GP
  # save host rax (guest state ptr)
  mov rax, rdi
  push rax
  # save RSP
  mov rbx, HOST_RSP
  mov rsi, rsp
  vmwrite rbx, rsi
  mov rax, rdi
  RESTORE_GUEST_GPRS(rax)
  vmresume
  # failure case. probably don't care about saving guest regs if we failed to launch
  pop rax
  RESTORE_GP
  jmp check_vmx_error
.size _vmresume, .-_vmresume


_vmwrite:
	vmwrite rdi, [rsi]
	jmp check_vmx_error
.size _vmwrite, .-_vmwrite

_vmread:
	vmread [rdi], rsi
	jmp check_vmx_error
.size _vmread, .-_vmread

cr0_fixed0:
	mov rcx, IA32_VMX_CR0_FIXED0
	rdmsr
	ret
.size cr0_fixed0, .-cr0_fixed0

cr0_fixed1:
	mov rcx, IA32_VMX_CR0_FIXED1
	rdmsr
	ret
.size cr0_fixed1, .-cr0_fixed1

__readmsr:
	mov rcx, rdi
	rdmsr
	shl rax, 32
	shrd rax, rdx, 32
	ret
.size __readmsr, .-__readmsr;

cr4_fixed0:
	mov rcx, IA32_VMX_CR4_FIXED0
	rdmsr
	ret
.size cr4_fixed0, .-cr4_fixed0

cr4_fixed1:
	mov rcx, IA32_VMX_CR4_FIXED1
	rdmsr
	ret
.size cr4_fixed1, .-cr4_fixed1

fc_status:
	mov rcx, 0x3a
	rdmsr
	ret
.size fc_status, .-fc_status;

_read_cr0:
	mov rax, cr0
	ret
.size _read_cr0, .-_read_cr0

_read_cr3:
	mov rax, cr3
	ret
.size _read_cr4, .-_read_cr4

_read_cr4:
	mov rax, cr4
	ret
.size _read_cr4, .-_read_cr4

_read_dr7:
	mov rax, dr7
	ret
.size _read_dr7, .-_read_dr7

_read_es:
	mov ax, es
	ret
.size _read_es, .-_read_es

_read_rflags:
	pushfq
	pop rax
	ret
.size _read_rflags, .-_read_rflags

_read_cs:
	mov ax, cs
	ret
.size _read_cs, .-_read_cs

_read_ss:
	mov ax, ss
	ret
.size _read_ss, .-_read_ss

_read_ds:
	mov ax, ds
	ret
.size _read_ds, .-_read_ds

_read_fs:
	mov ax, fs
	ret
.size _read_fs, .-_read_fs

_read_gs:
	mov ax, gs
	ret
.size _read_gs, .-_read_gs

_read_tr:
	str ax
	ret
.size _read_tr, .-_read_tr

_read_ldtr:
	sldt ax
	ret
.size _read_ldtr, .-_read_ldtr

_sgdt:
	sgdt [rdi]
	ret
.size _sgdt, .-_sgdt

_sidt:
	sidt [rdi]
	ret
.size _sidt, .-_sidt

