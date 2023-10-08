#include "memory.h"

ALLOCATOR g_allocator;

uint64_t getCr3() {
  uint64_t cr3;
  asm("mov %%cr3, %[cr3];" : [cr3] "=r" (cr3));
  return cr3;
}

void initAllocator() {
  if (PAGE_CNT(PHYS_SIZE) >= UINT32_MAX) {
    panic("initAllocator : does not support total physical page count >= UINT32_MAX");
  }
  uint64_t start = KERNEL_HEAP;
  g_allocator.remain = PHYS_SIZE - start;
  CHUNK_HEAD = PAGE_IDX(start);
  CHUNK_PAGECNT(CHUNK_HEAD) = PAGE_CNT(g_allocator.remain);
  CHUNK_NEXT(CHUNK_HEAD) = NIL_CHUNK;
  return;
}

/* memory manipulation */
void memcpy(uint64_t to, uint64_t from, uint64_t size) {
  for(; size > 0; size--, to++, from++) {
    *((uint8_t*)to) = *((uint8_t*)from);
  }
  return;
}

void memset(uint64_t addr, uint8_t val, uint64_t size) {
  for(; size > 0; size--, addr++) {
    *((uint8_t*)addr) = val;
  }
  return;
}

uint64_t memcmp(uint64_t m1, uint64_t m2, uint64_t size) {
  for(; size > 0; size--, m1++, m2++) {
    if (*(uint8_t*)m1 != *(uint8_t*)m2) return FAIL;
  }
  return SUCCESS;
}

/* page table helpers */
//perm should be or between PDE64_RW, PDE64_USER, PDE64_PRESENT
uint64_t getPhysAddr(uint64_t vaddr, uint64_t perm, uint64_t *physAddr) {
  perm |= PDE64_PRESENT; //just in case
  if (!IS_CANON_ADDR(vaddr)) return FAIL;
  uint64_t pml4 = getCr3();
  uint64_t pdp = ((uint64_t*)PAGE_ADDR(pml4))[PML4_IDX(vaddr)];
  if (!CHECK_PERM(pdp, perm)) return FAIL;
  uint64_t pd = ((uint64_t*)PAGE_ADDR(pdp))[PDP_IDX(vaddr)];
  if (!CHECK_PERM(pd, perm)) return FAIL;
  uint64_t pt = ((uint64_t*)PAGE_ADDR(pd))[PD_IDX(vaddr)];
  if (!CHECK_PERM(pt, perm)) return FAIL;
  uint64_t page = ((uint64_t*)PAGE_ADDR(pt))[PT_IDX(vaddr)];
  if (!CHECK_PERM(page, perm)) return FAIL;
  if (physAddr != NULL) {
    *physAddr = PT_OFFSET(vaddr) | PT_ADDR(page);
  }
  return SUCCESS;
}

//sets the page permission as well as page table entries along the way
void setPagePerm(uint64_t vaddr, uint64_t permAdd, uint64_t permDel) {
  //does not check, trusts callers
  //insert / remove should not be handled here, so fix add / del perm just in case
  permAdd |= PDE64_PRESENT;
  permDel &= ~PDE64_PRESENT;
  uint64_t pml4 = getCr3();
  uint64_t pdp = ((uint64_t*)PAGE_ADDR(pml4))[PML4_IDX(vaddr)];
  uint64_t pd = ((uint64_t*)PAGE_ADDR(pdp))[PDP_IDX(vaddr)];
  uint64_t pt = ((uint64_t*)PAGE_ADDR(pd))[PD_IDX(vaddr)];
  //only need to modify pt in case of removing perms
  ((uint64_t*)PAGE_ADDR(pt))[PT_IDX(vaddr)] &= ~permDel;
  ((uint64_t*)PAGE_ADDR(pml4))[PML4_IDX(vaddr)] |= permAdd;
  ((uint64_t*)PAGE_ADDR(pdp))[PDP_IDX(vaddr)] |= permAdd;
  ((uint64_t*)PAGE_ADDR(pd))[PD_IDX(vaddr)] |= permAdd;
  ((uint64_t*)PAGE_ADDR(pt))[PT_IDX(vaddr)] |= permAdd;
  return;
}

