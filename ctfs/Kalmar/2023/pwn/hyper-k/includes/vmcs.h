#pragma once
#include <asm-generic/int-ll64.h>
#include "main.h"

#define LAUNCH_STATE_CLEAR 0
#define LAUNCH_STATE_ACTIVE 1



/*
 * CR0
 */
#define CR0_PE	0x00000001	/* Protected mode Enable */
#define CR0_MP	0x00000002	/* "Math" Present (NPX or NPX emulator) */
#define CR0_EM	0x00000004	/* EMulate non-NPX coproc. (trap ESC only) */
#define CR0_TS	0x00000008	/* Task Switched (if MP, trap ESC and WAIT) */
#define CR0_ET	0x00000010	/* Extension Type (387 (if set) vs 287) */
#define CR0_NE	0x00000020	/* Numeric Error enable (EX16 vs IRQ13) */
#define CR0_WP	0x00010000	/* Write Protect (honor PTE_W in all modes) */
#define CR0_AM	0x00040000	/* Alignment Mask (set to enable AC flag) */
#define CR0_NW	0x20000000	/* Not Write-through */
#define CR0_CD	0x40000000	/* Cache Disable */
#define CR0_PG	0x80000000	/* PaGing enable */

/*
 * Cyrix 486 DLC special registers, accessible as IO ports
 */
#define CCR0		0xc0	/* configuration control register 0 */
#define CCR0_NC0	0x01	/* first 64K of each 1M memory region is non-cacheable */
#define CCR0_NC1	0x02	/* 640K-1M region is non-cacheable */
#define CCR0_A20M	0x04	/* enables A20M# input pin */
#define CCR0_KEN	0x08	/* enables KEN# input pin */
#define CCR0_FLUSH	0x10	/* enables FLUSH# input pin */
#define CCR0_BARB	0x20	/* flushes internal cache when entering hold state */
#define CCR0_CO		0x40	/* cache org: 1=direct mapped, 0=2x set assoc */
#define CCR0_SUSPEND	0x80	/* enables SUSP# and SUSPA# pins */
#define CCR1		0xc1	/* configuration control register 1 */
#define CCR1_RPL	0x01	/* enables RPLSET and RPLVAL# pins */

/*
 * CR3
 */
#define CR3_PCID		__BITS(11,0)
#define CR3_PA			__BITS(62,12)
#define CR3_NO_TLB_FLUSH	__BIT(63)

/*
 * CR4
 */
#define CR4_VME		0x00000001 /* virtual 8086 mode extension enable */
#define CR4_PVI		0x00000002 /* protected mode virtual interrupt enable */
#define CR4_TSD		0x00000004 /* restrict RDTSC instruction to cpl 0 */
#define CR4_DE		0x00000008 /* debugging extension */
#define CR4_PSE		0x00000010 /* large (4MB) page size enable */
#define CR4_PAE		0x00000020 /* physical address extension enable */
#define CR4_MCE		0x00000040 /* machine check enable */
#define CR4_PGE		0x00000080 /* page global enable */
#define CR4_PCE		0x00000100 /* enable RDPMC instruction for all cpls */
#define CR4_OSFXSR	0x00000200 /* enable fxsave/fxrestor and SSE */
#define CR4_OSXMMEXCPT	0x00000400 /* enable unmasked SSE exceptions */
#define CR4_UMIP	0x00000800 /* user-mode instruction prevention */
#define CR4_LA57	0x00001000 /* 57-bit linear addresses */
#define CR4_VMXE	0x00002000 /* enable VMX operations */
#define CR4_SMXE	0x00004000 /* enable SMX operations */
#define CR4_FSGSBASE	0x00010000 /* enable *FSBASE and *GSBASE instructions */
#define CR4_PCIDE	0x00020000 /* enable Process Context IDentifiers */
#define CR4_OSXSAVE	0x00040000 /* enable xsave and xrestore */
#define CR4_SMEP	0x00100000 /* enable SMEP support */
#define CR4_SMAP	0x00200000 /* enable SMAP support */
#define CR4_PKE		0x00400000 /* enable Protection Keys for user pages */
#define CR4_CET		0x00800000 /* enable CET */
#define CR4_PKS		0x01000000 /* enable Protection Keys for kern pages */


#define CR0_STATIC_MASK \
	(CR0_ET | CR0_NW | CR0_CD)

#define CR4_VALID \
	(CR4_VME |			\
	 CR4_PVI |			\
	 CR4_TSD |			\
	 CR4_DE |			\
	 CR4_PSE |			\
	 CR4_PAE |			\
	 CR4_MCE |			\
	 CR4_PGE |			\
	 CR4_PCE |			\
	 CR4_OSFXSR |			\
	 CR4_OSXMMEXCPT |		\
	 CR4_UMIP |			\
	 /* CR4_LA57 excluded */	\
	 /* CR4_VMXE excluded */	\
	 /* CR4_SMXE excluded */	\
	 CR4_FSGSBASE |			\
	 CR4_PCIDE |			\
	 CR4_OSXSAVE |			\
	 CR4_SMEP |			\
	 CR4_SMAP			\
	 /* CR4_PKE excluded */		\
	 /* CR4_CET excluded */		\
	 /* CR4_PKS excluded */)
