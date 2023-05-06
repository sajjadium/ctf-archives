// Emit x86 machine code into the global code buffer. Provides different operations that consist of
// several assembly instructions each. `rdi` always points to the global VM state. `rsi` is used as
// a scratch register to transfer information between subsequent operations, called "temporary".
// `rdx` is used to transfer addresses for memory accesses. `rcx` is used as a second operand for
// some operations. Operations that need additional internal scratch registers use `r8` and `r9`.

#pragma once

#include "vm.h"

#include <stddef.h>

// An arithmetic or logical operation
typedef enum {
    // Addition
    EMIT_OP_ADD,
    // Subtraction
    EMIT_OP_SUB,
    // Logical and
    EMIT_OP_AND,
    // Logical or
    EMIT_OP_OR,
    // Logical exclusive or
    EMIT_OP_XOR,
    // Shift left logical
    EMIT_OP_SLL,
    // Shift right logical
    EMIT_OP_SRL,
    // Shift right arithmetic
    EMIT_OP_SRA,
    // Set if less than, signed
    EMIT_OP_SLT,
    // Set if less than, unsigned
    EMIT_OP_SLTU,
} emit_op_t;

// A comparison operation
typedef enum {
    // Equal
    EMIT_CMP_EQ,
    // Not equal
    EMIT_CMP_NE,
    // Less than, signed
    EMIT_CMP_LT,
    // Greater than, signed
    EMIT_CMP_GE,
    // Less than, unsigned
    EMIT_CMP_LTU,
    // Greater than, unsigned
    EMIT_CMP_GEU,
} emit_cmp_t;

// Width of a memory access
typedef enum {
    // Word access (32-bit)
    EMIT_WIDTH_WORD,
    // Halfword access (16-bit)
    EMIT_WIDTH_HALFWORD,
    // Byte access (8-bit)
    EMIT_WIDTH_BYTE,
} emit_width_t;

// Emit: Load an immediate into the temporary
void emit_load_imm(vm_word_t imm);

// Emit: Load a VM register into the temporary
void emit_load_reg(size_t reg);

// Emit: Save the temporary into a VM register. Stores to register 0 don't emit any code.
void emit_store_reg(size_t reg);

// Emit: Use the value of the temporary as second operand
void emit_set_operand(void);

// Emit: Put the value of the second operand into the temporary
void emit_get_operand(void);

// Emit: Perform an operation on the temporary and the second operand, store the result in the
// temporary
void emit_op(emit_op_t op);

// Emit: Compare the temporary with the second operand. If true, perform a VM exit with `pc_true` as
// re-entry PC. Else, perform a VM exit with `pc_false` as re-entry PC.
void emit_exit_cmp(emit_cmp_t cmp, vm_exit_reason_t reason, vm_word_t pc_true, vm_word_t pc_false);

// Emit: Perform a VM exit, use the temporary as re-entry PC
void emit_exit(vm_exit_reason_t reason);

// Emit: Use the temporary as guest memory address and validate that it is in bounds. Perform VM
// exit if the address is not in bounds.
void emit_mem_addr(void);

// Emit: Perform memory load operation from guest memory address and store zero-extended result in
// the temporary
void emit_mem_load(emit_width_t width);

// Emit: Perform memory store operation to guest memory address, store value of the temporary
void emit_mem_store(emit_width_t width);

// Emit: Sign-extend the temporary from the given width
void emit_ext(emit_width_t width);
