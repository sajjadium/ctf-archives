// gcc -no-pie -fno-stack-protector chall.c -o chall

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

#define floatbuffer_len 3
#define string_len 0x107

int idx;

void input_floats()
{
    char canary = 'A';
    char buffer[floatbuffer_len];

    for (idx = 0; idx < floatbuffer_len; idx++)
    {
        puts("Give me a crazy number!");
        scanf("%f", &buffer[idx]);
    }

    if (canary != 'A')
    {
        exit(0);
    }
}

int main()
{
    char canary = 'A';
    char buffer[string_len];

    setbuf(stdout, 0);
    setbuf(stdin, 0);

    puts("I live my life taking chances. Let's see how much of a risk-taker you are! Tell me an adventurous tale.");
    read(0, buffer, string_len);

    input_floats();

    if (canary != 'A')
    {
        exit(0);
    }

    return 0;
}