#pragma once

#include <asm-generic/int-ll64.h>

#define MODE_REAL 0
#define MODE_PROTECTED 1
#define MODE_PAGING 2


#define IOCTL_CREATE 0xdeadbeef
#define IOCTL_RUN    0xcafebabe
#define IOCTL_GET    0x13371337
#define IOCTL_PUT    0xbaadb10d

#define NR_INTERRUPTS 256

#define MAX_VCPUS 8
#define MAX_PCPUS 8

#define VCPUEVENT_VALID_NMI_PENDING	0x00000001
#define VCPUEVENT_VALID_SIPI_VECTOR	0x00000002
#define VCPUEVENT_VALID_SHADOW	        0x00000004
#define VCPUEVENT_VALID_SMM		0x00000008
#define VCPUEVENT_VALID_PAYLOAD	        0x00000010

#define X86_SHADOW_INT_MOV_SS	        0x01
#define X86_SHADOW_INT_STI		0x02

struct debug_exit_arch
{
	__u32 exception;
	__u32 pad;
	__u64 pc;
	__u64 dr6;
	__u64 dr7;
};


#pragma pack(push, 1)
struct regs
{
	__u64 rax;
	__u64 rcx;
	__u64 rdx;
	__u64 rbx;
	__u64 rsp;
	__u64 rbp;
	__u64 rsi;
	__u64 rdi;
	__u64 r8;
	__u64 r9;
	__u64 r10;
	__u64 r11;
	__u64 r12;
	__u64 r13;
	__u64 r14;        // 70h
	__u64 r15;
	__u64 rip, rflags;
};
#pragma pack(pop)


struct segment
{
	__u64 base;
	__u64 limit;
	__u64 selector;
	__u64 access;
};

struct dtable
{
	__u64 base;
	__u16 limit;
	__u16 padding[3];
};


typedef struct sregs
{
	struct segment cs, ds, es, fs, gs, ss;
	struct segment tr, ldt;
	struct segment gdt, idt;
	__u64 cr0, cr3, cr4, efer;
    __u64 sysenter_cs, sysenter_rip, sysenter_rsp;
    /* __u64 cr2, cr8; */ //fuck these regs no one cares anyway
} sregs_t;

#define EXIT_IO_IN  0
#define EXIT_IO_OUT 1
#define SYSTEM_EVENT_SHUTDOWN       1
#define SYSTEM_EVENT_RESET          2
#define SYSTEM_EVENT_CRASH          3

typedef struct state_t
{
	__u8 request_interrupt_window;
	__u8 immediate_exit;

	__u64 cr8;
	__u64 apic_base;

	__u8 mode;
	__u64 rip_gpa;
	__u64 apicbase;

	union
	{
		struct
		{
			__u64 hardware_exit_reason;
		} hw;
		struct
		{
			__u64 hardware_entry_failure_reason;
		} fail_entry;
		struct
		{
			__u32 exception;
			__u32 error_code;
		} ex;
		struct
		{
			__u8 direction;
			__u8 size; /* bytes */
			__u16 port;
			__u32 count;
			__u8 data[8]; 
		} io;
		struct
		{
			struct debug_exit_arch arch;
		} debug;
		struct
		{
			__u64 phys_addr;
			__u8  is_write;
		} mmio;
		struct
		{
			__u64 nr;
			__u64 args[6];
			__u64 ret;
			__u32 longmode;
			__u32 pad;
		} hypercall;
		struct
		{
			__u64 rip;
			__u32 is_write;
			__u32 pad;
		} tpr_access;
		struct
		{
			__u32 suberror;
			__u32 ndata;
			__u64 data[16];
		} internal;
		struct
		{
			__u64 gprs[32];
		} osi;
		struct
		{
			__u64 nr;
			__u64 ret;
			__u64 args[9];
		} papr_hcall;
		struct
		{
			__u32 epr;
		} epr;
		struct
		{
			__u32 type;
			__u64 flags;
		} system_event;
		struct
		{
			__u8 vector;
		} eoi;
		char padding[256];
	};

	__u64 fart;
	struct regs regs;
	struct sregs sregs;
	//struct vcpu_events events;
} state_t;

