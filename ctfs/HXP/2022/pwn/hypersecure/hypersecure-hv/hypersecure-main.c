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

#include "hypersecure.h"
#include "hypersecure-exit-codes.h"
#include "hypersecure-mm.h"
#include "hypersecure-debug.h"
#include "hypersecure-user.h"

#include <linux/build_bug.h>
#include "hypersecure-vmcb.h"

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/gfp.h>
#include <linux/slab.h>
#include <linux/context_tracking.h>
#include <asm/io.h>
#include <asm/string.h>


static cpumask_var_t svm_enabled;

bool hypersecure_debug_enable_logging = false;
module_param(hypersecure_debug_enable_logging, bool, 0);

struct hypersecure_context *global_ctx = NULL;

#define IMAGE_START 0x3000UL
#define CR0_PE (1UL << 0U)
#define CR0_ET (1UL << 4U)
#define CR0_ET (1UL << 4U)
#define CR0_NW (1UL << 29U)
#define CR0_CD (1UL << 30U)
#define CR0_PG (1UL << 31U)
#define CR4_PAE (1UL << 5U)
#define CR4_PGE (1UL << 7U)
#define CR4_OSFXSR (1UL << 9U)
#define CR4_OSXMMEXCPT (1UL << 10U)
#define CR4_OSXSAVE (1UL << 18U)

void __hypersecure_run(u64 vmcb_phys, void *regs);

static int hypersecure_intercept_npf(struct hypersecure_vmcb *vmcb, struct hypersecure_vm_state *state) {
	__u64 fault_phys_address = vmcb->control.exitinfo_v2;
	hypersecure_log_msg("Received NPF at phys addr: 0x%llx\n", vmcb->control.exitinfo_v2);
	hypersecure_dump_regs(state);
	if (fault_phys_address >= hypersecure_MAX_PHYS_SIZE) {
		return 1;
	}
	return 1;
}

static void hypersecure_handle_exception(const enum hypersecure_EXCEPTION excp, const struct hypersecure_vm_state *state) {
	hypersecure_log_msg("Received exception. # = %x. Name: %s\n", (unsigned)excp, translate_hypersecure_exception_number_to_str(excp));
	hypersecure_dump_regs(state);
}

static int hypersecure_handle_exit(struct hypersecure_vcpu *vcpu) {
	struct hypersecure_vmcb *vmcb = vcpu->vmcb;
	struct hypersecure_vm_state *state = vcpu->state;
	__u64 exitcode = get_exitcode(&vmcb->control);
	int should_exit = 0;

	hypersecure_log_msg("Exitcode: %s\n", translate_hypersecure_exitcode_to_str((enum hypersecure_EXITCODE)exitcode));
	hypersecure_dump_regs(state);

	switch((enum hypersecure_EXITCODE)exitcode) {
		case hypersecure_EXITCODE_VMEXIT_EXCP_0 ... hypersecure_EXITCODE_VMEXIT_EXCP_15:
			hypersecure_handle_exception((enum hypersecure_EXCEPTION)(exitcode - hypersecure_EXITCODE_VMEXIT_EXCP_0), state);
			should_exit = 1;
			break;
		case hypersecure_EXITCODE_VMEXIT_INVALID:
		case hypersecure_EXITCODE_VMEXIT_HLT:
		case hypersecure_EXITCODE_VMEXIT_SHUTDOWN:
			should_exit = 1;
			break;
		case hypersecure_EXITCODE_VMEXIT_NPF:
			should_exit = hypersecure_intercept_npf(vmcb, state);
			break;
		default:
			// Some are unhandled, but we're not reimplementing KVM or something.
			hypersecure_log_msg("Unkown exit code\n");
			should_exit = 1;
			break;
	}

	return should_exit;
}

