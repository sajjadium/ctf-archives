#ifndef _MAZE_H_
#define _MAZE_H_

struct maze {
    size_t size;
    char* maze;
    char* addr;
};

struct maze* gen_maze(size_t size, unsigned int (*get_rand_uint)(void));
int map_maze(struct maze* maze, void* addr);
int solve_maze(struct maze* maze, char* solution);

#endif // _MAZE_H_
