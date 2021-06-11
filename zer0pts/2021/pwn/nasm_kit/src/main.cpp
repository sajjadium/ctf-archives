#include "main.hpp"

/* Registers we are interested in */
const int syscall_abi[] = {
  UC_X86_REG_RAX,
  UC_X86_REG_RDI, UC_X86_REG_RSI, UC_X86_REG_RDX,
  UC_X86_REG_R10, UC_X86_REG_R8, UC_X86_REG_R9
};
uint64_t reg_vals[7];
void *reg_ptrs[7];

/**
 * Interruption Handler
 */
DEFINE_HANDLER(handler_interrupt)
{
  ABORT_PROGRAM("Cannot handle interruption (" << intno << ")");
}

/**
 * Memory Fault Handler
 */
DEFINE_HANDLER(handler_segv)
{
  ABORT_PROGRAM("Segmentation Fault");
}

/**
 * System Call Handler
 */
DEFINE_HANDLER(handler_syscall)
{
  char *buf;

  /* Read register values */
  if (UNICORN_ERROR(uc_reg_read_batch(uc, (int*)syscall_abi, reg_ptrs, 7)))
    ABORT_PROGRAM("Error on uc_reg_read_batch");

  /* Only allow read, write, mmap, munmap, exit and exit_group */
  switch(REG_SYSNUM) {
  case SYS_read:
    /** SYS_read */
    buf = new char[REG_ARG3]();

    /* Put data into temporary buffer */
    if (syscall(SYS_read, REG_ARG1, buf, REG_ARG3) < 0)
      REG_RETVAL = -1;
    else
      REG_RETVAL = 0;

    /* Copy data from temporary buffer to memory */
    if (UNICORN_ERROR(uc_mem_write(uc, REG_ARG2, buf, REG_ARG3))) {
      delete buf;
      ABORT_PROGRAM("Error on uc_mem_write");
    }

    delete buf;
    break;

  case SYS_write:
    /** SYS_write */
    buf = new char[REG_ARG3]();

    /* Read data from memory */
    if (UNICORN_ERROR(uc_mem_read(uc, REG_ARG2, buf, REG_ARG3))) {
      delete buf;
      ABORT_PROGRAM("Error on uc_mem_read");
    }

    /* Write to actual fd */
    if (syscall(SYS_write, REG_ARG1, buf, REG_ARG3) < 0)
      reg_vals[0] = -1;
    else
      reg_vals[0] = 0;

    delete buf;
    break;

  case SYS_mmap:
    /** SYS_mmap */
    REG_RETVAL = syscall(SYS_mmap, REG_ARG1, REG_ARG2, REG_ARG3, REG_ARG4, REG_ARG5, REG_ARG6);

    if ((void*)REG_RETVAL == MAP_FAILED) {

      /* Failed to allocate*/
      REG_RETVAL = -1;

    } else if (REG_RETVAL != REG_ARG1) {

      /* Invalid address */
      syscall(SYS_munmap, REG_RETVAL, REG_ARG2);
      REG_RETVAL = -1;

    } else {

      /* Success */
      if (UNICORN_ERROR(uc_mem_map_ptr(uc, REG_RETVAL, REG_ARG2, UNICORN_PROT(REG_ARG3), (void*)REG_RETVAL)))
        ABORT_PROGRAM("Error on uc_mem_map_ptr");

      REG_RETVAL = 0;

    }
    break;

  case SYS_munmap:
    /** SYS_munmap */
    if (syscall(SYS_munmap, REG_ARG1, REG_ARG2) != 0) {
      REG_RETVAL = -1;
    } else {
      if (UNICORN_ERROR(uc_mem_unmap(uc, REG_ARG1, REG_ARG2))) {
        ABORT_PROGRAM("Error on uc_mem_unmap");
      }
      REG_RETVAL = 0;
    }
    break;

  case SYS_exit:
  case SYS_exit_group:
    /* SYS_exit, SYS_exit_group */
    uc_emu_stop(uc);
    break;

  default:
    ABORT_PROGRAM("Unsupported system call (" << REG_SYSNUM << ")");
  }

  /* Update register values */
  if (UNICORN_ERROR(uc_reg_write_batch(uc, (int*)syscall_abi, reg_ptrs, 7))) {
    ABORT_PROGRAM("Error on uc_reg_write_batch");
  }
}

