#ifndef CAGE_HEAP_INTERNAL_H
#define CAGE_HEAP_INTERNAL_H

#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>
#include <limits.h>
#include <sys/user.h>
#include <inttypes.h>
#include <assert.h>
#include "heap.h"

/*! @file heap_internal.h
 *
 * Heap layout
 * =====
 *
 * This heap implementation uses the following layout for a heap mapping:
 *
 * ```
 * GUARD PAGE PRE (1 page, no access)
 * HEAP CONTENTS (n pages, rw access)
 * {
 *     // One header per heap zone, defines number of pages for this heap
 *     // contents region
 *     ArenaHeader header;
 *
 *     // One or more objects, surrounded and separated by HeapMetadata
 *     HeapMetadata { object HeapMetadata } object HeapMetadata
 * }
 * GUARD PAGE POST (1 page, no access)
 * ```
 *
 * The heap data is all in multiples of HEAP_ALLOC_GRANULARITY, which is the
 * size of HeapMetadata and ArenaHeader.
 *
 ******************************************************************************
 *
 * Free Tree format
 * =====
 *
 * Freed objects are tracked using a binary free tree. Objects to the left are
 * smaller than objects to the right. This is a self-balancing binary search
 * tree, implemented using a binary search tree. In a future update, this may
 * instead be a red-black tree, using the `rba` bit to track node colors.
 *
 * When a freed object is selected to be allocated, it is removed from the free
 * tree and its `cur->rba` bit is set to `RBA_ALLOCATED` to signify that the
 * current object is allocated.
 *
 * When an object is freed, the heap metadata directly before it is used as the
 * free tree node. The pointer value in its `cur` member points to the right
 * (bigger) free tree node child, and the pointer value in its `prev` member
 * points to the left (smaller) free tree node child. Any of the two children
 * may be NULL. The object's `cur->rba` bit will be set to `RBA_FREE`.
 *
 * After an object has been freed, the blocks directly before and after the
 * newly freed object are examined. If they are also free blocks, they will be
 * coalesced into a single larger free block.
 * 
 * Blocks with a `units` value of zero are never added to the free tree. They
 * will only be added to the free tree after they are coalesced into a larger
 * object during a `free` or `realloc` call.
 * 
 * When an object is resized using `realloc`:
 * 
 * If the new size is smaller, the object's `units` value will be shrunk, and
 * any extra units at the end are coalesced with the freed object to their
 * right (if any) before being inserted into the free tree (if units > 0).
 * 
 * If the new size is larger, the algorithm will first examine the object after
 * the current one. If it is free, it will be coalesced with the current
 * object. If the allocation is now large enough to hold the requested size,
 * then any extra units at the end will be turned into a new free node and
 * inserted into the free tree if units > 0. If the allocation size is still
 * too small, then the previous object will be examined. If the previous object
 * is free, then it will be coalesced into the current one. If the size is now
 * large enough, the data will be moved to the new beginning of the object, and
 * any extra units will be converted into a new free node, inserting into the
 * free tree if units > 0. If the new size is still not large enough, a new
 * object will instead be allocated of the requested size, the data will be
 * copied from the old object to the new one, and the entire current object
 * will be freed and added to the free tree.
 */

// Forward declarations of structures
typedef struct HeapMetadata HeapMetadata;
typedef struct GuardPage GuardPage;
typedef struct ArenaHeader ArenaHeader;
typedef uint32_t HeapUnits;
typedef union {
	bool is_black;
	bool is_allocated;
	bool raw;
} HeapRBA;
#define PRIuHU PRIu32

/*! Defines a bitmask containing `bits` number of bits */
#define MAKE_MASK(bits) ((1ULL << (bits)) - 1ULL)

/*! Bit-packed value. Pointers to free nodes have unused bits in them, specifically
 * the top 16 bits are unused (64-bit pointers only use 48 bits), and as all free nodes
 * are 16-byte aligned, the bottom 4 bits are unused. Therefore, the pointer value can
 * be stored in as little as 44 bits. This leaves 20 bits to use for whatever is needed.
 * 
 * Format of HeapAdjacency:
 * 
 * | 63-20   | 19  |  18-0  |
 * |---------|-----|--------|
 * | pointer | rba | ~units |
 * 
 * `pointer` is either NULL or a pointer to a child free tree node, either `smaller` or
 * `bigger`.
 * 
 * `rba` is a bit that changes meaning when this is in `node->prev` or `node->cur`. For
 * `node->cur.rba`, 1 means the following object is allocated and 0 means it's free. When
 * `node` is free, then `node->prev.rba` is 0 if the free node is red and 1 if it's black.
 * When `node` is allocated, `node->prev.rba` has no meaning. RB-tree not yet implemented!
 * 
 * `units` is the number of 16-byte units contained in the adjacent heap object.
 */
typedef uintptr_t HeapAdjacency;

