#include "../includes/asm_functions.h"
#include "../includes/vmcs.h"
#include "../includes/crx.h"
#include "../includes/msr.h"
#include <linux/mm.h>
#include <linux/slab.h>
#include <linux/uaccess.h>
#include <asm/io.h>
#include "../includes/vmcs_encoding.h"
#include "../includes/memory.h"

void init_sregs(sregs_t *sregs) {
    sregs->cr0 = 0x30;
    sregs->cr3 = 0x0;
    sregs->cr4 = 0x2040;

    sregs->cs.base = 0;
    sregs->cs.selector = 0x0;
    sregs->cs.limit = 0xffff;
    sregs->cs.access = 0x9b;

    sregs->ds.base = 0;
    sregs->ds.selector = 0x0;
    sregs->ds.limit = 0xffff;
    sregs->ds.access = 0x93;

    sregs->es.base = 0;
    sregs->es.selector = 0x0;
    sregs->es.limit = 0xffff;
    sregs->es.access = 0x93;

    sregs->fs.base = 0;
    sregs->fs.selector = 0x0;
    sregs->fs.limit = 0xffff;
    sregs->fs.access = 0x93;

    sregs->gs.base = 0;
    sregs->gs.selector = 0x0;
    sregs->gs.limit = 0xffff;
    sregs->gs.access = 0x93;

    sregs->ss.base = 0;
    sregs->ss.selector = 0x0;
    sregs->ss.limit = 0xffff;
    sregs->ss.access = 0x93;

    sregs->tr.base = 0x0;
    sregs->tr.limit = 0xffff;
    sregs->tr.access = 0x8b;

    sregs->ldt.base = 0;
    sregs->ldt.selector = 0x0;
    sregs->ldt.limit = 0xffff;
    sregs->ldt.access = 0x82;

    sregs->gdt.base = 0x0;
    sregs->gdt.limit = 0xffff;

    sregs->idt.base = 0x0;
    sregs->idt.limit = 0xffff;

    sregs->sysenter_cs = 0x0;
    sregs->sysenter_rip = 0x0;
    sregs->sysenter_rsp = 0x0;
    sregs->efer = 0x0;
}

int get_guest_mode(vcpu_t *vcpu)
{
        union __cr0_t cr0;
        int mode = -1;
        if (vmread(GUEST_CR0, &cr0.control))
        {
                panic("vmread");
        }


        if ( (cr0.bits.protection_enable == 0) && (cr0.bits.paging_enable == 0) )
        {
                mode = MODE_REAL;
        }

        else if ( (cr0.bits.protection_enable == 1) && (cr0.bits.paging_enable == 0) )
        {
                mode = MODE_PROTECTED;
        }

        else if ( (cr0.bits.protection_enable == 1) && (cr0.bits.paging_enable == 1) )
        {
                mode = MODE_PAGING;
        }


        return mode;
}

void update_rip(vcpu_t *vcpu, int instr_size)
{
        vcpu->state.regs.rip += instr_size;
        return;
}

__u64 get_segment_base(__u64 gdt_base, __u16 segment)
{
        __u64 segment_base = 0;
        union __segment_selector_t selector;
        struct __segment_descriptor_32_t *descriptor;
        struct __segment_descriptor_32_t *descriptor_table;
        selector.flags = segment;

        if (selector.index == 0)
        {
                return 0;
        }

        descriptor_table = (struct __segment_descriptor_32_t*)gdt_base;
        descriptor = &descriptor_table[selector.index];

        segment_base = (unsigned)(descriptor->base_low | ((descriptor->base_middle) << 16) | ((descriptor->base_high) << 24));

        if (descriptor->system == 0 &&
                        ((descriptor->type == SEGMENT_DESCRIPTOR_TYPE_TSS_AVAILABLE) || (descriptor->type == SEGMENT_DESCRIPTOR_TYPE_TSS_BUSY)))
        {
                struct __segment_descriptor_64_t *expanded_descriptor;
                expanded_descriptor = (struct __segment_descriptor_64_t*)descriptor;
                segment_base |= (__u64)expanded_descriptor->base_upper << 32;
        }

        return segment_base;
}


