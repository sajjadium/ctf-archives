#ifndef hypersecure_VMCB
#define hypersecure_VMCB

/* This file is auto-generated */

#include <linux/types.h>

struct hypersecure_vmcb_save_area {
	struct reg_es_t {
		__u16 selector;
		__u16 attribute;
		__u32 limit;
		__u64 base;
	} reg_es ;
	struct reg_cs_t {
		__u16 selector;
		__u16 attribute;
		__u32 limit;
		__u64 base;
	} reg_cs ;
	struct reg_ss_t {
		__u16 selector;
		__u16 attribute;
		__u32 limit;
		__u64 base;
	} reg_ss ;
	struct reg_ds_t {
		__u16 selector;
		__u16 attribute;
		__u32 limit;
		__u64 base;
	} reg_ds ;
	struct reg_fs_t {
		__u16 selector;
		__u16 attribute;
		__u32 limit;
		__u64 base;
	} reg_fs ;
	struct reg_gs_t {
		__u16 selector;
		__u16 attribute;
		__u32 limit;
		__u64 base;
	} reg_gs ;
	struct reg_gdtr_t {
		__u16 selector;
		__u16 attribute;
		__u32 limit;
		__u64 base;
	} reg_gdtr ;
	struct reg_ldtr_t {
		__u16 selector;
		__u16 attribute;
		__u32 limit;
		__u64 base;
	} reg_ldtr ;
	struct reg_idtr_t {
		__u16 selector;
		__u16 attribute;
		__u32 limit;
		__u64 base;
	} reg_idtr ;
	struct reg_tr_t {
		__u16 selector;
		__u16 attribute;
		__u32 limit;
		__u64 base;
	} reg_tr ;
	__u8 pad_full_0[43];
	__u8 cpl;
	__u8 pad_full_1[4];
	__u64 efer;
	__u8 pad_full_2[112];
	__u64 cr4;
	__u64 cr3;
	__u64 cr0;
	__u64 dr7;
	__u64 dr6;
	__u64 rflags;
	__u64 rip;
	__u8 pad_full_3[88];
	__u64 rsp;
	__u64 s_cet;
	__u64 ssp;
	__u64 isst_addr;
	__u64 rax;
	__u64 star;
	__u64 lstar;
	__u64 cstar;
	__u64 sfmask;
	__u64 kernel_gs_base;
	__u64 sysenter_cs;
	__u64 sysenter_esp;
	__u64 sysenter_eip;
	__u64 cr2;
	__u8 pad_full_4[32];
	__u64 g_pat;
	__u64 dbgctl;
	__u64 br_from;
	__u64 br_to;
	__u64 lastexcpfrom;
	__u8 pad_full_5[80];
	__u32 spec_ctrl;
} __attribute__ ((packed));

