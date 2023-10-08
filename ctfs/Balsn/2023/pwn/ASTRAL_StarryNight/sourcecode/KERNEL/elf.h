#ifndef __ELF_HEADER__
#define __ELF_HEADER__

#include <stdint.h>
#include <stdbool.h>
#include "const.h"
#include "memory.h"
#include "kernel.h"

#define EI_NIDENT 0x10

#define PT_LOAD 1
#define PF_W 2

typedef struct ELF64_EHDR {
  uint8_t e_ident[EI_NIDENT];
  uint16_t e_type;
  uint16_t e_machine;
  uint32_t e_version;
  uint64_t e_entry;
  uint64_t e_phoff;
  uint64_t e_shoff;
  uint32_t e_flags;
  uint16_t e_ehsize;
  uint16_t e_phentsize;
  uint16_t e_phnum;
  uint16_t e_shentsize;
  uint16_t e_shnum;
  uint16_t e_shstrndx;
} ELF64_EHDR;

typedef struct ELF64_PHDR {
  uint32_t p_type;
  uint32_t p_flags;
  uint64_t p_offset;
  uint64_t p_vaddr;
  uint64_t p_paddr;
  uint64_t p_filesz;
  uint64_t p_memsz;
  uint64_t p_align; 
} ELF64_PHDR;

uint64_t loadElf(uint64_t imageAddr, uint64_t vaddr, uint64_t *entry);
uint64_t initUserRuntime(uint64_t imageAddr, uint64_t vaddr, uint64_t userStack, uint64_t *entry);

#endif