int put_msr(vcpu_t *vcpu) {
    int ret = 0;
    __u64 tmp;
    ret |= vmread(VM_ENTRY_CONTROLS, &tmp);
    tmp |= (vcpu->state.sregs.efer & (1 << 10)) >> 1;

    ret |= vmwrite(VM_ENTRY_CONTROLS, tmp);
    ret |= vmwrite(GUEST_SYSENTER_CS, vcpu->state.sregs.sysenter_cs);
    ret |= vmwrite(GUEST_SYSENTER_EIP, vcpu->state.sregs.sysenter_rip);
    ret |= vmwrite(GUEST_SYSENTER_ESP, vcpu->state.sregs.sysenter_rsp);
    ret |= vmwrite(GUEST_IA32_EFER, vcpu->state.sregs.efer);

    return ret;
}

int get_msr(vcpu_t *vcpu) {
    int ret = 0;
    __u64 tmp;

    ret |= vmread(GUEST_SYSENTER_CS, &vcpu->state.sregs.sysenter_cs);
    ret |= vmread(GUEST_SYSENTER_EIP, &vcpu->state.sregs.sysenter_rip);
    ret |= vmread(GUEST_SYSENTER_ESP, &vcpu->state.sregs.sysenter_rsp);
    ret |= vmread(GUEST_IA32_EFER, &vcpu->state.sregs.efer);
    ret |= vmread(VM_ENTRY_CONTROLS, &tmp);
    tmp <<= 1;
    tmp &= 1 << 10;
    vcpu->state.sregs.efer |= tmp;

    return ret;
}

int put_sregs(vcpu_t *vcpu) {
    int ret = 0;
    ret |= vmwrite(GUEST_CS_SELECTOR, vcpu->state.sregs.cs.selector);
    ret |= vmwrite(GUEST_CS_BASE, vcpu->state.sregs.cs.base);
    ret |= vmwrite(GUEST_CS_LIMIT, vcpu->state.sregs.cs.limit);
    ret |= vmwrite(GUEST_CS_AR_BYTES, vcpu->state.sregs.cs.access);

    ret |= vmwrite(GUEST_DS_SELECTOR, vcpu->state.sregs.ds.selector);
    ret |= vmwrite(GUEST_DS_BASE, vcpu->state.sregs.ds.base);
    ret |= vmwrite(GUEST_DS_LIMIT, vcpu->state.sregs.ds.limit);
    ret |= vmwrite(GUEST_DS_AR_BYTES, vcpu->state.sregs.ds.access);

    ret |= vmwrite(GUEST_ES_SELECTOR, vcpu->state.sregs.es.selector);
    ret |= vmwrite(GUEST_ES_BASE, vcpu->state.sregs.es.base);
    ret |= vmwrite(GUEST_ES_LIMIT, vcpu->state.sregs.es.limit);
    ret |= vmwrite(GUEST_ES_AR_BYTES, vcpu->state.sregs.es.access);

    ret |= vmwrite(GUEST_FS_SELECTOR, vcpu->state.sregs.fs.selector);
    ret |= vmwrite(GUEST_FS_BASE, vcpu->state.sregs.fs.base);
    ret |= vmwrite(GUEST_FS_LIMIT, vcpu->state.sregs.fs.limit);
    ret |= vmwrite(GUEST_FS_AR_BYTES, vcpu->state.sregs.fs.access);

    ret |= vmwrite(GUEST_GS_SELECTOR, vcpu->state.sregs.gs.selector);
    ret |= vmwrite(GUEST_GS_BASE, vcpu->state.sregs.gs.base);
    ret |= vmwrite(GUEST_GS_LIMIT, vcpu->state.sregs.gs.limit);
    ret |= vmwrite(GUEST_GS_AR_BYTES, vcpu->state.sregs.gs.access);

    ret |= vmwrite(GUEST_SS_SELECTOR, vcpu->state.sregs.ss.selector);
    ret |= vmwrite(GUEST_SS_BASE, vcpu->state.sregs.ss.base);
    ret |= vmwrite(GUEST_SS_LIMIT, vcpu->state.sregs.ss.limit);
    ret |= vmwrite(GUEST_SS_AR_BYTES, vcpu->state.sregs.ss.access);

    ret |= vmwrite(GUEST_TR_SELECTOR, vcpu->state.sregs.tr.selector);
    ret |= vmwrite(GUEST_TR_BASE, vcpu->state.sregs.tr.base);
    ret |= vmwrite(GUEST_TR_LIMIT, vcpu->state.sregs.tr.limit);
    ret |= vmwrite(GUEST_TR_AR_BYTES, vcpu->state.sregs.tr.access);

    ret |= vmwrite(GUEST_LDTR_SELECTOR, vcpu->state.sregs.ldt.selector);
    ret |= vmwrite(GUEST_LDTR_BASE, vcpu->state.sregs.ldt.base);
    ret |= vmwrite(GUEST_LDTR_LIMIT, vcpu->state.sregs.ldt.limit);
    ret |= vmwrite(GUEST_LDTR_AR_BYTES, vcpu->state.sregs.ldt.access);

    ret |= vmwrite(GUEST_IDTR_BASE, vcpu->state.sregs.idt.base);
    ret |= vmwrite(GUEST_IDTR_LIMIT, vcpu->state.sregs.idt.limit);

    ret |= vmwrite(GUEST_GDTR_BASE, vcpu->state.sregs.gdt.base);
    ret |= vmwrite(GUEST_GDTR_LIMIT, vcpu->state.sregs.gdt.limit);

    ret |= vmwrite(GUEST_CR0, vcpu->state.sregs.cr0);
    ret |= vmwrite(GUEST_CR3, vcpu->state.sregs.cr3);
    ret |= vmwrite(GUEST_CR4, vcpu->state.sregs.cr4);

    ret |= vmwrite(GUEST_RFLAGS, vcpu->state.regs.rflags);

    return ret;
}

