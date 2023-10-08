#include "hypervisor.h"

void initRegs(VM *vm, uint64_t entry, uint64_t kernelBaseAddr, uint64_t kernelStackAddr) {
  struct kvm_regs regs;
  if (ioctl(vm->vcpufd, KVM_GET_REGS, &regs) < 0) printError("initRegs::KVM_GET_REGS failed");
  regs.rip = entry;
  regs.rsp = kernelStackAddr + KERNEL_STACK_SIZE;
  regs.rdi = kernelBaseAddr;
  regs.rsi = USER_PADDR;
  regs.rdx = 0;
  regs.rflags = 0x2;
  if (ioctl(vm->vcpufd, KVM_SET_REGS, &regs) < 0) printError("initRegs::KVM_SET_REGS failed");
  return;
}

void insertToPageTable(VM *vm, uint64_t vaddr, uint64_t paddr, uint64_t size, uint64_t ptPaddrStart, bool writable, bool hugepage, bool ignoreAlignCheck) {
  //NOTE: ignoreAlignCheck is dangerous, and should generally be avoided, only introduced to allow easy kernel code mapping
  uint64_t pml4 = PT_PADDR;
  uint64_t pdp = ptPaddrStart;
  uint64_t pd = pdp + PAGE_SIZE;
  uint64_t pt;
  if (hugepage) {
    if (!ignoreAlignCheck) {
      if ((vaddr & (HUGE_PAGE_ALIGNMENT - 1)) != 0) printError("insertToPageTable::huge page vaddr not aligned");
    }
    if ((size & (HUGE_PAGE_SIZE - 1)) != 0) printError("insertToPageTable::huge page size not aligned");
    if ((paddr & (HUGE_PAGE_SIZE - 1)) != 0) printError("insertToPageTable::huge page paddr not aligned");
    if ((vaddr & (HUGE_PAGE_ALIGNMENT - 1)) + size > HUGE_PAGE_ALIGNMENT) printError("insertToPageTable::huge page size too large");
  } else {
    if (!ignoreAlignCheck) {
      if ((vaddr & (NORMAL_PAGE_ALIGNMENT - 1)) != 0) printError("insertToPageTable::normal page vaddr not aligned");
    }
    if ((size & (PAGE_SIZE - 1)) != 0) printError("insertToPageTable::normal page size not aligned");
    if ((paddr & (PAGE_SIZE - 1)) != 0) printError("insertToPageTable::normal page paddr not aligned");
    if ((vaddr & (NORMAL_PAGE_ALIGNMENT - 1)) + size > NORMAL_PAGE_ALIGNMENT) printError("insertToPageTable::normal page size too large");
    pt = pd + PAGE_SIZE;
  }
  if ((((uint64_t*)(vm->mem + pml4))[PML4_IDX(vaddr)] & PDE64_PRESENT) == PDE64_PRESENT) {
    pdp = PAGE_ADDR(((uint64_t*)(vm->mem + pml4))[PML4_IDX(vaddr)]);
  } else {
    ((uint64_t*)(vm->mem + pml4))[PML4_IDX(vaddr)] = pdp | PDE64_PRESENT;
  }
  ((uint64_t*)(vm->mem + pml4))[PML4_IDX(vaddr)] |= (writable ? PDE64_RW : 0);
  if ((((uint64_t*)(vm->mem + pdp))[PDP_IDX(vaddr)] & PDE64_PRESENT) == PDE64_PRESENT) {
    pd = PAGE_ADDR(((uint64_t*)(vm->mem + pdp))[PDP_IDX(vaddr)]);
  } else {
    ((uint64_t*)(vm->mem + pdp))[PDP_IDX(vaddr)] = pd | PDE64_PRESENT | (writable ? PDE64_RW : 0);
  }
  ((uint64_t*)(vm->mem + pdp))[PDP_IDX(vaddr)] |= (writable ? PDE64_RW : 0);
  if (hugepage) {
    for (uint64_t offset = 0; offset < size; offset += HUGE_PAGE_SIZE) {
      if ((((uint64_t*)(vm->mem + pd))[PD_IDX(vaddr + offset)] & PDE64_PRESENT) == PDE64_PRESENT) printError("insertToPageTable::insert huge page failed");
      ((uint64_t*)(vm->mem + pd))[PD_IDX(vaddr + offset)] = (paddr + offset) | PDE64_PRESENT | (writable ? PDE64_RW : 0) | PDE64_PS;
    }
  } else {
    if ((((uint64_t*)(vm->mem + pd))[PD_IDX(vaddr)] & PDE64_PS) == PDE64_PS) printError("insertToPageTable::insert page failed");
    if ((((uint64_t*)(vm->mem + pd))[PD_IDX(vaddr)] & PDE64_PRESENT) == PDE64_PRESENT) {
      pt = PAGE_ADDR(((uint64_t*)(vm->mem + pd))[PD_IDX(vaddr)]);
    } else {
      ((uint64_t*)(vm->mem + pd))[PD_IDX(vaddr)] = pt | PDE64_PRESENT | (writable ? PDE64_RW : 0);
    }
    ((uint64_t*)(vm->mem + pd))[PD_IDX(vaddr)] |= (writable ? PDE64_RW : 0);
    for (uint64_t offset = 0; offset < size; offset += PAGE_SIZE) {
      if ((((uint64_t*)(vm->mem + pt))[PT_IDX(vaddr + offset)] & PDE64_PRESENT) == PDE64_PRESENT) printError("insertToPageTable::insert page failed");
      ((uint64_t*)(vm->mem + pt))[PT_IDX(vaddr + offset)] = (paddr + offset) | PDE64_PRESENT | (writable ? PDE64_RW : 0);
    }
  }
  return;
}

