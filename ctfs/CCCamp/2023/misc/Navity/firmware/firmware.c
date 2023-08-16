#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>

extern uint32_t __stack;

typedef void (*fn)();

typedef struct
{
    volatile uint32_t *STACK_END;
    volatile fn RESET;
    volatile fn NMI;
    volatile fn HARD_FAULT;
    volatile fn MM_FAULT;
    volatile fn BUS_FAULT;
    volatile fn USAGE_FAULT;
    volatile fn RESERVED0;
    volatile fn RESERVED1;
    volatile fn RESERVED2;
    volatile fn RESERVED3;
    volatile fn SVC_CALL;
    volatile fn RESERVED4;
    volatile fn RESERVED5;
    volatile fn PEND_SV;
    volatile fn SYS_TICK;
    volatile fn IRQ[];
} VectorTable_Type;

void _mainCRTStartup();
void loop();

VectorTable_Type _vectors
    __attribute__((section("vectors"))) = {
        .STACK_END = &__stack,
        .RESET = _mainCRTStartup,
        .NMI = loop,
        .HARD_FAULT = loop,
        .BUS_FAULT = loop,
        .USAGE_FAULT = loop,
};

int fib(int n)
{
    int a = 0;
    int b = 1;
    int s;
    if (n == 0)
    {
        return a;
    }
    if (n == 1)
    {
        return b;
    }
    for (int i = 1; i < n; i++)
    {
        s = b;
        b = a + b;
        a = s;
    }
    return b;
}

int _fstat(int file, struct stat *st)
{
    st->st_mode = S_IFCHR;
    return 0;
}

int _isatty(int file)
{
    return 1;
}

int _close(int file)
{
    return -1;
}

int _lseek(int file, int ptr, int dir)
{
    return 0;
}

__attribute__((naked)) void loop()
{
    while (1)
    {
    }
}

int result;

int _read(int file, char *ptr, int len)
{
    if (file != 0)
    {
        return -1;
    }
    int num = 0;
    uint8_t c;
    for (int i = 0; i < len; i++)
    {
        uint8_t s;
        for (s = 0; s == 0; s = *(volatile uint8_t *)0x40004C04)
        {
        }
        c = *(volatile uint8_t *)0x40004C00;
        *(volatile uint8_t *)0x40004C00 = c;
        ptr[i] = c;
        num++;
        if (c == '\r')
        {
            return num;
        }
    }
    return num;
}

int _write(int file, char *ptr, int len)
{
    if (file != 1)
    {
        return -1;
    }
    for (int i = 0; i < len; i++)
    {
        *(volatile uint8_t *)0x40004C00 = (*ptr++);
    }
    return len;
}

void main()
{
    puts("Welcome to my arm bare metal fib calculator!");

    int input;
    while (1)
    {
        printf("input: ");
        scanf(" %d", &input);
        printf("fib(%d) = %d\n", input, fib(input));
    }
}