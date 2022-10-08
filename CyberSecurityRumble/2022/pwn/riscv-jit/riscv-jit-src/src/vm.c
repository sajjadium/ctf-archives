#include "vm.h"

#include "codebuf.h"
#include "jit.h"

#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>

vm_state_t vm_state;

bool vm_verbose;

void vm_init(void) {
    // Allocate guest memory
    vm_state.mem =
            mmap(NULL, VM_MEM_SIZE, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
    if (vm_state.mem == MAP_FAILED)
        vm_error("Failed to allocate guest memory");

    vm_state.mem_size = VM_MEM_SIZE;
}

void vm_print(void) {
    printf("VM state:  re-entry PC: 0x%x\n"
           "    x0:  0x%08x, x1:  0x%08x, x2:  0x%08x, x3:  0x%08x, x4:  0x%08x, x5:  0x%08x, x6:  "
           "0x%08x, x7:  0x%08x\n"
           "    x8:  0x%08x, x9:  0x%08x, x10: 0x%08x, x11: 0x%08x, x12: 0x%08x, x13: 0x%08x, x14: "
           "0x%08x, x15: 0x%08x\n"
           "    x16: 0x%08x, x17: 0x%08x, x18: 0x%08x, x19: 0x%08x, x20: 0x%08x, x21: 0x%08x, x22: "
           "0x%08x, x23: 0x%08x\n"
           "    x24: 0x%08x, x25: 0x%08x, x26: 0x%08x, x27: 0x%08x, x28: 0x%08x, x29: 0x%08x, x30: "
           "0x%08x, x31: 0x%08x\n",
            vm_state.reentry_pc,
            vm_state.regs[0],
            vm_state.regs[1],
            vm_state.regs[2],
            vm_state.regs[3],
            vm_state.regs[4],
            vm_state.regs[5],
            vm_state.regs[6],
            vm_state.regs[7],
            vm_state.regs[8],
            vm_state.regs[9],
            vm_state.regs[10],
            vm_state.regs[11],
            vm_state.regs[12],
            vm_state.regs[13],
            vm_state.regs[14],
            vm_state.regs[15],
            vm_state.regs[16],
            vm_state.regs[17],
            vm_state.regs[18],
            vm_state.regs[19],
            vm_state.regs[20],
            vm_state.regs[21],
            vm_state.regs[22],
            vm_state.regs[23],
            vm_state.regs[24],
            vm_state.regs[25],
            vm_state.regs[26],
            vm_state.regs[27],
            vm_state.regs[28],
            vm_state.regs[29],
            vm_state.regs[30],
            vm_state.regs[31]);
}

noreturn void vm_error(const char *msg) {
    printf("ERROR: %s\n", msg);
    vm_print();
    exit(EXIT_FAILURE);
}

vm_word_t vm_load_instr(vm_word_t pc) {
    // Check that whole access is inside of guest memory
    if (pc >= vm_state.mem_size || pc + 4 >= vm_state.mem_size)
        vm_error("PC out of bounds");

    // Load instruction word
    vm_word_t w;
    memcpy(&w, vm_state.mem + pc, sizeof w);
    return w;
}

vm_exit_t vm_run() {
    vm_word_t pc = vm_state.reentry_pc;

    // Get chunk for re-entry PC
    codebuf_chunk_t chunk = codebuf_get_chunk(pc);
    // If the chunk is not yet JITed, do it now
    if (!chunk)
        chunk = jit_compile(pc);

    if (vm_verbose)
        printf("VM enter at PC 0x%x\n", pc);

    // Enter the VM
    vm_exit_t exit = chunk(&vm_state);
    // Update our re-entry PC
    vm_state.reentry_pc = exit.reentry_pc;

    if (vm_verbose) {
        printf("VM exit with reason 0x%x\n", exit.reason);
        vm_print();
    }
    return exit;
}