struct hypersecure_vmcb_control {
	struct cr_rd_intercepts_t {
		__u8 cr_0_rd_intercept : 1;
		__u8 cr_1_rd_intercept : 1;
		__u8 cr_2_rd_intercept : 1;
		__u8 cr_3_rd_intercept : 1;
		__u8 cr_4_rd_intercept : 1;
		__u8 cr_5_rd_intercept : 1;
		__u8 cr_6_rd_intercept : 1;
		__u8 cr_7_rd_intercept : 1;
		__u8 cr_8_rd_intercept : 1;
		__u8 cr_9_rd_intercept : 1;
		__u8 cr_10_rd_intercept : 1;
		__u8 cr_11_rd_intercept : 1;
		__u8 cr_12_rd_intercept : 1;
		__u8 cr_13_rd_intercept : 1;
		__u8 cr_14_rd_intercept : 1;
		__u8 cr_15_rd_intercept : 1;
	} cr_rd_intercepts ;
	struct cr_wr_intercepts_t {
		__u8 cr_0_wr_intercept : 1;
		__u8 cr_1_wr_intercept : 1;
		__u8 cr_2_wr_intercept : 1;
		__u8 cr_3_wr_intercept : 1;
		__u8 cr_4_wr_intercept : 1;
		__u8 cr_5_wr_intercept : 1;
		__u8 cr_6_wr_intercept : 1;
		__u8 cr_7_wr_intercept : 1;
		__u8 cr_8_wr_intercept : 1;
		__u8 cr_9_wr_intercept : 1;
		__u8 cr_10_wr_intercept : 1;
		__u8 cr_11_wr_intercept : 1;
		__u8 cr_12_wr_intercept : 1;
		__u8 cr_13_wr_intercept : 1;
		__u8 cr_14_wr_intercept : 1;
		__u8 cr_15_wr_intercept : 1;
	} cr_wr_intercepts ;
	struct dr_rd_intercepts_t {
		__u8 dr_0_rd_intercept : 1;
		__u8 dr_1_rd_intercept : 1;
		__u8 dr_2_rd_intercept : 1;
		__u8 dr_3_rd_intercept : 1;
		__u8 dr_4_rd_intercept : 1;
		__u8 dr_5_rd_intercept : 1;
		__u8 dr_6_rd_intercept : 1;
		__u8 dr_7_rd_intercept : 1;
		__u8 dr_8_rd_intercept : 1;
		__u8 dr_9_rd_intercept : 1;
		__u8 dr_10_rd_intercept : 1;
		__u8 dr_11_rd_intercept : 1;
		__u8 dr_12_rd_intercept : 1;
		__u8 dr_13_rd_intercept : 1;
		__u8 dr_14_rd_intercept : 1;
		__u8 dr_15_rd_intercept : 1;
	} dr_rd_intercepts ;
	struct dr_wr_intercepts_t {
		__u8 dr_0_wr_intercept : 1;
		__u8 dr_1_wr_intercept : 1;
		__u8 dr_2_wr_intercept : 1;
		__u8 dr_3_wr_intercept : 1;
		__u8 dr_4_wr_intercept : 1;
		__u8 dr_5_wr_intercept : 1;
		__u8 dr_6_wr_intercept : 1;
		__u8 dr_7_wr_intercept : 1;
		__u8 dr_8_wr_intercept : 1;
		__u8 dr_9_wr_intercept : 1;
		__u8 dr_10_wr_intercept : 1;
		__u8 dr_11_wr_intercept : 1;
		__u8 dr_12_wr_intercept : 1;
		__u8 dr_13_wr_intercept : 1;
		__u8 dr_14_wr_intercept : 1;
		__u8 dr_15_wr_intercept : 1;
	} dr_wr_intercepts ;
	struct excp_vec_intercepts_t {
		__u8 exception_0_intercept : 1;
		__u8 exception_1_intercept : 1;
		__u8 exception_2_intercept : 1;
		__u8 exception_3_intercept : 1;
		__u8 exception_4_intercept : 1;
		__u8 exception_5_intercept : 1;
		__u8 exception_6_intercept : 1;
		__u8 exception_7_intercept : 1;
		__u8 exception_8_intercept : 1;
		__u8 exception_9_intercept : 1;
		__u8 exception_10_intercept : 1;
		__u8 exception_11_intercept : 1;
		__u8 exception_12_intercept : 1;
		__u8 exception_13_intercept : 1;
		__u8 exception_14_intercept : 1;
		__u8 exception_15_intercept : 1;
	} excp_vec_intercepts ;
	struct vec3_t {
		__u8 pad_full_0[2];
		__u8 intr_intercept : 1;
		__u8 nmi_intercept : 1;
		__u8 smi_intercept : 1;
		__u8 init_intercept : 1;
		__u8 vintr_intercept : 1;
		__u8 cr0_intercept : 1;
		__u8 idtr_rd_intercept : 1;
		__u8 gdtr_rd_intercept : 1;
		__u8 ldtr_rd_intercept : 1;
		__u8 tr_rd_intercept : 1;
		__u8 idtr_wr_intercept : 1;
		__u8 gdtr_wr_intercept : 1;
		__u8 ldtr_wr_intercept : 1;
		__u8 tr_wr_intercept : 1;
		__u8 rdtsc_intercept : 1;
		__u8 rdpmc_intercept : 1;
		__u8 pushf_intercept : 1;
		__u8 popf_intercept : 1;
		__u8 cpuid_intercept : 1;
		__u8 rsm_intercept : 1;
		__u8 iret_intercept : 1;
		__u8 intn_intercept : 1;
		__u8 invd_intercept : 1;
		__u8 pause_intercept : 1;
		__u8 hlt_intercept : 1;
		__u8 invlpg_intercept : 1;
		__u8 invlpga_intercept : 1;
		__u8 ioio_prot_intercept : 1;
		__u8 msr_prot_intercept : 1;
		__u8 task_switch_intercept : 1;
		__u8 ferr_freeze_intercept : 1;
		__u8 shutdown_events_intercept : 1;
	} vec3 ;
	struct vec4_t {
		__u8 vmrun_intercept : 1;
		__u8 vmmcall_intercept : 1;
		__u8 vmload_intercept : 1;
		__u8 vmsave_intercept : 1;
		__u8 stgi_intercept : 1;
		__u8 clgi_intercept : 1;
		__u8 skinit_intercept : 1;
		__u8 rdtscp_intercept : 1;
		__u8 icebp_intercept : 1;
		__u8 wbinvd_wbnoinvd_intercept : 1;
		__u8 monitor_monitorx_intercept : 1;
		__u8 mwait_mwaitx_intercept : 1;
		__u8 xsetbvrdpru_intercept : 1;
		__u8 efer_wr_after_done_intercept : 1;
		__u8 pad_pre_1 : 2;
		__u8 cr0_wr_after_done_intercept : 1;
		__u8 cr1_wr_after_done_intercept : 1;
		__u8 cr2_wr_after_done_intercept : 1;
		__u8 cr3_wr_after_done_intercept : 1;
		__u8 cr4_wr_after_done_intercept : 1;
		__u8 cr5_wr_after_done_intercept : 1;
		__u8 cr6_wr_after_done_intercept : 1;
		__u8 cr7_wr_after_done_intercept : 1;
		__u8 cr8_wr_after_done_intercept : 1;
		__u8 cr9_wr_after_done_intercept : 1;
		__u8 cr10_wr_after_done_intercept : 1;
		__u8 cr11_wr_after_done_intercept : 1;
		__u8 cr12_wr_after_done_intercept : 1;
		__u8 cr13_wr_after_done_intercept : 1;
		__u8 cr14_wr_after_done_intercept : 1;
		__u8 cr15_wr_after_done_intercept : 1;
	} vec4 ;
	__u8 pad_full_2[0x2c];
	__u64 iopm_base_pa;
	__u8 pad_full_more[60 - 0x34];
	__u64 tsc_offset;
	__u32 guest_asid;
	__u8 tlb_control;
	__u8 pad_full_3[19];
	__u64 exitcode;
	__u64 exitinfo_v1;
	__u64 exitinfo_v2;
	__u64 exitintinfo;
	__u8 np_enable : 1;
	__u8 pad_pre_4 : 7;
	__u8 pad_full_5[31];
	__u64 ncr3;
	__u8 pad_full_6[8];
	__u32 vmcb_clean;
	__u8 pad_full_7[4];
	__u64 nRIP;
	__u8 num_bytes_fetched;
	__u64 bytes_fetched_low : 56;
	__u64 bytes_fetched_hi;
	struct vmsa_info_t {
		__u8 pad_full_8[40];
		__u16 padding : 12;
		__u64 vmsa_ptr : 40;
	} vmsa_info ;
} __attribute__ ((packed));

