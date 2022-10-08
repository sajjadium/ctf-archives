#include "jit.h"

#include "codebuf.h"
#include "emit.h"

#include <stdbool.h>
#include <stdio.h>

// Extract a sequence of bits from the given word
static vm_word_t bits(vm_word_t word, size_t start, size_t len) {
    return (word >> start) & (((vm_word_t)1 << len) - 1);
}

// Sign-extend the given value with the sign bit taken from the given bit index
static vm_word_t ext(vm_word_t word, size_t bit) {
    if (word & ((vm_word_t)1 << bit))
        word |= (vm_word_t)-1 << bit;
    return word;
}

// Decode `I`-type immediate
static vm_word_t imm_i(vm_word_t instr) {
    vm_word_t imm = bits(instr, 20, 12);
    return ext(imm, 11);
}

// Decode `S`-type immediate
static vm_word_t imm_s(vm_word_t instr) {
    // Extract both parts
    vm_word_t p1 = bits(instr, 7, 5);
    vm_word_t p2 = bits(instr, 25, 7);
    // Put them together
    vm_word_t imm = p1 | (p2 << 5);
    // Sign-extend
    return ext(imm, 11);
}

// Decode `B`-type immediate
static vm_word_t imm_b(vm_word_t instr) {
    vm_word_t imm = imm_s(instr);
    // Put bit 0 at index 11
    imm = (imm & ~(((vm_word_t)1 << 11) | 1)) | ((imm & 1) << 11);
    return imm;
}

// Decode `U`-type immediate
static vm_word_t imm_u(vm_word_t instr) {
    vm_word_t imm = bits(instr, 12, 20);
    return imm << 12;
}

// Decode `J`-type immediate
static vm_word_t imm_j(vm_word_t instr) {
    // Extract parts
    vm_word_t p1 = bits(instr, 21, 10);
    vm_word_t p2 = bits(instr, 20, 1);
    vm_word_t p3 = bits(instr, 12, 8);
    vm_word_t p4 = bits(instr, 31, 1);
    // Put them together
    vm_word_t imm = (p1 << 1) | (p2 << 11) | (p3 << 12) | (p4 << 20);
    // Sign-extend
    return ext(imm, 20);
}

// Decode ALU operation
static emit_op_t alu_op(vm_word_t funct3, vm_word_t funct7, bool has_imm) {
    // Decode according to `funct3`
    emit_op_t op;
    switch (funct3) {
        case 0b000:
            op = EMIT_OP_ADD;
            break;
        case 0b001:
            op = EMIT_OP_SLL;
            break;
        case 0b010:
            op = EMIT_OP_SLT;
            break;
        case 0b011:
            op = EMIT_OP_SLTU;
            break;
        case 0b100:
            op = EMIT_OP_XOR;
            break;
        case 0b101:
            op = EMIT_OP_SRL;
            break;
        case 0b110:
            op = EMIT_OP_OR;
            break;
        case 0b111:
            op = EMIT_OP_AND;
            break;
        default:
            vm_error("Invalid ALU instruction");
    }

    // Check `funct7` if it is not part of the immediate
    if (!has_imm || op == EMIT_OP_SLL || op == EMIT_OP_SRL) {
        if (op == EMIT_OP_ADD && funct7 == 0b0100000) {
            // This add is actually a sub
            op = EMIT_OP_SUB;
        } else if (op == EMIT_OP_SRL && funct7 == 0b0100000) {
            // This shift right logical is actually a shift right arithmetic
            op = EMIT_OP_SRA;
        } else if (funct7 != 0b0000000) {
            vm_error("Invalid ALU instruction: funct7");
        }
    }

    return op;
}

