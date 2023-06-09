#include "libsecureheap.h"


void create_chunk(void *ptr, size_t size, void *next) {
	Chunk new_chunk;
	u64 cookie = gen_cookie();
 	new_chunk.cookie = cookie;
 	new_chunk.magic = CHUNK_MAGIC;
	new_chunk.size = size | ALLOCATED_FLAG;
	new_chunk.next = next;
	memcpy(ptr, &new_chunk, sizeof(new_chunk));

	update_cookie_jar((Chunk *)ptr, cookie);
}

void delete_from_cookie_jar(Chunk *chunk) {
	CookieJar *current_jar = xmain_arena.cookie_jar;
	if (current_jar->next == NULL) {
		if (current_jar->chunk == chunk) {
			memset(current_jar, 0, sizeof(CookieJar));
			return;
		}
	}

	while (current_jar != NULL) {
		if (current_jar->next->chunk == chunk) {
			memset(current_jar->next, 0, sizeof(CookieJar));
			current_jar->next = current_jar->next->next;
			return;
		}
		current_jar = current_jar->next;
	}
}

void update_cookie_jar(Chunk *chunk, u64 cookie) {
	CookieJar *current_jar = xmain_arena.cookie_jar;
	while (current_jar != NULL) {
		if (current_jar->chunk == chunk) {
			// chunk is already in the list. update the cookie
			current_jar->cookie = cookie;
			return;
		} else if (current_jar->next == NULL) {
			break;
		}
		current_jar = current_jar->next;
	}

	// chunk not in the list. add it
	CookieJar *new_jar;
	if (current_jar->chunk == NULL && current_jar->cookie == 0) {
		new_jar = xmain_arena.cookie_jar;	
	} else {
		new_jar = (CookieJar *)(((void *)current_jar) + sizeof(CookieJar));
		current_jar->next = new_jar;
	}
	new_jar->chunk = chunk;
	new_jar->cookie = cookie;	
}

void verify_cookies() {
	CookieJar *current_jar = xmain_arena.cookie_jar;
	while (current_jar != NULL) {
		if (current_jar->chunk == NULL) break;
		if (current_jar->chunk->cookie != current_jar->cookie) {
			xerror("Memory corruption detected: Cookie overwritten.");
		}
		current_jar = current_jar->next;
	}
}

void xerror(char *str) {
	puts(str);
	exit(-1);
}

void *xmalloc(size_t size) {
	if (__xmalloc_hook != NULL) {
		return __xmalloc_hook(size);
	}

	verify_cookies();

	// align to 8 byte boundary
	size = ALIGN_SIZE(size);

	if (USER_SIZE_TO_REAL_CHUNK_SIZE(size) >= HEAP_SIZE) {
		return NULL;
	}

	if (arena_count > MAX_ARENAS) {
		return NULL;
	}

	if (USER_SIZE_TO_REAL_CHUNK_SIZE(size) >= xmain_arena.available) {
		setup_new_arena();
	}

	// check if we have a fit in the free chunks
	if (IN_SMALL_CHUNK_RANGE(size) && xmain_arena.small_chunk_free_list != NULL) {
		FreeChunk *current_freelist_head_chunk = xmain_arena.small_chunk_free_list;
		xmain_arena.small_chunk_free_list = xmain_arena.small_chunk_free_list->next_free;
		create_chunk((void *)current_freelist_head_chunk, SMALL_CHUNK_SIZE, NULL);
		return CHUNK_TO_DATA_PTR((Chunk *)current_freelist_head_chunk);		
	} else {
		LargeFreeChunk *current_free_chunk = xmain_arena.large_chunk_free_list;
		if (current_free_chunk->next_free != &guard_tail) {
			while (current_free_chunk != &guard_tail) {
				u64 old_size = CHUNK_SIZE((Chunk *) current_free_chunk);
				u64 size_diff = old_size - size;
				// reuse chunks that differ only slightly in size 
				if (size_diff <= MAX_LARGE_CHUNK_DIFF) {
					// update free list
					current_free_chunk->prev_free->next_free = current_free_chunk->next_free;
					current_free_chunk->next_free->prev_free = current_free_chunk->prev_free;

					create_chunk(current_free_chunk, old_size, ((Chunk *)current_free_chunk)->next);
					return CHUNK_TO_DATA_PTR(current_free_chunk);
				}
				current_free_chunk = current_free_chunk->next_free;
			}
		}
	}

	// no fitting free chunk was found that could be reused
	// create a new chunk
	Chunk *chunk = (Chunk *)current_heap_top_ptr();
	create_chunk(chunk, size, NULL);
				

	if (xmain_arena.head_chunk == NULL) {
		xmain_arena.head_chunk = chunk;
	} else {
		Chunk *current_chunk = xmain_arena.head_chunk;
		while (current_chunk->next != NULL) {
			current_chunk = current_chunk->next;
		}
		current_chunk->next = chunk;
	}

	xmain_arena.available -= USER_SIZE_TO_REAL_CHUNK_SIZE(size);
	return CHUNK_TO_DATA_PTR(chunk);
}