int get_sregs(vcpu_t *vcpu) {
    int ret = 0;
    ret |= vmread(GUEST_CS_SELECTOR, &vcpu->state.sregs.cs.selector);
    ret |= vmread(GUEST_CS_BASE, &vcpu->state.sregs.cs.base);
    ret |= vmread(GUEST_CS_LIMIT, &vcpu->state.sregs.cs.limit);
    ret |= vmread(GUEST_CS_AR_BYTES, &vcpu->state.sregs.cs.access);

    ret |= vmread(GUEST_DS_SELECTOR, &vcpu->state.sregs.ds.selector);
    ret |= vmread(GUEST_DS_BASE, &vcpu->state.sregs.ds.base);
    ret |= vmread(GUEST_DS_LIMIT, &vcpu->state.sregs.ds.limit);
    ret |= vmread(GUEST_DS_AR_BYTES, &vcpu->state.sregs.ds.access);

    ret |= vmread(GUEST_ES_SELECTOR, &vcpu->state.sregs.es.selector);
    ret |= vmread(GUEST_ES_BASE, &vcpu->state.sregs.es.base);
    ret |= vmread(GUEST_ES_LIMIT, &vcpu->state.sregs.es.limit);
    ret |= vmread(GUEST_ES_AR_BYTES, &vcpu->state.sregs.es.access);

    ret |= vmread(GUEST_FS_SELECTOR, &vcpu->state.sregs.fs.selector);
    ret |= vmread(GUEST_FS_BASE, &vcpu->state.sregs.fs.base);
    ret |= vmread(GUEST_FS_LIMIT, &vcpu->state.sregs.fs.limit);
    ret |= vmread(GUEST_FS_AR_BYTES, &vcpu->state.sregs.fs.access);

    ret |= vmread(GUEST_GS_SELECTOR, &vcpu->state.sregs.gs.selector);
    ret |= vmread(GUEST_GS_BASE, &vcpu->state.sregs.gs.base);
    ret |= vmread(GUEST_GS_LIMIT, &vcpu->state.sregs.gs.limit);
    ret |= vmread(GUEST_GS_AR_BYTES, &vcpu->state.sregs.gs.access);

    ret |= vmread(GUEST_SS_SELECTOR, &vcpu->state.sregs.ss.selector);
    ret |= vmread(GUEST_SS_BASE, &vcpu->state.sregs.ss.base);
    ret |= vmread(GUEST_SS_LIMIT, &vcpu->state.sregs.ss.limit);
    ret |= vmread(GUEST_SS_AR_BYTES, &vcpu->state.sregs.ss.access);

    ret |= vmread(GUEST_TR_SELECTOR, &vcpu->state.sregs.tr.selector);
    ret |= vmread(GUEST_TR_BASE, &vcpu->state.sregs.tr.base);
    ret |= vmread(GUEST_TR_LIMIT, &vcpu->state.sregs.tr.limit);
    ret |= vmread(GUEST_TR_AR_BYTES, &vcpu->state.sregs.tr.access);

    ret |= vmread(GUEST_LDTR_SELECTOR, &vcpu->state.sregs.ldt.selector);
    ret |= vmread(GUEST_LDTR_BASE, &vcpu->state.sregs.ldt.base);
    ret |= vmread(GUEST_LDTR_LIMIT, &vcpu->state.sregs.ldt.limit);
    ret |= vmread(GUEST_LDTR_AR_BYTES, &vcpu->state.sregs.ldt.access);

    ret |= vmread(GUEST_IDTR_BASE, &vcpu->state.sregs.idt.base);
    ret |= vmread(GUEST_IDTR_LIMIT, &vcpu->state.sregs.idt.limit);

    ret |= vmread(GUEST_GDTR_BASE, &vcpu->state.sregs.gdt.base);
    ret |= vmread(GUEST_GDTR_LIMIT, &vcpu->state.sregs.gdt.limit);

    ret |= vmread(GUEST_CR0, &vcpu->state.sregs.cr0);
    ret |= vmread(GUEST_CR3, &vcpu->state.sregs.cr3);
    ret |= vmread(GUEST_CR4, &vcpu->state.sregs.cr4);

    ret |= vmread(GUEST_RFLAGS, &vcpu->state.regs.rflags);

    return ret;
}

