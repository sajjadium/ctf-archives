#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    size_t size = 0;
    size_t idx = 0;
    unsigned int i = 0;
    unsigned char val = 0;
    unsigned char *ptr = NULL;
    size_t *doit = NULL;

    if (scanf("%zx", &size) != 1)
        goto fail;

    ptr = calloc(size, sizeof(unsigned char));

    if (!ptr)
        goto fail;

    if ((scanf("%zx", &size) != 1) || !((size < 11) && (size >= 0)))
        goto fail;

    doit = calloc(size, 2 * sizeof(size_t));

    if (!doit)
        goto fail;

    while ((i < size) && (scanf("%zx %hhx", &idx, &val) == 2)) {
        doit[2 * i] = idx;
        doit[2 * i + 1] = val;
        i++;
    }

    for (i = 0; i < size; i++) {
        ptr[doit[2 * i]] = (unsigned char)doit[2 * i + 1];
    }

    exit(0);
fail:
    exit(-1);
}
