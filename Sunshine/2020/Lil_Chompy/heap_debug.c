#include "heap_debug.h"
#include "heap_internal.h"
#include <inttypes.h>
#include <stdbool.h>
#include <stdio.h>


static void drawMeta(FILE* fout, HeapMetadata* node) {
	// Default color when a heap metadata struct is corrupt
	const char* color;
	const char* node_type;
	bool is_free = heap_meta_is_free(node);
	if(is_free) {
		color = "mistyrose";
		if(heap_meta_is_red(node)) {
			node_type = "free, red";
		}
		else {
			node_type = "free, black";
		}
	}
	else {
		color = "palegreen";
		node_type = "live";
	}
	
	// Node formatting
	HeapUnits prev_units = heap_meta_get_prev_units(node);
	HeapUnits cur_units = heap_meta_get_cur_units(node);
	const char* prev_str;
	const char* cur_str;
	char prev_buf[20] = {};
	char cur_buf[20] = {};
	
	// Get string for prev_units
	if(prev_units == HEAP_META_BOOKEND) {
		prev_str = "HEAP_META_BOOKEND";
	}
	else {
		snprintf(prev_buf, sizeof(prev_buf), "%"PRIuHU, prev_units);
		prev_str = prev_buf;
	}
	
	// Get string for cur_units
	if(cur_units == HEAP_META_BOOKEND) {
		cur_str = "HEAP_META_BOOKEND";
	}
	else {
		snprintf(cur_buf, sizeof(cur_buf), "%"PRIuHU, cur_units);
		cur_str = cur_buf;
	}
	
	fprintf(
		fout,
		"<%p> [label=<"
			"<table border=\"0\" cellborder=\"1\" cellspacing=\"0\" bgcolor=\"%s\">"
				"<tr><td port=\"tp\" colspan=\"2\">%p (%s)</td></tr>"
				"<tr><td port=\"ob\" colspan=\"2\">%p (object address)</td></tr>"
				"<tr>"
					"<td port=\"pv\"%s>prev_units=%s</td>"
					"<td port=\"nx\"%s>cur_units=%s</td>"
				"</tr>"
				"<tr><td port=\"sm\">smaller=%p</td><td port=\"bg\">bigger=%p</td></tr>"
			"</table>"
		">];\n",
		node,
		color,
		node, node_type,
		node + 1,
		heap_units_valid(prev_units) ? "" : " bgcolor=\"red\"", prev_str,
		heap_units_valid(cur_units) ? "" : " bgcolor=\"red\"", cur_str,
		heap_adj_get_pointer(node->prev), heap_adj_get_pointer(node->cur)
	);
}

static void drawFreeTreeRecursive(FILE* fout, HeapMetadata* node) {
	// Indent one level
	fprintf(fout, "\t");
	drawMeta(fout, node);
	
	// Smaller child
	HeapMetadata* smaller = heap_meta_get_smaller(node);
	if(smaller != NULL) {
		drawFreeTreeRecursive(fout, smaller);
		fprintf(fout, "\t\t<%p>:sm -> <%p>:tp;\n", node, smaller);
	}
	
	// Bigger child
	HeapMetadata* bigger = heap_meta_get_bigger(node);
	if(bigger != NULL) {
		drawFreeTreeRecursive(fout, bigger);
		fprintf(fout, "\t\t<%p>:bg -> <%p>:tp;\n", node, bigger);
	}
}

