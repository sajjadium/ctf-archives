#include <stdio.h>
#include <unistd.h>
#include <inttypes.h>
#include <stdlib.h>

#define MAX_ALLOCATIONS 0x400

void* allocations[MAX_ALLOCATIONS];

void fail(char* msg) {
    fprintf(stderr, "%s\n", msg);
    exit(0);
}

void malloc_one() {
    uint16_t index;
    size_t size;

    printf("malloc at index: ");
    if (fscanf(stdin, "%hu", &index) != 1)
	fail("could not read index");

    if (index >= MAX_ALLOCATIONS)
        fail("index oob");

    if (allocations[index])
	fail("index already occupied");

    printf("with size: ");
    if (fscanf(stdin, "%lu", &size) != 1)
	fail("could not read size");

    allocations[index] = malloc(size);
    if (!allocations[index])
	fail("could not allocate memory");
}

void free_one() {
    uint16_t index;

    printf("free at index: ");
    if (fscanf(stdin, "%hu", &index) != 1)
	fail("could not read index");

    if (index >= MAX_ALLOCATIONS)
        fail("index oob");
    
    if (!allocations[index])
	fail("calling free on a nullptr");

    free(allocations[index]);
    allocations[index] = NULL;
}

void read_one() {
    uint16_t index;
    size_t size;

    printf("read at index: ");
    if (fscanf(stdin, "%hu", &index) != 1)
	fail("could not read index");

    if (index >= MAX_ALLOCATIONS)
        fail("index oob");
    
    if (!allocations[index])
        fail("calling read on a nullptr");

    printf("of size: ");
    if (fscanf(stdin, "%lu", &size) != 1)
	fail("could not read size");

    if (write(STDOUT_FILENO, allocations[index], size) != size)
	fail("read failed");
}

void write_one() {
    uint16_t index;
    size_t size;

    printf("write to index: ");
    if (fscanf(stdin, "%hu", &index) != 1)
	fail("could not read index");

    if (index >= MAX_ALLOCATIONS)
        fail("index oob");
    
    if (!allocations[index])
        fail("calling write on a nullptr");

    printf("of size: ");
    if (fscanf(stdin, "%lu", &size) != 1)
	fail("could not read size");

    if (read(STDIN_FILENO, allocations[index], size) != size)
	fail("write failed");
}

int main() {
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    setvbuf(stderr, 0, _IONBF, 0);

    printf("how-to-heap\n> 0 => exit\n> 1 => malloc\n> 2 => free\n> 3 => read\n> 4 => write\n");
    for(;;) {
	uint8_t option;

        printf("> ");
	if (fscanf(stdin, "%hhu", &option) != 1)
            fail("could not read menu option");
	
	switch(option) {
	    case 0: return 0;
            case 1: malloc_one(); break;
	    case 2: free_one(); break;
	    case 3: read_one(); break;
	    case 4: write_one(); break;
	    default: fail("invalid option");
	}
    }
}