void xfree(void *ptr) {
	if (__xfree_hook != NULL) {
		return __xfree_hook(ptr);
	}

	
	verify_cookies();
	
	if (ptr == NULL) return;
	Chunk *chunk = DATA_TO_CHUNK_PTR(ptr);

	if (chunk->magic != CHUNK_MAGIC) {
		xerror("Memory corruption detected on xfree: Chunk was not obtained by xmalloc.");
	}

	if (!(CHUNK_FLAGS(chunk) & ALLOCATED_FLAG)) {
		xerror("Double free detected.");
	}

	// if last chunk is freed we make the memory available again
	u32 full_chunk_size = USER_SIZE_TO_REAL_CHUNK_SIZE(CHUNK_SIZE(chunk));
	if (chunk != xmain_arena.head_chunk && chunk == current_heap_top_ptr() - full_chunk_size) {
		Chunk *current_chunk = xmain_arena.head_chunk;
		while (current_chunk != NULL) {
			if (current_chunk->next == chunk) {
				memset(chunk, 0 , full_chunk_size);
				xmain_arena.available += full_chunk_size;
				current_chunk->next = NULL;
				delete_from_cookie_jar(chunk);
				return;
			}
			current_chunk = current_chunk->next;
		}
	}

	CLEAR_ALLOCATED_FLAG(chunk);

	if (IN_SMALL_CHUNK_RANGE(CHUNK_SIZE(chunk))) {
		FreeChunk *chunk_to_free = (FreeChunk *)chunk;
		FreeChunk *free_list_chunk = xmain_arena.small_chunk_free_list;
		if (free_list_chunk != NULL) {
			chunk_to_free->next_free = free_list_chunk;
		} 
		xmain_arena.small_chunk_free_list = chunk_to_free;
	} else {
		LargeFreeChunk *chunk_to_free = (LargeFreeChunk *)chunk;
		LargeFreeChunk *free_list_head = xmain_arena.large_chunk_free_list;
		LargeFreeChunk *free_list_tail = free_list_head->prev_free;

		free_list_tail->next_free = chunk_to_free;
		chunk_to_free->prev_free = free_list_tail;

		chunk_to_free->next_free = free_list_head;
		free_list_head->prev_free = chunk_to_free;
	}
}

u32 get_random4() {
	char buf[4];
	FILE *fp = fopen("/dev/urandom", "rb");
	size_t ret = fread(buf, 1, 4, fp);
	if (ret != 4) {
		xerror("Getting random bytes failed.");
	}
	return buf[0] + (buf[1] << 8) + (buf[2] << 16) + (buf[3] << 24);
}

void setup_new_arena() {
	void *current_arena_end = xmain_arena.heap_start + HEAP_SIZE;
	memset((void *)xmain_arena.cookie_jar, 0, COOKIE_JAR_SIZE);
	init_main_arena(current_arena_end + 0x1000, xmain_arena.cookie_jar);
	arena_count += 1;
}

void *current_heap_top_ptr() {
	return xmain_arena.heap_start + (HEAP_SIZE - xmain_arena.available);
}

void init_main_arena(void *heap_start, CookieJar *cookie_jar) {
	xmain_arena.head_chunk = NULL;
	xmain_arena.heap_start = heap_start;
	xmain_arena.available = HEAP_SIZE;
	xmain_arena.cookie_jar = cookie_jar;
	xmain_arena.small_chunk_free_list = NULL;

	guard_head.next_free = &guard_tail;
	guard_head.prev_free = &guard_tail;
	
	guard_tail.next_free = &guard_head;
	guard_tail.prev_free = &guard_head;
	

	xmain_arena.large_chunk_free_list = &guard_head;
	srand(seed);
}

u64 gen_cookie() {
	u64 cookie = (((u64)rand()) << 32) | (rand());
	
	// zero out the LSB so that no str-function will be able to leak/overwrite anything
	cookie &= ~0xff;
	return cookie;
}

void init_heap() __attribute__((constructor));
void init_heap()
{
	void *heapaddr = mmap((void *)HEAP_BASE, HEAP_SIZE * MAX_ARENAS, PROT_READ|PROT_WRITE, MAP_ANON|MAP_PRIVATE, -1, 0);
	if (heapaddr == MAP_FAILED) {
		xerror("Error allocating heap.");
	}

	u64 rand_addr = ((u64)get_random4() << 32) | get_random4();
	rand_addr &= 0xffffffff000;
	void *cookie_jar_addr = mmap((void *)rand_addr, COOKIE_JAR_SIZE, PROT_READ|PROT_WRITE, MAP_ANON|MAP_PRIVATE, -1, 0);
	if (cookie_jar_addr == MAP_FAILED) {
		xerror("Error allocating cookie jar.");
	}
	seed = get_random4();
	init_main_arena(heapaddr, (CookieJar *)cookie_jar_addr);
}

void destroy_heap() __attribute__((destructor));
void destroy_heap() {
	munmap(xmain_arena.heap_start, HEAP_SIZE);
	munmap(xmain_arena.cookie_jar, COOKIE_JAR_SIZE);
	memset(&xmain_arena, 0, sizeof(Arena));
}