void cage_drawFreeTree(CageHeap* heap, FILE* fout) {
	if(heap == NULL) {
		heap = cage_default_heap();
	}
	
	fprintf(fout, "digraph cage_free_tree {\n");
	fprintf(fout, "\tnewrank=\"true\";\n");
	fprintf(fout, "\tgraph [fontname=\"Courier\"];\n");
	fprintf(fout, "\tnode [fontname=\"Courier\", shape=\"plaintext\"];\n");
	fprintf(fout, "\tedge [fontname=\"Courier\"];\n");
	
	// Draw heap descriptor object
	fprintf(fout,
		"\t<%p> [label=<"
			"<table border=\"0\" cellborder=\"1\" cellspacing=\"0\" bgcolor=\"orange\">"
				"<tr><td>%p (CageHeap)</td></tr>"
				"<tr><td port=\"al\">arena_list=%p</td></tr>"
				"<tr><td port=\"ft\">free_tree=%p</td></tr>"
			"</table>"
		">];\n",
		heap,
		heap,
		heap->arena_list,
		heap_meta_get_bigger(&heap->free_tree)
	);
	
	// Draw edge from heap descriptor to free_tree
	HeapMetadata* free_node = heap_meta_get_bigger(&heap->free_tree);
	if(free_node != NULL) {
		fprintf(fout, "\t<%p>:ft -> <%p>:tp;\n", heap, free_node);
		
		// Draw links to rest of nodes in the free tree
		drawFreeTreeRecursive(fout, free_node);
	}
	
	fprintf(fout, "}\n");
}

static void drawZone(FILE* fout, ArenaHeader* arena) {
	// Open cluster subgraph
	fprintf(fout, "\tsubgraph cluster_%p {\n", arena);
	
	// Subgraph formatting
	fprintf(fout, "\t\tconcentrate=true;\n");
	fprintf(fout, "\t\tcolor=\"blue\";\n");
	fprintf(fout, "\t\tlabel=<%p (%zu page%s)>;\n", arena, arena->page_count, &"s"[arena->page_count == 1]);
	
	// Add node for arena header
	fprintf(fout,
		"\t\t<%p> [label=<"
			"<table border=\"0\" cellborder=\"1\" cellspacing=\"0\" bgcolor=\"dodgerblue\">"
				"<tr><td port=\"tp\">%p (ArenaHeader)</td></tr>"
				"<tr><td>page_count=%zu</td></tr>"
				"<tr><td port=\"nx\">next=%p</td></tr>"
			"</table>"
		">];\n",
		arena,
		arena,
		arena->page_count,
		arena->next
	);
	
	// Add "first_meta" edge
	HeapMetadata* meta = (HeapMetadata*)arena + 1;
	fprintf(fout, "\t\t<%p>:tp -> <%p>:tp [label=<first_meta>];\n", arena, meta);
	
	// Add each metadata object in the heap arena
	while(meta != NULL) {
		// Draw current metadata object, indented twice
		fprintf(fout, "\t\t");
		drawMeta(fout, meta);
		
		// Link with next metadata object
		HeapMetadata* next = heap_meta_get_next(meta);
		if(next != NULL) {
			HeapMetadata* np = heap_meta_get_prev(next);
			
			fprintf(fout, "\t\t<%p>:nx -> <%p>:pv;\n", meta, next);
			fprintf(fout, "\t\t<%p>:pv -> <%p>:nx [constraint=\"false\"];\n", next, np);
		}
		
		// Advance to next metadata object
		meta = heap_meta_get_next(meta);
	}
	
	// Set rank=same for each metadata node in this heap arena
	fprintf(fout, "\t\t{rank=\"same\" <%p>", arena);
	meta = (HeapMetadata*)arena + 1;
	while(meta != NULL) {
		fprintf(fout, " <%p>", meta);
		
		// Advance to next metadata object
		meta = heap_meta_get_next(meta);
	}
	fprintf(fout, "}\n");
	
	// Close cluster subgraph
	fprintf(fout, "\t}\n");
	
	// Draw edge to next heap arena
	if(arena->next != NULL) {
		fprintf(fout, "\t\t<%p>:nx -> <%p>;\n", arena, arena->next);
	}
}

static void drawFreeTreeInHeap(FILE* fout, HeapMetadata* node) {
	// Smaller child
	HeapMetadata* smaller = heap_meta_get_smaller(node);
	if(smaller != NULL) {
		fprintf(fout, "\t\t<%p>:sm -> <%p> [constraint=\"false\"];\n", node, smaller);
		drawFreeTreeInHeap(fout, smaller);
	}
	
	// Bigger child
	HeapMetadata* bigger = heap_meta_get_bigger(node);
	if(bigger != NULL) {
		fprintf(fout, "\t\t<%p>:bg -> <%p> [constraint=\"false\"];\n", node, bigger);
		drawFreeTreeInHeap(fout, bigger);
	}
}