//populate page table entries for vaddr
void insertToPageTable(uint64_t vaddr, uint64_t physAddr) {
  //does not check, trusts callers
  uint64_t tablePhysAddr, remainSize;
  uint64_t pml4 = getCr3();
  uint64_t pdp = ((uint64_t*)PAGE_ADDR(pml4))[PML4_IDX(vaddr)];
  if (!CHECK_PERM(pdp, PDE64_PRESENT)) {
    if (allocatePhys(PAGE_SIZE, &tablePhysAddr, &remainSize) == FAIL) panic("insertPageTable failed");
    ((uint64_t*)PAGE_ADDR(pml4))[PML4_IDX(vaddr)] = tablePhysAddr | PDE64_PRESENT;
    pdp = tablePhysAddr;
  }
  uint64_t pd = ((uint64_t*)PAGE_ADDR(pdp))[PDP_IDX(vaddr)];
  if (!CHECK_PERM(pd, PDE64_PRESENT)) {
    if (allocatePhys(PAGE_SIZE, &tablePhysAddr, &remainSize) == FAIL) panic("insertPageTable failed");
    ((uint64_t*)PAGE_ADDR(pdp))[PDP_IDX(vaddr)] = tablePhysAddr | PDE64_PRESENT;
    pd = tablePhysAddr;
  }
  uint64_t pt = ((uint64_t*)PAGE_ADDR(pd))[PD_IDX(vaddr)];
  if (!CHECK_PERM(pt, PDE64_PRESENT)) {
    if (allocatePhys(PAGE_SIZE, &tablePhysAddr, &remainSize) == FAIL) panic("insertPageTable failed");
    ((uint64_t*)PAGE_ADDR(pd))[PD_IDX(vaddr)] = tablePhysAddr | PDE64_PRESENT;
    pt = tablePhysAddr;
  }
  ((uint64_t*)PAGE_ADDR(pt))[PT_IDX(vaddr)] = physAddr | PDE64_PRESENT;
  return;
}


//remove page table entries
void removeFromPageTable(uint64_t vaddr) {
  //does not check, trusts callers
  //we do not attempt to recycle page table either way, so just mark pt entries
  uint64_t pml4 = getCr3();
  uint64_t pdp = ((uint64_t*)PAGE_ADDR(pml4))[PML4_IDX(vaddr)];
  uint64_t pd = ((uint64_t*)PAGE_ADDR(pdp))[PDP_IDX(vaddr)];
  uint64_t pt = ((uint64_t*)PAGE_ADDR(pd))[PD_IDX(vaddr)];
  ((uint64_t*)PAGE_ADDR(pt))[PT_IDX(vaddr)] = 0;
  return;
}