static void hypersecure_setup_regs(struct hypersecure_vm_regs *regs, unsigned int vcpu_id) {
	regs->rip = IMAGE_START;
	regs->rsp = IMAGE_START;
	regs->rax = 0;
	regs->rbx = 0;
	regs->rcx = 0;
	regs->rdx = 0;
	regs->rdi = vcpu_id;
	regs->rsi = 0;
	regs->rbp = 0;
	regs->r8 = 0;
	regs->r9 = 0;
	regs->r10 = 0;
	regs->r11 = 0;
	regs->r12 = 0;
	regs->r13 = 0;
	regs->r14 = 0;
	regs->r15 = 0;
}

static int hypersecure_setup_ioio_prot(struct hypersecure_context *ctx) {
	// Only 12 KiB are necessary.
	unsigned long ioio_prot = __get_free_pages(GFP_KERNEL, 4);
	if (!ioio_prot) {
		return -ENOMEM;
	}
	memset((void *)ioio_prot, 0xFF, 1024 * 12);
	ctx->ioio_prot = ioio_prot;
	return 0;
}

static void hypersecure_free_ioio_prot(struct hypersecure_context *ctx) {
	if (ctx->ioio_prot) {
		free_pages(ctx->ioio_prot, 4);
		ctx->ioio_prot = 0;
	}
}

static void hypersecure_setup_vmcb(struct hypersecure_vmcb *vmcb, u64 ncr3, u64 iopm_pa) {
	struct hypersecure_vmcb_save_area *save = &vmcb->save;
	struct hypersecure_vmcb_control *ctrl = &vmcb->control;

	// Intercept everything
	memset(&ctrl->excp_vec_intercepts, 0xFF, sizeof(ctrl->excp_vec_intercepts));
	ctrl->vec3.hlt_intercept = 1;
	ctrl->vec4.vmrun_intercept = 1;
	ctrl->vec4.vmload_intercept = 1;
	ctrl->vec4.vmsave_intercept = 1;
	ctrl->vec4.vmmcall_intercept = 1;
	ctrl->vec3.ioio_prot_intercept = 1;
	ctrl->vec3.rdpmc_intercept = 1;
	ctrl->vec3.rdtsc_intercept = 1;
	ctrl->vec3.cpuid_intercept = 1;
	ctrl->vec3.pushf_intercept = 1;
	ctrl->vec3.popf_intercept = 1;
	ctrl->vec3.rsm_intercept = 1;
	ctrl->vec3.msr_prot_intercept = 1;
	ctrl->vec3.idtr_wr_intercept = 1;
	ctrl->vec3.gdtr_wr_intercept = 1;
	ctrl->vec3.ldtr_wr_intercept = 1;
	ctrl->vec3.pause_intercept = 1;
	ctrl->tlb_control = 0;
	ctrl->guest_asid = 1;
	ctrl->np_enable = 1;
	ctrl->ncr3 = ncr3;
	ctrl->iopm_base_pa = iopm_pa;

	// Setup long mode.
	save->efer = EFER_SVME | EFER_LME | EFER_LMA;
	save->cr0 = (CR0_PE | CR0_PG);
	save->cr3 = 0x0;
	save->cr4 = (CR4_PAE | CR4_PGE /*| CR4_OSXMMEXCPT | CR4_OSFXSR | CR4_OSXSAVE*/);

	// Setup gdt
	save->reg_gdtr.base = 0x0;
	save->reg_gdtr.limit = -1;

	// Setup segments
	save->reg_cs.base = 0x0;
	save->reg_cs.limit = -1;
	save->reg_cs.attribute = 0x029b;
	save->reg_cs.selector = 0x8;

	save->reg_ss.base = 0;
	save->reg_ss.limit = -1;
	save->reg_ss.attribute = 0x0a93;
	save->reg_ss.selector = 0x10;

	memcpy(&save->reg_ds, &save->reg_ss, sizeof(save->reg_ss));
	memcpy(&save->reg_ss, &save->reg_ss, sizeof(save->reg_ss));
	memcpy(&save->reg_fs, &save->reg_ss, sizeof(save->reg_ss));
	memcpy(&save->reg_gs, &save->reg_ss, sizeof(save->reg_ss));

	// Every index is cacheable.
	save->g_pat = 0x0606060606060606ULL;
}

