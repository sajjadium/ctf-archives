#ifndef CAGE_HEAP_DEBUG_H
#define CAGE_HEAP_DEBUG_H

#include <stdio.h>
#include <stdlib.h>
#include "heap.h"

void cage_drawFreeTree(CageHeap* heap, FILE* fout);
void cage_drawHeapGraph(CageHeap* heap, FILE* fout);
void cage_printAllBlockDescriptions(CageHeap* heap, FILE* fout);
void cage_dumpAllDebugInfo(CageHeap* heap, const char* tree_fname, const char* graph_fname, const char* blocks_description_fname);

#endif /* CAGE_HEAP_DEBUG_H */
