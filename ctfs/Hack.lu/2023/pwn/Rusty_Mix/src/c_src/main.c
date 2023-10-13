#include "ffi.h"
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include "stdio.h"

uint32_t uh[NUM_MAPS] = { [0 ... NUM_MAPS-1 ] = NUM_MAPS };
Maps maps;

uint32_t alloc_handle(uint32_t ind) {
    for(int i = 0; i < NUM_MAPS; ++i) {
        if(uh[i] >= NUM_MAPS) {
            uh[i] = ind;
            return i;
        }
    }
    assert(0);
}

uint32_t lookup_handle(uint32_t req) {
    uint32_t res = uh[req];

    assert(req < NUM_MAPS);
    assert(res < NUM_MAPS);
    return res;
}

uint32_t create_map(enum AllocType type) {
    uint32_t user_handle;

    for(int i = 0; i < NUM_MAPS; ++i) {
        if(maps.allocs[i] == ALLOC_NONE){
            maps.allocs[i] = type;
            user_handle = alloc_handle(i);
            create(&maps, i, type);
            return user_handle;
        }
    }
    assert(0);
}

void put_value(uint32_t user_handle, uint32_t k, uint32_t v) {
    uint32_t ind = lookup_handle(user_handle);

    put(&maps, ind, k, v);
}

void get_value(uint32_t user_handle, uint32_t k) {
    uint32_t ind = lookup_handle(user_handle);

    maps.results[ind] = get(&maps, ind, k);
}

void show_value(uint32_t user_handle) {
    uint32_t ind = lookup_handle(user_handle);

    printf("Value: %u\n", maps.results[ind]);
}

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void welcome() {
    puts("Welcome to our rust-collections-in-C integration.\n");
}

#define OP_CREATE 1
#define OP_PUT    2
#define OP_FETCH  3
#define OP_SHOW   4
#define OP_EXIT   5
void menu() {
    puts("1: create");
    puts("2: put");
    puts("3: fetch");
    puts("4: show");
    puts("5: exit");
}

uint32_t get_choice(const char *msg) {
    uint32_t choice;

    printf("%s", msg);
    if(scanf("%u", &choice) != 1) {
        puts("Valid input please. :-(");
        exit(1);
    }
    getchar();

    return choice;
}

int main() {
    setup();
    init(&maps);

    welcome();
    uint32_t choice, uh, type, k, v;
    while(1) {
        menu();
        switch(get_choice("> ")) {
            case OP_CREATE:
                type = get_choice("Type (1 | 2)?\n> ");
                uh = create_map(type);
                printf("Here is your handle: %d\n", uh);
                break;
            case OP_PUT:
                uh = get_choice("For which handle?\n> ");
                k = get_choice("For which key?\n> ");
                v = get_choice("Which value?\n> ");
                put_value(uh, k, v);
                break;
            case OP_FETCH:
                uh = get_choice("For which handle?\n> ");
                k = get_choice("Which key?\n> ");
                get_value(uh, k);
                break;
            case OP_SHOW:
                uh = get_choice("For which handle?\n> ");
                show_value(uh);
                break;
            case OP_EXIT:
                puts("Bye!");
                exit(0);
                break;
            default:
                puts("Unknown option :-(");
                break;
        }
    }
}