codebuf_chunk_t jit_compile(vm_word_t pc) {
    // Tell the code buffer that we start emitting a new chunk
    codebuf_chunk_t chunk = codebuf_register_chunk(pc);
    if (vm_verbose)
        printf("Compiling code at PC 0x%x to chunk at %p\n", pc, chunk);

    // Iterate over all following instructions
    for (;; pc += 4) {
        // Get the current instruction
        vm_word_t instr = vm_load_instr(pc);

        // Extract instruction fields
        vm_word_t opcode = bits(instr, 0, 7);
        vm_word_t rd = bits(instr, 7, 5);
        vm_word_t funct3 = bits(instr, 12, 3);
        vm_word_t rs1 = bits(instr, 15, 5);
        vm_word_t rs2 = bits(instr, 20, 5);
        vm_word_t funct7 = bits(instr, 25, 7);

        // Handle individual instructions
        switch (opcode) {
            // `lui`
            case 0b0110111:
                emit_load_imm(imm_u(instr));
                emit_store_reg(rd);
                break;

            // `auipc`
            case 0b0010111:
                emit_load_imm(pc + imm_u(instr));
                emit_store_reg(rd);
                break;

            // `jal`
            case 0b1101111:
                // Store return address
                emit_load_imm(pc + 4);
                emit_store_reg(rd);
                // Perform jump
                emit_load_imm(pc + imm_j(instr));
                emit_exit(VM_EXIT_JUMP);
                goto vm_exit;

            // `jalr`
            case 0b1100111:
                if (funct3 != 0)
                    vm_error("Invalid jalr instruction");
                // Calculate jump target
                emit_load_imm(imm_i(instr));
                emit_set_operand();
                emit_load_reg(rs1);
                emit_op(EMIT_OP_ADD);
                // Clear least-significant bit
                emit_set_operand();
                emit_load_imm(~(vm_word_t)1);
                emit_op(EMIT_OP_AND);
                emit_set_operand();
                // Store return address
                emit_load_imm(pc + 4);
                emit_store_reg(rd);
                // Perform jump
                emit_get_operand();
                emit_exit(VM_EXIT_JUMP);
                goto vm_exit;

            // Conditional branches
            case 0b1100011: {
                // Determine condition
                emit_cmp_t cmp;
                switch (funct3) {
                    case 0b000:
                        cmp = EMIT_CMP_EQ;
                        break;
                    case 0b001:
                        cmp = EMIT_CMP_NE;
                        break;
                    case 0b100:
                        cmp = EMIT_CMP_LT;
                        break;
                    case 0b101:
                        cmp = EMIT_CMP_GE;
                        break;
                    case 0b110:
                        cmp = EMIT_CMP_LTU;
                        break;
                    case 0b111:
                        cmp = EMIT_CMP_GEU;
                        break;
                    default:
                        vm_error("Invalid branch instruction");
                }
                // Load second operand
                emit_load_reg(rs2);
                emit_set_operand();
                // Load first operand
                emit_load_reg(rs1);
                // Perform conditional jump
                emit_exit_cmp(cmp, VM_EXIT_JUMP, pc + imm_b(instr), pc + 4);
                goto vm_exit;
            }

            // Memory loads
            case 0b0000011: {
                // Compute memory address
                emit_load_reg(rs1);
                emit_set_operand();
                emit_load_imm(imm_i(instr));
                emit_op(EMIT_OP_ADD);
                emit_mem_addr();
                // Determine access width and signedness
                emit_width_t width;
                bool sign;
                switch (funct3) {
                    case 0b000:
                        width = EMIT_WIDTH_BYTE;
                        sign = true;
                        break;
                    case 0b001:
                        width = EMIT_WIDTH_HALFWORD;
                        sign = true;
                        break;
                    case 0b010:
                        width = EMIT_WIDTH_WORD;
                        sign = false;
                        break;
                    case 0b100:
                        width = EMIT_WIDTH_BYTE;
                        sign = false;
                        break;
                    case 0b101:
                        width = EMIT_WIDTH_HALFWORD;
                        sign = false;
                        break;
                    default:
                        vm_error("Invalid load instruction");
                }
                // Perform load operation
                emit_mem_load(width);
                if (sign)
                    emit_ext(width);
                emit_store_reg(rd);
                break;
            }

            // Memory stores
            case 0b0100011: {
                // Compute memory address
                emit_load_reg(rs1);
                emit_set_operand();
                emit_load_imm(imm_s(instr));
                emit_op(EMIT_OP_ADD);
                emit_mem_addr();
                // Determine access width
                emit_width_t width;
                switch (funct3) {
                    case 0b000:
                        width = EMIT_WIDTH_BYTE;
                        break;
                    case 0b001:
                        width = EMIT_WIDTH_HALFWORD;
                        break;
                    case 0b010:
                        width = EMIT_WIDTH_WORD;
                        break;
                    default:
                        vm_error("Invalid store instruction");
                }
                // Perform store operation
                emit_load_reg(rs2);
                emit_mem_store(width);
                break;
            }

            // ALU with immediate operand
            case 0b0010011:
                emit_load_imm(imm_i(instr));
                emit_set_operand();
                emit_load_reg(rs1);
                emit_op(alu_op(funct3, funct7, true));
                emit_store_reg(rd);
                break;

            // ALU with register operand
            case 0b0110011:
                emit_load_reg(rs2);
                emit_set_operand();
                emit_load_reg(rs1);
                emit_op(alu_op(funct3, funct7, false));
                emit_store_reg(rd);
                break;

            // Fence instructions
            case 0b0001111:
                switch (funct3) {

                    // `fence`
                    case 0b000:
                        // No-op, don't emit any code
                        break;

                    // `fence.i`
                    case 0b001:
                        emit_load_imm(pc + 4);
                        emit_exit(VM_EXIT_FENCE_I);
                        goto vm_exit;

                    default:
                        vm_error("Invalid fence instruction");
                }
                break;

            // System instructions
            case 0b1110011:
                if (instr == 0x00000073) {
                    // `ecall`
                    emit_load_imm(pc + 4);
                    emit_exit(VM_EXIT_ECALL);
                    goto vm_exit;

                } else if (instr == 0x00100073) {
                    // `ebreak`
                    emit_load_imm(pc + 4);
                    emit_exit(VM_EXIT_EBREAK);
                    goto vm_exit;

                } else {
                    vm_error("Invalid system instruction");
                }
                break;

            default:
                vm_error("Invalid instruction");
        }
    }

// Stop emitting code when we emitted an instruction that performs a VM exit
vm_exit:
    return chunk;
}