typedef struct userspace_regs_t
{
	struct regs regs;
	struct sregs sregs;
} userspace_regs_t;

/* VMX basic exit reasons. */
#define VMX_EXIT_REASONS_FAILED_VMENTRY         0x80000000
#define VMX_EXIT_REASONS_SGX_ENCLAVE_MODE	    0x08000000

#define EXIT_REASON_EXCEPTION_NMI       0
#define EXIT_REASON_EXTERNAL_INTERRUPT  1
#define EXIT_REASON_TRIPLE_FAULT        2
#define EXIT_REASON_INIT_SIGNAL			3
#define EXIT_REASON_SIPI_SIGNAL         4

#define EXIT_REASON_INTERRUPT_WINDOW    7
#define EXIT_REASON_NMI_WINDOW          8
#define EXIT_REASON_TASK_SWITCH         9
#define EXIT_REASON_CPUID               10
#define EXIT_REASON_HLT                 12
#define EXIT_REASON_INVD                13
#define EXIT_REASON_INVLPG              14
#define EXIT_REASON_RDPMC               15
#define EXIT_REASON_RDTSC               16
#define EXIT_REASON_VMCALL              18
#define EXIT_REASON_VMCLEAR             19
#define EXIT_REASON_VMLAUNCH            20
#define EXIT_REASON_VMPTRLD             21
#define EXIT_REASON_VMPTRST             22
#define EXIT_REASON_VMREAD              23
#define EXIT_REASON_VMRESUME            24
#define EXIT_REASON_VMWRITE             25
#define EXIT_REASON_VMOFF               26
#define EXIT_REASON_VMON                27
#define EXIT_REASON_CR_ACCESS           28
#define EXIT_REASON_DR_ACCESS           29
#define EXIT_REASON_IO_INSTRUCTION      30
#define EXIT_REASON_MSR_READ            31
#define EXIT_REASON_MSR_WRITE           32
#define EXIT_REASON_INVALID_STATE       33
#define EXIT_REASON_MSR_LOAD_FAIL       34
#define EXIT_REASON_MWAIT_INSTRUCTION   36
#define EXIT_REASON_MONITOR_TRAP_FLAG   37
#define EXIT_REASON_MONITOR_INSTRUCTION 39
#define EXIT_REASON_PAUSE_INSTRUCTION   40
#define EXIT_REASON_MCE_DURING_VMENTRY  41
#define EXIT_REASON_TPR_BELOW_THRESHOLD 43
#define EXIT_REASON_APIC_ACCESS         44
#define EXIT_REASON_EOI_INDUCED         45
#define EXIT_REASON_GDTR_IDTR           46
#define EXIT_REASON_LDTR_TR             47
#define EXIT_REASON_EPT_VIOLATION       48
#define EXIT_REASON_EPT_MISCONFIG       49
#define EXIT_REASON_INVEPT              50
#define EXIT_REASON_RDTSCP              51
#define EXIT_REASON_PREEMPTION_TIMER    52
#define EXIT_REASON_INVVPID             53
#define EXIT_REASON_WBINVD              54
#define EXIT_REASON_XSETBV              55
#define EXIT_REASON_APIC_WRITE          56
#define EXIT_REASON_RDRAND              57
#define EXIT_REASON_INVPCID             58
#define EXIT_REASON_VMFUNC              59
#define EXIT_REASON_ENCLS               60
#define EXIT_REASON_RDSEED              61
#define EXIT_REASON_PML_FULL            62
#define EXIT_REASON_XSAVES              63
#define EXIT_REASON_XRSTORS             64
#define EXIT_REASON_UMWAIT              67
#define EXIT_REASON_TPAUSE              68
#define EXIT_REASON_BUS_LOCK            74