int vmexit_handle(vcpu_t *vcpu)
{
        __u64 msr = 0;
        __u64 val = 0;
        union __vmx_exit_info_t exit_info = {0};
        union __vmx_exit_qual_t exit_qual = {0};
        int ret = 0;
        __u64 fault_gpa = 0;
        __u64 eptp = 0;
        ret = vmread(VM_EXIT_REASON, &exit_info.flags);
        ret |= vmread(GUEST_RIP, &vcpu->state.regs.rip);
        vcpu->state.mode = get_guest_mode(vcpu);

        ret |= vmread(GUEST_PHYSICAL_ADDRESS, &fault_gpa);
        ret |= vmread(EXIT_QUALIFICATION, &exit_qual.flags);
        ret |= vmread(EPT_POINTER, &eptp);

        if (ret != 0)
        {
                printk(KERN_ERR "vmread failed\n");
                return -1;
        }
        switch (exit_info.bits.exit_reason)
        {
                case EXIT_REASON_CPUID:
                        vcpu->state.regs.rax = 0x4f4f4f4f4f4f4f4f;
                        vcpu->state.regs.rbx = 0x4f4f4f4f4f4f4f4f;
                        vcpu->state.regs.rcx = 0x4f4f4f4f4f4f4f4f;
                        vcpu->state.regs.rdx = 0x4f4f4f4f4f4f4f4f;
                        update_rip(vcpu, 2);
                        return VMEXIT_HANDLED;

                case EXIT_REASON_HLT:
                        update_rip(vcpu, 1);
                        break;

                case EXIT_REASON_EPT_VIOLATION:
                        if (!handle_ept_violation(vcpu->vm->memory, fault_gpa, eptp))
                            break;
                        return VMEXIT_HANDLED;

                case EXIT_REASON_MSR_READ:
                        if(get_msr(vcpu)) {
                            panic("could not get MSRs.\n");
                        };
                        msr = vcpu->state.regs.rcx & 0xffffffff;
                        val = 0x0;
                        switch(msr) {
                            case 0xC0000080: //efer
                                val = vcpu->state.sregs.efer;
                                break;
                            case 0x174:
                                val = vcpu->state.sregs.sysenter_cs;
                                break;
                            case 0x175:
                                val = vcpu->state.sregs.sysenter_rsp;
                                break;
                            case 0x176:
                                val = vcpu->state.sregs.sysenter_rip;
                                break;
                        }
                        vcpu->state.regs.rax = (__u64)(val & 0xffffffff);
                        vcpu->state.regs.rdx = (__u64)((val >> 32) & 0xffffffff);
                        update_rip(vcpu, 2);
                        return VMEXIT_HANDLED;

                case EXIT_REASON_MSR_WRITE:
                        msr = vcpu->state.regs.rcx & 0xffffffff;
                        val = vcpu->state.regs.rdx & 0xffffffff;
                        val <<= 32;
                        val |= vcpu->state.regs.rax & 0xffffffff;
                        switch(msr) {
                            case 0xC0000080:
                                vcpu->state.sregs.efer = val;
                                break;
                            case 0x174:
                                vcpu->state.sregs.sysenter_cs = val;
                                break;
                            case 0x175:
                                vcpu->state.sregs.sysenter_rsp = val;
                                break;
                            case 0x176:
                                vcpu->state.sregs.sysenter_rip = val;
                                break;
                        }
                        update_rip(vcpu, 2);
                        if (put_msr(vcpu))
                        {
                            panic("could not put MSRs.\n");
                        }
                        return VMEXIT_HANDLED;

                default:
                        printk(KERN_INFO "reason: %d, qulalification: %d\n", exit_info.bits.exit_reason, exit_qual.flags);
                        break;
        }

        return exit_info.bits.exit_reason;
}

