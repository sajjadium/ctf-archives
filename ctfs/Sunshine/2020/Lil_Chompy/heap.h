#ifndef CAGE_HEAP_H
#define CAGE_HEAP_H

#include <stddef.h>

typedef struct CageHeap CageHeap;

void* cage_malloc(CageHeap* heap, size_t size) __attribute__((__warn_unused_result__)) __attribute__((__alloc_size__(2)));
void cage_free(CageHeap* heap, void* obj);
void* cage_realloc(CageHeap* heap, void* obj, size_t new_size) __attribute__((__warn_unused_result__)) __attribute__((__alloc_size__(3)));

CageHeap* create_cage(void) __attribute__((__warn_unused_result__));
void destroy_cage(CageHeap* heap);

#endif /* CAGE_HEAP_H */
