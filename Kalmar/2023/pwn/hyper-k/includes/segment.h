#pragma once
#include <asm-generic/int-ll64.h>

// Check Table 3-2 of 3-14 Vol 3A (Page 102)
#define SEGMENT_DESCRIPTOR_TYPE_TSS_AVAILABLE 9
#define SEGMENT_DESCRIPTOR_TYPE_TSS_BUSY 11

#pragma pack(push, 1)
struct __pseudo_descriptor_64_t
{
	__u16 limit;
	__u64 base_address;
};
#pragma pack(pop)

struct __segment_descriptor_64_t
{
	__u16 segment_limit_low;
	__u16 base_low;
	union
	{
		struct
		{
			__u32 base_middle                                           : 8;
			__u32 type                                                  : 4;
			__u32 descriptor_type                                       : 1;
			__u32 dpl                                                   : 2;
			__u32 present                                               : 1;
			__u32 segment_limit_high                                    : 4;
			__u32 system                                                : 1;
			__u32 long_mode                                             : 1;
			__u32 default_big                                           : 1;
			__u32 granularity                                           : 1;
			__u32 base_high                                             : 8;
		};

		__u32 flags;
	} ;
	__u32 base_upper;
	__u32 reserved;
};

struct __segment_descriptor_32_t
{
	__u16 segment_limit_low;
	__u16 base_low;
	union
	{
		struct
		{
			__u32 base_middle                                           : 8;
			__u32 type                                                  : 4;
			__u32 descriptor_type                                       : 1;
			__u32 dpl                                                   : 2;
			__u32 present                                               : 1;
			__u32 segment_limit_high                                    : 4;
			__u32 system                                                : 1;
			__u32 long_mode                                             : 1;
			__u32 default_big                                           : 1;
			__u32 granularity                                           : 1;
			__u32 base_high                                             : 8;
		};

		__u32 flags;
	};
};

union __segment_selector_t
{
	struct
	{
		__u16 rpl                                   : 2;
		__u16 table                                 : 1;
		__u16 index                                 : 13;
	};

	__u16 flags;
};

union __segment_access_rights_t
{
	struct
	{
		__u32 type                                                    : 4;  // 0 - 3
		__u32 descriptor_type                                         : 1;  // 4S
		__u32 dpl                                                     : 2;  // 5 - 6
		__u32 present                                                 : 1;  // 7
		__u32 reserved0                                               : 4;  // 8 - 11
		__u32 available                                               : 1;  // 12
		__u32 long_mode                                               : 1;  // 13
		__u32 default_big                                             : 1;  // 14
		__u32 granularity                                             : 1;  // 15
		__u32 unusable                                                : 1;  // 17
		__u32 reserved1                                               : 15; // 18 - 31
	};

	__u32 flags;
};