void vmcs_reinit(vcpu_t *vcpu)
{
        int ret = 0;
        __u64 selector_mask = 7;
        struct __pseudo_descriptor_64_t gdtr;
        struct __pseudo_descriptor_64_t idtr;

        ret |= vmwrite(GUEST_RSP, vcpu->state.regs.rsp);
        ret |= vmwrite(GUEST_RIP, vcpu->state.regs.rip);

        _sgdt(&gdtr);
        _sidt(&idtr);

        ret |= vmwrite(HOST_CR0, _read_cr0());
        ret |= vmwrite(HOST_CR3, _read_cr3());
        ret |= vmwrite(HOST_CR4, _read_cr4());

        ret |= vmwrite(HOST_RIP, (__u64)vm_entrypoint);

        ret |= vmwrite(HOST_CS_SELECTOR, _read_cs() & ~selector_mask);
        ret |= vmwrite(HOST_SS_SELECTOR, _read_ss() & ~selector_mask);
        ret |= vmwrite(HOST_DS_SELECTOR, _read_ds() & ~selector_mask);
        ret |= vmwrite(HOST_ES_SELECTOR, _read_es() & ~selector_mask);
        ret |= vmwrite(HOST_FS_SELECTOR, _read_fs() & ~selector_mask);
        ret |= vmwrite(HOST_GS_SELECTOR, _read_gs() & ~selector_mask);
        ret |= vmwrite(HOST_TR_SELECTOR, _read_tr() & ~selector_mask);

        ret |= vmwrite(HOST_FS_BASE, __readmsr(IA32_FS_BASE));
        ret |= vmwrite(HOST_GS_BASE, __readmsr(IA32_GS_BASE));
        ret |= vmwrite(HOST_TR_BASE, get_segment_base(gdtr.base_address, _read_tr()));
        ret |= vmwrite(HOST_GDTR_BASE, gdtr.base_address);
        ret |= vmwrite(HOST_IDTR_BASE, idtr.base_address);

        ret |= vmwrite(HOST_IA32_SYSENTER_CS, __readmsr(IA32_SYSENTER_CS));
        ret |= vmwrite(HOST_IA32_SYSENTER_ESP, __readmsr(IA32_SYSENTER_ESP));
        ret |= vmwrite(HOST_IA32_SYSENTER_EIP, __readmsr(IA32_SYSENTER_EIP));
        ret |= vmwrite(HOST_IA32_PERF_GLOBAL_CTRL, __readmsr(IA32_PERF_GLOBAL_CTRL));
        if (ret) panic("no good (host)\n");
}

