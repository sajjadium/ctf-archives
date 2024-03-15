

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

union __vmx_exception_bitmap_t
{
	__u64 control;
	struct
	{
		__u64 excep0 : 1;
		__u64 excep1 : 1;
		__u64 excep2 : 1;
		__u64 excep3 : 1;
		__u64 excep4 : 1;
		__u64 excep5 : 1;
		__u64 excep6 : 1;
		__u64 excep7 : 1;
		__u64 excep8 : 1;
		__u64 excep9 : 1;
		__u64 excep10 : 1;
		__u64 excep11 : 1;
		__u64 excep12 : 1;
		__u64 excep13 : 1;
		__u64 excep14 : 1;
		__u64 excep15 : 1;
		__u64 excep16 : 1;
		__u64 excep17 : 1;
		__u64 excep18 : 1;
		__u64 excep19 : 1;
		__u64 excep20 : 1;
		__u64 excep21 : 1;
		__u64 excep22 : 1;
		__u64 excep23 : 1;
		__u64 excep24 : 1;
		__u64 excep25 : 1;
		__u64 excep26 : 1;
		__u64 excep27 : 1;
		__u64 excep28 : 1;
		__u64 excep29 : 1;
		__u64 excep30 : 1;
		__u64 excep31 : 1;
	} bits;
};

union __vmx_general_bits_t
{
	__u64 control;
	struct
	{
		__u64 bit0 : 1;
		__u64 bit1 : 1;
		__u64 bit2 : 1;
		__u64 bit3 : 1;
		__u64 bit4 : 1;
		__u64 bit5 : 1;
		__u64 bit6 : 1;
		__u64 bit7 : 1;
		__u64 bit8 : 1;
		__u64 bit9 : 1;
		__u64 bit10 : 1;
		__u64 bit11 : 1;
		__u64 bit12 : 1;
		__u64 bit13 : 1;
		__u64 bit14 : 1;
		__u64 bit15 : 1;
		__u64 bit16 : 1;
		__u64 bit17 : 1;
		__u64 bit18 : 1;
		__u64 bit19 : 1;
		__u64 bit20 : 1;
		__u64 bit21 : 1;
		__u64 bit22 : 1;
		__u64 bit23 : 1;
		__u64 bit24 : 1;
		__u64 bit25 : 1;
		__u64 bit26 : 1;
		__u64 bit27 : 1;
		__u64 bit28 : 1;
		__u64 bit29 : 1;
		__u64 bit30 : 1;
		__u64 bit31 : 1;
		__u64 bit32 : 1;
		__u64 bit33 : 1;
		__u64 bit34 : 1;
		__u64 bit35 : 1;
		__u64 bit36 : 1;
		__u64 bit37 : 1;
		__u64 bit38 : 1;
		__u64 bit39 : 1;
		__u64 bit40 : 1;
		__u64 bit41 : 1;
		__u64 bit42 : 1;
		__u64 bit43 : 1;
		__u64 bit44 : 1;
		__u64 bit45 : 1;
		__u64 bit46 : 1;
		__u64 bit47 : 1;
		__u64 bit48 : 1;
		__u64 bit49 : 1;
		__u64 bit50 : 1;
		__u64 bit51 : 1;
		__u64 bit52 : 1;
		__u64 bit53 : 1;
		__u64 bit54 : 1;
		__u64 bit55 : 1;
		__u64 bit56 : 1;
		__u64 bit57 : 1;
		__u64 bit58 : 1;
		__u64 bit59 : 1;
		__u64 bit60 : 1;
		__u64 bit61 : 1;
		__u64 bit62 : 1;
		__u64 bit63 : 1;
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

