#include "heap.h"
#include "heap_internal.h"
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>


CageHeap* cage_default_heap(void) {
	static CageHeap s_default_heap;
	static bool s_default_heap_initialized;
	
	if(!s_default_heap_initialized) {
		s_default_heap_initialized = true;
		s_default_heap.free_tree.prev = heap_adj_make(NULL, RBA_DEFAULT, 0);
		s_default_heap.free_tree.cur = heap_adj_make(NULL, RBA_FREE, 0);
	}
	
	return &s_default_heap;
}

/*! Traverses the free tree until `node` is found, returning its parent */
static HeapMetadata* free_tree_find_parent(HeapMetadata* tree, HeapMetadata* node) {
	assert(heap_meta_is_free(tree));
	assert(heap_meta_is_free(node));
	
	// Look at how this node's value compares to the tree node's value
	HeapUnits units = heap_meta_get_cur_units(node);
	HeapUnits tree_units = heap_meta_get_cur_units(tree);
	
	assert(units != 0);
	
	// Bigger or same size?
	if(units >= tree_units) {
		// Look at the bigger subtree
		HeapMetadata* bigger = heap_meta_get_bigger(tree);
		if(bigger == node) {
			// Bigger child is the target node, all done
			return tree;
		}
		
		// Recurse to the bigger subtree
		HeapMetadata* parent = free_tree_find_parent(bigger, node);
		if(parent != NULL) {
			return parent;
		}
	}
	
	// Smaller or same size?
	if(units <= tree_units) {
		// Look at the smaller subtree
		HeapMetadata* smaller = heap_meta_get_smaller(tree);
		if(smaller == node) {
			// Smaller child is the target node, all done
			return tree;
		}
		
		// Recurse to the smaller subtree
		HeapMetadata* parent = free_tree_find_parent(smaller, node);
		if(parent != NULL) {
			return parent;
		}
	}
	
	// Not found in this subtree
	return NULL;
}

/*! Remove `node` (which is a child of `parent`) from the free tree, moving its children as necessary.
 * This is usually done because `node` is being converted into an allocated chunk.
 */
static void free_tree_remove(CageHeap* heap, HeapMetadata* node, HeapMetadata* parent) {
	assert(heap_meta_is_free(node));
	
	// Metadata objects with 0 units will not be in the free tree
	if(heap_meta_get_cur_units(node) == 0) {
		return;
	}
	
	// TODO: red-black
	
	// Search the tree for the parent if it's passed as NULL
	if(parent == NULL) {
		parent = free_tree_find_parent(&heap->free_tree, node);
	}
	
	assert(heap_meta_is_free(parent));
	
	// Is node the smaller child or bigger child?
	if(node == heap_meta_get_smaller(parent)) {
		// Bring node's larger subtree up to replace the node
		HeapMetadata* bigger = heap_meta_get_bigger(node);
		if(bigger != NULL) {
			// Move deleted node's bigger subtree up to replace that node
			heap_meta_set_smaller(parent, bigger);
			
			// Find smallest node of node's larger subtree
			parent = bigger;
			HeapMetadata* going_smaller;
			while((going_smaller = heap_meta_get_smaller(parent)) != NULL) {
				parent = going_smaller;
			}
		}
		
		// Move node's smaller subtree under the smallest node left under parent
		heap_meta_set_smaller(parent, heap_meta_get_smaller(node));
	}
	else {
		assert(node == heap_meta_get_bigger(parent));
		
		// Bring node's smaller subtree up to replace the node
		HeapMetadata* smaller = heap_meta_get_smaller(node);
		if(smaller != NULL) {
			// Move deleted node's smaller subtree up to replace that node
			heap_meta_set_bigger(parent, smaller);
			
			// Find biggest node of node's smaller subtree
			parent = smaller;
			HeapMetadata* going_bigger;
			while((going_bigger = heap_meta_get_bigger(parent)) != NULL) {
				parent = going_bigger;
			}
		}
		
		// Move node's bigger subtree under the biggest node left under parent
		heap_meta_set_bigger(parent, heap_meta_get_bigger(node));
	}
	
	// Mark node as allocated
	heap_meta_set_allocated(node, RBA_ALLOCATED);
}


