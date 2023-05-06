// Provides a global buffer in that generated code chunks are stored. Also stores mapping from guest
// PCs to code chunks.

#pragma once

#include "vm.h"

#include <stddef.h>
#include <stdint.h>

// Pointer to a chunk of generated code
typedef vm_exit_t (*codebuf_chunk_t)(vm_state_t *);

// Initialize the global code buffer
void codebuf_init(void);

// Remove all entries from the global code buffer
void codebuf_clear(void);

// Associates the next emitted code chunk with the given guest PC and returns it
codebuf_chunk_t codebuf_register_chunk(vm_word_t pc);

// Get the code chunk for the given guest PC, or NULL if it has not been JITed yet
codebuf_chunk_t codebuf_get_chunk(vm_word_t pc);

// Emit the contents of a buffer
void codebuf_emit_raw(void *buf, size_t size);

// Emit the content of a string literal, without the terminating null byte
#define codebuf_emit_lit(lit) codebuf_emit_raw(lit, sizeof lit - 1)

// Emit an 8-bit value, in native byte order
void codebuf_emit_8(uint8_t val);

// Emit a 16-bit value, in native byte order
void codebuf_emit_16(uint16_t val);

// Emit a 32-bit value, in native byte order
void codebuf_emit_32(uint32_t val);

// Emit a 64-bit value, in native byte order
void codebuf_emit_64(uint64_t val);
