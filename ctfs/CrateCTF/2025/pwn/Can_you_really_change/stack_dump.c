/*
 * stack_dump.c (by ChatGPT)
 *
 * Print a formatted table of stack memory starting from a local variable.
 * Reads up to 'bytes' before and after the starting point, in rows of 16 bytes.
 *
 * Build: gcc -O0 stack_dump.c main.c -o stack_dump
 * (optional) add -fno-omit-frame-pointer for more consistent frames when experimenting.
 *
 * WARNING: This program reads raw memory; it catches SIGSEGV and stops gracefully when
 * it hits unmapped pages. Use only in controlled/testing environments.
 */

#define _POSIX_C_SOURCE 200112L
#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>
#include <signal.h>
#include <setjmp.h>
#include <string.h>
#include <ctype.h>

typedef struct dump_variable
{
    uint8_t* address;
    size_t length;
    char* name;
} dump_variable;

static sigjmp_buf sjb;

static void sigsegv_handler(int signo)
{
    (void)signo;
    siglongjmp(sjb, 1);
}

/* Print one line: address, hex bytes, ascii */
static void print_row(uint8_t *row_addr, size_t bytes_this_row, uint8_t *start_addr, dump_variable variables[], size_t num_variables)
{
    /* Print offset from start pointer to show relative position */
    intptr_t rel = (intptr_t)row_addr - (intptr_t)start_addr;

    char* variable_name = "";
    char* variable_symbol = "";
    if (variables != NULL)
    {
        for (int i = 0; i < num_variables; i++)
        {
            if (row_addr == variables[i].address)
            {
                variable_name = variables[i].name;
                variable_symbol = "┬";
            }
            else if (row_addr > variables[i].address && row_addr < variables[i].address + variables[i].length - 1)
            {
                variable_symbol = "│";
            }
            else if (row_addr == variables[i].address + variables[i].length - 1)
            {
                variable_symbol = "└";
            }
        }
    }

    printf("  %4d %20s %1s  ", (long)rel, variable_name, variable_symbol);
    /* Hex bytes in groups of 1, mark start pointer */
    for (size_t i = 0; i < 1; ++i)
    {
        if (i < bytes_this_row)
        {
            unsigned char c = row_addr[i];
            if (isprint(c))
            {
                printf("%04c (0x%02x)", c, row_addr[i]);
            }
            else
            {
                printf("   � (0x%02x)", row_addr[i]);
            }
        }
        else
        {
            printf("  ");
        }
    }
    putchar('\n');
}

void dump_stack(void *start, size_t bytes_before, size_t bytes_after, dump_variable variables[], size_t num_variables)
{
    /* Install SIGSEGV handler to recover safely if we hit unmapped memory */
    struct sigaction sa_old, sa_new;
    memset(&sa_new, 0, sizeof(sa_new));
    sa_new.sa_handler = sigsegv_handler;
    sigemptyset(&sa_new.sa_mask);
    sa_new.sa_flags = 0;
    sigaction(SIGSEGV, &sa_new, &sa_old);

    uint8_t *start_addr = (uint8_t *)start;
    /* Calculate start of dump */
    intptr_t begin = (intptr_t)start_addr - (intptr_t)bytes_before;
    uint8_t *addr = (uint8_t *)begin;

    size_t total = bytes_before + bytes_after;
    size_t rows = total;

    printf("Stackdump av stack_variables (%p)\n",
           (void *)start_addr, total, bytes_before, bytes_after);
    printf("Offset              Variabel   ASCII (och hex)\n");
    printf("--------------------------------------------------------------------------------\n");

    for (size_t r = 0; r < rows; ++r)
    {
        if (sigsetjmp(sjb, 1) != 0)
        {
            /* we hit SIGSEGV while trying to read; stop gracefully */
            printf("... stopped: attempted to read unmapped memory at or near %p\n",
                   (void *)addr);
            break;
        }

        /* Try to read 1 byte (but printing logic handles end partials) */
        /* To ensure the read actually occurs so we can catch segfault, read each byte */
        uint8_t buffer[1];
        size_t bytes_to_read = 1;
        for (size_t i = 0; i < bytes_to_read; ++i)
        {
            /* volatile read to avoid optimizer removing reads */
            volatile uint8_t v = addr[i];
            buffer[i] = v;
        }

        /* Print the row using the buffer */
        /* We choose bytes_this_row = 1 always except possibly last (but we pre-rounded total) */
        print_row(addr, 1, start_addr, variables, num_variables);

        addr += 1;
    }

    /* restore previous handler */
    sigaction(SIGSEGV, &sa_old, NULL);
}