#ifndef __HYPERVISOR_HEADER__
#define __HYPERVISOR_HEADER__

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <linux/kvm.h>
#include <sys/mman.h>
#include <sys/ioctl.h>
#include "util.h"
#include "elf.h"
#include "vm.h"
#include "hypercall.h"
#include "device.h"
#include "interrupt.h"

#define HUGE_PAGE_ALIGNMENT 0x40000000
#define HUGE_PAGE_SIZE 0x200000
#define NORMAL_PAGE_ALIGNMENT 0x200000
#define PAGE_SIZE 0x1000

#define PAGE_MASK 0xfff
#define PAGE_UPALIGN(addr) (((addr) + PAGE_MASK) & (~PAGE_MASK))
#define PAGE_OFFSET(addr) ((addr) & PAGE_MASK)
#define PAGE_ADDR(addr) ((addr) & (~PAGE_MASK))

/* CR0 bits */
#define CR0_PE 1u
#define CR0_MP (1u << 1)
#define CR0_EM (1u << 2)
#define CR0_TS (1u << 3)
#define CR0_ET (1u << 4)
#define CR0_NE (1u << 5)
#define CR0_WP (1u << 16)
#define CR0_AM (1u << 18)
#define CR0_NW (1u << 29)
#define CR0_CD (1u << 30)
#define CR0_PG (1u << 31)

/* CR4 bits */
#define CR4_VME 1u
#define CR4_PVI (1u << 1)
#define CR4_TSD (1u << 2)
#define CR4_DE (1u << 3)
#define CR4_PSE (1u << 4)
#define CR4_PAE (1u << 5)
#define CR4_MCE (1u << 6)
#define CR4_PGE (1u << 7)
#define CR4_PCE (1u << 8)
#define CR4_OSFXSR (1u << 9)
#define CR4_OSXMMEXCPT (1u << 10)
#define CR4_UMIP (1u << 11)
#define CR4_VMXE (1u << 13)
#define CR4_SMXE (1u << 14)
#define CR4_FSGSBASE (1u << 16)
#define CR4_PCIDE (1u << 17)
#define CR4_OSXSAVE (1u << 18)
#define CR4_SMEP (1u << 20)
#define CR4_SMAP (1u << 21)
#define CR4_PKE (1u << 22)

#define EFER_SCE 1
#define EFER_LME (1 << 8)
#define EFER_LMA (1 << 10)
#define EFER_NXE (1 << 11)
#define EFER_SVME (1 << 12)
#define EFER_LMSLE (1 << 13)
#define EFER_FFXSR (1 << 14)
#define EFER_TCE (1 << 15)

/* 64-bit page * entry bits */
#define PDE64_PRESENT 0x01
#define PDE64_RW      0x02
#define PDE64_USER    0x04
#define PDE64_PS      0x80

#define PML4_SHIFT 39
#define PDP_SHIFT 30
#define PD_SHIFT 21
#define PT_SHIFT 12

#define PML4_SIZE (1 << PML4_SHIFT)
#define PDP_SIZE (1 << PDP_SHIFT)
#define PD_SIZE (1 << PD_SHIFT)
#define PT_SIZE (1 << PT_SHIFT)

#define PML4_OFFSET_MASK (PML4_SIZE - 1)
#define PDP_OFFSET_MASK (PDP_SIZE - 1)
#define PD_OFFSET_MASK (PD_SIZE - 1)
#define PT_OFFSET_MASK (PT_SIZE - 1)

#define PML4_MASK (~PML4_OFFSET_MASK)
#define PDP_MASK (~PDP_OFFSET_MASK)
#define PD_MASK (~PD_OFFSET_MASK)
#define PT_MASK (~PT_OFFSET_MASK)

#define PTIDX_MASK 0x1ff
#define NIL_PTIDX 0x200

#define PML4_IDX(vaddr) (((vaddr) >> PML4_SHIFT) & PTIDX_MASK)
#define PDP_IDX(vaddr) (((vaddr) >> PDP_SHIFT) & PTIDX_MASK)
#define PD_IDX(vaddr) (((vaddr) >> PD_SHIFT) & PTIDX_MASK)
#define PT_IDX(vaddr) (((vaddr) >> PT_SHIFT) & PTIDX_MASK)

#define PML4_UPALIGN(vaddr) (((vaddr) + PML4_OFFSET_MASK) & PML4_MASK)
#define PDP_UPALIGN(vaddr) (((vaddr) + PDP_OFFSET_MASK) & PDP_MASK)
#define PD_UPALIGN(vaddr) (((vaddr) + PD_OFFSET_MASK) & PD_MASK)
#define PT_UPALIGN(vaddr) (((vaddr) + PT_OFFSET_MASK) & PT_MASK)

#define PML4_ADDR(vaddr) ((vaddr) & PML4_MASK)
#define PDP_ADDR(vaddr) ((vaddr) & PDP_MASK)
#define PD_ADDR(vaddr) ((vaddr) & PD_MASK)
#define PT_ADDR(vaddr) ((vaddr) & PT_MASK)

void execute(VM* vm, uint64_t interruptEntry, uint64_t kernelInterruptStackAddr);

#endif