/*! Search through `node` for the smallest block large enough to hold `units` */
static HeapMetadata* free_tree_search(CageHeap* heap, HeapMetadata* node, HeapMetadata* parent, HeapUnits units) {
	// No nodes in the free tree large enough to hold the requested size
	if(node == NULL) {
		return NULL;
	}
	
	assert(heap_meta_is_free(parent));
	assert(node == heap_meta_get_smaller(parent) || node == heap_meta_get_bigger(parent));
	assert(heap_meta_is_free(node));
	
	HeapUnits cur_units = heap_meta_get_cur_units(node);
	
	assert(cur_units != 0);
	
	// Is the requested size larger than the current node?
	if(cur_units < units) {
		return free_tree_search(heap, heap_meta_get_bigger(node), node, units);
	}
	
	// Is the requested size smaller than the current node?
	if(cur_units > units) {
		HeapMetadata* found = free_tree_search(heap, heap_meta_get_smaller(node), node, units);
		if(found != NULL) {
			return found;
		}
		
		// If we didn't find a node smaller than this one, just use this node
		// as it is big enough to hold the requested size
	}
	
	// Pulling out the current node, so remove it from the tree
	free_tree_remove(heap, node, parent);
	return node;
}

/*! Mark `node` as being free */
static void mark_free_node(HeapMetadata* node) {
	// Mark as free
	heap_meta_set_allocated(node, RBA_FREE);
	
	// No children in the free tree yet
	heap_meta_set_bigger(node, NULL);
	heap_meta_set_smaller(node, NULL);
}

/*! Insert `node` into the binary search free tree `tree` */
static void free_tree_insert(HeapMetadata* tree, HeapMetadata* node) {
	assert(heap_meta_is_free(tree));
	
	// There's no sense in adding a node with 0 units to the free tree.
	// Just leave it hanging around in the heap, because the next time an
	// adjacent object is freed it will automatically be coalesced and
	// added to the free tree at that time.
	if(heap_meta_get_cur_units(node) == 0) {
		return;
	}
	
	// TODO: red-black
	
	if(heap_meta_get_cur_units(node) >= heap_meta_get_cur_units(tree)) {
		// Insert down right subtree
		HeapMetadata* bigger = heap_meta_get_bigger(tree);
		if(bigger == NULL) {
			mark_free_node(node);
			heap_meta_set_bigger(tree, node);
		}
		else {
			free_tree_insert(bigger, node);
		}
	}
	else {
		// Insert down left subtree
		HeapMetadata* smaller = heap_meta_get_smaller(tree);
		if(smaller == NULL) {
			mark_free_node(node);
			heap_meta_set_smaller(tree, node);
		}
		else {
			free_tree_insert(smaller, node);
		}
	}
}

