// Copyright (C) 2022? 2023? hxp. License expires after HXP CTF 2022
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

#ifndef hypersecure_H
#define hypersecure_H

#include "hypersecure-mm.h"

#include <linux/build_bug.h>
#include "hypersecure-vmcb.h"

#include <asm/string.h>

extern struct hypersecure_context *global_ctx;
extern bool hypersecure_debug_enable_logging;

static const __u64 hypersecure_PRESENT_MASK = 0x1UL;
static const __u64 hypersecure_WRITEABLE_MASK = 0x2UL;
static const __u64 hypersecure_USER_MASK = 0x4UL;
static const __u64 hypersecure_LEAF_MASK = (1UL << 7U);

#define hypersecure_4KB (4096UL)
#define hypersecure_2MB (512UL * hypersecure_4KB)
#define hypersecure_1GB (512UL * hypersecure_2MB)
#define hypersecure_512GB (512UL * hypersecure_1GB)

static inline __u64 hypersecure_create_entry(__u64 pa, __u64 mask) {
	return pa | mask;
}

struct hypersecure_vm_regs {
	__u64 rbx;
	__u64 rcx;
	__u64 rdx;
	__u64 rdi;
	__u64 rsi;
	__u64 rbp;
	__u64 r8;
	__u64 r9;
	__u64 r10;
	__u64 r11;
	__u64 r12;
	__u64 r13;
	__u64 r14;
	__u64 r15;
	__u64 rip;
	__u64 rax;
	__u64 rsp;
};

struct hypersecure_vm_state {
	struct hypersecure_vm_regs regs;
	__u64 clock;
};

struct hypersecure_vcpu {
	struct hypersecure_vmcb *vmcb;
	struct hypersecure_vm_state *state;
	unsigned long host_save_va;
	unsigned long host_save_pa;
	unsigned vcpu_id;
};

struct hypersecure_context {
	struct hypersecure_mm *mm;
	struct hypersecure_vcpu *vcpus;
	unsigned num_vcpus;
	unsigned long ioio_prot;
};

int hypersecure_write_memory(const void *memory, size_t sz);
int hypersecure_init_and_run(void);

#endif // hypersecure_H