struct hypersecure_vmcb {
	struct hypersecure_vmcb_control control;
	unsigned char pad[0x400 - sizeof(struct hypersecure_vmcb_control)];
	struct hypersecure_vmcb_save_area save;
} __attribute__ ((aligned (0x1000)));

static_assert(offsetof(struct hypersecure_vmcb_control, iopm_base_pa) == 0x40);
static_assert(offsetof(struct hypersecure_vmcb_control, cr_rd_intercepts) == 0);
static_assert(offsetof(struct hypersecure_vmcb_control, dr_rd_intercepts) == 0x4);
static_assert(offsetof(struct hypersecure_vmcb_control, excp_vec_intercepts) == 0x8);
static_assert(offsetof(struct hypersecure_vmcb_control, guest_asid) == 0x58);
static_assert(offsetof(struct hypersecure_vmcb_control, nRIP) == 0xc8);
static_assert(offsetof(struct hypersecure_vmcb_control, exitinfo_v1) == 0x78);
static_assert(offsetof(struct hypersecure_vmcb_control, exitinfo_v2) == 0x80);
static_assert(offsetof(struct hypersecure_vmcb_control, ncr3) == 0xb0);
static_assert(offsetof(struct hypersecure_vmcb, save) == 0x400);
static_assert(sizeof(struct hypersecure_vmcb) <= 0x1000);
static inline __u16 get_reg_es_selector(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_es.selector;
}

static inline __u16 get_reg_es_attribute(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_es.attribute;
}

static inline __u32 get_reg_es_limit(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_es.limit;
}

static inline __u64 get_reg_es_base(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_es.base;
}

static inline __u16 get_reg_cs_selector(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_cs.selector;
}

static inline __u16 get_reg_cs_attribute(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_cs.attribute;
}