void vmcs_full_init(vm_t *vm, vcpu_t *vcpu)
{
        int ret = 0;
        __u64 vmx_misc;
        union __vmx_pinbased_control_msr_t pin_controls;
        union __vmx_primary_processor_based_control_t primary_proc_controls;
        union __vmx_secondary_processor_based_control_t secondary_proc_controls;

        vmwrite(CPU_BASED_VM_EXEC_CONTROL, 0xa5986dfa);
        vmwrite(CR0_GUEST_HOST_MASK, 0);
        vmwrite(CR0_READ_SHADOW, 0x60000010);
        vmwrite(CR3_TARGET_COUNT, 0x0);
        vmwrite(CR4_GUEST_HOST_MASK, 0);
        vmwrite(CR4_READ_SHADOW, 0x0);
        vmwrite(EXCEPTION_BITMAP, 0x60042);

        vmwrite(GUEST_DR7, 0x400);
        vmwrite(GUEST_IA32_DEBUGCTL, 0x0);
        vmwrite(GUEST_IA32_PAT, 0x7040600070406);
        vmwrite(GUEST_INTERRUPTIBILITY_INFO, 0x0);
        vmwrite(GUEST_PENDING_DBG_EXCEPTIONS, 0x0);
        vmwrite(GUEST_PML_INDEX, 0x1ff);
        vmwrite(GUEST_TR_SELECTOR, 0x0);

        vmwrite(HOST_IA32_EFER, 0xd01);
        vmwrite(PAGE_FAULT_ERROR_CODE_MASK, 0x0);
        vmwrite(PAGE_FAULT_ERROR_CODE_MATCH, 0x0);

        vmwrite(SECONDARY_VM_EXEC_CONTROL, 0x128a2);
        vmwrite(TPR_THRESHOLD, 0x0);
        vmwrite(VIRTUAL_APIC_PAGE_ADDR, 0x0);
        vmwrite(VIRTUAL_PROCESSOR_ID, 0x1);
        vmwrite(VMCS_GUEST_ACTIVITY_STATE, 0x0);
        vmwrite(VMCS_LINK_POINTER, 0xffffffffffffffff);
        vmwrite(VMX_PREEMPTION_TIMER_VALUE, 0xffffffff);

        vmwrite(VM_ENTRY_CONTROLS, 0xd1ff);
        vmwrite(VM_ENTRY_INTR_INFO_FIELD, 0x0);
        vmwrite(VM_ENTRY_MSR_LOAD_COUNT, 0x0);
        vmwrite(VM_EXIT_CONTROLS, 0x2befff);
        vmwrite(VM_FUNCTION_CONTROL, 0x0);
        vmwrite(XSS_EXIT_BITMAP, 0x0);

        ret |= vmwrite(PIN_BASED_VM_EXEC_CONTROL, 0x7e);
        ret |= vmread(PIN_BASED_VM_EXEC_CONTROL, &pin_controls.control);
        pin_controls.bits.vmx_preemption_timer = 1;
        vmwrite(PIN_BASED_VM_EXEC_CONTROL, pin_controls.control);

        vmx_misc = __readmsr(IA32_VMX_MISC_MSR);
        vmx_misc &= 0xFFFFFFFFFFFFFFE1;
        vmread(CPU_BASED_VM_EXEC_CONTROL, &primary_proc_controls.control);
        primary_proc_controls.bits.use_msr_bitmaps = 0;
        vmwrite(CPU_BASED_VM_EXEC_CONTROL, primary_proc_controls.control);

        vmread(SECONDARY_VM_EXEC_CONTROL, &secondary_proc_controls.control);
        secondary_proc_controls.bits.wbinvd_exiting = 0;
        secondary_proc_controls.bits.enable_pml = 0;
        vmwrite(SECONDARY_VM_EXEC_CONTROL, secondary_proc_controls.control);

        vmwrite(EPTP_LIST_ADDRESS, virt_to_phys(vcpu->vm->memory->eptp));
        vmwrite(VM_FUNCTION_CONTROL, 0x1);
        vmwrite(EPT_POINTER, vcpu->vm->memory->eptp[0]);

        vmcs_reinit(vcpu);

        if (ret) panic("no good (full)\n");
}

void vcpu_handle_vmcs(vcpu_t *vcpu, int cur_cpu_id)
{
        uint64_t cur_vmcs_pa;
        if (_vmptrst((__u64) &cur_vmcs_pa) < 0) panic("VMPTRST FAILED\n");

        if (vcpu->vmcs_pa != cur_vmcs_pa)
        {
                if(_vmptrld((__u64) &vcpu->vmcs_pa) < 0) panic("VMPTRLD Failed\n");
        }

        vcpu->host_cpu_id = cur_cpu_id;

        if (!vcpu->initialized)
        {
                vmcs_full_init(vcpu->vm, vcpu);
                vcpu->initialized = 1;
        }
        else
        {
                vmcs_reinit(vcpu);
        }
}

void clearvm(vcpu_t *vcpu) {
        if (_vmclear((__u64) &vcpu->vmcs_pa) < 0) panic("vmclear failed!");
        vcpu->launched = 0;
}