//setup 4 mappings
//1. direct mapping for easy page table access
//2. kaslr memory usage
//3. kernel stack
//4. kernel interrupt stack
void initPageTable(VM *vm) {
  struct kvm_sregs sregs;
  if (ioctl(vm->vcpufd, KVM_GET_SREGS, &sregs) < 0) printError("initPageTable::KVM_GET_SREGS failed");
  //NOTE: image size should fit in a pd (0x40000000)
  insertToPageTable(vm, 0, 0, MEM_SIZE, DIRECT_MAP_PT_PADDR, true, true, false);
  sregs.cr3 = PT_PADDR;
  sregs.cr4 = CR4_PAE;
  sregs.cr4 |= CR4_OSFXSR | CR4_OSXMMEXCPT; /* enable SSE instruction */
  sregs.cr0 = CR0_PE | CR0_MP | CR0_ET | CR0_NE | CR0_WP | CR0_AM | CR0_PG;
  sregs.efer = EFER_LME | EFER_LMA;
  sregs.efer |= EFER_SCE; /* enable syscall instruction */
  if (ioctl(vm->vcpufd, KVM_SET_SREGS, &sregs) < 0) printError("initPageTable::KVM_SET_SREGS failed");
  return;
}

void loadKernel(VM *vm, uint8_t *imageAddr, int kernelSize, uint64_t kernelBaseAddr, uint64_t *entry, uint64_t *interruptEntry) {
  ELF64_EHDR *ehdr = (ELF64_EHDR*)imageAddr;
  ELF64_PHDR *phdr = (ELF64_PHDR*)(imageAddr + ehdr->e_phoff);
  ELF64_SHDR *shdr = (ELF64_SHDR*)(imageAddr + ehdr->e_shoff);
  ELF64_SYM *symtab = NULL;
  char *shstrtab = (char*)(imageAddr + shdr[ehdr->e_shstrndx].sh_offset);
  char *strtab = NULL;
  uint64_t symtabEntryCnt;
  uint64_t maxLoad = 0;
  for (uint64_t i = 0; i < ehdr->e_phnum; i++) {
    if (phdr[i].p_type == PT_LOAD) {
      if (PAGE_UPALIGN(phdr[i].p_vaddr + phdr[i].p_memsz) > maxLoad) {
        maxLoad = PAGE_UPALIGN(phdr[i].p_vaddr + phdr[i].p_memsz);
      }
    }
  }
  kernelBaseAddr -= maxLoad;
  for (uint64_t i = 0; i < ehdr->e_phnum; i++) {
    if (phdr[i].p_type == PT_LOAD) {
      if (phdr[i].p_offset + phdr[i].p_filesz > kernelSize) printError("loadKernel::invalid p_offset / p_filesz");
      if (PAGE_UPALIGN(phdr[i].p_vaddr + phdr[i].p_memsz) > KERNEL_SIZE) printError("loadKernel::kernel vsize limit exceeded");
      insertToPageTable(vm, kernelBaseAddr + PAGE_ADDR(phdr[i].p_vaddr), KERNEL_PADDR + PAGE_ADDR(phdr[i].p_vaddr), PAGE_UPALIGN(phdr[i].p_memsz + PAGE_OFFSET(phdr[i].p_vaddr)), KERNEL_PT_PADDR, (phdr[i].p_flags & PF_W) == PF_W, false, true);
      memcpy(vm->mem + KERNEL_PADDR + phdr[i].p_vaddr, imageAddr + phdr[i].p_offset, phdr[i].p_filesz);
    }
  }
  for (uint64_t i = 0; i < ehdr->e_shnum && (symtab == NULL || strtab == NULL); i++) {
    if (shdr[i].sh_type == SHT_SYMTAB && !strcmp(&shstrtab[shdr[i].sh_name], ".symtab")) {
      symtab = (ELF64_SYM*)(imageAddr + shdr[i].sh_offset);
      symtabEntryCnt = shdr[i].sh_size / sizeof(ELF64_SYM);
    } else if (shdr[i].sh_type == SHT_STRTAB && !strcmp(&shstrtab[shdr[i].sh_name], ".strtab")) {
      strtab = (char*)(imageAddr + shdr[i].sh_offset);
    }
  }
  for (uint64_t i = 0; i < symtabEntryCnt; i++) {
    if (!strcmp(&strtab[symtab[i].st_name], "_interruptStart")) {
      *interruptEntry = kernelBaseAddr + symtab[i].st_value;
      break;
    }
  }
  *entry = kernelBaseAddr + ehdr->e_entry;
  return;
}

