#ifndef __MAIN_HEADER__
#define __MAIN_HEADER__

#include <iostream>
#include <fcntl.h>
#include <sys/mman.h>
#include <syscall.h>
#include <unistd.h>
#include <unicorn/unicorn.h>

/* Stack */
#define SIZE_STACK ((uint64_t)0x1000)
#define ADDR_STACK ((uint64_t)(0x7ffffffff000 - SIZE_STACK))

/* Target code goes to virtual address 0x00000000 */
#define ADDR_CODE ((uint64_t)0x0)

/* Maximum size of target code is 4096 */
#define SIZE_CODE ((uint64_t)0x1000)

/* Human-friendly register names */
#define REG_RETVAL reg_vals[0]
#define REG_SYSNUM (reg_vals[0])
#define REG_ARG1   (reg_vals[1])
#define REG_ARG2   (reg_vals[2])
#define REG_ARG3   (reg_vals[3])
#define REG_ARG4   (reg_vals[4])
#define REG_ARG5   (reg_vals[5])
#define REG_ARG6   (reg_vals[6])

#define DEFINE_HANDLER(name)                                \
  void name(uc_engine *uc, uint32_t intno, void *user_data)

#define ADD_HANDLER(uh, type, handler, extra)                     \
  uc_hook_add(uc, &uh, type, (void*)handler, NULL, 1, 0, extra);

#define ABORT_PROGRAM(msg)                         \
  {                                                \
    std::cerr << "[-] " << msg << std::endl;       \
    uc_emu_stop(uc);                               \
    return;                                        \
  }

#define UNICORN_ERROR(stmt)                     \
  (stmt) != UC_ERR_OK

#define UNICORN_PROT(prot)                      \
  ((prot & PROT_READ ? UC_PROT_READ : 0)        \
   | (prot & PROT_WRITE ? UC_PROT_WRITE : 0)    \
   | (prot & PROT_EXEC ? UC_PROT_EXEC : 0))

#define ABORT(msg)                              \
  {                                             \
    std::cerr << "[-] " << msg << std::endl;    \
    uc_close(uc);                               \
    exit(1);                                    \
  }

#endif