void cage_drawHeapGraph(CageHeap* heap, FILE* fout) {
	if(heap == NULL) {
		heap = cage_default_heap();
	}
	
	fprintf(fout, "digraph cage_default_heap {\n");
	fprintf(fout, "\tnewrank=\"true\";\n");
	fprintf(fout, "\tgraph [fontname=\"Courier\"];\n");
	fprintf(fout, "\tnode [fontname=\"Courier\", shape=\"plaintext\"];\n");
	fprintf(fout, "\tedge [fontname=\"Courier\"];\n");
	
	// Draw heap descriptor object
	fprintf(fout,
		"\t<%p> [label=<"
			"<table border=\"0\" cellborder=\"1\" cellspacing=\"0\" bgcolor=\"orange\">"
				"<tr><td>%p (CageHeap)</td></tr>"
				"<tr><td port=\"al\">arena_list=%p</td></tr>"
				"<tr><td port=\"ft\">free_tree=%p</td></tr>"
			"</table>"
		">];\n",
		heap,
		heap,
		heap->arena_list,
		heap_meta_get_bigger(&heap->free_tree)
	);
	
	// Draw edge from heap descriptor to free_tree
	HeapMetadata* free_node = heap_meta_get_bigger(&heap->free_tree);
	if(free_node != NULL) {
		fprintf(fout, "\t<%p>:ft -> <%p> [constraint=\"false\"];\n", heap, free_node);
		
		// Draw links to rest of nodes in the free tree
		drawFreeTreeInHeap(fout, free_node);
	}
	
	// Is there at least one arena?
	ArenaHeader* arena = heap->arena_list;
	if(arena != NULL) {
		// Draw edge from heap descriptor to arena_list
		fprintf(fout, "\t<%p>:al -> <%p>:tp [constraint=\"false\"];\n", heap, arena);
		
		// Draw each arena as a subgraph
		do {
			drawZone(fout, arena);
			arena = arena->next;
		} while(arena != NULL);
	}
	
	fprintf(fout, "}\n");
}

static void printRange(FILE* fout, uintptr_t lo, uintptr_t hi) {
	fprintf(fout, "%016"PRIxPTR" - %016"PRIxPTR"\n", lo, hi);
}