/*! Create a new heap mapping large enough to contain an object of `units` */
static HeapMetadata* allocate_free_block(CageHeap* heap, HeapUnits units) {
	// TODO: Handle this case by marking the object as the only one in the arena somehow
	if(units > HEAP_MAX_ALLOC_UNITS) {
		return NULL;
	}
	
	// Convert size from number of units of size HEAP_ALLOC_GRANULARITY to a multiple
	// of PAGE_SIZE bytes that's large enough to hold the requested size
	size_t map_size = (size_t)(3 + units) * HEAP_ALLOC_GRANULARITY;
	map_size += PAGE_SIZE - 1;
	map_size /= PAGE_SIZE;
	map_size *= PAGE_SIZE;
	
	// Map entire heap region
	void* block = mmap(NULL, map_size + 2 * sizeof(GuardPage), PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
	if(block == MAP_FAILED) {
		return NULL;
	}
	
	// Change mapping of first page to PROT_NONE as a guard page
	int status;
	status = mprotect(block, sizeof(GuardPage), PROT_NONE);
	if(status < 0) {
		abort();
	}
	
	// Change mapping of last page to PROT_NONE as a guard page
	void* guard_post = (char*)block + sizeof(GuardPage) + map_size;
	status = mprotect(guard_post, sizeof(GuardPage), PROT_NONE);
	if(status < 0) {
		abort();
	}
	
	// Create header metadata
	ArenaHeader* header = (ArenaHeader*)((char*)block + sizeof(GuardPage));
	header->page_count = map_size / PAGE_SIZE;
	
	// Insert new block at the front of the linked list
	header->next = heap->arena_list;
	heap->arena_list = header;
	
	// Create free tree node but don't add it to the tree yet
	HeapMetadata* free_node = (HeapMetadata*)(header + 1);
	free_node->prev = heap_adj_make(NULL, RBA_DEFAULT, HEAP_META_BOOKEND);
	
	// Subtract three because of the ArenaHeader, this HeapMetadata, and the end HeapMetadata
	HeapUnits obj_units = (HeapUnits)(map_size / HEAP_ALLOC_GRANULARITY - 3);
	free_node->cur = heap_adj_make(NULL, RBA_ALLOCATED, obj_units);
	
	// Write end metadata block
	HeapMetadata* meta_end = (HeapMetadata*)((char*)header + map_size - sizeof(*meta_end));
	meta_end->prev = heap_adj_make(NULL, RBA_DEFAULT, obj_units);
	meta_end->cur = heap_adj_make(NULL, RBA_ALLOCATED, HEAP_META_BOOKEND);
	
	return free_node;
}


void* cage_malloc(CageHeap* heap, size_t size) {
	// malloc(0) -> NULL, and too large malloc size returns NULL
	if(size == 0 || size > HEAP_MAX_ALLOC_SIZE) {
		return NULL;
	}
	
	// Use default heap if NULL
	if(heap == NULL) {
		heap = cage_default_heap();
	}
	
	// Convert from size in bytes to number of units needed to hold requested size (including metadata)
	HeapUnits units = (HeapUnits)((size + HEAP_ALLOC_GRANULARITY - 1) / HEAP_ALLOC_GRANULARITY);
	
	// Search the free tree for an available free object
	HeapMetadata* new_meta = free_tree_search(heap, heap_meta_get_bigger(&heap->free_tree), &heap->free_tree, units);
	if(new_meta == NULL) {
		// No free node large enough, so map a new heap region
		new_meta = allocate_free_block(heap, units);
		if(new_meta == NULL) {
			return NULL;
		}
	}
	
	assert(heap_meta_is_allocated(new_meta));
	assert(heap_meta_get_cur_units(new_meta) >= units);
	
	// Check if there is more than enough space in the free node to hold the new object,
	// splitting it if so
	HeapUnits extra_units = heap_meta_get_cur_units(new_meta) - units;
	heap_meta_set_cur_units(new_meta, units);
	
	if(extra_units > 0) {
		// Build free node in extra space
		HeapMetadata* free_node = heap_meta_get_next(new_meta);
		free_node->prev = heap_adj_make(NULL, RBA_DEFAULT, units);
		free_node->cur = heap_adj_make(NULL, RBA_FREE, extra_units - 1);
		
		// Update next->prev.units
		HeapMetadata* next = free_node + extra_units;
		heap_meta_set_prev_units(next, extra_units - 1);
		
		assert(heap_meta_get_next(free_node) == next);
		assert(free_node == heap_meta_get_prev(next));
		
		// Insert resized free node back into the free tree
		free_tree_insert(&heap->free_tree, free_node);
		
		assert(heap_meta_get_next(new_meta) == free_node);
		assert(new_meta == heap_meta_get_prev(free_node));
	}
	
	// Returned object comes directly after metadata unit
	return new_meta + 1;
}


/*! Merge `obj` and `next`, which must be adjacent objects, into a single big object */
static HeapMetadata* coalesce_adjacent_objects(HeapMetadata* obj, HeapMetadata* next) {
	assert(heap_meta_get_next(obj) == next);
	assert(obj == heap_meta_get_prev(next));
	
	// Look up sizes, then update first size. Plus one for merging the metadata block
	HeapUnits next_units = heap_meta_get_cur_units(next);
	HeapUnits coalesced_units = heap_meta_get_cur_units(obj) + 1 + next_units;
	
	// Add sizes, plus one for merging the metadata block into the object's size
	heap_meta_set_cur_units(obj, coalesced_units);
	
	// Update following metadata block's prev size
	HeapMetadata* after = obj + 1 + coalesced_units;
	heap_meta_set_prev_units(after, coalesced_units);
	
	{
		HeapMetadata* prev = heap_meta_get_prev(obj);
		if(prev != NULL) {
			assert(heap_meta_get_next(prev) == obj);
		}
		
		assert(heap_meta_get_next(obj) == after);
		assert(obj == heap_meta_get_prev(after));
	}
	
	// Return value is first object that has been expanded by consuming its next object
	return obj;
}

void cage_free(CageHeap* heap, void* obj) {
	// free(NULL) does nothing
	if(obj == NULL) {
		return;
	}
	
	// Use default heap if NULL
	if(heap == NULL) {
		heap = cage_default_heap();
	}
	
	// Use preceeding metadata object to find object's size
	HeapMetadata* meta = (HeapMetadata*)obj - 1;
	if(heap_meta_is_free(meta)) {
		// Double-free detected
		abort();
	}
	
	// Is there an object before the newly freed one, or are we at the left bookend?
	HeapMetadata* prev = heap_meta_get_prev(meta);
	if(prev != NULL && heap_meta_is_free(prev)) {
		// Previous object is freed, so coalesce it with this one
		free_tree_remove(heap, prev, NULL);
		meta = coalesce_adjacent_objects(prev, meta);
	}
	
	// Is the object after the current one free? (Right bookend is marked as allocated)
	HeapMetadata* next = heap_meta_get_next(meta);
	if(heap_meta_is_free(next)) {
		// Next object is freed, so coalesce it with this one
		free_tree_remove(heap, next, NULL);
		meta = coalesce_adjacent_objects(meta, next);
	}
	
	// Insert the free node into the tree
	free_tree_insert(&heap->free_tree, meta);
}

void* cage_realloc(CageHeap* heap, void* obj, size_t new_size) {
	// Max size check
	if(new_size > HEAP_MAX_ALLOC_SIZE) {
		return NULL;
	}
	
	// Use default heap if NULL
	if(heap == NULL) {
		heap = cage_default_heap();
	}
	
	// realloc(NULL, size) -> malloc(size)
	if(obj == NULL) {
		return cage_malloc(heap, new_size);
	}
	
	// realloc(obj, 0) -> free(obj)
	if(new_size == 0) {
		cage_free(heap, obj);
		return NULL;
	}
	
	// Pointer to the object after reallocating
	void* new_obj = NULL;
	
	// Convert from size in bytes to number of units needed to hold requested size
	HeapUnits units = (HeapUnits)((new_size + HEAP_ALLOC_GRANULARITY - 1) / HEAP_ALLOC_GRANULARITY);
	
	// Look up metadata to get the object's size
	HeapMetadata* meta = (HeapMetadata*)obj - 1;
	
	// Shrink or grow?
	HeapUnits obj_units = heap_meta_get_cur_units(meta);
	size_t obj_size = obj_units * HEAP_ALLOC_GRANULARITY;
	
	// Get info about adjacent objects
	HeapMetadata* next = heap_meta_get_next(meta);
	HeapMetadata* prev = heap_meta_get_prev(meta);
	
	if(units <= obj_units) {
		HeapUnits shrink_by = obj_units - units;
		
		// Are we shrinking the allocation?
		if(shrink_by > 0) {
			// Update cur units
			heap_meta_set_cur_units(meta, units);
			
			// Shrinking is easy, just decrease the allocated size in the metadata and
			// add the extra data at the end as a new free block
			HeapMetadata* free_node = meta + 1 + units;
			free_node->prev = heap_adj_make(NULL, RBA_DEFAULT, units);
			free_node->cur = heap_adj_make(NULL, RBA_FREE, shrink_by - 1);
			
			// Update previous size in metadata following new free object
			heap_meta_set_prev_units(next, shrink_by - 1);
			
			// Add the new node to the free tree
			free_tree_insert(&heap->free_tree, free_node);
		}
		
		// Return the original object (it didn't go away, just got smaller)
		new_obj = obj;
	}
	else {
		/*
		 * Need to expand the allocation, so there are three cases to handle:
		 *
		 * 1. Next object is free and coalescing into next would be large enough for new size
		 * 2. Both next and prev objects are free and coalescing into both would be large enough
		 * 3. Not possible to coalesce with adjacent objects for enough space, need to allocate
		 *    new object, copy into that, and free current object.
		 *
		 * Strategy to handle these cases:
		 *
		 * if next object is free:
		 *     consider coalescing into next object
		 * if size after possible coalescing is still not large enough and prev object is free:
		 *     consider coalescing into prev object
		 * if size would be large enough after coalescing:
		 *     coalesce forwards and potentially backwards
		 *     if coalesced backwards:
		 *         memmove data from old object start backwards to new object start
		 * else:
		 *     allocate new object, copy into that, free current object (after coalescing)
		 */
		
		bool coalesce_forward = false;
		bool coalesce_backward = false;
		HeapUnits coalesced_units = obj_units;
		
		// Consider coalescing into next object
		if(heap_meta_is_free(next)) {
			coalesce_forward = true;
			coalesced_units += 1 + heap_meta_get_cur_units(next);
		}
		
		// Consider coalescing into prev object
		if(coalesced_units < units && prev != NULL && heap_meta_is_free(prev)) {
			coalesce_backward = true;
			coalesced_units += 1 + heap_meta_get_cur_units(prev);
		}
		
		// Will coalescing make the allocation large enough?
		if(coalesced_units >= units) {
			if(coalesce_forward) {
				// Coalesce into next object
				free_tree_remove(heap, next, NULL);
				meta = coalesce_adjacent_objects(meta, next);
			}
			
			if(coalesce_backward) {
				// Coalesce into previous object
				free_tree_remove(heap, prev, NULL);
				meta = coalesce_adjacent_objects(prev, meta);
				
				// Copy object contents to new start
				new_obj = meta + 1;
				memmove(new_obj, obj, obj_size);
			}
			else {
				// Object start didn't move
				new_obj = obj;
			}
		}
		else {
			// Cannot enlarge in-place, must allocate a new object and copy the data there
			new_obj = cage_malloc(heap, new_size);
			if(!new_obj) {
				return NULL;
			}
			
			// Copy existing object data into the new, larger object
			memcpy(new_obj, obj, obj_size);
			
			// Free this now-unnecessary object
			cage_free(heap, obj);
		}
	}
	
	return new_obj;
}

CageHeap* create_cage(void) {
	// Use a temporary stack object as the heap descriptor
	CageHeap heap = {0};
	
	// Allocate new heap object using temporary stack heap descriptor
	CageHeap* ret = cage_malloc(&heap, sizeof(*ret));
	if(ret != NULL) {
		// Copy heap descriptor into the new heap allocation
		memcpy(ret, &heap, sizeof(heap));
	}
	
	return ret;
}

void destroy_cage(CageHeap* heap) {
	if(heap == NULL) {
		return;
	}
	
	// Unmap each arena's mmap region
	ArenaHeader* arena = heap->arena_list;
	while(arena != NULL) {
		ArenaHeader* next = arena->next;
		
		// Compute mmap region start and size
		void* map = (char*)arena - PAGE_SIZE;
		size_t map_size = (2 + arena->page_count) * PAGE_SIZE;
		
		// Unmap mapped memory for this heap arena
		int status = munmap(map, map_size);
		if(status != 0) {
			abort();
		}
		
		// Advance to the next heap arena
		arena = next;
	}
}