/* management */
//fetches physical address of allocated chunk, may not complete in one go, call until *remainSize is 0
uint64_t allocatePhys(uint64_t size, uint64_t *res, uint64_t *remainSize) {
  //caller must ensure size is reasonable, no checks done here
  uint32_t pageCnt = PAGE_CNT(size);
  uint32_t bestIdx = NIL_CHUNK;
  uint32_t bestPrevIdx = NIL_CHUNK;
  if (size > g_allocator.remain) return FAIL;
  for (uint32_t prevIdx = NIL_CHUNK, curIdx = CHUNK_HEAD; curIdx != NIL_CHUNK; prevIdx = curIdx, curIdx = CHUNK_NEXT(curIdx)) {
    if (CHUNK_PAGECNT(curIdx) >= pageCnt) {
      if (bestIdx == NIL_CHUNK || CHUNK_PAGECNT(bestIdx) < pageCnt || CHUNK_PAGECNT(bestIdx) > CHUNK_PAGECNT(curIdx)) {
        bestIdx = curIdx;
        bestPrevIdx = prevIdx;
      }
    } else if (bestIdx == NIL_CHUNK || CHUNK_PAGECNT(bestIdx) < CHUNK_PAGECNT(curIdx)) {
      bestIdx = curIdx;
      bestPrevIdx = prevIdx;
    }
  }
  if (bestIdx == NIL_CHUNK) return FAIL;
  if (CHUNK_PAGECNT(bestIdx) > pageCnt) {
    uint32_t remainIdx = bestIdx + pageCnt;
    CHUNK_NEXT(remainIdx) = CHUNK_NEXT(bestIdx);
    CHUNK_PAGECNT(remainIdx) = CHUNK_PAGECNT(bestIdx) - pageCnt;
    if (bestPrevIdx != NIL_CHUNK) {
      CHUNK_NEXT(bestPrevIdx) = remainIdx;
    } else {
      CHUNK_HEAD = remainIdx;
    }
    *remainSize = 0;
    *res = PAGE_IDX2ADDR(bestIdx);
  } else {
    if (bestPrevIdx != NIL_CHUNK) {
      CHUNK_NEXT(bestPrevIdx) = CHUNK_NEXT(bestIdx);
    } else {
      CHUNK_HEAD = CHUNK_NEXT(bestIdx);
    }
    *remainSize = size - PAGE_CNT2SIZE(CHUNK_PAGECNT(bestIdx));
    *res = PAGE_IDX2ADDR(bestIdx);
  }
  g_allocator.remain -= (size - *remainSize);
  return SUCCESS;
}

//inserts physical addr into free chunk list
void deallocatePhys(uint64_t paddr) {
  //caller must ensure paddr / size is reasonable, no checks done here
  uint32_t pageIdx = PAGE_IDX(paddr);
  CHUNK_NEXT(pageIdx) = CHUNK_HEAD;
  CHUNK_PAGECNT(pageIdx) = PAGE_CNT(PAGE_SIZE);
  CHUNK_HEAD = pageIdx;
  g_allocator.remain += PAGE_SIZE;
  return;
}

//search for range of virtual address that is free, size must be multiple of PAGE_SIZE
uint64_t searchFreeVrange(uint64_t startVaddr, uint64_t endVaddr, uint64_t size, bool upward, uint64_t *vaddrFound) {
  //does not check. trusts caller
  uint64_t delta = upward ? -PAGE_SIZE : PAGE_SIZE;
  if (upward) {
    if (startVaddr <= endVaddr) return FAIL;
    endVaddr += delta;
    startVaddr += delta;
  } else {
    if (startVaddr >= endVaddr) return FAIL;
  }
  for (uint64_t curVaddr = startVaddr; curVaddr != endVaddr;) {
    uint64_t remainSize;
    for (remainSize = size; remainSize > 0; remainSize -= PAGE_SIZE) {
      if (curVaddr == endVaddr) return FAIL;
      if (getPhysAddr(curVaddr, 0, NULL) == SUCCESS) {
        curVaddr += delta;
        break;
      }
      curVaddr += delta;
    }
    if (remainSize == 0) {
      *vaddrFound = curVaddr - delta;
      return SUCCESS;
    }
  }
  return FAIL;
}

uint64_t allocateVrange(uint64_t vaddr, uint64_t size, bool isUser, bool isWritable) {
  uint64_t newPerm = PDE64_RW | (isUser ? PDE64_USER : 0), remainSize, physAddr;
  if (!PAGE_ALIGNED(vaddr) || !PAGE_ALIGNED(size) || ADD_OVERFLOW(vaddr, size)) return FAIL;
  //ensure user / kernel memory can only be allocate in its respected virtual memory space
  if (isUser) {
    if (!IS_USER_ADDR(vaddr) || !IS_USER_ADDR(vaddr + size)) return FAIL;
  } else {
    if (!IS_KERN_ADDR(vaddr) || !IS_KERN_ADDR(vaddr + size)) return FAIL;
  }
  for (uint64_t curSize = size, curVaddr = vaddr; curSize > 0; curSize -= PAGE_SIZE, curVaddr += PAGE_SIZE) {
    //do not allow overwriting / partial allocations, don't care about perm here, since any form of overwriting is prohibited
    if (getPhysAddr(curVaddr, 0, NULL) == SUCCESS) return FAIL;
  }
  for (uint64_t curSize = size; curSize > 0; curSize = remainSize) {
    if (allocatePhys(curSize, &physAddr, &remainSize) == FAIL) panic("allocateVrange failed");
    for (uint64_t endVaddr = vaddr + curSize - remainSize, curVaddr = vaddr; curVaddr < endVaddr; curVaddr += PAGE_SIZE, physAddr += PAGE_SIZE) {
      insertToPageTable(curVaddr, physAddr);
      setPagePerm(curVaddr, newPerm, 0);
    }
    memset(vaddr, '\0', curSize - remainSize);
    if (!isWritable) {
      changeVrangePerm(vaddr, curSize - remainSize, newPerm ^ PDE64_RW, isUser);
    }
    vaddr += curSize - remainSize;
  }
  return SUCCESS;
}