/*! Bitmasks and other constants for manipulating metadata values */
#define HEAP_META_POINTER_BITS 44U
#define HEAP_META_POINTER_SHIFT 20U
#define HEAP_META_POINTER_MASK ((HeapAdjacency)MAKE_MASK(HEAP_META_POINTER_BITS))

#define HEAP_META_RBA_BITS 1U
#define HEAP_META_RBA_SHIFT 19U
#define HEAP_META_RBA_MASK ((HeapAdjacency)MAKE_MASK(HEAP_META_RBA_BITS))

#define HEAP_META_UNITS_BITS 19U
#define HEAP_META_UNITS_SHIFT 0U
#define HEAP_META_UNITS_MASK ((HeapAdjacency)MAKE_MASK(HEAP_META_UNITS_BITS))

// Values for the `rba` bit
#define RBA_RED ((HeapRBA){.is_black = false})
#define RBA_BLACK ((HeapRBA){.is_black = true})
#define RBA_DEFAULT RBA_RED
#define RBA_ALLOCATED ((HeapRBA){.is_allocated = true})
#define RBA_FREE ((HeapRBA){.is_allocated = false})

/*! All allocated objects are rounded up to a multiple of this size */
#define HEAP_ALLOC_GRANULARITY ((size_t)(2UL * sizeof(HeapAdjacency)))

/*! Number of units should never be greater than this value (8MiB - 3 units for metadata) */
#define HEAP_MAX_ALLOC_UNITS ((HeapUnits)((1U << HEAP_META_UNITS_BITS) - 3))

/*! Maximum bytes per allocation = 8MiB - 3 units for metadata */
#define HEAP_MAX_ALLOC_SIZE ((size_t)HEAP_MAX_ALLOC_UNITS * (size_t)HEAP_ALLOC_GRANULARITY)

/*! As the units value, marks that there is no object in this direction (it is at one end of the arena) */
#define HEAP_META_BOOKEND ((HeapUnits)(HEAP_MAX_ALLOC_UNITS + 1))

//TODO: For objects larger than HEAP_MAX_ALLOC_SIZE, allow an object to be the only one in the
//mapped arena. Will be marked with units=(HeapUnits)-1, aka HEAP_META_BOOKEND + 1.

//TODO: Consider adding a parent pointer by using the next object's prev.pointer

/*! Data placed between heap allocations and at either end of the heap contents */
struct HeapMetadata {
	/*! Stores the size of the previous object and, when allocated, the `smaller` free tree link */
	HeapAdjacency prev;
	
	/*! Stores the size of the current object and, when allocated, the `bigger` free tree link */
	HeapAdjacency cur;
};

static_assert(
	sizeof(HeapMetadata) == HEAP_ALLOC_GRANULARITY,
	"The HeapMetadata struct is expected to be the size of one heap unit"
);

/* Utility functions to manipulate metadata values */

static inline bool heap_units_valid(HeapUnits units) {
	return units <= HEAP_MAX_ALLOC_UNITS;
}

static inline void* heap_adj_get_pointer(HeapAdjacency adj) {
	return (void*)(((adj >> HEAP_META_POINTER_SHIFT) & HEAP_META_POINTER_MASK) << 4);
}

static inline HeapAdjacency heap_adj_set_pointer(HeapAdjacency adj, void* ptr) {
	return (
		// Mask off pointer bits in `adj`
		(adj & ~(HEAP_META_POINTER_MASK << HEAP_META_POINTER_SHIFT))
		
		// Set pointer bits to the bits from `ptr`, shifted into place
		| ((HeapAdjacency)((uintptr_t)ptr >> 4) << HEAP_META_POINTER_SHIFT)
	);
}

static inline HeapRBA heap_adj_get_rba(HeapAdjacency adj) {
	return (HeapRBA){.raw = ((adj >> HEAP_META_RBA_SHIFT) & HEAP_META_RBA_MASK)};
}

static inline bool heap_meta_is_allocated(HeapMetadata* meta) {
	return heap_adj_get_rba(meta->cur).is_allocated;
}

static inline bool heap_meta_is_free(HeapMetadata* meta) {
	return !heap_adj_get_rba(meta->cur).is_allocated;
}

static inline HeapUnits heap_adj_get_units(HeapAdjacency adj) {
	return (HeapUnits)(HEAP_META_UNITS_MASK & ~(adj >> HEAP_META_UNITS_SHIFT));
}

static inline HeapUnits heap_meta_get_prev_units(HeapMetadata* meta) {
	return heap_adj_get_units(meta->prev);
}

static inline HeapUnits heap_meta_get_cur_units(HeapMetadata* meta) {
	return heap_adj_get_units(meta->cur);
}

static inline HeapMetadata* heap_meta_get_smaller(HeapMetadata* meta) {
	assert(heap_meta_is_free(meta));
	HeapMetadata* smaller = heap_adj_get_pointer(meta->prev);
	
	if(smaller != NULL) {
		assert(heap_meta_get_cur_units(smaller) < heap_meta_get_cur_units(meta));
	}
	
	return smaller;
}