static inline __u32 get_reg_cs_limit(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_cs.limit;
}

static inline __u64 get_reg_cs_base(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_cs.base;
}

static inline __u16 get_reg_ss_selector(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_ss.selector;
}

static inline __u16 get_reg_ss_attribute(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_ss.attribute;
}

static inline __u32 get_reg_ss_limit(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_ss.limit;
}

static inline __u64 get_reg_ss_base(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_ss.base;
}

static inline __u16 get_reg_ds_selector(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_ds.selector;
}

static inline __u16 get_reg_ds_attribute(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_ds.attribute;
}

static inline __u32 get_reg_ds_limit(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_ds.limit;
}

static inline __u64 get_reg_ds_base(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_ds.base;
}

static inline __u16 get_reg_fs_selector(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_fs.selector;
}

static inline __u16 get_reg_fs_attribute(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_fs.attribute;
}

static inline __u32 get_reg_fs_limit(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_fs.limit;
}

static inline __u64 get_reg_fs_base(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_fs.base;
}

static inline __u16 get_reg_gs_selector(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_gs.selector;
}

static inline __u16 get_reg_gs_attribute(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_gs.attribute;
}

static inline __u32 get_reg_gs_limit(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_gs.limit;
}

static inline __u64 get_reg_gs_base(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_gs.base;
}

static inline __u16 get_reg_gdtr_selector(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_gdtr.selector;
}

static inline __u16 get_reg_gdtr_attribute(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_gdtr.attribute;
}

static inline __u32 get_reg_gdtr_limit(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_gdtr.limit;
}

static inline __u64 get_reg_gdtr_base(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_gdtr.base;
}

static inline __u16 get_reg_ldtr_selector(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_ldtr.selector;
}

static inline __u16 get_reg_ldtr_attribute(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_ldtr.attribute;
}

static inline __u32 get_reg_ldtr_limit(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_ldtr.limit;
}

static inline __u64 get_reg_ldtr_base(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_ldtr.base;
}

static inline __u16 get_reg_idtr_selector(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_idtr.selector;
}

static inline __u16 get_reg_idtr_attribute(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_idtr.attribute;
}

static inline __u32 get_reg_idtr_limit(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_idtr.limit;
}

static inline __u64 get_reg_idtr_base(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_idtr.base;
}

static inline __u16 get_reg_tr_selector(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_tr.selector;
}

static inline __u16 get_reg_tr_attribute(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_tr.attribute;
}

static inline __u32 get_reg_tr_limit(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_tr.limit;
}

static inline __u64 get_reg_tr_base(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->reg_tr.base;
}

static inline __u8 get_cpl(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->cpl;
}

static inline __u64 get_efer(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->efer;
}

static inline __u64 get_cr4(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->cr4;
}

static inline __u64 get_cr3(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->cr3;
}

static inline __u64 get_cr0(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->cr0;
}

static inline __u64 get_dr7(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->dr7;
}

static inline __u64 get_dr6(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->dr6;
}

static inline __u64 get_rflags(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->rflags;
}

static inline __u64 get_rip(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->rip;
}

static inline __u64 get_rsp(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->rsp;
}

static inline __u64 get_s_cet(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->s_cet;
}

static inline __u64 get_ssp(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->ssp;
}

static inline __u64 get_isst_addr(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->isst_addr;
}

static inline __u64 get_rax(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->rax;
}

static inline __u64 get_star(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->star;
}

static inline __u64 get_lstar(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->lstar;
}

static inline __u64 get_cstar(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->cstar;
}

static inline __u64 get_sfmask(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->sfmask;
}

static inline __u64 get_kernel_gs_base(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->kernel_gs_base;
}

static inline __u64 get_sysenter_cs(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->sysenter_cs;
}

static inline __u64 get_sysenter_esp(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->sysenter_esp;
}

static inline __u64 get_sysenter_eip(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->sysenter_eip;
}

static inline __u64 get_cr2(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->cr2;
}

static inline __u64 get_g_pat(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->g_pat;
}

static inline __u64 get_dbgctl(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->dbgctl;
}

static inline __u64 get_br_from(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->br_from;
}

static inline __u64 get_br_to(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->br_to;
}

static inline __u64 get_lastexcpfrom(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->lastexcpfrom;
}

static inline __u32 get_spec_ctrl(struct hypersecure_vmcb_save_area *ctx) {
	return ctx->spec_ctrl;
}

static inline __u8 get_cr_rd_intercepts_cr_0_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_rd_intercepts.cr_0_rd_intercept;
}