int vcpu_run(vcpu_t *vcpu)
{
        int cur_cpu_id = smp_processor_id();
        int ret = 0;
        int tmp = 0;

        vcpu_handle_vmcs(vcpu, cur_cpu_id);
        tmp = put_sregs(vcpu);
        if (tmp) {
            printk(KERN_ERR "sregs put status:  %d\n", tmp);
            panic("faild to put sregs\n");
        }
        tmp = put_msr(vcpu);
        if (tmp) {
            printk(KERN_ERR "msr put status:  %d\n", tmp);
            panic("faild to put msr\n");
        }

        if (vmwrite(GUEST_RSP, vcpu->state.regs.rsp)) {
                panic("vmwrite");
        }

        if (vcpu->launched) {
            printk(KERN_INFO "Resuming VM!\n");
            ret = _vmresume(&vcpu->state.regs);
        } else {
            printk(KERN_INFO "Launching VM!\n");
            ret = _vmlaunch(&vcpu->state.regs);
        }
        vcpu->launched = 1;


        if (ret < 0)
        {
                __u64 read_ret = 0;
                __u64 error = 0;
                read_ret = vmread(VM_INSTRUCTION_ERROR, &error);
                printk(KERN_ERR "VM_INSTRUCTION_ERROR: %d\n", error);
                return -error;
        }

        if (vmread(GUEST_RSP, &vcpu->state.regs.rsp)) {
                panic("vmread");
        }

        ret = vmexit_handle(vcpu);
        tmp = get_sregs(vcpu);
        if (tmp) {
            printk(KERN_ERR "sregs get status:  %d\n", tmp);
            panic("faild to get sregs\n");
        }
        tmp = get_msr(vcpu);
        if (tmp) {
            printk(KERN_ERR "msr get status:  %d\n", tmp);
            panic("faild to get msr\n");
        }

        return ret;
}

int vmcs_alloc( vcpu_t *vcpu )
{
        vcpu->vmcs_pa = __pa(&vcpu->vmcs);
        vcpu->vmcs.header.bits.revision_identifier = vmcs_revision_id();
        vcpu->vmcs.header.bits.shadow_vmcs_indicator = 0;
        return true;
}

vcpu_t *vcpu_alloc(vm_t *vm)
{
        vcpu_t *vcpu = &vm->vcpu;
        vcpu->host_cpu_id = -1;
        vcpu->vm = vm;

        if (!vmcs_alloc(vcpu)) panic("Failed to alloc vmcs\n");

        return vcpu;
}


struct __vmcs_t *vmxon_virtual[MAX_PCPUS];
__u64 vmxon_physical[MAX_PCPUS];

vm_t *vm_alloc(void)
{
        vm_t *vm = kzalloc(sizeof(vm_t), GFP_KERNEL);

        if (!vm)
        {
                printk(KERN_ERR "Couldn't allocate memory for vm\n");
                return NULL;
        }

        vcpu_alloc(vm);
        return vm;
}

void vcpu_destroy(vcpu_t *vcpu) {
        vcpu->vmcs_pa = 0;
        vcpu->vmcs.header.bits.revision_identifier = 0;
        vcpu->vmcs.header.bits.shadow_vmcs_indicator = 0;
        vcpu->host_cpu_id = -1;
        vcpu->vm = 0;
}

int vm_destroy(vm_t *vm)
{
        if (!vm)
        {
                printk(KERN_ERR "Bad VMM context in destroy\n");
                return false;
        }
        printk(KERN_INFO "Destroying vcpu\n");
        vcpu_destroy(&vm->vcpu);

        kfree(vm);
        return true;
}

void vmx_cpu_off(void *arg) {
        int cpu = smp_processor_id();
        int ret;

        ret = _vmxoff();
        if (ret < 0)
                panic("vmxoff failed for CPU %d\n", cpu);

        kfree(vmxon_virtual[cpu]);
}

void vmx_cpu_on(void *arg) {
        int cpu = smp_processor_id();
        int supported;
        int ret;
        supported = get_vmx_support();
        if (!supported)
                panic("VMX Operation is not supported\n");

        vmxon_virtual[cpu] = kzalloc(4096, GFP_KERNEL);
        if (!vmxon_virtual[cpu])
                panic("Couldn't allocate space for vmxon");

        vmxon_virtual[cpu]->header.all = vmcs_revision_id();
        vmxon_physical[cpu] = __pa(vmxon_virtual[cpu]);

        ret = _vmxon((__u64)&vmxon_physical[cpu]);
        if (ret < 0)
                panic("VMXON Failed: %d\n", ret);
}

void vmx_off() {
        int i;
        for (i = 0; i < num_online_cpus(); i++)
                smp_call_function_single(i, &vmx_cpu_off, NULL, 1);
}

void vmx_on() {
        int i;
        for (i = 0; i < num_online_cpus(); i++)
                smp_call_function_single(i, &vmx_cpu_on, NULL, 1);
}
