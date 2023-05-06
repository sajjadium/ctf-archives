union __cr0_t
{
	__u64 control;
	struct
	{
		__u64 protection_enable : 1;
		__u64 monitor_coprocessor : 1;
		__u64 emulate_fpu : 1;
		__u64 task_switched : 1;
		__u64 extension_type : 1;
		__u64 numeric_error : 1;
		__u64 reserved_0 : 10;
		__u64 write_protection : 1;
		__u64 reserved_1 : 1;
		__u64 alignment_mask : 1;
		__u64 reserved_2 : 10;
		__u64 not_write_through : 1;
		__u64 cache_disable : 1;
		__u64 paging_enable : 1;
	} bits;
};


union __cr3_t
{
	__u64 control;
	struct
	{
		__u64 pcid : 12;
		__u64 page_frame_number : 36;
		__u64 reserved_0 : 12;
		__u64 reserved_1 : 3;
		__u64 pcid_invalidate : 1;
	} bits;
};




union __cr4_t
{
	__u64 control;
	struct
	{
		__u64 vme : 1;									 // bit 0
		__u64 pvi : 1;									 // bit 1
		__u64 time_stamp_disable : 1;					 // bit 2
		__u64 debug_extensions : 1;						 // bit 3
		__u64 page_size_extension : 1;					 // bit 4
		__u64 physical_address_extension : 1;			 // bit 5
		__u64 machine_check_enable : 1;					 // bit 6
		__u64 page_global_enable : 1;					 // bit 7
		__u64 perf_counter_enable : 1;					 // bit 8
		__u64 os_fxsave_support : 1;						 // bit 9
		__u64 os_xmm_exception_support : 1;				 // bit 10
		__u64 usermode_execution_prevention : 1;			 // bit 11
		__u64 reserved_0 : 1;							 // bit 12
		__u64 vmx_enable : 1;							 // bit 13
		__u64 smx_enable : 1;							 // bit 14
		__u64 reserved_1 : 1;							 // bit 15
		__u64 fs_gs_enable : 1;							 // bit 16
		__u64 pcide : 1;									 // bit 17
		__u64 os_xsave : 1;								 // bit 18
		__u64 reserved_2 : 1;							 // bit 19
		__u64 smep : 1;									 // bit 20
		__u64 smap : 1;									 // bit 21
		__u64 protection_key_enable : 1;					 // bit 22
	} bits;
};


union __cr8_t
{
	__u64 control;
	struct
	{
		__u64 task_priority_level : 4;
		__u64 reserved : 59;
	} bits;
};
