#include "codebuf.h"

#include <stddef.h>
#include <string.h>
#include <sys/mman.h>

// Max. 64 kiB generated code
#define CODE_SIZE 0x10000

// Max. 4096 compiled chunks
#define NUM_CHUNKS 0x1000

// Entry of mapping from guest PCs to code chunks
typedef struct {
    // Guest PC
    vm_word_t pc;
    // Code chunk
    codebuf_chunk_t code;
} chunk_map_t;

// Beginning of generated code region
static unsigned char *code;

// Current index into generated code region
static size_t code_idx;

// Mapping from guest PCs to code chunks
static chunk_map_t chunk_map[NUM_CHUNKS];

void codebuf_init(void) {
    // Allocate RWX memory for generated code
    code = mmap(NULL,
            CODE_SIZE,
            PROT_READ | PROT_WRITE | PROT_EXEC,
            MAP_ANONYMOUS | MAP_PRIVATE,
            -1,
            0);
    if (code == MAP_FAILED)
        vm_error("Failed to allocate code buffer");
}

void codebuf_clear(void) {
    // Continue emitting code at the beginning of the code buffer
    code_idx = 0;
    // Forget all existing code chunks
    for (size_t i = 0; i < NUM_CHUNKS; i++)
        chunk_map[i].code = NULL;
}

codebuf_chunk_t codebuf_register_chunk(vm_word_t pc) {
    // Position where next generated code will be
    codebuf_chunk_t chunk = (codebuf_chunk_t)(code + code_idx);

    // Insert into map
    size_t i;
    for (i = 0; i < NUM_CHUNKS; i++) {
        if (!chunk_map[i].code) {
            chunk_map[i].pc = pc;
            chunk_map[i].code = chunk;
            break;
        }
    }
    if (i == NUM_CHUNKS)
        vm_error("Maximum number of code chunks reached");

    return chunk;
}

codebuf_chunk_t codebuf_get_chunk(vm_word_t pc) {
    for (size_t i = 0; i < NUM_CHUNKS; i++)
        if (chunk_map[i].code && chunk_map[i].pc == pc)
            return chunk_map[i].code;
    return NULL;
}

void codebuf_emit_raw(void *buf, size_t size) {
    if (CODE_SIZE - code_idx < size)
        vm_error("Maximum amount of generated code reached");

    memcpy(code + code_idx, buf, size);
    code_idx += size;
}

void codebuf_emit_8(uint8_t val) {
    codebuf_emit_raw(&val, sizeof val);
}

void codebuf_emit_16(uint16_t val) {
    codebuf_emit_raw(&val, sizeof val);
}

void codebuf_emit_32(uint32_t val) {
    codebuf_emit_raw(&val, sizeof val);
}

void codebuf_emit_64(uint64_t val) {
    codebuf_emit_raw(&val, sizeof val);
}
