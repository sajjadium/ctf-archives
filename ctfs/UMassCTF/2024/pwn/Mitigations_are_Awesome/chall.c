#include <stdio.h>
#include <stddef.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/user.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <string.h>

#include <sys/ptrace.h>

__attribute__((constructor)) void ignore_me(){
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

#define NUM_ALLOCS 10

typedef struct allocation {
    char *buf;
    int magic;
} Allocation;

int get_num() {
	char buf[0x20];

	if (fgets(buf, sizeof(buf), stdin) == NULL) { exit(-1); }  
    return atoi(buf);
}

void print_menu() {
	puts("+=========:[ Menu ]:========+");
	puts("| [1] Make Allocation       |");
	puts("| [2] Resize Allocation     |");
	puts("| [3] Edit Allocation       |");
	puts("| [4] Retrieve Flag         |");
	puts("| [5] Exit Shop	    	    |");
	puts("+===========================+");
	printf("\n > ");
}

int win() {
	printf("The flag is: %s\n", getenv("FLAG"));
	exit(1);
}

int main() {
    int choice;
    Allocation allocation_array [NUM_ALLOCS];
    int cur_alloc_index = 0;
    int sz, idx;
    char *heap;

    while (1) {
        print_menu();
        printf("What action do you want to take?\n");
        choice = get_num();

        switch (choice) {
            case 1:
                if (cur_alloc_index >= NUM_ALLOCS) {
                    printf("Too many allocations, won't perform any more!\n");
                    continue;
                }

                printf("What size should the allocation be?\n");
                sz = get_num();
                allocation_array[cur_alloc_index].buf = malloc(sz);
                allocation_array[cur_alloc_index].magic = 0x41414141;

                if (allocation_array[cur_alloc_index].buf == NULL) {
                    printf("Alloc call failed\n");
                    exit(1);
                }

                printf("Successfully allocated heap-buffer of size %d at Idx-%d\n", sz, cur_alloc_index);
                cur_alloc_index++;
                break;
            case 2:
                printf("What index do you wish to resize?\n");
                idx = get_num();

                if (idx >= NUM_ALLOCS) {
                    printf("Provided index out of bounds, this is not possible!\n");
                    continue;
                }

                if (allocation_array[idx].magic != 0x41414141) {
                    printf("Provided index hasn't yet been allocated, can't reallocate!\n");
                    continue;
                }

                printf("What should the new size be?\n");
                sz = get_num();

                allocation_array[idx].buf = realloc(allocation_array[idx].buf, sz);

                if (allocation_array[idx].buf == NULL) {
                    printf("Realloc call failed\n");
                    exit(1);
                }
                printf("Idx-%d successfully resized to %d\n", idx, sz);
                break;
            case 3:
                printf("What index do you wish to edit?\n");
                idx = get_num();

                if (idx >= NUM_ALLOCS) {
                    printf("Provided index out of bounds, this is not possible!\n");
                    continue;
                }

                if (allocation_array[idx].magic != 0x41414141) {
                    printf("Provided index hasn't yet been allocated, can't reallocate!\n");
                    continue;
                }

                printf("How many bytes do you want to write to the buffer?\n");
                sz = get_num();

                printf("What data do you want to write? Now be good and don't go out of bounds!\n");
                read(0, allocation_array[idx].buf, (unsigned int)sz);

                break;
            case 4:
                heap = malloc(0x20);
                if (strcmp(heap, "Ez W") == 0) {
                    win();
                } else {
                    printf("Hah, you missed your shot!\n");
                    exit(0);
                }

                break;
            case 5:
                printf("Goodbye, you will never find a safer program!\n\n");
                exit(0);
            default:
                printf("Invalid option!\n\n");
        }
    }
}
