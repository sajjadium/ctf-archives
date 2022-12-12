#ifndef _LIBRSECUREHEAP_H_
#define _LIBRSECUREHEAP_H_

#include <stddef.h>
#include <stdint.h>
#include <sys/mman.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

typedef unsigned long long int u64;
typedef unsigned int u32;

#define HEAP_SIZE 0x10000
#define HEAP_BASE 0x31337000

#define SMALL_CHUNK_SIZE 0x80
#define MINSIZE 8
#define MAX_LARGE_CHUNK_DIFF 0x500

#define COOKIE_JAR_SIZE ((HEAP_SIZE / MINSIZE) * sizeof(LargeFreeChunk))

#define ALLOCATED_FLAG 0x1

#define CLEAR_ALLOCATED_FLAG(CHK) (CHK->size = CHK->size & (~ALLOCATED_FLAG))
#define CHUNK_FLAGS(CHK) (((CHK)->size) & 0b111)
#define IS_FREE_CHUNK(CHK) ((CHUNK_FLAGS(CHK) & ALLOCATED_FLAG) == 0) ? 1 : 0;
#define CHUNK_SIZE(CHK) (((CHK)->size) & ~0b111)
#define USER_SIZE_TO_REAL_CHUNK_SIZE(sz) (sz + sizeof(LargeFreeChunk))
#define CHUNK_TO_DATA_PTR(CHK) ((void *)(((u64)CHK) + sizeof(LargeFreeChunk)))
#define DATA_TO_CHUNK_PTR(PTR) ((Chunk *)((PTR) - sizeof(LargeFreeChunk)))
#define IN_SMALL_CHUNK_RANGE(sz) (sz <= SMALL_CHUNK_SIZE && sz >= 0)

#define CHUNK_MAGIC 0xdeadbeef

// https://elixir.bootlin.com/glibc/latest/source/malloc/malloc.c#L1331
#define ALIGN_SIZE(req)                                  \
  (((req) + sizeof(size_t) + 0xf < MINSIZE)  ? MINSIZE : \
   ((req) + sizeof(size_t) + 0xf) & ~0xf)                \

#define MAX_ARENAS 0x10

struct Chunk {
	u64 cookie;
	u32 magic;
	// flags are stored in lower 8 bits of the size
	u32 size; 
	struct Chunk *next;
};
typedef struct Chunk Chunk;


struct FreeChunk {
	Chunk chunk;
	struct FreeChunk *next_free;
};
typedef struct FreeChunk FreeChunk;


struct LargeFreeChunk {
	Chunk chunk;
	struct LargeFreeChunk *prev_free;
	struct LargeFreeChunk *next_free;
};
typedef struct LargeFreeChunk LargeFreeChunk;

struct CookieJar {
	Chunk *chunk;
	u64 cookie;
	struct CookieJar *next;
};
typedef struct CookieJar CookieJar;

struct Arena {
	Chunk *head_chunk;
	void *heap_start;
	u32 available;
	CookieJar *cookie_jar;

	FreeChunk *small_chunk_free_list;
	LargeFreeChunk *large_chunk_free_list;
};
typedef struct Arena Arena;


static Arena xmain_arena = {.head_chunk = NULL, .heap_start = (void *)HEAP_BASE,
					.available = HEAP_SIZE, .cookie_jar = NULL,
					.small_chunk_free_list = NULL, 
					.large_chunk_free_list =  NULL};


static LargeFreeChunk guard_head = {.chunk = {.cookie = -1, .magic = CHUNK_MAGIC, .size = 0,
								  .next = NULL},
								  .next_free = NULL, .prev_free = NULL};
static LargeFreeChunk guard_tail = {.chunk = {.cookie = -1, .magic = CHUNK_MAGIC, .size = 0,
								  .next = NULL},
								  .next_free = NULL, .prev_free = NULL};

static u32 arena_count = 1;
static u32 seed = 0;

static void init_heap();
static void destroy_heap();
static void init_main_arena(void *heap_start, CookieJar *cookie_jar);
static void setup_new_arena();
static u32 get_random4();
static void xerror(char *str);
static void create_chunk(void *ptr, size_t size, void *next);
static u64 gen_cookie();
static void *current_heap_top_ptr();
static void update_cookie_jar(Chunk *chunk, u64 cookie);
static void delete_from_cookie_jar(Chunk *chunk);

static void *(*volatile __xmalloc_hook)(size_t __size);
static void (*volatile __xfree_hook)(void *ptr);

void *xmalloc(size_t size);
void xfree(void *ptr);	

#endif