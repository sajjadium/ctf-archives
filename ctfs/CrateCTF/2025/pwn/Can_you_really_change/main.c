// Compile with gcc -O0 main.c stack_dump.c -o chall
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>

// Stack dump related things
typedef struct dump_variable
{
    uint8_t* address;
    size_t length;
    char* name;
} dump_variable;

dump_variable dump_variables[16];
size_t num_variables;

void dump_stack(void *start, size_t bytes_before, size_t bytes_after, dump_variable variables[], size_t num_variables);
// End stack dump related things

void print_flag()
{
    FILE *fptr = fopen("/flag.txt", "r");
    if (fptr == NULL)
    {
        printf("\nGick inte att öppna flag.txt... Om du kör mot servern, kontakta en admin.");
        exit(0);
    }

    char c;
    while ((c = getc(fptr)) != EOF)
    {
        putchar(c);
    }
    fflush(stdout);
    fclose(fptr);
}

// This struct will make sure that changeme is placed immediately after buf
// Example: buf = "ABCDEFGH", changeme = 0x11223344 (little-endian, least significant byte first)
// ┌────────┬───────┐
// │ Offset │ Value │
// ├────────┼───────┤
// │      0 │ A     │
// │      1 │ B     │
// │      2 │ C     │
// │      3 │ D     │
// │      4 │ E     │
// │      5 │ F     │
// │      6 │ G     │
// │      7 │ H     │
// │      8 │ 0x44  │
// │      9 │ 0x33  │
// │     10 │ 0x22  │
// │     11 │ 0x11  │
// └────────┴───────┘
typedef struct variables
{
    char buffer[8];
    int changeme;
} variables;

int main(int argc, char **argv)
{
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin, 0, 2, 0);
    
    while (1)
    {
        // Define variables
        variables stack_variables;

        // Stack dump related things
        dump_variables[0] = (dump_variable){(uint8_t*) stack_variables.buffer, sizeof(stack_variables.buffer), "buffer"};
        dump_variables[1] = (dump_variable){(uint8_t*) &stack_variables.changeme, sizeof(stack_variables.changeme), "changeme"};
        num_variables = 2;
        // End stack dump related things

        // Reset variables
        memset(&stack_variables.buffer, 0, sizeof(stack_variables.buffer));
        stack_variables.changeme = 0xaaaaaaaa;

        // Get input
        printf("Värdet är: 0x%02x\n", stack_variables.changeme);
        printf("Skriv något tack: ");
        int rc = read(STDIN_FILENO, &stack_variables.buffer, 256);
        if (rc <= 0)
        {
            exit(0);
        }
        printf("Du skrev: %s\n", stack_variables.buffer);

        // Print stack dump
        dump_stack(&stack_variables, 0, sizeof(stack_variables), dump_variables, num_variables);
        printf("\n");

        // Check variable value
        if (stack_variables.changeme == 0xaaaaaaaa)
        {
            printf("Värdet är fortfarande 0x%02x\n", stack_variables.changeme);
            printf("Prova igen!\n\n");
        }
        else
        {
            printf("Oj, nu är värdet plötsligt 0x%02x! Här har du flaggan: ", stack_variables.changeme);
            print_flag();
            exit(0);
        }
    }
}
