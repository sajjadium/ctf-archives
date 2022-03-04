#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "helpers.h"

// reads an int from stdin using fgets
// returns 0 if bad input
int get_int(void) {
    char buf[256];

    fgets(buf, sizeof(buf), stdin);
    return atoi(buf);
}

// like fgets, but trims newline
// returns length of string
size_t get_line(char *buf, size_t n) {
    size_t len;

    fgets(buf, n, stdin);
    len = strcspn(buf, "\n");

    buf[len] = '\0';

    return len;
}