#define CR4_INVALID \
	(0xFFFFFFFFFFFFFFFFULL & ~CR4_VALID)


struct __vmcs_t
{
	union
	{
		unsigned int all;
		struct
		{
			unsigned int revision_identifier : 31;
			unsigned int shadow_vmcs_indicator : 1;
		} bits;
	} header;

	unsigned int abort_indicator;
	char data[ 0x1000 - 2 * sizeof( unsigned ) ];
};

union __vmx_entry_control_t
{
	__u64 control;
	struct
	{
		__u64 reserved_0 : 2;
		__u64 load_dbg_controls : 1;
		__u64 reserved_1 : 6;
		__u64 ia32e_mode_guest : 1;
		__u64 entry_to_smm : 1;
		__u64 deactivate_dual_monitor_treament : 1;
		__u64 reserved_3 : 1;
		__u64 load_ia32_perf_global_control : 1;
		__u64 load_ia32_pat : 1;
		__u64 load_ia32_efer : 1;
		__u64 load_ia32_bndcfgs : 1;
		__u64 conceal_vmx_from_pt : 1;
	} bits;
};

union __vmx_exit_control_t
{
	__u64 control;
	struct
	{
		__u64 reserved_0 : 2;
		__u64 save_dbg_controls : 1;
		__u64 reserved_1 : 6;
		__u64 host_address_space_size : 1;
		__u64 reserved_2 : 2;
		__u64 load_ia32_perf_global_control : 1;
		__u64 reserved_3 : 2;
		__u64 ack_interrupt_on_exit : 1;
		__u64 reserved_4 : 2;
		__u64 save_ia32_pat : 1;
		__u64 load_ia32_pat : 1;
		__u64 save_ia32_efer : 1;
		__u64 load_ia32_efer : 1;
		__u64 save_vmx_preemption_timer_value : 1;
		__u64 clear_ia32_bndcfgs : 1;
		__u64 conceal_vmx_from_pt : 1;
	} bits;
};

union __vmx_pinbased_control_msr_t
{
	__u64 control;
	struct
	{
		__u64 external_interrupt_exiting : 1;
		__u64 reserved_0 : 2;
		__u64 nmi_exiting : 1;
		__u64 reserved_1 : 1;
		__u64 virtual_nmis : 1;
		__u64 vmx_preemption_timer : 1;
		__u64 process_posted_interrupts : 1;
	} bits;
};

union __vmx_primary_processor_based_control_t
{
	__u64 control;
	struct
	{
		__u64 reserved_0 : 2;
		__u64 interrupt_window_exiting : 1;
		__u64 use_tsc_offsetting : 1;
		__u64 reserved_1 : 3;
		__u64 hlt_exiting : 1;
		__u64 reserved_2 : 1;
		__u64 invldpg_exiting : 1;
		__u64 mwait_exiting : 1;
		__u64 rdpmc_exiting : 1;
		__u64 rdtsc_exiting : 1;
		__u64 reserved_3 : 2;
		__u64 cr3_load_exiting : 1;
		__u64 cr3_store_exiting : 1;
		__u64 reserved_4 : 2;
		__u64 cr8_load_exiting : 1;
		__u64 cr8_store_exiting : 1;
		__u64 use_tpr_shadow : 1;
		__u64 nmi_window_exiting : 1;
		__u64 mov_dr_exiting : 1;
		__u64 unconditional_io_exiting : 1;
		__u64 use_io_bitmaps : 1;
		__u64 reserved_5 : 1;
		__u64 monitor_trap_flag : 1;
		__u64 use_msr_bitmaps : 1;
		__u64 monitor_exiting : 1;
		__u64 pause_exiting : 1;
		__u64 active_secondary_controls : 1;
	} bits;
};

union __vmx_secondary_processor_based_control_t
{
	__u64 control;
	struct
	{
		__u64 virtualize_apic_accesses : 1;
		__u64 enable_ept : 1;
		__u64 descriptor_table_exiting : 1;
		__u64 enable_rdtscp : 1;
		__u64 virtualize_x2apic : 1;
		__u64 enable_vpid : 1;
		__u64 wbinvd_exiting : 1;
		__u64 unrestricted_guest : 1;
		__u64 apic_register_virtualization : 1;
		__u64 virtual_interrupt_delivery : 1;
		__u64 pause_loop_exiting : 1;
		__u64 rdrand_exiting : 1;
		__u64 enable_invpcid : 1;
		__u64 enable_vmfunc : 1;
		__u64 vmcs_shadowing : 1;
		__u64 enable_encls_exiting : 1;
		__u64 rdseed_exiting : 1;
		__u64 enable_pml : 1;
		__u64 use_virtualization_exception : 1;
		__u64 conceal_vmx_from_pt : 1;
		__u64 enable_xsave_xrstor : 1;
		__u64 reserved_0 : 1;
		__u64 mode_based_execute_control_ept : 1;
		__u64 reserved_1 : 2;
		__u64 use_tsc_scaling : 1;
	} bits;
};
