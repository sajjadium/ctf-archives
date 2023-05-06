#pragma once
#include <asm-generic/int-ll64.h>
#include <linux/list.h>
#include <linux/types.h>
#include <linux/hashtable.h>
#include <linux/hash.h>

#define HASH_MAP_BITS 9

// See Table 24-8. Format of Extended-Page-Table Pointer
typedef union _EPTP {
    __u64 all;
    struct {
        __u64 memoryType : 3; // bit 2:0 (0 = Uncacheable (UC) - 6 = Write - back(WB))
        __u64 pageWalkLength : 3; // bit 5:3 (This value is 1 less than the EPT page-walk length) 
        __u64 dirtyAndAceessEnabled : 1; // bit 6  (Setting this control to 1 enables accessed and dirty flags for EPT)
        __u64 reserved1 : 5; // bit 11:7 
        __u64 PML4Address : 36;
        __u64 reserved2 : 16;
    }fields;
}EPTP, *PEPTP;

typedef union _EPT_PML4E {
    __u64 all;
    struct {
        __u64 read : 1; // bit 0
        __u64 write : 1; // bit 1
        __u64 execute : 1; // bit 2
        __u64 reserved1 : 5; // bit 7:3 (Must be Zero)
        __u64 accessed : 1; // bit 8
        __u64 ignored1 : 1; // bit 9
        __u64 executeForUserMode : 1; // bit 10
        __u64 ignored2 : 1; // bit 11
        __u64 physicalAddress : 36; // bit (N-1):12 or Page-Frame-Number
        __u64 reserved2 : 4; // bit 51:N
        __u64 ignored3 : 12; // bit 63:52
    }fields;
}EPT_PML4E, *PEPT_PML4E;

typedef union _EPT_PDPTE {
    __u64 all;
    struct {
        __u64 read : 1; // bit 0
        __u64 write : 1; // bit 1
        __u64 execute : 1; // bit 2
        __u64 reserved1 : 5; // bit 7:3 (Must be Zero)
        __u64 accessed : 1; // bit 8
        __u64 ignored1 : 1; // bit 9
        __u64 executeForUserMode : 1; // bit 10
        __u64 ignored2 : 1; // bit 11
        __u64 physicalAddress : 36; // bit (N-1):12 or Page-Frame-Number
        __u64 reserved2 : 4; // bit 51:N
        __u64 ignored3 : 12; // bit 63:52
    }fields;
}EPT_PDPTE, *PEPT_PDPTE;

// See Table 28-5
typedef union _EPT_PDE {
    __u64 all;
    struct {
        __u64 read : 1; // bit 0
        __u64 write : 1; // bit 1
        __u64 execute : 1; // bit 2
        __u64 reserved1 : 5; // bit 7:3 (Must be Zero)
        __u64 accessed : 1; // bit 8
        __u64 ignored1 : 1; // bit 9
        __u64 executeForUserMode : 1; // bit 10
        __u64 ignored2 : 1; // bit 11
        __u64 physicalAddress : 36; // bit (N-1):12 or Page-Frame-Number
        __u64 reserved2 : 4; // bit 51:N
        __u64 ignored3 : 12; // bit 63:52
    }fields;
}EPT_PDE, *PEPT_PDE;

// See Table 28-6
typedef union _EPT_PTE {
    __u64 all;
    struct {
        __u64 read : 1; // bit 0
        __u64 write : 1; // bit 1
        __u64 execute : 1; // bit 2
        __u64 eptMemoryType : 3; // bit 5:3 (EPT Memory type)
        __u64 ignorePAT : 1; // bit 6
        __u64 ignored1 : 1; // bit 7
        __u64 accessedFlag : 1; // bit 8	
        __u64 dirtyFlag : 1; // bit 9
        __u64 executeForUserMode : 1; // bit 10
        __u64 ignored2 : 1; // bit 11
        __u64 physicalAddress : 36; // bit (N-1):12 or Page-Frame-Number
        __u64 reserved : 4; // bit 51:N
        __u64 ignored3 : 11; // bit 62:52
        __u64 suppressVE : 1; // bit 63
    }fields;
}EPT_PTE, *PEPT_PTE;

typedef struct mapping_t {
    struct hlist_node map;
    __u64 paddr;
    struct page *page;
} mapping_t;

typedef struct memory_t
{
    __u64 eptp[512];
    DECLARE_HASHTABLE(maps, HASH_MAP_BITS);
} memory_t;

memory_t *alloc_mem(void);
void destroy_mem(memory_t *mem);
mapping_t *handle_mmap_fault(memory_t *mem, __u64 paddr);
mapping_t *handle_ept_violation(memory_t *mem, __u64 paddr, __u64 eptp);