int main(int argc, char **argv)
{
  if (argc < 2) {
    std::cout << "Usage: " << argv[0] << " <code.bin>" << std::endl;
    return 1;
  }

  /* Read target program */
  int fd = open(argv[1], O_RDONLY);
  if (fd == -1) {
    std::cerr << "File not found" << std::endl;
    return 1;
  }
  char *code = new char[SIZE_CODE]();
  read(fd, code, SIZE_CODE);
  close(fd);

  /* Create new unicorn instance */
  uc_engine *uc;
  if (UNICORN_ERROR(uc_open(UC_ARCH_X86, UC_MODE_64, &uc)))
    ABORT("Error on uc_mem_map (unexpected)");

  /* Allocate code region and copy machine code */
  if (UNICORN_ERROR(uc_mem_map(uc, ADDR_CODE, SIZE_CODE, UC_PROT_READ|UC_PROT_EXEC)))
    ABORT("Error on uc_mem_map (unexpected)");
  if (UNICORN_ERROR(uc_mem_write(uc, ADDR_CODE, code, SIZE_CODE)))
    ABORT("Error on uc_mem_write (unexpected)");

  /* Allocate stack region */
  if (UNICORN_ERROR(uc_mem_map(uc, ADDR_STACK, SIZE_STACK, UC_PROT_READ|UC_PROT_WRITE)))
    ABORT("Error on uc_mem_map (unexpected)");

  /* Add handlers */
  uc_hook uh_syscall, uh_trap, uh_segv;
  ADD_HANDLER(uh_syscall, UC_HOOK_INSN, handler_syscall, UC_X86_INS_SYSCALL);
  ADD_HANDLER(uh_trap, UC_HOOK_INTR, handler_interrupt, 0);
  ADD_HANDLER(uh_segv, UC_HOOK_MEM_INVALID, handler_segv, 0);

  /* Go! */
  std::cout << "[+] Starting emulation" << std::endl;
  uint64_t rsp = ADDR_STACK + SIZE_STACK;
  uc_reg_write(uc, UC_X86_REG_RSP, &rsp);
  uc_emu_start(uc, ADDR_CODE, ADDR_CODE + SIZE_CODE, 0, 0);
  std::cout << "[+] Emulator terminated" << std::endl;

  /* Print register values */
  if (UNICORN_ERROR(uc_reg_read_batch(uc, (int*)syscall_abi, reg_ptrs, 7)))
    ABORT("Error on uc_mem_map (unexpected)");
  
  std::cout << "===== registers =====" << std::endl;
  std::cout << "RAX: " << std::hex << reg_vals[0] << std::endl;
  std::cout << "RDI: " << std::hex << reg_vals[1] << std::endl;
  std::cout << "RSI: " << std::hex << reg_vals[2] << std::endl;
  std::cout << "RDX: " << std::hex << reg_vals[3] << std::endl;
  std::cout << "R10: " << std::hex << reg_vals[4] << std::endl;
  std::cout << "R8 : " << std::hex << reg_vals[5] << std::endl;
  std::cout << "R9 : " << std::hex << reg_vals[6] << std::endl;
  std::cout << "=====================" << std::endl;

  uc_close(uc);
  delete code;
  return 0;
}

/* Initialize */
__attribute__((constructor))
void setup() {
  alarm(60);
  for(int i = 0; i < 7; i++) {
    reg_ptrs[i] = &reg_vals[i];
  }
}
