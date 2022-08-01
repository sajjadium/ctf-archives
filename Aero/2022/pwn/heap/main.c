#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define STDIN_FD 0
#define STDOUT_FD 1

#define MAX_CHUNK_SIZE 100
#define CHUNKS_LIST_SIZE 32


enum Action {
    ACTION_ADD = 1,
    ACTION_DELETE,
    ACTION_VIEW,
    ACTION_EXIT,
};

typedef struct chunk_t {
    int64_t size;
    int64_t used;
    void *ptr;
} chunk_t;

chunk_t *chunks[CHUNKS_LIST_SIZE];
size_t chunk_idx = 0;


void setup(void)
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

ssize_t read_into_buffer(void *buf, uint32_t size) 
{
    if (buf == NULL) {
        puts("[-] invalid buffer pointer");
        return -1;
    }

    if (size == 0) {
        puts("[-] invalid buffer size");
        return -1;
    }

    ssize_t nbytes = read(STDIN_FD, buf, size);

    if (nbytes < 0) {
        puts("[-] failed to read into buffer");
        return -1;
    }

    return nbytes;
}

ssize_t write_from_buffer(const void *buf, uint32_t size) 
{
    if (buf == NULL) {
        puts("[-] invalid buffer pointer");
        return -1;
    }

    if (size == 0) {
        puts("[-] invalid buffer size");
        return -1;
    }

    ssize_t nbytes = write(STDOUT_FD, buf, size);

    if (nbytes < 0) {
        puts("[-] failed to write from buffer");
        return -1;
    }

    return nbytes;
}

int read_integer(void)
{
    const size_t buflen = 8;

    char buf[buflen];
    ssize_t nbytes = read_into_buffer(buf, buflen);

    if (nbytes == -1) {
        puts("[-] failed to read int");
        return -1;
    }

    return atoi(buf);
}

void add_chunk(void) 
{
    if (chunk_idx >= CHUNKS_LIST_SIZE) {
        puts("[-] Chunk limit exceeded!");
        return;
    }

    printf("[?] Enter chunk size: ");
    size_t chunk_size = read_integer();

    if (chunk_size > MAX_CHUNK_SIZE) {
        puts("[-] Chunk is too large!");
        return;
    }

    chunk_t *new_chunk = (chunk_t *)malloc(sizeof(chunk_t));

    if (new_chunk == NULL) {
        puts("[-] Failed to create new chunk!");
        return;
    }

    void *ptr = (void *)malloc(chunk_size);

    if (ptr == NULL) {
        puts("[-] Failed to create chunk for data!");
        return;
    }

    printf("[?] Enter chunk data: ");
    ssize_t nbytes = read_into_buffer(ptr, chunk_size);

    new_chunk->size = chunk_size;
    new_chunk->used = true;
    new_chunk->ptr = ptr;

    chunks[chunk_idx] = new_chunk;
    chunk_idx += 1;
}

void delete_chunk(void) 
{
    printf("[?] Enter chunk id: ");
    size_t chunk_id = read_integer();

    if (chunk_id >= chunk_idx) {
        puts("[-] Invalid chunk index!");
        return;
    }

    chunk_t *chunk = chunks[chunk_id];

    if (chunk == NULL) {
        puts("[-] No such chunk!");
        return;
    }

    if (!chunk->used || chunk->ptr == NULL) {
        puts("[-] Chunk is not used!");
        return;
    }

    free(chunk->ptr); 
    chunk->ptr = NULL;
    chunk->used = false;
    free(chunks[chunk_id]);
}

void view_chunk(void)
{
    printf("[?] Enter chunk id: ");
    size_t chunk_id = read_integer();

    if (chunk_id >= CHUNKS_LIST_SIZE) {
        puts("[-] Invalid chunk index!");
        return;
    }

    if (chunks[chunk_id] == NULL) {
        puts("[-] No such chunk!");
        return;
    }

    if (!chunks[chunk_id]->used || chunks[chunk_id]->ptr == NULL) {
        puts("[-] Chunk is not used!");
        return;
    }

    write_from_buffer(chunks[chunk_id]->ptr, chunks[chunk_id]->size);
}

int main() 
{
    setup();

    while (true) {
        printf(
            "%d. Add\n%d. Delete\n%d. View\n%d. Exit\n> ",
            ACTION_ADD, ACTION_DELETE, ACTION_VIEW, ACTION_EXIT
        );

        switch (read_integer()) 
        { 
            case ACTION_ADD:
                add_chunk();
                break;
            case ACTION_DELETE:
                delete_chunk();
                break;
            case ACTION_VIEW:
                view_chunk();
                break;
            case ACTION_EXIT:
                return 0;
            default:
                puts("[-] Invalid option.");
                continue;
        }
    }
}
