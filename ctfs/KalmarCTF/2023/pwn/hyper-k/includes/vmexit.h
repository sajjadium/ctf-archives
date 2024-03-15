#pragma once
#include <asm-generic/int-ll64.h>
#include "main.h"


#define MODE_REAL 0
#define MODE_PROTECTED 1
#define MODE_PAGING 2

#define SEGMENT_CS 0x2e
#define SEGMENT_SS 0x36
#define SEGMENT_DS 0x3e
#define SEGMENT_ES 0x26
#define SEGMENT_FS 0x64
#define SEGMENT_GS 0x65


#define REALMODE_REG_AL	0x1
#define REALMODE_REG_CL	0x2
#define REALMODE_REG_DL	0x3
#define REALMODE_REG_BL	0x4

#define REALMODE_REG_AX	0x5
#define REALMODE_REG_CX	0x6
#define REALMODE_REG_DX	0x7
#define REALMODE_REG_BX	0x8

#define SRC_TYPE_REG 0
#define SRC_TYPE_ADDR 1

#define DEST_TYPE_REG 0
#define DEST_TYPE_ADDR 1


#define MOV_RM8_TO_R8 	0x8a
#define MOV_RM16_TO_R16	0x8b

// from nvmm
/* General Purpose Registers. */
#define X64_GPR_RAX		0
#define X64_GPR_RCX		1
#define X64_GPR_RDX		2
#define X64_GPR_RBX		3
#define X64_GPR_RSP		4
#define X64_GPR_RBP		5
#define X64_GPR_RSI		6
#define X64_GPR_RDI		7
#define X64_GPR_R8		8
#define X64_GPR_R9		9
#define X64_GPR_R10		10
#define X64_GPR_R11		11
#define X64_GPR_R12		12
#define X64_GPR_R13		13
#define X64_GPR_R14		14
#define X64_GPR_R15		15
#define X64_GPR_RIP		16
#define X64_GPR_RFLAGS		17
#define X64_NGPR		18

union __vmx_exit_info_t
{
	__u64 flags;
	struct
	{
		__u64 exit_reason : 16;
		__u64 reserved_0 : 11;
		__u64 was_enclave : 1;
		__u64 pending_mtf_exit : 1;
		__u64 exit_from_vmx_root : 1;
		__u64 reserved_1 : 1;
		__u64 vm_entry_failure : 1;
	} bits;
};

union __vmx_exit_qual_t
{
	__u64 flags;
	struct
	{
		__u64 data_read : 1;
		__u64 data_write : 1;
		__u64 fetch : 1;
		__u64 bits_and_ept : 4;
		__u64 linear_addr_valid : 1;
		__u64 page_walk : 1;
		__u64 fuck0 : 1;
		__u64 fuck1 : 1;
		__u64 fuck2 : 1;
		__u64 iret : 1;
		__u64 reserved : 52;
	} bits;
};