static void printBlockDescription(FILE* fout, ArenaHeader* arena) {
	fprintf(fout, "================\n");
	
	// Sanity check
	uintptr_t arena_addr = (uintptr_t)arena;
	if((arena_addr & (PAGE_SIZE - 1)) != 0) {
		fprintf(fout, "!!! HEAP CORRUPT: arena pointer must start at beginning of memory page: %p !!!\n\n", arena);
		return;
	}
	
	// Describe guard_pre
	uintptr_t guard_pre = arena_addr - sizeof(GuardPage);
	printRange(fout, guard_pre, guard_pre + sizeof(GuardPage));
	fprintf(fout, "  GUARD PRE\n\n");
	
	// Describe ArenaHeader
	size_t page_count = arena->page_count;
	printRange(fout, arena_addr, arena_addr + HEAP_ALLOC_GRANULARITY);
	fprintf(fout, "  ARENA HEADER\n");
	fprintf(fout, "  page_count = %zu\n\n", page_count);
	
	// Sanity check
	if(page_count > (HEAP_MAX_ALLOC_SIZE + PAGE_SIZE - 1) / PAGE_SIZE) {
		fprintf(fout, "!!! HEAP CORRUPT: page_count is too large: %zu !!!\n\n", page_count);
		return;
	}
	
	// Describe heap chunks
	HeapMetadata* meta = (HeapMetadata*)arena + 1;
	HeapMetadata* end = (HeapMetadata*)(arena_addr + page_count * PAGE_SIZE);
	
	while(meta < end) {
		// Range of metadata
		printRange(fout, (uintptr_t)meta, (uintptr_t)(meta + 1));
		
		HeapMetadata* smaller = heap_adj_get_pointer(meta->prev);
		HeapMetadata* bigger = heap_adj_get_pointer(meta->cur);
		
		// Default description for a heap metadata struct
		const char* desc;
		const char* prev_rba_desc;
		const char* cur_rba_desc;
		bool is_free = heap_meta_is_free(meta);
		bool is_red = !heap_adj_get_rba(meta->prev).is_black;
		if(is_free) {
			if(is_red) {
				desc = "FREE RED";
				prev_rba_desc = "RBA_RED";
			}
			else {
				desc = "FREE BLACK";
				prev_rba_desc = "RBA_BLACK";
			}
			cur_rba_desc = "RBA_FREE";
		}
		else {
			desc = "ALLOCATED";
			if(is_red) {
				prev_rba_desc = "RBA_DEFAULT";
			}
			else {
				fprintf(fout, "!!! HEAP CORRUPT: prev.rba is 1 when cur.rba is RBA_ALLOCATED !!!\n\n");
				return;
			}
			cur_rba_desc = "RBA_ALLOCATED";
		}
		
		// Describe metadata
		HeapUnits cur_units = heap_meta_get_cur_units(meta);
		fprintf(fout, "  METADATA (%s)\n", desc);
		fprintf(fout, "  smaller = ");
		if(smaller == NULL) {
			fprintf(fout, "NULL\n");
		}
		else {
			fprintf(fout, "%p\n", smaller);
		}
		fprintf(fout, "  bigger = ");
		if(bigger == NULL) {
			fprintf(fout, "NULL\n\n");
		}
		else {
			fprintf(fout, "%p\n\n", bigger);
		}
		fprintf(fout, "  prev.rba = %s\n", prev_rba_desc);
		fprintf(fout, "  cur.rba = %s\n", cur_rba_desc);
		fprintf(fout, "  prev.units = %"PRIuHU"\n", heap_meta_get_prev_units(meta));
		fprintf(fout, "  cur.units = %"PRIuHU"\n\n", cur_units);
		
		// At right bookend?
		if(!heap_units_valid(cur_units)) {
			if(cur_units == HEAP_META_BOOKEND) {
				break;
			}
			else {
				fprintf(fout, "!!! HEAP CORRUPT: cur_units is invalid: %"PRIuHU"\n", cur_units);
				return;
			}
		}
		
		// Advance to next metadata object
		meta = meta + 1 + cur_units;
	}
	
	// Sanity check
	if(meta != end - 1) {
		fprintf(fout, "!!! HEAP CORRUPT: found right bookend before end of heap arena: %p !!!\n", meta);
		return;
	}
	
	// Describe guard_post
	printRange(fout, (uintptr_t)end, (uintptr_t)end + sizeof(GuardPage));
	fprintf(fout, "  GUARD POST\n");
	fprintf(fout, "================\n\n");
}

void cage_printAllBlockDescriptions(CageHeap* heap, FILE* fout) {
	if(heap == NULL) {
		heap = cage_default_heap();
	}
	
	ArenaHeader* block = heap->arena_list;
	while(block != NULL) {
		printBlockDescription(fout, block);
		block = block->next;
	}
}

void cage_dumpAllDebugInfo(CageHeap* heap, const char* tree_fname, const char* graph_fname, const char* blocks_description_fname) {
	if(tree_fname != NULL) {
		FILE* tree_file = fopen(tree_fname, "w");
		if(tree_file == NULL) {
			perror(tree_fname);
		}
		else {
			cage_drawFreeTree(heap, tree_file);
			fclose(tree_file);
		}
	}
	
	if(graph_fname != NULL) {
		FILE* graph_file = fopen(graph_fname, "w");
		if(graph_file == NULL) {
			perror(graph_fname);
		}
		else {
			cage_drawHeapGraph(heap, graph_file);
			fclose(graph_file);
		}
	}
	
	if(blocks_description_fname != NULL) {
		FILE* blocks_description_file = fopen(blocks_description_fname, "w");
		if(blocks_description_file == NULL) {
			perror(blocks_description_fname);
		}
		else {
			cage_printAllBlockDescriptions(heap, blocks_description_file);
			fclose(blocks_description_file);
		}
	}
}
