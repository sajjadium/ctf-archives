#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <stdbool.h>

#define BUFFER_SIZE (64)
#define NAME_MAX_SIZE (12)
#define TYPE_MAX_SIZE (15)
#define POINTS_FOR_FLAG ((uint32_t)(1<<31)-1)
#define LUCK_LIMIT ((uint64_t)(1ULL<<60))

typedef struct _player{
    char name[NAME_MAX_SIZE+1];
    char player_type[NAME_MAX_SIZE+1];
    uint32_t game_points;
    uint32_t health_points;
    uint32_t strength;
    uint32_t shield;
    uint64_t luck;
}player;

typedef struct _enemy{
    char name[NAME_MAX_SIZE+1];
    uint32_t health_points;
    uint32_t strength;
    uint32_t shield;
}Enemy;