void allocateKernelStack(VM *vm, uint64_t kernelStackAddr, uint64_t kernelInterruptStackAddr) {
  //NOTE: kernel stack size should fit in a pt (0x200000), and kernelStackAddr should be aligned by pt
  insertToPageTable(vm, kernelStackAddr, KERNEL_STACK_PADDR, KERNEL_STACK_SIZE, KERNEL_STACK_PT_PADDR, true, false, false);
  //NOTE: kernel stack size should fit in a pt (0x200000), and kernelInterruptStackAddr should be aligned by pt
  insertToPageTable(vm, kernelInterruptStackAddr, KERNEL_INTERRUPT_STACK_PADDR, KERNEL_STACK_SIZE, KERNEL_INTERRUPT_STACK_PT_PADDR, true, false, false);
}

void initSegRegs(VM *vm) {
  struct kvm_sregs sregs;
  if (ioctl(vm->vcpufd, KVM_GET_SREGS, &sregs) < 0) printError("initSegRegs::KVM_GET_SREGS failed");
  struct kvm_segment seg = {
    .base = 0,
    .limit = 0xffffffff,
    .selector = 1 << 3,
    .present = 1,
    .type = 0xb, //Code segment 
    .dpl = 0, //Kernel: level 0
    .db = 0,
    .s = 1,
    .l = 1, //long mode
    .g = 1
  };
  sregs.cs = seg;
  seg.type = 0x3; //Data segment 
  seg.selector = 2 << 3;
  sregs.ds = sregs.es = sregs.fs = sregs.gs = sregs.ss = seg;
  if (ioctl(vm->vcpufd, KVM_SET_SREGS, &sregs) < 0) printError("initSegRegs::KVM_SET_SREGS failed");
  return;
}

uint64_t initKernelRuntime(VM *vm, uint8_t *kernel, int kernelSize, uint64_t kernelBaseAddr, uint64_t kernelStackAddr, uint64_t kernelInterruptStackAddr) {
  uint64_t entry, interruptEntry;
  initPageTable(vm);
  loadKernel(vm, kernel, kernelSize, kernelBaseAddr, &entry, &interruptEntry);
  allocateKernelStack(vm, kernelStackAddr, kernelInterruptStackAddr);
  initSegRegs(vm);
  initRegs(vm, entry, kernelBaseAddr, kernelStackAddr);
  return interruptEntry;
}

