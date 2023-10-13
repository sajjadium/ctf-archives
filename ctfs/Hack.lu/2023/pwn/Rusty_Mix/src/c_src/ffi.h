#ifndef FFI_H
#define FFI_H

#include "stdint.h"

#define NUM_MAPS 10

enum AllocType {
    ALLOC_NONE = 0,
    ALLOC_RUST_BTREEMAP = 1,
    ALLOC_RUST_HASHMAP = 2,
};

typedef struct Maps {
    enum AllocType allocs[NUM_MAPS];
    uint32_t results[NUM_MAPS];
    void *maps[NUM_MAPS];
} Maps;

void init(Maps *m);
void create(Maps *m, uint32_t ind, enum AllocType type);
void destroy(Maps *m, uint32_t ind);
uint32_t get(Maps *m, uint32_t ind, uint32_t k);
void put(Maps *m, uint32_t ind, uint32_t k, uint32_t v);

#endif