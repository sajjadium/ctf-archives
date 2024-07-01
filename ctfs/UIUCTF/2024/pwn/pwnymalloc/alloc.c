
#include <unistd.h>
#include <stdio.h>

#include "alloc.h"

typedef struct chunk_meta {
    size_t size;
    struct chunk_meta *next; // only for free blocks
    struct chunk_meta *prev; // only for free blocks
} chunk_meta_t;

typedef struct btag { // only for free blocks
    size_t size;
} btag_t;

typedef chunk_meta_t *chunk_ptr;


#define ALIGNMENT 16
#define ALIGN(size) (((size) + (ALIGNMENT - 1)) & ~(ALIGNMENT - 1))
#define MAX(x, y) ((x) > (y) ? (x) : (y))

#define INUSE_META_SIZE (sizeof(chunk_meta_t) - 2 * sizeof(chunk_meta_t *))
#define FREE_META_SIZE sizeof(chunk_meta_t)
#define BTAG_SIZE sizeof(btag_t)
#define MIN_BLOCK_SIZE (FREE_META_SIZE + BTAG_SIZE)

#define FREE 0
#define INUSE 1


static size_t pack_size(size_t size, int status);
static size_t get_size(chunk_ptr block);
static size_t get_prev_size(chunk_ptr block);
static void set_btag(chunk_ptr block, size_t size);
static int get_status(chunk_ptr block);
static void set_status(chunk_ptr block, int status);
static chunk_ptr next_chunk(chunk_ptr block);
static chunk_ptr prev_chunk(chunk_ptr block);

static chunk_ptr extend_heap(size_t size);
static chunk_ptr find_fit(size_t size);
static void free_list_insert(chunk_ptr block);
static void free_list_remove(chunk_ptr block);
static chunk_ptr coalesce(chunk_ptr block);
static void split(chunk_ptr block, size_t size);


static void *heap_start = NULL;
static void *heap_end = NULL;

static chunk_ptr free_list = NULL;


/**
`* Utils
`*/

static size_t pack_size(size_t size, int status) {
    return size | status;
}

static size_t get_size(chunk_ptr block) {
    return block->size & ~1;
}

static size_t get_prev_size(chunk_ptr block) {
    btag_t *prev_footer = (btag_t *) ((char *) block - BTAG_SIZE);
    return prev_footer->size;
}

static void set_btag(chunk_ptr block, size_t size) {
    btag_t *footer = (btag_t *) ((char *) block + size - BTAG_SIZE);
    footer->size = size;
}

static int get_status(chunk_ptr block) {
    return block->size & 1;
}

static void set_status(chunk_ptr block, int status) {
    block->size = (block->size & ~1) | status;
}

static chunk_ptr next_chunk(chunk_ptr block) {
    size_t size = get_size(block);
    if ((void *) block >= heap_end - size) {
        return NULL;
    }
    return (chunk_ptr) ((char *) block + size);
}

static chunk_ptr prev_chunk(chunk_ptr block) {
    if ((void *) block - get_prev_size(block) < heap_start || get_prev_size(block) == 0) {
        return NULL;
    }
    return (chunk_ptr) ((char *) block - get_prev_size(block));
}


/**
`* Core helpers
`*/


static chunk_ptr extend_heap(size_t size) {
    chunk_ptr block = (chunk_ptr) sbrk(size);
    if (block == (void *) -1) {
        return NULL;
    }

    block->size = pack_size(size, INUSE);
    heap_end = (void *) block + size;
    return block;
}


static chunk_ptr find_fit(size_t size) {
    chunk_ptr block = free_list;
    while (block != NULL) {
        if (get_size(block) >= size) {
            free_list_remove(block);
            set_status(block, INUSE);
            return block;
        }
        block = block->next;
    }
    return NULL;
}

static void free_list_insert(chunk_ptr block) {
    block->next = free_list;
    block->prev = NULL;
    if (free_list != NULL) {
        free_list->prev = block;
    }
    free_list = block;
}

static void free_list_remove(chunk_ptr block) {
    if (block->prev != NULL) {
        block->prev->next = block->next;
    } else {
        free_list = block->next;
    }

    if (block->next != NULL) {
        block->next->prev = block->prev;
    }
}

static chunk_ptr coalesce(chunk_ptr block) {
    chunk_ptr prev_block = prev_chunk(block);
    chunk_ptr next_block = next_chunk((chunk_ptr) block);
    size_t size = get_size(block);

    int prev_status = prev_block == NULL ? -1 : get_status(prev_block);
    int next_status = next_block == NULL ? -1 : get_status(next_block);

    if (prev_status == FREE && next_status == FREE) {
        free_list_remove(next_block);
        free_list_remove(prev_block);

        size += get_size(prev_block) + get_size(next_block);
        prev_block->size = pack_size(size, FREE);
        set_btag(prev_block, size);
        
        return prev_block;
    } 
    if (prev_status == FREE) {
        free_list_remove(prev_block);

        size += get_size(prev_block);
        prev_block->size = pack_size(size, FREE);
        set_btag(prev_block, size);

        return prev_block;
    } 
    if (next_status == FREE) {
        free_list_remove(next_block);

        size += get_size(next_block);
        block->size = pack_size(size, FREE);
        set_btag(block, size);

        return block;
    }

    return block;
}

static void split(chunk_ptr block, size_t size) {
    size_t old_size = get_size(block);
    size_t new_size = old_size - size;

    chunk_ptr new_block = (chunk_ptr) ((char *) block + size);
    new_block->size = pack_size(new_size, FREE);
    set_btag(new_block, new_size);

    block->size = pack_size(size, INUSE);
    
    new_block = coalesce(new_block);
    free_list_insert(new_block);
}




void *pwnymalloc(size_t size) {
    if (heap_start == NULL) {
        heap_start = sbrk(0);
        heap_end = heap_start;
    }

    if (size == 0) {
        return NULL;
    }

    size_t total_size = MAX(ALIGN(size + INUSE_META_SIZE), MIN_BLOCK_SIZE);

    chunk_ptr block = find_fit(total_size);

    if (block == NULL) {
        block = extend_heap(total_size);
        if (block == NULL) {
            return NULL;
        }
    } else if (get_size((chunk_ptr) block) >= total_size + MIN_BLOCK_SIZE) {
        split(block, total_size);
    }

    return (void *) ((char *) block + INUSE_META_SIZE);
}


void pwnyfree(void *ptr) {
    if (ptr == NULL) {
        return;
    }

    chunk_ptr block = (chunk_ptr) ((char *) ptr - INUSE_META_SIZE);

    // eheck alignment and status
    if ((size_t) block % ALIGNMENT != 0 || get_status(block) != INUSE) {
        return;
    }

    set_status(block, FREE);
    set_btag(block, get_size(block));

    block = coalesce(block);

    printf("Block size: %zu\n", get_size(block));

    free_list_insert(block);
}