VM *initKvm(uint8_t *kernel, int kernelSize, uint8_t *user, int userSize, uint64_t kernelBaseAddr, uint64_t kernelStackAddr, uint64_t kernelInterruptStackAddr, uint64_t *interruptEntry) {
  int kvmfd, vmfd, apiVer;
  uint64_t vcpu_mmap_size;
  struct kvm_userspace_memory_region region = {.slot = 0, .flags = 0, .guest_phys_addr = 0, .memory_size = MEM_SIZE, .userspace_addr = 0};
  struct kvm_run *run;
  VM *vm;
  if ((vm = malloc(sizeof(VM))) == NULL) printError("kvmInit::malloc failed");
  if ((kvmfd = open("/dev/kvm", O_RDWR | O_CLOEXEC)) < 0) printError("kvmInit::open failed");
  if ((apiVer = ioctl(kvmfd, KVM_GET_API_VERSION, 0)) < 0) printError("kvmInit::KVM_GET_API_VERSION failed");
  if (apiVer != KVM_API_VERSION) printError("kvmInit::incorrect api version");
  if ((vmfd = ioctl(kvmfd, KVM_CREATE_VM, 0)) < 0) printError("kvmInit::KVM_CREATE_VM failed");
  if ((region.userspace_addr = (uint64_t)mmap(0, MEM_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0)) == -1) printError("kvmInit::mmap failed");
  if (ioctl(vmfd, KVM_SET_USER_MEMORY_REGION, &region) < 0) printError("kvmInit::KVM_SET_USER_MEMORY_REGION failed");
  if ((vm->vcpufd = ioctl(vmfd, KVM_CREATE_VCPU, 0)) < 0) printError("kvmInit::KVM_CREATE_VCPU failed");
  if ((vcpu_mmap_size = ioctl(kvmfd, KVM_GET_VCPU_MMAP_SIZE, NULL)) < 0) printError("kvmInit::KVM_GET_VCPU_MMAP_SIZE");
  if ((vm->run = (struct kvm_run*) mmap(0, vcpu_mmap_size, PROT_READ | PROT_WRITE, MAP_SHARED, vm->vcpufd, 0)) == (void*)-1) printError("kvmInit::mmap failed");
  vm->mem = (void*)region.userspace_addr;
  vm->mem_size = MEM_SIZE;
  //copy code to memory
  memcpy(&(((char*)vm->mem)[USER_PADDR]), user, userSize);
  vm->withinInterrupt = false;
  //setup page table and registers + reallocate kernel
  *interruptEntry = initKernelRuntime(vm, kernel, kernelSize, kernelBaseAddr, kernelStackAddr, kernelInterruptStackAddr);
  close(kvmfd);
  return vm;
}

void setupBuffering() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
  return;
}

int loadFile(uint8_t *fname, uint8_t **data) {
  int size, fd = open(fname, O_RDONLY);
  if (fd < 0) printError("loadFile::open failed");
  if ((size = lseek(fd, 0, SEEK_END)) < 0) printError("loadFile::lseek failed");
  if (lseek(fd, 0, SEEK_SET) < 0) printError("loadFile::lseek failed");
  if ((*data = malloc(size)) == NULL) printError("loadFile::malloc failed");
  for (int cnt = 0, cursor = 0; cursor < size; cursor += cnt) {
    if ((cnt = read(fd, &((*data)[cursor]), size - cursor)) <= 0) printError("loadFile::read failed");
  }
  close(fd);
  return size;
}

void genKaslr(uint64_t *kernelBaseAddr, uint64_t *kernelStackAddr, uint64_t *kernelInterruptStackAddr) {
  int fd = open("/dev/urandom", O_RDONLY);
  if (fd < 0) printError("genKaslr::open failed");
  if (read(fd, kernelBaseAddr, sizeof(uint64_t)) != sizeof(uint64_t)) printError("genKaslr::read failed");
  *kernelBaseAddr |= 0xffff800000000000ULL;
  *kernelBaseAddr &= 0xffffffffffe00000ULL;
  do {
    if (read(fd, kernelStackAddr, sizeof(uint64_t)) != sizeof(uint64_t)) printError("genKaslr::read failed");
    *kernelStackAddr |= 0xffff800000000000ULL;
    *kernelStackAddr &= 0xffffffffffe00000ULL;
  } while(*kernelBaseAddr == *kernelStackAddr);
  do {
    if (read(fd, kernelInterruptStackAddr, sizeof(uint64_t)) != sizeof(uint64_t)) printError("genKaslr::read failed");
    *kernelInterruptStackAddr |= 0xffff800000000000ULL;
    *kernelInterruptStackAddr &= 0xffffffffffe00000ULL;
  } while(*kernelBaseAddr == *kernelInterruptStackAddr || *kernelStackAddr == *kernelInterruptStackAddr);
  if (*kernelBaseAddr > *kernelStackAddr) {
    *kernelBaseAddr ^= *kernelStackAddr;
    *kernelStackAddr ^= *kernelBaseAddr;
    *kernelBaseAddr ^= *kernelStackAddr;
  }
  if (*kernelBaseAddr > *kernelInterruptStackAddr) {
    *kernelBaseAddr ^= *kernelInterruptStackAddr;
    *kernelInterruptStackAddr ^= *kernelBaseAddr;
    *kernelBaseAddr ^= *kernelInterruptStackAddr;
  }
  if (*kernelStackAddr > *kernelInterruptStackAddr) {
    *kernelStackAddr ^= *kernelInterruptStackAddr;
    *kernelInterruptStackAddr ^= *kernelStackAddr;
    *kernelStackAddr ^= *kernelInterruptStackAddr;
  }
  close(fd);
  return;
}

