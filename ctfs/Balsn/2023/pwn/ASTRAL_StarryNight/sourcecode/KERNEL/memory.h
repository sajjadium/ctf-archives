#ifndef __MEMORY_HEADER__
#define __MEMORY_HEADER__

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include "const.h"
#include "panic.h"
#include "hypercall.h"

//MEMORY
#define MEM_ALIGNED(val, alignment) (((val) & (alignment - 1)) == 0)

//NOTE: careful, must keep in sync with hypervisor
#define PHYS_SIZE 0x4000000
#define KERNEL_HEAP 0x25c000

#define USER_PAGE_MIN PHYS_SIZE
#define USER_PAGE_MAX PAGE_ADDR((1ULL << 47) - 1)
#define USER_MASK ((1ULL << 47) - 1)
#define KERN_PAGE_MIN 0xffff800000000000
#define KERN_PAGE_MAX 0xffffffffffffe000
#define IS_DIRECT_PHYS(vaddr) (((uint64_t)(vaddr)) < PHYS_SIZE)
#define IS_KERN_ADDR(vaddr) ((((uint64_t)(vaddr)) >> 47) == 0x1ffff)
#define IS_USER_ADDR(vaddr) (((((uint64_t)(vaddr)) >> 47) == 0x00000) && (!IS_DIRECT_PHYS(vaddr)))
#define IS_CANON_ADDR(vaddr) (IS_KERN_ADDR(vaddr) || IS_USER_ADDR(vaddr))

#define PDE64_PRESENT 0x01
#define PDE64_RW      0x02
#define PDE64_USER    0x04

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

#define PML4_OFFSET(vaddr) ((vaddr) & PML4_OFFSET_MASK)
#define PDP_OFFSET(vaddr) ((vaddr) & PDP_OFFSET_MASK)
#define PD_OFFSET(vaddr) ((vaddr) & PD_OFFSET_MASK)
#define PT_OFFSET(vaddr) ((vaddr) & PT_OFFSET_MASK)

#define PAGE_SHIFT PT_SHIFT
#define PAGE_SIZE (1 << PT_SHIFT)
#define PAGE_OFFSET_MASK (PAGE_SIZE - 1)
#define PAGE_MASK (~PAGE_OFFSET_MASK)
#define PAGE_OFFSET(vaddr) ((vaddr) & PAGE_OFFSET_MASK)
#define PAGE_ADDR(vaddr) ((vaddr) & PAGE_MASK)
#define PAGE_UPALIGN(vaddr) (((vaddr) + PAGE_OFFSET_MASK) & PAGE_MASK)
#define PAGE_ALIGNED(vaddr) (PAGE_OFFSET(vaddr) == 0)
#define PAGE_IDX(vaddr) ((vaddr) >> PAGE_SHIFT)
#define PAGE_CNT(size) ((size) >> PAGE_SHIFT)
#define PAGE_IDX2ADDR(idx) ((idx) << PAGE_SHIFT)
#define PAGE_CNT2SIZE(pageCnt) ((pageCnt) << PAGE_SHIFT)

#define CHECK_PERM(target, perm) (((target) & (perm)) == (perm))
#define ADD_OVERFLOW(a, b) (((a) + (b)) < (a))

//ALLOCATOR
#define NIL_CHUNK 0xffffffff

#define CHUNK_HEAD g_allocator.freeList
#define CHUNK_NEXT(idx) g_allocator.freeTable[idx].nextPageIdx
#define CHUNK_PAGECNT(idx) g_allocator.freeTable[idx].pageCnt

typedef struct ALLOCATOR_CHUNK_TABLE {
  uint32_t pageCnt;
  uint32_t nextPageIdx;
} ALLOCATOR_FREE_CHUNK_TABLE;

typedef struct ALLOCATOR {
  uint32_t remain;
  uint32_t freeList;
  ALLOCATOR_FREE_CHUNK_TABLE freeTable[PAGE_CNT(PHYS_SIZE)];
} ALLOCATOR;

extern ALLOCATOR g_allocator;

uint64_t getCr3();
void initPagetable();
void initAllocator();
void memcpy(uint64_t to, uint64_t from, uint64_t size);
void memset(uint64_t addr, uint8_t val, uint64_t size);
uint64_t memcmp(uint64_t m1, uint64_t m2, uint64_t size);
uint64_t getPhysAddr(uint64_t vaddr, uint64_t perm, uint64_t *physAddr);
void setPagePerm(uint64_t vaddr, uint64_t permAdd, uint64_t permDel);
void insertToPageTable(uint64_t vaddr, uint64_t physAddr);
void removeFromPageTable(uint64_t vaddr);
uint64_t allocatePhys(uint64_t size, uint64_t *res, uint64_t *remainSize);
void deallocatePhys(uint64_t paddr);
uint64_t searchFreeVrange(uint64_t startVaddr, uint64_t endVaddr, uint64_t size, bool upward, uint64_t *vaddrFound);
uint64_t allocateVrange(uint64_t vaddr, uint64_t size, bool isUser, bool isWritable);
uint64_t deallocateVrange(uint64_t vaddr, uint64_t size, bool isUser);
uint64_t changeVrangePerm(uint64_t vaddr, uint64_t size, uint64_t perm, bool isUser);
uint64_t checkVrange(uint64_t vaddr, uint64_t size, uint64_t perm);
uint64_t copyGeneral(uint64_t to, uint64_t from, uint64_t size, uint64_t toPerm, uint64_t fromPerm);
uint64_t copyFromUser(uint64_t to, uint64_t from, uint64_t size);
uint64_t copyToUser(uint64_t to, uint64_t from, uint64_t size);
uint64_t genUaslr();

#endif
