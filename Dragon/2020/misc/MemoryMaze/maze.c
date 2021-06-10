#define _GNU_SOURCE
#include <stdlib.h>
#include <sys/mman.h>

#include "maze.h"

#define PAGE_SIZE 0x1000ul

struct maze* gen_maze(size_t size, unsigned int (*get_rand_uint)(void)) {
    if (size < 10 || size % 4 != 3) {
        return NULL;
    }

    struct maze* maze = malloc(sizeof(*maze));
    if (!maze) {
        return NULL;
    }

    maze->size = size;
    maze->maze = calloc(size * size, sizeof(*maze->maze));
    if (!maze->maze) {
        free(maze);
        return NULL;
    }

    size_t i, j;
    for (i = 1; i < size - 1; ++i) {
        if (i % 2 == 0) {
            maze->maze[i * size + (i % 4 == 0 ? 1 : size - 2)] = 1;
            unsigned int b = get_rand_uint();
            maze->maze[i * size + 1 + (b % (size - 2))] = 1;
        } else {
            for (j = 1; j < size - 1; ++j) {
                maze->maze[i * size + j] = 1;
            }
        }
    }

    return maze;
}

int map_maze(struct maze* maze, void* addr) {
    maze->addr = addr;

    size_t i, j;
    for (i = 0; i < maze->size; ++i) {
        for (j = 0; j < maze->size; ++j) {
            if (!maze->maze[i * maze->size + j]) {
                continue;
            }

            void* ptr = mmap(maze->addr + (i * maze->size + j) * PAGE_SIZE,
                             PAGE_SIZE,
                             PROT_READ | PROT_WRITE,
                             MAP_ANONYMOUS | MAP_SHARED | MAP_FIXED_NOREPLACE,
                             -1, 0);
            if (ptr == MAP_FAILED) {
                return 1;
            }
        }
    }

    return 0;
}

int solve_maze(struct maze* maze, char* solution) {
    size_t x = 1;
    size_t y = 1;

    while (*solution) {
        switch (*solution) {
            case 'N':
                --y;
                break;
            case 'S':
                ++y;
                break;
            case 'E':
                ++x;
                break;
            case 'W':
                --x;
                break;
            default:
                x = 0;
                y = 0;
                break;
        }
        ++solution;

        char* ptr = maze->addr + (y * maze->size + x) * PAGE_SIZE;
        *(volatile char*)ptr = 'X';
    }

    if (x == maze->size - 2 && y == maze->size - 2) {
        return 0;
    }

    return 1;
}
