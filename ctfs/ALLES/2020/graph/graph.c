#include <stdlib.h>
#include <stdio.h>
#include <string.h>

typedef struct {
    unsigned short first_edge; // index into graph->edges
    unsigned short edge_cnt; // edgecount, starts at first edge
    unsigned int island; // id of island
} Vtx;

typedef struct {
    unsigned short other_vtx; // vertex this edge points to
} Edge;

typedef struct {
    char name[32 + 1]; // name of graph
    Vtx* vertices; // vector of vertices
    unsigned short vtx_cnt; // size of vertices vector
    Edge* edges; // vector of edges
    unsigned short edge_cnt; // size of edges vector
} Graph;

#define ASSERT(a) if (!(a)) { printf("Assertion \"%s\" at %s:%d failed!\n", #a, __FILE__, __LINE__); exit(-1); }
#define BITSET_SET_BIT(bitset, bit) bitset[bit / 8] |= 1 << (bit % 8);
#define BITSET_IS_BIT_SET(bitset, bit) !!(bitset[bit / 8] & (1 << (bit % 8)))

void print_graph(Graph* g) {
    printf("Graph %p: name = \"%s\"\n", g, g->name);

    for (int i = 0; i < g->vtx_cnt; i++) {
        Vtx* vtx = &g->vertices[i];
        printf("    Vertex %p: first_edge = %u, edge_cnt = %u, island = %u\n", vtx, vtx->first_edge, vtx->edge_cnt, vtx->island);
    }

    for (int i = 0; i < g->edge_cnt; i++) {
        Edge* edge = &g->edges[i];
        printf("    Edge %p: other_vtx = %u\n", edge, edge->other_vtx);
    }
}

void graph_island(Graph* graph) {
    unsigned short vtx_stack[graph->vtx_cnt * sizeof(unsigned short)];
    unsigned char visited[(graph->vtx_cnt + 7) / 8 * sizeof(unsigned char)];
    memset(visited, 0, (graph->vtx_cnt + 7) / 8 * sizeof(unsigned char));

    for (int i = 0; i < graph->vtx_cnt; i++) {
        unsigned int vtx_idx = i;
        unsigned int stack_idx = 0;

        if (!BITSET_IS_BIT_SET(visited, i)) {
            BITSET_SET_BIT(visited, i)

            while (1) {
                ASSERT(vtx_idx < graph->vtx_cnt)
                Vtx* vtx = &graph->vertices[vtx_idx];
                vtx->island = i;

                if (vtx->edge_cnt > 0) {
                    ASSERT(vtx->first_edge < graph->edge_cnt)
                    ASSERT(vtx->edge_cnt <= graph->edge_cnt)
                    ASSERT(vtx->first_edge + vtx->edge_cnt <= graph->edge_cnt)
                    
                    for (int j = vtx->first_edge; j < vtx->first_edge + vtx->edge_cnt; j++) {
                        Edge* e = &graph->edges[j];
                        if (!BITSET_IS_BIT_SET(visited, e->other_vtx)) {
                            vtx_stack[stack_idx++] = e->other_vtx;
                            BITSET_SET_BIT(visited, e->other_vtx);
                        }
                    }
                }
                if (stack_idx == 0) {
                    break;
                }
                vtx_idx = vtx_stack[--stack_idx];
            }
        }
    }
}

void main() {
    Graph g;
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    printf("Input your graph:\n");

    printf("Graph name: ");
    ASSERT(fscanf(stdin, "%32s", g.name) == 1);

    printf("Vertex count: ");
    ASSERT(scanf("%hu", &g.vtx_cnt) == 1);
    g.vertices = NULL;
    if (g.vtx_cnt > 0) {
        g.vertices = malloc(g.vtx_cnt * sizeof(Vtx));
        ASSERT(g.vertices != NULL)

        for (int i = 0; i < g.vtx_cnt; i++) {
            printf("Input vertex #%d\n", i);
            printf("    first edge: ");
            ASSERT(scanf("%hu", &g.vertices[i].first_edge) == 1);
            printf("    edge count: ");
            ASSERT(scanf("%hu", &g.vertices[i].edge_cnt) == 1);
            g.vertices[i].island = 0xFFFFFFFFU;
        }    
    }

    printf("Edge count: ");
    ASSERT(scanf("%hu", &g.edge_cnt) == 1);
    g.edges = NULL;
    if (g.edge_cnt > 0) {
        g.edges = malloc(g.edge_cnt * sizeof(Edge));
        ASSERT(g.edges != NULL)

        for (int i = 0; i < g.edge_cnt; i++) {
            printf("Input vertex #%d\n", i);
            printf("    other vertex: ");
            ASSERT(scanf("%hu", &g.edges[i].other_vtx) == 1);
        } 
    }
    
    printf("Computing the islands...");
    graph_island(&g);
    print_graph(&g);

    if (g.edges) {
        free(g.edges);
    }
    if (g.vertices) {
        free(g.vertices);
    }
}