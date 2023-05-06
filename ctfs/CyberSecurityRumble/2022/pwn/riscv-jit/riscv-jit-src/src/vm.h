// Main structure and behavior of the VM

#pragma once

#include <stddef.h>
#include <stdint.h>
#include <stdnoreturn.h>
#include <stdbool.h>

// 64 kiB guest memory
#define VM_MEM_SIZE 0x10000

// Word-size of the guest
typedef uint32_t vm_word_t;

// Reason for a VM exit
typedef enum {
    // Jump to another code chunk
    VM_EXIT_JUMP,
    // Invalid memory access
    VM_EXIT_FAULT,
    // `ebreak` instruction
    VM_EXIT_EBREAK,
    // `ecall` instruction
    VM_EXIT_ECALL,
    // `fence.i` instruction
    VM_EXIT_FENCE_I,
} vm_exit_reason_t;

// Data returned from the VM when it exits
typedef struct {
    // Guest PC for re-entry
    vm_word_t reentry_pc;
    // Reason for the exit
    vm_exit_reason_t reason;
} vm_exit_t;

// State of the VM
typedef struct {
    // Guest registers. The first one will always be 0.
    vm_word_t regs[32];
    // Pointer to guest memory
    unsigned char *mem;
    // Size of guest memory
    size_t mem_size;
    // Guest program counter for re-entry. This field is not accessed by the generated code.
    vm_word_t reentry_pc;
} vm_state_t;

// Global VM state
extern vm_state_t vm_state;

// Whether we should log on VM entry and exit
extern bool vm_verbose;

// Initialize the VM state
void vm_init(void);

// Print the VM register state
void vm_print(void);

// Print a message, dump the VM state, and exit
noreturn void vm_error(const char *msg);

// Load an instruction word from the given VM address. Checks that `pc` is in bounds.
vm_word_t vm_load_instr(vm_word_t pc);

// Run the VM until a single VM exit
vm_exit_t vm_run(void);