static inline void heap_meta_set_smaller(HeapMetadata* meta, HeapMetadata* smaller) {
	assert(heap_meta_is_free(meta));
	
	if(smaller != NULL) {
		assert(heap_meta_get_cur_units(smaller) < heap_meta_get_cur_units(meta));
	}
	
	meta->prev = heap_adj_set_pointer(meta->prev, smaller);
}

static inline HeapMetadata* heap_meta_get_bigger(HeapMetadata* meta) {
	assert(heap_meta_is_free(meta));
	HeapMetadata* bigger = heap_adj_get_pointer(meta->cur);
	
	if(bigger != NULL) {
		assert(heap_meta_get_cur_units(bigger) >= heap_meta_get_cur_units(meta));
	}
	
	return bigger;
}

static inline void heap_meta_set_bigger(HeapMetadata* meta, HeapMetadata* bigger) {
	assert(heap_meta_is_free(meta));
	
	if(bigger != NULL) {
		assert(heap_meta_get_cur_units(bigger) >= heap_meta_get_cur_units(meta));
	}
	
	meta->cur = heap_adj_set_pointer(meta->cur, bigger);
}

static inline bool heap_meta_is_red(HeapMetadata* meta) {
	assert(heap_meta_is_free(meta));
	return !heap_adj_get_rba(meta->prev).is_black;
}

static inline bool heap_meta_is_black(HeapMetadata* meta) {
	assert(heap_meta_is_free(meta));
	return heap_adj_get_rba(meta->prev).is_black;
}

static inline HeapAdjacency heap_adj_set_rba(HeapAdjacency adj, HeapRBA rba) {
	return (
		// Mask off rba bit in `adj`
		(adj & ~(HEAP_META_RBA_MASK << HEAP_META_RBA_SHIFT))
		
		// Replace rba bit with value of `rba`
		| ((HeapAdjacency)rba.raw << HEAP_META_RBA_SHIFT)
	);
}

static inline void heap_meta_set_color(HeapMetadata* meta, HeapRBA color) {
	assert(heap_meta_is_free(meta));
	meta->prev = heap_adj_set_rba(meta->prev, color);
}

static inline void heap_meta_set_allocated(HeapMetadata* meta, HeapRBA allocated) {
	meta->cur = heap_adj_set_rba(meta->cur, allocated);
}

static inline HeapAdjacency heap_adj_set_units(HeapAdjacency adj, HeapUnits units) {
	return (
		// Mask on units bits in `adj`
		(adj | (HEAP_META_UNITS_MASK << HEAP_META_UNITS_SHIFT))
		
		// Turn off bits from `units`
		& ~((HeapAdjacency)units << HEAP_META_UNITS_SHIFT)
	);
}

static inline void heap_meta_set_prev_units(HeapMetadata* meta, HeapUnits prev_units) {
	meta->prev = heap_adj_set_units(meta->prev, prev_units);
}

static inline void heap_meta_set_cur_units(HeapMetadata* meta, HeapUnits cur_units) {
	meta->cur = heap_adj_set_units(meta->cur, cur_units);
}

static inline HeapMetadata* heap_meta_get_prev(HeapMetadata* meta) {
	HeapUnits prev_units = heap_meta_get_prev_units(meta);
	if(!heap_units_valid(prev_units)) {
		return NULL;
	}
	
	return meta - prev_units - 1;
}

static inline HeapMetadata* heap_meta_get_next(HeapMetadata* meta) {
	HeapUnits cur_units = heap_meta_get_cur_units(meta);
	if(!heap_units_valid(cur_units)) {
		return NULL;
	}
	
	return meta + 1 + cur_units;
}

static inline HeapAdjacency heap_adj_make(void* pointer, HeapRBA rba, HeapUnits units) {
	return (
		((HeapAdjacency)((uintptr_t)pointer >> 4) << HEAP_META_POINTER_SHIFT)
		| ((HeapAdjacency)rba.raw << HEAP_META_RBA_SHIFT)
		| (((HeapAdjacency)(HEAP_META_UNITS_MASK & ~units)) << HEAP_META_UNITS_SHIFT)
	);
}

/*! Used to define an isolated heap */
struct CageHeap {
	ArenaHeader* arena_list;
	HeapMetadata free_tree;
};

/*! Objects of this type will always be mapped as guard pages with PROT_NONE */
struct GuardPage {
	char noaccess[PAGE_SIZE];
};

/*! Used to keep the arenas in a linked list */
struct ArenaHeader {
	size_t page_count;
	ArenaHeader* next;
};

static_assert(
	sizeof(ArenaHeader) == HEAP_ALLOC_GRANULARITY,
	"The ArenaHeader struct must fit in a single heap unit"
);


/*! Retrieve the default heap pointer */
CageHeap* cage_default_heap(void);

#endif /* CAGE_HEAP_INTERNAL_H */