static void hypersecure_run(struct hypersecure_vmcb *vmcb, struct hypersecure_vm_regs *regs) {
	u64 vmcb_phys = virt_to_phys(vmcb);

	// Load the special registers into vmcb from the regs context
	vmcb->save.rip = regs->rip;
	vmcb->save.rax = regs->rax;
	vmcb->save.rsp = regs->rsp;

	__hypersecure_run(vmcb_phys, regs);

	// Save registers from vmcb to the regs context
	regs->rip = vmcb->save.rip;
	regs->rax = vmcb->save.rax;
	regs->rsp = vmcb->save.rsp;
}

static void enable_svm(struct hypersecure_vcpu *vcpu) {
	u64 hsave_pa;
	u64 efer;

	// Enable SVM.
	rdmsrl(MSR_EFER, efer);
	wrmsrl(MSR_EFER, efer | EFER_SVME);

	hsave_pa = virt_to_phys((void *)vcpu->host_save_va);
	wrmsrl(MSR_VM_HSAVE_PA, hsave_pa);
}

static void run_vm(struct hypersecure_vcpu *vcpu) {
	const int cpu = raw_smp_processor_id();
	// It may be that SVM is disabled. Let's enable it.
	if (!cpumask_test_cpu(cpu, svm_enabled)) {
		enable_svm(vcpu);
		cpumask_set_cpu(cpu, svm_enabled);
	}
	hypersecure_run(vcpu->vmcb, &vcpu->state->regs);
}

int hypersecure_init_and_run(void) {
	unsigned int cpu_index;
	struct hypersecure_vcpu *vcpu;
	int r;

	cpu_index = get_cpu();
	vcpu = &global_ctx->vcpus[cpu_index];

	vcpu->state->regs.rip = IMAGE_START;
	run_vm(vcpu);

	put_cpu();

	r = hypersecure_handle_exit(vcpu);
	if (r < 0) {
		return r;
	}

	vcpu->state->regs.rip = vcpu->vmcb->control.nRIP;

	return 0;
}

static int hypersecure_create_vcpu(struct hypersecure_vcpu *vcpu, const struct hypersecure_mm *mm, const unsigned int id) {
	struct hypersecure_vmcb *vmcb = NULL;
	unsigned long host_save_va = 0;
	struct hypersecure_vm_state *vm_state = NULL;
	int r = 0;

	vmcb = (struct hypersecure_vmcb *)get_zeroed_page(GFP_KERNEL);
	if (!vmcb) {
		hypersecure_log_msg("Failed to allocate vmcb\n");
		r = -ENOMEM;
		goto exit;
	}

	host_save_va = get_zeroed_page(GFP_KERNEL);
	if (!host_save_va) {
		hypersecure_log_msg("Failed to allocate host_save\n");
		r = -ENOMEM;
		goto exit;
	}

	vm_state = (struct hypersecure_vm_state *)get_zeroed_page(GFP_KERNEL);
	if (!vm_state) {
		r = -ENOMEM;
		goto exit;
	}

	vcpu->host_save_va = host_save_va;
	vcpu->vmcb = vmcb;
	vcpu->state = vm_state;
	vcpu->vcpu_id = id;

exit:
	return r;
}

static void hypersecure_destroy_vcpu(struct hypersecure_vcpu *vcpu) {
	free_page((unsigned long)vcpu->vmcb);
	free_page((unsigned long)vcpu->state);
	free_page(vcpu->host_save_va);
}

// For writing to memory via user node
int hypersecure_write_memory(const void *memory, size_t sz) {
	BUG_ON(sz != 0x1000);
	return hypersecure_mm_write_phys_memory(global_ctx->mm, IMAGE_START, memory, sz);
}