static inline __u8 get_cr_rd_intercepts_cr_1_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_rd_intercepts.cr_1_rd_intercept;
}

static inline __u8 get_cr_rd_intercepts_cr_2_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_rd_intercepts.cr_2_rd_intercept;
}

static inline __u8 get_cr_rd_intercepts_cr_3_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_rd_intercepts.cr_3_rd_intercept;
}

static inline __u8 get_cr_rd_intercepts_cr_4_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_rd_intercepts.cr_4_rd_intercept;
}

static inline __u8 get_cr_rd_intercepts_cr_5_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_rd_intercepts.cr_5_rd_intercept;
}

static inline __u8 get_cr_rd_intercepts_cr_6_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_rd_intercepts.cr_6_rd_intercept;
}

static inline __u8 get_cr_rd_intercepts_cr_7_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_rd_intercepts.cr_7_rd_intercept;
}

static inline __u8 get_cr_rd_intercepts_cr_8_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_rd_intercepts.cr_8_rd_intercept;
}

static inline __u8 get_cr_rd_intercepts_cr_9_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_rd_intercepts.cr_9_rd_intercept;
}

static inline __u8 get_cr_rd_intercepts_cr_10_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_rd_intercepts.cr_10_rd_intercept;
}

static inline __u8 get_cr_rd_intercepts_cr_11_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_rd_intercepts.cr_11_rd_intercept;
}

static inline __u8 get_cr_rd_intercepts_cr_12_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_rd_intercepts.cr_12_rd_intercept;
}

static inline __u8 get_cr_rd_intercepts_cr_13_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_rd_intercepts.cr_13_rd_intercept;
}

static inline __u8 get_cr_rd_intercepts_cr_14_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_rd_intercepts.cr_14_rd_intercept;
}

static inline __u8 get_cr_rd_intercepts_cr_15_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_rd_intercepts.cr_15_rd_intercept;
}

static inline __u8 get_cr_wr_intercepts_cr_0_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_wr_intercepts.cr_0_wr_intercept;
}

static inline __u8 get_cr_wr_intercepts_cr_1_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_wr_intercepts.cr_1_wr_intercept;
}

static inline __u8 get_cr_wr_intercepts_cr_2_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_wr_intercepts.cr_2_wr_intercept;
}

static inline __u8 get_cr_wr_intercepts_cr_3_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_wr_intercepts.cr_3_wr_intercept;
}

static inline __u8 get_cr_wr_intercepts_cr_4_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_wr_intercepts.cr_4_wr_intercept;
}

static inline __u8 get_cr_wr_intercepts_cr_5_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_wr_intercepts.cr_5_wr_intercept;
}

static inline __u8 get_cr_wr_intercepts_cr_6_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_wr_intercepts.cr_6_wr_intercept;
}

static inline __u8 get_cr_wr_intercepts_cr_7_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_wr_intercepts.cr_7_wr_intercept;
}

static inline __u8 get_cr_wr_intercepts_cr_8_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_wr_intercepts.cr_8_wr_intercept;
}

static inline __u8 get_cr_wr_intercepts_cr_9_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_wr_intercepts.cr_9_wr_intercept;
}

static inline __u8 get_cr_wr_intercepts_cr_10_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_wr_intercepts.cr_10_wr_intercept;
}

static inline __u8 get_cr_wr_intercepts_cr_11_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_wr_intercepts.cr_11_wr_intercept;
}

static inline __u8 get_cr_wr_intercepts_cr_12_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_wr_intercepts.cr_12_wr_intercept;
}

static inline __u8 get_cr_wr_intercepts_cr_13_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_wr_intercepts.cr_13_wr_intercept;
}

static inline __u8 get_cr_wr_intercepts_cr_14_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_wr_intercepts.cr_14_wr_intercept;
}

static inline __u8 get_cr_wr_intercepts_cr_15_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->cr_wr_intercepts.cr_15_wr_intercept;
}

static inline __u8 get_dr_rd_intercepts_dr_0_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_rd_intercepts.dr_0_rd_intercept;
}

static inline __u8 get_dr_rd_intercepts_dr_1_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_rd_intercepts.dr_1_rd_intercept;
}

static inline __u8 get_dr_rd_intercepts_dr_2_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_rd_intercepts.dr_2_rd_intercept;
}

static inline __u8 get_dr_rd_intercepts_dr_3_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_rd_intercepts.dr_3_rd_intercept;
}

