#define _GNU_SOURCE
#include <err.h>
#include <stdbool.h>
#include <stddef.h>

#include "shellcodeverifier.h"

/* This might be useful for you: http://ref.x86asm.net/coder64.html :) */

#define ARRAY_LEN(a) (sizeof(a) / sizeof(a[0]))

struct modrm {
    union {
        struct {
            unsigned rm:3;
            unsigned reg:3;
            unsigned mod:2;
        };
        unsigned val;
    };
};

static bool verify_simple_binop(const unsigned char* buf, size_t offset) {
    (void)offset;
    struct modrm modrm = { .val = buf[1] };

    if (modrm.mod == 0b00) {
        if (modrm.reg == 0b100) {
            return false;
        }
        if (modrm.rm == 0b100 || modrm.rm == 0b101) {
            return false;
        }
        return true;
    } else if (modrm.mod == 0b11) {
        if (modrm.reg == 0b100) {
            return false;
        }
        if (modrm.rm == 0b100) {
            return false;
        }
        return true;
    }

    return false;
}

static bool verify_f7(const unsigned char* buf, size_t offset) {
    (void)offset;
    struct modrm modrm = { .val = buf[1] };

    switch (modrm.reg) {
        case 2: // not
        case 3: // neg
        case 4: // mul
        case 5: // imul
        case 6: // div
        case 7: // idiv
            if (modrm.mod == 0b00) {
                if (modrm.rm == 0b100 || modrm.rm == 0b101) {
                    return false;
                }
                return true;
            } else if (modrm.mod == 0b11) {
                if (modrm.rm == 0b100) {
                    return false;
                }
                return true;
            }
            return false;
        default:
            return false;
    }
}

struct {
    unsigned char opcode;
    size_t size;
    bool (*verifier)(const unsigned char* buf, size_t offset);
} allowed_opcodes[] = {
    { 0x01, 2, verify_simple_binop }, // add
    { 0x09, 2, verify_simple_binop }, // or
    { 0x21, 2, verify_simple_binop }, // and
    { 0x29, 2, verify_simple_binop }, // sub
    { 0x31, 2, verify_simple_binop }, // xor
    { 0x39, 2, verify_simple_binop }, // cmp
    { 0x87, 2, verify_simple_binop }, // xchg
    { 0x89, 2, verify_simple_binop }, // mov
    { 0x8b, 2, verify_simple_binop }, // mov
    { 0x90, 1, NULL }, // nop
    { 0xb8, 5, NULL }, // mov
    { 0xb9, 5, NULL }, // mov
    { 0xba, 5, NULL }, // mov
    { 0xbb, 5, NULL }, // mov
    { 0xbd, 5, NULL }, // mov
    { 0xbe, 5, NULL }, // mov
    { 0xbf, 5, NULL }, // mov
    { 0xc3, 1, NULL }, // ret
    { 0xf7, 2, verify_f7 },
};

bool verify_buffer(const unsigned char* buf, size_t size) {
    size_t i = 0;
    while (i < size) {
        bool ok = false;
        for (size_t idx = 0; idx < ARRAY_LEN(allowed_opcodes); ++idx) {
            if (buf[i] == allowed_opcodes[idx].opcode) {
                if (i + allowed_opcodes[idx].size > size) {
                    return false;
                }
                if (allowed_opcodes[idx].verifier && !allowed_opcodes[idx].verifier(&buf[i], i)) {
                    return false;
                }
                i += allowed_opcodes[idx].size;
                ok = true;
                break;
            }
        }
        if (!ok) {
            return false;
        }
    }
    if (i != size) {
        return false;
    }

    return true;
}
