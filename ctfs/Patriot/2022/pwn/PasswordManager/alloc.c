#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include "alloc.h"

static void *heap_start = NULL;
static void *heap_end = NULL;

static heap_header_t *head = NULL;

static pthread_mutex_t *heap_lock = NULL;

void *heap_alloc(size_t size) {
    heap_err_t err = HEAP_FAIL;
    heap_header_t *ret = NULL;

    if(size == 0) {
        err = HEAP_INVALID_SIZE;
        goto end;
    }

    if(heap_start == NULL && heap_end == NULL) {
        heap_start = sbrk(0);
        heap_end = heap_start;
        pthread_mutex_init(heap_lock, NULL);
    }

    pthread_mutex_lock(heap_lock);

    ret = first_fit(size);
    if(ret) {
        if(ret->data.prev) {
            ret->data.prev->data.next = ret->data.next;
        }
        if(ret->data.next) {
            ret->data.next->data.prev = ret->data.prev;
        }
        if(ret == head) {
            head = ret->data.next;
            if(head) {
                head->data.prev = NULL;
            }
        }
    } else {
        ret = sbrk(size + sizeof(heap_header_t));
        if(ret == (void *) -1) {
            err = HEAP_SBRK_FAIL;
            goto end;
        }
        ret->data.size = size;
        heap_end += size + sizeof(heap_header_t);
    }

    ret->data.free = 0;
    ret = (void *)ret + sizeof(heap_header_t);
    err = HEAP_SUCCESS;

end:
    pthread_mutex_unlock(heap_lock);
    heap_err(err, "heap_alloc()");
    return ret;
}

heap_header_t *first_fit(size_t size) {
    heap_header_t *ret = NULL;
    heap_header_t *curr = head;
    while(curr) {
        if(curr->data.size >= size) {
            ret = curr;
            break;
        }
        curr = curr->data.next;
    }

    return ret;
}

void heap_free(void *block) {
    if(block == NULL) {
        heap_err(HEAP_INVALID_BLOCK, "heap_free()");
    } else {
        heap_header_t *to_free = (heap_header_t *) (block - sizeof(heap_header_t));
        to_free->data.free = 1;

        heap_defrag();
    }
}

void heap_defrag() {
    heap_err_t err = HEAP_FAIL;
    heap_header_t *chunk = NULL, *last_free_chunk = NULL;
    void *curr = NULL;
    int size = 0;

    pthread_mutex_lock(heap_lock);

    head = NULL;

    curr = heap_start;
    while(curr < heap_end) {
        chunk = (heap_header_t *) curr;
        if(chunk->data.free) {
            if(!head) {
                head = chunk;
                head->data.next = NULL;
                head->data.prev = NULL;
                last_free_chunk = chunk;
            } else {
                if((void *)last_free_chunk + last_free_chunk->data.size
                        + sizeof(heap_header_t) == curr) {
                    last_free_chunk->data.size += sizeof(heap_header_t) + chunk->data.size;
                } else {
                    chunk->data.prev = last_free_chunk;
                    if(last_free_chunk) {
                        last_free_chunk->data.next = chunk;
                    }
                    chunk->data.next = NULL;
                    last_free_chunk = chunk;
                }
            }
        }
        curr += chunk->data.size + sizeof(heap_header_t);
    }

    size = sizeof(heap_header_t) + last_free_chunk->data.size;
    if((void *)last_free_chunk + size == heap_end) {
        if(sbrk(-1 * size) == (void *) -1) {
            err = HEAP_SBRK_FAIL;
            goto end;
        }

        if((void *)head + size == heap_end &&
                head != heap_start && head) {

            head = head->data.prev;
            if(head) {
                head->data.next = NULL;
            }
        }

        heap_end -= size;
    }

    err = HEAP_SUCCESS;

end:
    pthread_mutex_unlock(heap_lock);
    heap_err(err, "heap_defrag()");
}

void heap_err(heap_err_t err, const char *func) {
    switch(err) {
        case HEAP_SUCCESS:
            break;
        case HEAP_FAIL:
            printf("%s: failed.\n", func);
            break;
        case HEAP_INVALID_SIZE:
            printf("%s: invalid size.\n", func);
            break;
        case HEAP_INVALID_BLOCK:
            printf("%s: invalid block.\n", func);
            break;
        case HEAP_SBRK_FAIL:
            printf("%s: srbk() failed.\n", func);
            break;
    }
}