static inline __u8 get_dr_rd_intercepts_dr_4_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_rd_intercepts.dr_4_rd_intercept;
}

static inline __u8 get_dr_rd_intercepts_dr_5_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_rd_intercepts.dr_5_rd_intercept;
}

static inline __u8 get_dr_rd_intercepts_dr_6_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_rd_intercepts.dr_6_rd_intercept;
}

static inline __u8 get_dr_rd_intercepts_dr_7_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_rd_intercepts.dr_7_rd_intercept;
}

static inline __u8 get_dr_rd_intercepts_dr_8_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_rd_intercepts.dr_8_rd_intercept;
}

static inline __u8 get_dr_rd_intercepts_dr_9_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_rd_intercepts.dr_9_rd_intercept;
}

static inline __u8 get_dr_rd_intercepts_dr_10_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_rd_intercepts.dr_10_rd_intercept;
}

static inline __u8 get_dr_rd_intercepts_dr_11_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_rd_intercepts.dr_11_rd_intercept;
}

static inline __u8 get_dr_rd_intercepts_dr_12_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_rd_intercepts.dr_12_rd_intercept;
}

static inline __u8 get_dr_rd_intercepts_dr_13_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_rd_intercepts.dr_13_rd_intercept;
}

static inline __u8 get_dr_rd_intercepts_dr_14_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_rd_intercepts.dr_14_rd_intercept;
}

static inline __u8 get_dr_rd_intercepts_dr_15_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_rd_intercepts.dr_15_rd_intercept;
}

static inline __u8 get_dr_wr_intercepts_dr_0_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_wr_intercepts.dr_0_wr_intercept;
}

static inline __u8 get_dr_wr_intercepts_dr_1_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_wr_intercepts.dr_1_wr_intercept;
}

static inline __u8 get_dr_wr_intercepts_dr_2_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_wr_intercepts.dr_2_wr_intercept;
}

static inline __u8 get_dr_wr_intercepts_dr_3_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_wr_intercepts.dr_3_wr_intercept;
}

static inline __u8 get_dr_wr_intercepts_dr_4_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_wr_intercepts.dr_4_wr_intercept;
}

static inline __u8 get_dr_wr_intercepts_dr_5_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_wr_intercepts.dr_5_wr_intercept;
}

static inline __u8 get_dr_wr_intercepts_dr_6_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_wr_intercepts.dr_6_wr_intercept;
}

static inline __u8 get_dr_wr_intercepts_dr_7_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_wr_intercepts.dr_7_wr_intercept;
}

static inline __u8 get_dr_wr_intercepts_dr_8_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_wr_intercepts.dr_8_wr_intercept;
}

static inline __u8 get_dr_wr_intercepts_dr_9_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_wr_intercepts.dr_9_wr_intercept;
}

static inline __u8 get_dr_wr_intercepts_dr_10_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_wr_intercepts.dr_10_wr_intercept;
}

static inline __u8 get_dr_wr_intercepts_dr_11_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_wr_intercepts.dr_11_wr_intercept;
}

static inline __u8 get_dr_wr_intercepts_dr_12_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_wr_intercepts.dr_12_wr_intercept;
}

static inline __u8 get_dr_wr_intercepts_dr_13_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_wr_intercepts.dr_13_wr_intercept;
}

static inline __u8 get_dr_wr_intercepts_dr_14_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_wr_intercepts.dr_14_wr_intercept;
}

static inline __u8 get_dr_wr_intercepts_dr_15_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->dr_wr_intercepts.dr_15_wr_intercept;
}

static inline __u8 get_excp_vec_intercepts_exception_0_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->excp_vec_intercepts.exception_0_intercept;
}

static inline __u8 get_excp_vec_intercepts_exception_1_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->excp_vec_intercepts.exception_1_intercept;
}

static inline __u8 get_excp_vec_intercepts_exception_2_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->excp_vec_intercepts.exception_2_intercept;
}

static inline __u8 get_excp_vec_intercepts_exception_3_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->excp_vec_intercepts.exception_3_intercept;
}

static inline __u8 get_excp_vec_intercepts_exception_4_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->excp_vec_intercepts.exception_4_intercept;
}

static inline __u8 get_excp_vec_intercepts_exception_5_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->excp_vec_intercepts.exception_5_intercept;
}

static inline __u8 get_excp_vec_intercepts_exception_6_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->excp_vec_intercepts.exception_6_intercept;
}

static inline __u8 get_excp_vec_intercepts_exception_7_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->excp_vec_intercepts.exception_7_intercept;
}

