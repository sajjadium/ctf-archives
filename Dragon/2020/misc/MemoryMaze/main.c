#include <err.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#include "maze.h"

#define SIZE 303ul
#define MAX_SOL_SIZE (SIZE * SIZE)

#define BASE_ADDR ((char*)0x13370000ul)

static int g_rand_fd;

static void inits(void) {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    g_rand_fd = open("/dev/urandom", O_RDONLY);
    if (g_rand_fd < 0) {
        err(1, "open urandom");
    }
}

static void recv_line(char* buf, size_t size) {
    char c;
    size_t i = 0;

    if (size == 0) {
        return;
    }

    while (i < size - 1) {
        ssize_t x = fread(&c, sizeof(c), 1, stdin);
        if (x < 0) {
            err(1, "fread");
        } else if (x == 0) {
            break;
        }

        if (c == '\n') {
            break;
        }

        buf[i] = c;
        ++i;
    }

    buf[i] = '\0';
}

static void write_all(int fd, char* buf, size_t size) {
    size_t i = 0;

    while (i < size) {
        ssize_t x = write(fd, buf + i, size - i);
        if (x < 0) {
            err(1, "write");
        } else if (x == 0) {
            break;
        }

        i += x;
    }
}

static unsigned int get_rand_uint(void) {
    unsigned int c = 0;

    if (read(g_rand_fd, &c, sizeof(c)) != sizeof(c)) {
        err(1, "read");
    }

    return c;
}

int main(void) {
    inits();

    struct maze* m = gen_maze(SIZE, get_rand_uint);
    if (!m) {
        errx(1, "gen_maze");
    }

    if (map_maze(m, BASE_ADDR)) {
        errx(1, "map_maze");
    }

    printf("Maze size: %zu\n", m->size);
    printf("Maze address: %p\n", m->addr);

    char path[0x200];
    int solution_fd;

    do {
        char name[0x100] = { 0 };
        puts("Your name:");

        recv_line(name, sizeof(name));
        if (name[0] == '\0') {
            puts("Goodbye!");
            return 1;
        }
        printf("Hello %s!\n", name);

        if (snprintf(path, sizeof(path), "/tmp/%s", name) < 0) {
            err(1, "snprintf");
        }

        solution_fd = open(path, O_WRONLY | O_CREAT, S_IRWXU);
        if (solution_fd < 0) {
            printf("Path \"%s\" is invalid: %m\n", path);
        }
    } while (solution_fd < 0);

    printf("Solution size (max %zu):\n", MAX_SOL_SIZE);
    size_t size = 0;
    if (scanf("%zu", &size) != 1) {
        err(1, "scanf");
    }
    if (!size || size > MAX_SOL_SIZE) {
        errx(1, "bad solution size");
    }

    char* solution = calloc(size + 1, sizeof(*solution));
    if (!solution) {
        err(1, "malloc");
    }

    puts("Solution:");
    if (scanf(" ") < 0) {
        err(1, "scanf");
    }

    size_t i = 0;
    do {
        char c = 0;
        if (fread(&c, sizeof(c), 1, stdin) != 1) {
            err(1, "fread");
        }
        switch (c) {
            case 'N':
            case 'S':
            case 'E':
            case 'W':
                break;
            default:
                errx(1, "invalid character: %c", c);
        }
        solution[i] = c;
        ++i;
    } while (i < size);

    write_all(solution_fd, solution, size);

    if (solve_maze(m, solution)) {
        errx(1, "solution is not correct");
    }

    int flag_fd = open("flag.txt", O_RDONLY);
    if (flag_fd < 0) {
        err(1, "flag open");
    }

    char flag[0x100] = { 0 };
    if (read(flag_fd, flag, sizeof(flag)) < 0) {
        err(1, "read flag");
    }

    printf("CONGRATULATIONS: %s\n", flag);

    return 0;
}
