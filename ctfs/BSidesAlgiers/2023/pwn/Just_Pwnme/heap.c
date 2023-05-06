#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <unistd.h>

#define INDEX 1
#define SIZE 0x100

char* Allocation[2];
size_t Size[2];


void setup(){
    setbuf(stdin, 0LL);
    setbuf(stdout, 0LL);
    setbuf(stderr, 0LL);
}

void menu(){
    puts("0) Allocate a chunk\n"
         "1) Free a chunk\n"
         "2) Print a chunk\n"
         "3) Edit a chunk\n"
         "4) Exit\n"
         "[*] choice : ");
}

size_t choice(size_t max){
    char input[10];
    size_t val = 0;
    fgets(input, 10, stdin);
    val = atoll(input);
    if(val > max){
        printf("Mmh nope %ld", val);
        exit(-1);
    }
    return val;
}

int main(void){
    size_t action = 0;
    size_t index = 0;
    char input[10];
    setup();

    while(true){
        menu();
        fgets(input, 10, stdin);
        action = atoll(input);
        switch(action){
            case 0:
                printf("[*] Index : ");
                index = choice(INDEX);

                printf("[*] Size : ");
                Size[index] = choice(SIZE);
                Allocation[index] = malloc(Size[index]);

                printf("[*] Data : ");
                read(0, Allocation[index], Size[index]);
                printf("\n");
                break;

            case 1:
                printf("[*] Index : ");
                index = choice(INDEX);
                free(Allocation[index]);
                break;

            case 2:
                printf("[*] Index : ");
                index = choice(INDEX);
                printf("%s\n", Allocation[index]);
                break;

            case 3:
                printf("[*] Index : ");
                index = choice(INDEX);

                printf("[*] Data : ");
                read(0, Allocation[index], Size[index]);
                Allocation[index][strcspn(Allocation[index], "\n")] = 0;
                printf("\n");
                break;

            case 4:
                return 0;
                
            default:
                puts("Just read the menu...");
                break;
        }
    }
}