uint64_t deallocateVrange(uint64_t vaddr, uint64_t size, bool isUser) {
  uint64_t reqPerm = isUser ? PDE64_USER : 0;
  if (!PAGE_ALIGNED(vaddr) || !PAGE_ALIGNED(size) || ADD_OVERFLOW(vaddr, size)) return FAIL;
  for (; size > 0; size -= PAGE_SIZE, vaddr += PAGE_SIZE) {
    //require page exists and has reqPerm
    uint64_t physAddr;
    if (getPhysAddr(vaddr, reqPerm, &physAddr) == FAIL) continue;
    deallocatePhys(physAddr);
    removeFromPageTable(vaddr);
  }
  return SUCCESS;
}

uint64_t changeVrangePerm(uint64_t vaddr, uint64_t size, uint64_t perm, bool isUser) {
  uint64_t reqPerm = isUser ? PDE64_USER : 0;
  uint64_t delPerm = 0;
  delPerm |= !(perm & PDE64_USER) ? PDE64_USER : 0;
  delPerm |= !(perm & PDE64_RW) ? PDE64_RW : 0;
  if (!PAGE_ALIGNED(vaddr) || !PAGE_ALIGNED(size) || ADD_OVERFLOW(vaddr, size)) return FAIL;
  for (; size > 0; size -= PAGE_SIZE, vaddr += PAGE_SIZE) {
    if (getPhysAddr(vaddr, reqPerm, NULL) == FAIL) continue;
    setPagePerm(vaddr, perm, delPerm);
  }
}

/* access */
uint64_t checkVrange(uint64_t vaddr, uint64_t size, uint64_t perm) {
  if (ADD_OVERFLOW(vaddr, size)) return FAIL;
  size += PAGE_OFFSET(vaddr);
  size = PAGE_UPALIGN(size);
  vaddr = PAGE_ADDR(vaddr);
  for (; size > 0; vaddr += PAGE_SIZE, size -= PAGE_SIZE) {
    if (getPhysAddr(vaddr, perm, NULL) == FAIL) return FAIL;
  }
  return SUCCESS;
}

uint64_t copyGeneral(uint64_t to, uint64_t from, uint64_t size, uint64_t toPerm, uint64_t fromPerm) {
  toPerm |= PDE64_RW; // just in case
  //We do not want partial copies, so traverse all pages here to check validity
  if (checkVrange(from, size, fromPerm) == FAIL || checkVrange(to, size, toPerm) == FAIL) return FAIL;
  memcpy(to, from, size);
  return SUCCESS;
}

uint64_t copyFromUser(uint64_t to, uint64_t from, uint64_t size) {
  if (copyGeneral(to, from, size, PDE64_RW, PDE64_USER) == FAIL) return FAIL;
  return SUCCESS;
}

uint64_t copyToUser(uint64_t to, uint64_t from, uint64_t size) {
  if (copyGeneral(to, from, size, PDE64_RW | PDE64_USER, 0) == FAIL) return FAIL;
  return SUCCESS;
}

uint64_t genUaslr() {
  uint64_t rand = 0;
  while (rand <= USER_PAGE_MIN) {
    hp_rand(&rand);
    rand = (rand << PD_SHIFT) & USER_MASK;
  }
  return rand;
}