static inline __u8 get_excp_vec_intercepts_exception_8_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->excp_vec_intercepts.exception_8_intercept;
}

static inline __u8 get_excp_vec_intercepts_exception_9_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->excp_vec_intercepts.exception_9_intercept;
}

static inline __u8 get_excp_vec_intercepts_exception_10_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->excp_vec_intercepts.exception_10_intercept;
}

static inline __u8 get_excp_vec_intercepts_exception_11_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->excp_vec_intercepts.exception_11_intercept;
}

static inline __u8 get_excp_vec_intercepts_exception_12_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->excp_vec_intercepts.exception_12_intercept;
}

static inline __u8 get_excp_vec_intercepts_exception_13_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->excp_vec_intercepts.exception_13_intercept;
}

static inline __u8 get_excp_vec_intercepts_exception_14_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->excp_vec_intercepts.exception_14_intercept;
}

static inline __u8 get_excp_vec_intercepts_exception_15_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->excp_vec_intercepts.exception_15_intercept;
}

static inline __u8 get_vec3_intr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.intr_intercept;
}

static inline __u8 get_vec3_nmi_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.nmi_intercept;
}

static inline __u8 get_vec3_smi_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.smi_intercept;
}

static inline __u8 get_vec3_init_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.init_intercept;
}

static inline __u8 get_vec3_vintr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.vintr_intercept;
}

static inline __u8 get_vec3_cr0_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.cr0_intercept;
}

static inline __u8 get_vec3_idtr_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.idtr_rd_intercept;
}

static inline __u8 get_vec3_gdtr_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.gdtr_rd_intercept;
}

static inline __u8 get_vec3_ldtr_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.ldtr_rd_intercept;
}

static inline __u8 get_vec3_tr_rd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.tr_rd_intercept;
}

static inline __u8 get_vec3_idtr_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.idtr_wr_intercept;
}

static inline __u8 get_vec3_gdtr_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.gdtr_wr_intercept;
}

static inline __u8 get_vec3_ldtr_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.ldtr_wr_intercept;
}

static inline __u8 get_vec3_tr_wr_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.tr_wr_intercept;
}

static inline __u8 get_vec3_rdtsc_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.rdtsc_intercept;
}

static inline __u8 get_vec3_rdpmc_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.rdpmc_intercept;
}

static inline __u8 get_vec3_pushf_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.pushf_intercept;
}

static inline __u8 get_vec3_popf_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.popf_intercept;
}

static inline __u8 get_vec3_cpuid_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.cpuid_intercept;
}

static inline __u8 get_vec3_rsm_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.rsm_intercept;
}

static inline __u8 get_vec3_iret_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.iret_intercept;
}

static inline __u8 get_vec3_intn_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.intn_intercept;
}

static inline __u8 get_vec3_invd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.invd_intercept;
}

static inline __u8 get_vec3_pause_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.pause_intercept;
}

static inline __u8 get_vec3_hlt_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.hlt_intercept;
}

static inline __u8 get_vec3_invlpg_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.invlpg_intercept;
}

static inline __u8 get_vec3_invlpga_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.invlpga_intercept;
}

static inline __u8 get_vec3_ioio_prot_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.ioio_prot_intercept;
}

static inline __u8 get_vec3_msr_prot_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.msr_prot_intercept;
}

static inline __u8 get_vec3_task_switch_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.task_switch_intercept;
}

static inline __u8 get_vec3_ferr_freeze_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.ferr_freeze_intercept;
}

static inline __u8 get_vec3_shutdown_events_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec3.shutdown_events_intercept;
}

static inline __u8 get_vec4_vmrun_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.vmrun_intercept;
}

static inline __u8 get_vec4_vmmcall_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.vmmcall_intercept;
}

static inline __u8 get_vec4_vmload_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.vmload_intercept;
}

static inline __u8 get_vec4_vmsave_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.vmsave_intercept;
}

static inline __u8 get_vec4_stgi_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.stgi_intercept;
}

static inline __u8 get_vec4_clgi_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.clgi_intercept;
}

static inline __u8 get_vec4_skinit_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.skinit_intercept;
}

static inline __u8 get_vec4_rdtscp_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.rdtscp_intercept;
}

static inline __u8 get_vec4_icebp_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.icebp_intercept;
}

static inline __u8 get_vec4_wbinvd_wbnoinvd_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.wbinvd_wbnoinvd_intercept;
}

