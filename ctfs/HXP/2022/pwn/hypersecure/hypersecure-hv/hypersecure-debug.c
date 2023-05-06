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

#ifndef hypersecure_DEBUG_H
#define hypersecure_DEBUG_H

#include "hypersecure-debug.h"
#include "hypersecure.h"

#include <linux/build_bug.h>
#include <linux/slab.h>
#include <linux/kernel.h>
#include "hypersecure-vmcb.h"

#define gva_to_gpa(X) ((u64)slow_virt_to_phys(X))

void hypersecure_log_msg(const char *format, ...) {
	if (hypersecure_debug_enable_logging) {
		va_list args;
		va_start(args, format);
		vprintk(format, args);
		va_end(args);
	}
}

void hypersecure_dump_regs(const struct hypersecure_vm_state *state) {
	hypersecure_log_msg("rax = %llx\n", state->regs.rax);
	hypersecure_log_msg("rbx = %llx\n", state->regs.rbx);
	hypersecure_log_msg("rcx = %llx\n", state->regs.rcx);
	hypersecure_log_msg("rdx = %llx\n", state->regs.rdx);
	hypersecure_log_msg("rsi = %llx\n", state->regs.rsi);
	hypersecure_log_msg("rdi = %llx\n", state->regs.rdi);
	hypersecure_log_msg("rip = %llx\n", state->regs.rip);
	hypersecure_log_msg("rsp = %llx\n", state->regs.rsp);
	hypersecure_log_msg("rbp = %llx\n", state->regs.rbp);
	hypersecure_log_msg("r8 = %llx\n", state->regs.r8);
	hypersecure_log_msg("r9 = %llx\n", state->regs.r9);
	hypersecure_log_msg("r10 = %llx\n", state->regs.r10);
	hypersecure_log_msg("r11 = %llx\n", state->regs.r11);
	hypersecure_log_msg("r12 = %llx\n", state->regs.r12);
	hypersecure_log_msg("r13 = %llx\n", state->regs.r13);
	hypersecure_log_msg("r14 = %llx\n", state->regs.r14);
	hypersecure_log_msg("r15 = %llx\n", state->regs.r15);
}

void hypersecure_dump_vmcb(struct hypersecure_vmcb *vmcb) {
	hypersecure_log_msg("=============\n");
	hypersecure_log_msg("Control:\n");
	hypersecure_log_msg("CR read: %.16llx\n", *(__u64 *)&vmcb->control.cr_rd_intercepts);
	hypersecure_log_msg("CR write: %.16llx\n", *(__u64 *)&vmcb->control.cr_wr_intercepts);
	hypersecure_log_msg("exitcode: %.16llx\n", *(__u64 *)&vmcb->control.exitcode);
	hypersecure_log_msg("exitinfo_v1: %.16llx\n", *(__u64 *)&vmcb->control.exitinfo_v1);
	hypersecure_log_msg("exitinfo_v2: %.16llx\n", *(__u64 *)&vmcb->control.exitinfo_v2);
	hypersecure_log_msg("exitintinfo: %.16llx\n", *(__u64 *)&vmcb->control.exitintinfo);
	hypersecure_log_msg("nRIP: %.16llx\n", *(__u64 *)&vmcb->control.nRIP);
	hypersecure_log_msg("ncr3: %.16llx\n", *(__u64 *)&vmcb->control.ncr3);
	hypersecure_log_msg("num bytes fetched: %.16llx\n", *(__u64 *)&vmcb->control.num_bytes_fetched);
	hypersecure_log_msg("\nSave:\n");
	hypersecure_log_msg("cr0: %.16llx\n", *(__u64 *)&vmcb->save.cr0);
	hypersecure_log_msg("cr2: %.16llx\n", *(__u64 *)&vmcb->save.cr2);
	hypersecure_log_msg("cr3: %.16llx\n", *(__u64 *)&vmcb->save.cr3);
	hypersecure_log_msg("cr4: %.16llx\n", *(__u64 *)&vmcb->save.cr4);
	hypersecure_log_msg("rax: %.16llx\n", *(__u64 *)&vmcb->save.rax);
	hypersecure_log_msg("rip: %.16llx\n", *(__u64 *)&vmcb->save.rip);
	hypersecure_log_msg("rsp: %.16llx\n", *(__u64 *)&vmcb->save.rsp);
	hypersecure_log_msg("=============\n");
}

#endif // hypersecure_DEBUG_H
