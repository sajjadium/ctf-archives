#include "emit.h"

#include "codebuf.h"

#include <stdint.h>

void emit_load_imm(vm_word_t imm) {
    // `mov esi, imm32`
    codebuf_emit_lit("\xbe");
    codebuf_emit_32(imm);
}

void emit_load_reg(size_t reg) {
    // `mov esi, dword ptr [rdi + imm8]`
    codebuf_emit_lit("\x8b\x77");
    codebuf_emit_8((uint8_t)(reg * 4));
}

void emit_store_reg(size_t reg) {
    if (reg == 0)
        return;

    // `mov dword ptr [rdi + imm8], esi`
    codebuf_emit_lit("\x89\x77");
    codebuf_emit_8((uint8_t)(reg * 4));
}

void emit_set_operand(void) {
    // `mov ecx, esi`
    codebuf_emit_lit("\x89\xf1");
}

void emit_get_operand(void) {
    // `mov esi, ecx`
    codebuf_emit_lit("\x89\xce");
}

void emit_op(emit_op_t op) {
    switch (op) {
        case EMIT_OP_ADD:
            // `add esi, ecx`
            codebuf_emit_lit("\x01\xce");
            break;
        case EMIT_OP_SUB:
            // `sub esi, ecx`
            codebuf_emit_lit("\x29\xce");
            break;
        case EMIT_OP_AND:
            // `and esi, ecx`
            codebuf_emit_lit("\x21\xce");
            break;
        case EMIT_OP_OR:
            // `or esi, ecx`
            codebuf_emit_lit("\x09\xce");
            break;
        case EMIT_OP_XOR:
            // `xor esi, ecx`
            codebuf_emit_lit("\x31\xce");
            break;
        case EMIT_OP_SLL:
            // `and ecx, 0x1f; shl esi, cl`
            codebuf_emit_lit("\x83\xe1\x1f\xd3\xe6");
            break;
        case EMIT_OP_SRL:
            // `and ecx, 0x1f; shr esi, cl`
            codebuf_emit_lit("\x83\xe1\x1f\xd3\xee");
            break;
        case EMIT_OP_SRA:
            // `and ecx, 0x1f; sar esi, cl`
            codebuf_emit_lit("\x83\xe1\x1f\xd3\xfe");
            break;
        case EMIT_OP_SLT:
            // `cmp esi, ecx; setl sil; movzx esi, sil`
            codebuf_emit_lit("\x39\xce\x40\x0f\x9c\xc6\x40\x0f\xb6\xf6");
            break;
        case EMIT_OP_SLTU:
            // `cmp esi, ecx; setb sil; movzx esi, sil`
            codebuf_emit_lit("\x39\xce\x40\x0f\x92\xc6\x40\x0f\xb6\xf6");
            break;
    }
}

void emit_exit_cmp(emit_cmp_t cmp, vm_exit_reason_t reason, vm_word_t pc_true, vm_word_t pc_false) {
    uint64_t exit_code_true = ((uint64_t)reason << 32) | pc_true;
    uint64_t exit_code_false = ((uint64_t)reason << 32) | pc_false;

    // Determine opcode for conditional move
    uint8_t cmov;
    switch (cmp) {
        case EMIT_CMP_EQ:
            cmov = 0x44;
            break;
        case EMIT_CMP_NE:
            cmov = 0x45;
            break;
        case EMIT_CMP_LT:
            cmov = 0x4c;
            break;
        case EMIT_CMP_GE:
            cmov = 0x4d;
            break;
        case EMIT_CMP_LTU:
            cmov = 0x42;
            break;
        case EMIT_CMP_GEU:
            cmov = 0x43;
            break;
    }

    // Default to exit code for false: `movabs rax, imm64`
    codebuf_emit_lit("\x48\xb8");
    codebuf_emit_64(exit_code_false);
    // Prepare exit code for true: `movabs r8, imm64`
    codebuf_emit_lit("\x49\xb8");
    codebuf_emit_64(exit_code_true);

    // Perform comparison: `cmp rsi, rcx`
    codebuf_emit_lit("\x48\x39\xce");
    // Set exit code for true if condition is true: `cmovCC rax, r8`
    codebuf_emit_lit("\x49\x0f");
    codebuf_emit_8(cmov);
    codebuf_emit_8(0xc0);

    // `ret`
    codebuf_emit_lit("\xc3");
}

void emit_exit(vm_exit_reason_t reason) {
    // `movabs rax, imm64`
    codebuf_emit_lit("\x48\xb8");
    codebuf_emit_64((uint64_t)reason << 32);
    // `or rax, rsi; ret`
    codebuf_emit_lit("\x48\x09\xf0\xc3");
}

void emit_mem_addr(void) {
    // Get size of guest memory: `mov r8, qword ptr [rdi + 0x88]`
    codebuf_emit_lit("\x4c\x8b\x87\x88\x00\x00\x00");
    // Compare with temporary: `cmp rsi, r8; jb inbounds`
    codebuf_emit_lit("\x4c\x39\xc6\x72\x0b");
    // VM exit if out of bounds: `movabs rax, imm64; ret`
    codebuf_emit_lit("\x48\xb8");
    codebuf_emit_64((uint64_t)VM_EXIT_FAULT << 32);
    codebuf_emit_lit("\xc3");
    // Store in guest memory address register: `inbounds: mov edx, esi`
    codebuf_emit_lit("\x89\xf2");
    // Add guest memory base address: `add rdx, qword ptr [rdi + 0x80]`
    codebuf_emit_lit("\x48\x03\x97\x80\x00\x00\x00");
}

void emit_mem_load(emit_width_t width) {
    switch (width) {
        case EMIT_WIDTH_WORD:
            // `mov esi, dword ptr [rdx]`
            codebuf_emit_lit("\x8b\x32");
            break;
        case EMIT_WIDTH_HALFWORD:
            // `movzx esi, word ptr [rdx]`
            codebuf_emit_lit("\x0f\xb7\x32");
            break;
        case EMIT_WIDTH_BYTE:
            // `movzx esi, byte ptr [rdx]`
            codebuf_emit_lit("\x0f\xb6\x32");
            break;
    }
}

void emit_mem_store(emit_width_t width) {
    switch (width) {
        case EMIT_WIDTH_WORD:
            // `mov dword ptr [rdx], esi`
            codebuf_emit_lit("\x89\x32");
            break;
        case EMIT_WIDTH_HALFWORD:
            // `mov word ptr [rdx], si`
            codebuf_emit_lit("\x66\x89\x32");
            break;
        case EMIT_WIDTH_BYTE:
            // `mov byte ptr [rdx], sil`
            codebuf_emit_lit("\x40\x88\x32");
            break;
    }
}

void emit_ext(emit_width_t width) {
    switch (width) {
        case EMIT_WIDTH_HALFWORD:
            // `movsx esi, si`
            codebuf_emit_lit("\x0f\xbf\xf6");
            break;
        case EMIT_WIDTH_BYTE:
            // `movsx esi, sil`
            codebuf_emit_lit("\x40\x0f\xbe\xf6");
            break;
        default:
            break;
    }
}
