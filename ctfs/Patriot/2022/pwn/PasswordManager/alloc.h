#ifndef HEAP_H
#define HEAP_H

#include <stdio.h>

typedef union heap_header {
    struct {
        union heap_header *next;
        union heap_header *prev;
        size_t size;
        char free;
    } data;
    char align[32];
} heap_header_t;

typedef enum {
    HEAP_SUCCESS = 0,
    HEAP_FAIL,
    HEAP_INVALID_SIZE,
    HEAP_INVALID_BLOCK,
    HEAP_SBRK_FAIL
} heap_err_t;

void *heap_alloc(size_t size);
heap_header_t *first_fit(size_t size);
void heap_free(void *block);
void heap_defrag();
void heap_err(heap_err_t err, const char *func);
void heap_print();

#endif
