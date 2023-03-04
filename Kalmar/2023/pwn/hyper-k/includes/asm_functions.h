#pragma once
#include <asm-generic/int-ll64.h>
#include "segment.h"
#include "vmexit.h"

#define X86_CR4_VMXE_BIT	13
#define X86_CR4_VMXE		_BITUL(X86_CR4_VMXE_BIT)

__u8 asm_foo(int blah);
__u32 get_vmx_support(void);

int _vmxon(__u64 mem_region);
int _vmxoff(void);
int _vmclear(__u64 vmcs_ptr);
int _vmptrld(__u64 vmcs_ptr);
int _vmptrst(__u64 vmcs_ptr);
int _vmwrite(__u64 field, __u64 val);
int _vmwread(__u64 dest, __u64 field);
int _vmlaunch(struct regs *guest_gprs);
int _vmresume(struct regs *guest_gprs);
unsigned long _segmentlimit(unsigned long segment);

void vm_entrypoint(void);

__u32 fc_status(void);
__u32 vmcs_revision_id(void);

__u32 cr0_fixed0(void);
__u32 cr0_fixed1(void);

__u32 cr4_fixed0(void);
__u32 cr4_fixed1(void);

__u64 __readmsr(unsigned int);
__u64 _read_cr0(void);
__u64 _read_cr3(void);
__u64 _read_cr4(void);
__u64 _read_dr7(void);
__u64 _read_rflags(void);

__u16 _read_cs(void);
__u16 _read_ss(void);
__u16 _read_ds(void);
__u16 _read_es(void);
__u16 _read_fs(void);
__u16 _read_gs(void);
__u16 _read_tr(void);
__u16 _read_ldtr(void);

void _sgdt(struct __pseudo_descriptor_64_t *desc);
void _sidt(struct __pseudo_descriptor_64_t *desc);

__u32 _load_ar(__u16 segment);

static inline int vmread(__u64 encoding, __u64 *value)
{
	__u64 tmp;
	__u8 ret;
	asm volatile("vmread %[encoding], %[tmp]; setna %[ret];"
	             : [tmp]"=rm"(tmp), [ret]"=rm"(ret)
	             : [encoding]"r"(encoding)
	             : "cc", "memory");

	*value = tmp;
	return ret;
}

static inline __u64 vmreadz(__u64 encoding)
{
	__u64 value = 0;
	vmread(encoding, &value);
	return value;
}

static inline int vmwrite(__u64 encoding, __u64 value)
{
	__u8 ret;
	__asm__ __volatile__ ("vmwrite %[value], %[encoding]; setna %[ret]"
	                      : [ret]"=rm"(ret)
	                      : [value]"rm"(value), [encoding]"r"(encoding)
	                      : "cc", "memory");

	return ret;
}
