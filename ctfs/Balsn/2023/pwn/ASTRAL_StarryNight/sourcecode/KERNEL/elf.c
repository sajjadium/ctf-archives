#include "elf.h"

//This function trust provided elf and does not check whether it is malformed or not
//Also assumes no relocation are required, and directly calls main. Simplified for our specific use case here, most likely unusable elsewhere.
uint64_t loadElf(uint64_t imageAddr, uint64_t vaddr, uint64_t *entry) {
  ELF64_EHDR *ehdr = (ELF64_EHDR*)imageAddr;
  ELF64_PHDR *phdr = (ELF64_PHDR*)(imageAddr + ehdr->e_phoff);
  uint64_t maxLoad = 0;
  for (uint64_t i = 0; i < ehdr->e_phnum; i++) {
    if (phdr[i].p_type == PT_LOAD) {
      if (PAGE_UPALIGN(phdr[i].p_vaddr + phdr[i].p_memsz) > maxLoad) {
        maxLoad = PAGE_UPALIGN(phdr[i].p_vaddr + phdr[i].p_memsz);
      }
    }
  }
  vaddr -= maxLoad;
  for (uint64_t i = 0; i < ehdr->e_phnum; i++) {
    if (phdr[i].p_type == PT_LOAD) {
      if (allocateVrange(vaddr + PAGE_ADDR(phdr[i].p_vaddr), PAGE_UPALIGN(phdr[i].p_memsz + PAGE_OFFSET(phdr[i].p_vaddr)), true, true) == FAIL) return FAIL;
      memcpy(vaddr + phdr[i].p_vaddr, imageAddr + phdr[i].p_offset, phdr[i].p_filesz);
      if ((phdr[i].p_flags & PF_W) == 0) {
        changeVrangePerm(vaddr + PAGE_ADDR(phdr[i].p_vaddr), PAGE_UPALIGN(phdr[i].p_memsz + PAGE_OFFSET(phdr[i].p_vaddr)), PDE64_USER, true);
      }
    }
  }
  *entry = vaddr + ehdr->e_entry;
  return SUCCESS;
}

uint64_t initUserRuntime(uint64_t imageAddr, uint64_t vaddr, uint64_t userStack, uint64_t *entry) {
  if (loadElf(imageAddr, vaddr, entry) == FAIL) return FAIL;
  if (allocateVrange(userStack, USER_STACK_SIZE, true, true) == FAIL) return FAIL;
  return SUCCESS;
}