static int hypersecure_allocate_ctx(struct hypersecure_context **out_ctx) {
	int r = 0;
	struct hypersecure_mm *mm = NULL;
	struct hypersecure_vcpu *vcpus = NULL;
	struct hypersecure_context *ctx = NULL;
	unsigned i = 0;

	if (!zalloc_cpumask_var(&svm_enabled, GFP_KERNEL)) {
		hypersecure_log_msg("Failed to allocate cpu mask for svm tracking\n");
		r = -ENOMEM;
		goto fail;
	}

	ctx = kzalloc(sizeof(*ctx), GFP_KERNEL);
	if (!ctx) {
		hypersecure_log_msg("Failed to allocate ctx\n");
		r = -ENOMEM;
		goto fail;
	}

	// Setup NPT and GPT
	if (hypersecure_create_mm(&mm)) {
		hypersecure_log_msg("Failed to allocate mm\n");
		r = -ENOMEM;
		goto fail;
	}

	vcpus = kzalloc(nr_cpu_ids * sizeof(struct hypersecure_vcpu), GFP_KERNEL);
	if (!vcpus) {
		hypersecure_log_msg("Failed to allocate vcpu structures\n");
		r = -ENOMEM;
		goto fail;
	}

	// No IO
	r = hypersecure_setup_ioio_prot(ctx);
	if (r < 0) {
		hypersecure_log_msg("Failed to setup ioio prot\n");
		goto fail;
	}

	// Create each vCPU
	for (i = 0; i < nr_cpu_ids; ++i) {
		r = hypersecure_create_vcpu(&vcpus[i], mm, i);
		if (r < 0) {
			goto fail;
		}
	}

	ctx->mm = mm;
	ctx->vcpus = vcpus;

	// Setup VMCB and context registers for each vCPU
	for (i = 0; i < nr_cpu_ids; ++i) {
		struct hypersecure_vcpu *vcpu = &vcpus[i];
		hypersecure_setup_vmcb(vcpu->vmcb, mm->pml4.pa, virt_to_phys((void *)ctx->ioio_prot));
		hypersecure_setup_regs(&vcpu->state->regs, i);
	}

	*out_ctx = ctx;

	return 0;

fail:
	if (vcpus) {
		for (; i != 0;) {
			--i;
			hypersecure_destroy_vcpu(&vcpus[i]);
		}
		kfree(vcpus);
	}
	if (mm) {
		hypersecure_destroy_mm(mm);
	}
	if (ctx) {
		hypersecure_free_ioio_prot(ctx);
		kfree(ctx);
	}
	return r;
}

static void hypersecure_free_ctx(struct hypersecure_context *ctx) {
	u64 efer;
	unsigned i;

	for (i = 0; i < nr_cpu_ids; ++i) {
		hypersecure_destroy_vcpu(&ctx->vcpus[i]);
	}
	kfree(ctx->vcpus);
	hypersecure_destroy_mm(ctx->mm);
	kfree(ctx);

	// Disable SVME.
	// Otherwise, KVM would whine.
	rdmsrl(MSR_EFER, efer);
	wrmsrl(MSR_EFER, efer & ~EFER_SVME);
}

static int hypersecure_init(void) {
	int r;

	// Check if svm is supported.
	if (!boot_cpu_has(X86_FEATURE_SVM)) {
		hypersecure_log_msg("SVM not supported\n");
		return -EINVAL;
	}

	r = hypersecure_allocate_ctx(&global_ctx);
	if (r) {
		return r;
	}

	r = hypersecure_register_user_node();
	if (r < 0) {
		hypersecure_log_msg("Failed to allocate user node\n");
		return r;
	}

	hypersecure_log_msg("Hypersecure init done\n");

	return 0;
}

static void __exit hypersecure_exit(void) {
	hypersecure_log_msg("SVM exit module\n");

	hypersecure_free_ctx(global_ctx);
	hypersecure_deregister_user_node();
}

module_init(hypersecure_init);
module_exit(hypersecure_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("hxp");
