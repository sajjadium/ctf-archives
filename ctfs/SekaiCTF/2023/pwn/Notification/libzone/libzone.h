/*
	Simple Zone Allocator
	Author: peter
*/
#ifndef LIBZONE_H
#define LIBZONE_H

#include <stdint.h>
#include <sys/cdefs.h>
// use Balance Tree to speed up search time for duplicate hash entry
#include "bltree.h"

#ifdef DEBUG
#define LOG(fmt, ...) fprintf(stderr, fmt, ##__VA_ARGS__);
#else
#define LOG(fmt, ...)
#endif

#define panic(fmt, ...) do { \
		fprintf(stderr, fmt, ##__VA_ARGS__);\
		abort(); \
	} while(0)

#define DEFAULT_PAGE_SIZE 4096

#define PAGE_MAPPED_MAX_THRESHOLD 3
#define PAGE_MAP_MAX_BITMAP 512
#define OBJECT_ALIGMENT (2 * sizeof(size_t))

#define BIT_PER_BYTE sizeof(uint64_t)
#define BIT_ARRAY_SIZE (8 * BIT_PER_BYTE)
#define MIN_OBJECT_PER_MAP 8

#define MAX_ZONE_NAME 64

#define Z_ZONE_BOOTSTRAP_NAME "zone_bootstrap"
#define Z_ZONE_BOOTSTRAP 0
#define Z_ZONE_CHILD 1

#define OUTOFMEM -2
#define MAPERR -1

struct page_mapped;
typedef struct page_mapped* page_mapped_t;

struct page_mapped {
	uint32_t mapped_capacity;
	uint32_t mapped_num_allocation;
	uint32_t mapped_num_free;
	uint32_t page_size;
	void *base_address;
	void *cur_address;
	page_mapped_t next;
	page_mapped_t prev;
	uint64_t bitmap[];
};

struct zone {
	char zone_name[MAX_ZONE_NAME];
	uint32_t flags:1;
	uint32_t object_size; // size of each object
	uint32_t capacity; // maximum number of objects store in this zone
	uint32_t num_allocation; // current number of allocation object
	uint32_t num_freed; // current number of free object
	uint32_t num_page_mapped; // number of page mapped in this zone
	page_mapped_t page_mapped_head; // point to head of mapped page
	page_mapped_t page_min_num_free; // point to page has smallest number of free chunk
	page_mapped_t page_min_num_alloc; // point to page has largest number of free chunk
	// because hashtable could have duplicate item
	// we add this Balance Tree for each node in hashtable to store duplicate item
	// to make sure when we search a zone by name the time complexity is O(log(N))
	BLTREE_ROOT_DECL(blnode);
};
typedef struct zone* zone_t;

struct zone_hashtable {
	uint32_t capacity; // size of this hashtable
	uint32_t num_zone; // current number of zone in this hashtable
	uint32_t page_size; // size of memory page
	struct zone zone_bootstrap; // bootstrap zone attached in zone_hashtable to allocate a zone object
	zone_t zones[]; // array of zone_t pointer
};
typedef struct zone_hashtable* zone_hastable_t;

extern zone_hastable_t zone_table;
extern uint64_t        cookie[2]; // 0x10 bytes for cookie padding

#ifdef USE_ZONE_SIZE
#define DEFAULT_ZONE_SIZE USE_ZONE_SIZE
#else
#define DEFAULT_ZONE_SIZE ((DEFAULT_PAGE_SIZE - sizeof(struct zone_hashtable)) / sizeof(zone_t))
#endif

#define PAGEMAP_INIT_HEAD(zone, pagep) do {\
		zone->page_mapped_head       = pagep;\
		zone->page_mapped_head->next = zone->page_mapped_head;\
		zone->page_mapped_head->prev = zone->page_mapped_head;\
	} while(0)

#define PAGEMAP_HEAD(zone) zone->page_mapped_head
#define PAGEMAP_TAIL(zone) zone->page_mapped_head->prev

#define PAGEMAP_APPEND(zone, pagep) do { \
		page_mapped_t tailp; \
		tailp = PAGEMAP_TAIL(zone); \
		tailp->next = pagep; \
		pagep->prev = tailp; \
		pagep->next = PAGEMAP_HEAD(zone); \
		PAGEMAP_TAIL(zone) = pagep; \
	}while(0)

#define PAGEMAP_REMOVE(zone, pagep) do { \
		page_mapped_t ppage; \
		if(PAGEMAP_HEAD(zone) == pagep) {\
			ppage = PAGEMAP_HEAD(zone)->next; \
			ppage->prev = PAGEMAP_TAIL(zone); \
			PAGEMAP_TAIL(zone)->next = ppage; \
			PAGEMAP_HEAD(zone) = ppage; \
		} else if(PAGEMAP_TAIL(zone) == pagep) { \
			ppage = PAGEMAP_TAIL(zone)->prev; \
			ppage->next = PAGEMAP_HEAD(zone); \
			PAGEMAP_TAIL(zone) = ppage; \
		} else {\
			for(ppage = PAGEMAP_HEAD(zone); ppage->next != pagep; ppage = ppage->next); \
			ppage->next = pagep->next; \
			pagep->next->prev = ppage; \
		}\
	}while(0)

#define BIT64_SET(bit_array, bit_idx) (bit_array |= (1ULL << bit_idx))
#define BIT64_CLEAR(bit_array, bit_idx) (bit_array &= ~(1ULL << bit_idx))
#define BIT64_IS_SET(bit_array, bit_idx) ((bit_array >> bit_idx) & 1)
#define BIT64_IS_NOT_SET(bit_array, bit_idx) (!BIT64_IS_SET(bit_array, bit_idx))

__BEGIN_DECLS

void  zone_create(const char *zone_name, uint32_t object_size); // create a new zone for specific object
void* zone_alloc(const char *zone_name); // alloc a new object
void  zone_free(const char *zone_name, void *ptr); // free an object

#ifdef DEBUG
void zone_list();
void zone_list2();
#endif

#ifdef USEZMALLOC
#define MIN_CHUNK_SIZE 0x10

#define ZMALLOC_SIZE_ARRAY_LENGTH 19
const uint32_t zmalloc_size_array[] = {16, 32, 48, 64, 80, 96, 128, 160, 192, 256, 320, 384, 448, 512, 768, 1024, 2048, 4096, 8192};

void* zmalloc(size_t size);
void* zcalloc(size_t count, size_t object_size);
void* zrealloc(void *old_ptr, size_t old_size, size_t size);
void  zfree(void *ptr, size_t ptr_size);
#endif

__END_DECLS

// don't public this functions
// void zone_table_init();
// void zone_table_deinit();
#endif