static inline __u8 get_vec4_monitor_monitorx_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.monitor_monitorx_intercept;
}

static inline __u8 get_vec4_mwait_mwaitx_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.mwait_mwaitx_intercept;
}

static inline __u8 get_vec4_xsetbvrdpru_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.xsetbvrdpru_intercept;
}

static inline __u8 get_vec4_efer_wr_after_done_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.efer_wr_after_done_intercept;
}

static inline __u8 get_vec4_cr0_wr_after_done_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.cr0_wr_after_done_intercept;
}

static inline __u8 get_vec4_cr1_wr_after_done_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.cr1_wr_after_done_intercept;
}

static inline __u8 get_vec4_cr2_wr_after_done_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.cr2_wr_after_done_intercept;
}

static inline __u8 get_vec4_cr3_wr_after_done_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.cr3_wr_after_done_intercept;
}

static inline __u8 get_vec4_cr4_wr_after_done_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.cr4_wr_after_done_intercept;
}

static inline __u8 get_vec4_cr5_wr_after_done_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.cr5_wr_after_done_intercept;
}

static inline __u8 get_vec4_cr6_wr_after_done_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.cr6_wr_after_done_intercept;
}

static inline __u8 get_vec4_cr7_wr_after_done_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.cr7_wr_after_done_intercept;
}

static inline __u8 get_vec4_cr8_wr_after_done_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.cr8_wr_after_done_intercept;
}

static inline __u8 get_vec4_cr9_wr_after_done_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.cr9_wr_after_done_intercept;
}

static inline __u8 get_vec4_cr10_wr_after_done_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.cr10_wr_after_done_intercept;
}

static inline __u8 get_vec4_cr11_wr_after_done_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.cr11_wr_after_done_intercept;
}

static inline __u8 get_vec4_cr12_wr_after_done_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.cr12_wr_after_done_intercept;
}

static inline __u8 get_vec4_cr13_wr_after_done_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.cr13_wr_after_done_intercept;
}

static inline __u8 get_vec4_cr14_wr_after_done_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.cr14_wr_after_done_intercept;
}

static inline __u8 get_vec4_cr15_wr_after_done_intercept(struct hypersecure_vmcb_control *ctx) {
	return ctx->vec4.cr15_wr_after_done_intercept;
}

static inline __u64 get_tsc_offset(struct hypersecure_vmcb_control *ctx) {
	return ctx->tsc_offset;
}

static inline __u32 get_guest_asid(struct hypersecure_vmcb_control *ctx) {
	return ctx->guest_asid;
}

static inline __u8 get_tlb_control(struct hypersecure_vmcb_control *ctx) {
	return ctx->tlb_control;
}

static inline __u64 get_exitcode(struct hypersecure_vmcb_control *ctx) {
	return ctx->exitcode;
}

static inline __u64 get_exitinfo_v1(struct hypersecure_vmcb_control *ctx) {
	return ctx->exitinfo_v1;
}

static inline __u64 get_exitinfo_v2(struct hypersecure_vmcb_control *ctx) {
	return ctx->exitinfo_v2;
}

static inline __u64 get_exitintinfo(struct hypersecure_vmcb_control *ctx) {
	return ctx->exitintinfo;
}

static inline __u8 get_np_enable(struct hypersecure_vmcb_control *ctx) {
	return ctx->np_enable;
}

static inline __u64 get_ncr3(struct hypersecure_vmcb_control *ctx) {
	return ctx->ncr3;
}

static inline __u32 get_vmcb_clean(struct hypersecure_vmcb_control *ctx) {
	return ctx->vmcb_clean;
}

static inline __u64 get_nRIP(struct hypersecure_vmcb_control *ctx) {
	return ctx->nRIP;
}

static inline __u8 get_num_bytes_fetched(struct hypersecure_vmcb_control *ctx) {
	return ctx->num_bytes_fetched;
}

static inline __u64 get_bytes_fetched_low(struct hypersecure_vmcb_control *ctx) {
	return ctx->bytes_fetched_low;
}

static inline __u64 get_bytes_fetched_hi(struct hypersecure_vmcb_control *ctx) {
	return ctx->bytes_fetched_hi;
}

static inline __u16 get_vmsa_info_padding(struct hypersecure_vmcb_control *ctx) {
	return ctx->vmsa_info.padding;
}

static inline __u64 get_vmsa_info_vmsa_ptr(struct hypersecure_vmcb_control *ctx) {
	return ctx->vmsa_info.vmsa_ptr;
}

#endif
