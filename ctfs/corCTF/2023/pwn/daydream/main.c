#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main()
{
    uint8_t bytes[16] = {0};
    size_t idx, value = 0;

    setbuf(stdin, malloc(0x2000));

    while (!bytes[0])
    {
        scanf("%ld %ld", &idx, &value);
        bytes[idx] = value;
    }
}