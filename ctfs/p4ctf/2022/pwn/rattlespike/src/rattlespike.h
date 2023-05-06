#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

struct character {
    int value;
    int *data;
    size_t capacity;
    size_t num;
};

#define PUSH(ch, v) \
    if (ch.num >= ch.capacity) { \
        if (ch.capacity >= SIZE_MAX / 16) { \
            fprintf(stderr, #ch " too big\n"); \
            abort(); \
        } else if (ch.capacity == 0) { \
            ch.capacity = 8; \
        } else { \
            ch.capacity *= 2; \
        } \
        ch.data = realloc(ch.data, sizeof(int) * ch.capacity); \
    } \
    ch.data[ch.num++] = (v)

#define POP(ch) \
    if (ch.num == 0) { \
        fprintf(stderr, #ch " underflow\n"); \
        abort(); \
    } \
    ch.value = ch.data[--ch.num]

int square(int v) {
    return v * v;
}

int cube(int v) {
    return v * v * v;
}

int factorial(int v) {
    int r = 1;
    for (int i = 1; i <= v; i++) {
        r *= v;
    }
    return r;
}

int isqrt(int v) {
    if (v < 0) {
        fprintf(stderr, "Tried to compute isqrt(%d)\n", v);
        abort();
    }

    int x0 = v / 2;
    int x1 = (x0 + v / x0) / 2;
    while (x1 < x0) {
        x0 = x1;
        x1 = (x0 + v / x0) / 2;
    }

    return x0;
}

int readint(void) {
    int v;
    if (scanf("%d", &v) != 1) {
        fprintf(stderr, "Couldn't parse integer\n");
        abort();
    }

    return v;
}