bool checkIopl(VM *vm) {
  struct kvm_regs regs;
  struct kvm_sregs sregs;
  if(ioctl(vm->vcpufd, KVM_GET_REGS, &regs) < 0) printError("checkIopl::KVM_GET_REGS failed");
  if(ioctl(vm->vcpufd, KVM_GET_SREGS, &sregs) < 0) printError("checkIopl::KVM_GET_SREGS failed");
  return sregs.cs.dpl <= ((regs.rflags >> 12) & 3);
}

void execute(VM* vm, uint64_t interruptEntry, uint64_t kernelInterruptStackAddr) {
  uint32_t res;
  while(true) {
    ioctl(vm->vcpufd, KVM_RUN, NULL);
    switch (vm->run->exit_reason) {
      case KVM_EXIT_HLT:
        //NOTE: hlt is used to exit from execute, (needed for interrupt handling)
        return;
      case KVM_EXIT_IO:
        if(!checkIopl(vm)) printError("execute::KVM_EXIT_SHUTDOWN");
        uint64_t reason = vm->run->exit_reason;
        uint64_t port = vm->run->io.port;
        uint64_t direction = vm->run->io.direction;
        uint64_t data_offset = vm->run->io.data_offset;
        uint32_t argPaddr = *(uint32_t*)((uint8_t*)vm->run + vm->run->io.data_offset);
        vm->run->exit_reason = 0;
        injectInterrupt(vm, interruptEntry, kernelInterruptStackAddr);
        vm->run->exit_reason = reason;
        vm->run->io.port = port;
        vm->run->io.direction = direction;
        vm->run->io.data_offset = data_offset;
        *(uint32_t*)((uint8_t*)vm->run + vm->run->io.data_offset) = argPaddr;
        hp_handle(vm, &res);
        break;
      case KVM_EXIT_FAIL_ENTRY:
        printError("execute::KVM_EXIT_FAIL_ENTRY");
      case KVM_EXIT_INTERNAL_ERROR:
        printError("execute::KVM_EXIT_INTERNAL_ERROR");
      case KVM_EXIT_SHUTDOWN:
        printError("execute::KVM_EXIT_SHUTDOWN");
      default:
        printError("execute::Unhandled exit");
    }
  }
}

int main(int argc, char **argv, char **envp) {
  if(argc != 5) {
    printError("Usage: ./hypervisor [DEVICE] [KERNEL] [USER] [TIMEOUT]");
  }
  uint8_t *kernel, *user;
  uint64_t kernelBaseAddr, kernelStackAddr, kernelInterruptStackAddr, interruptEntry;
  int kernelSize, userSize;
  setupBuffering();
  kernelSize = loadFile(argv[2], &kernel);
  userSize = loadFile(argv[3], &user);
  if (userSize > USER_SIZE) printError("image size limit exceeded");
  genKaslr(&kernelBaseAddr, &kernelStackAddr, &kernelInterruptStackAddr);
  VM* vm = initKvm(kernel, kernelSize, user, userSize, kernelBaseAddr, kernelStackAddr, kernelInterruptStackAddr, &interruptEntry);
  free(kernel);
  free(user);
  launchDevice(argv[1], argv[4]);
  execute(vm, interruptEntry, kernelInterruptStackAddr);
  printError("kernel exited");
  return 0;
}
