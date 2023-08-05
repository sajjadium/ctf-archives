#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

unsigned int size = 0x20;

void alarm_handler() {
    exit(-1);
}

void initialize() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    signal(SIGALRM, alarm_handler);
    alarm(60);
}

int main() {
    int idx;
    char *bomb = NULL;

    initialize();
    printf("stdout: %p\n", stdout);

    printf("Oops! Ji-yong faces Bomb!!\n\n");
    bomb = malloc(0x20);

    while(1){
        printf("----------------------------\n");
        printf("1. Drop the extra Bomb\n");
        printf("2. Attempt to remove the bomb\n");
        printf("3. Print the Bomb name\n");
        printf("4. Modify the Bomb name\n");
        printf(">> ");
        scanf("%d", &idx);

        switch(idx){
            case 1:
                bomb = malloc(size);
                printf("Bomb name: ");
                read(0, bomb, size - 1);
                break;
            case 2:
                free(bomb);
                break;
            case 3:
                printf("Bomb name: %s", bomb);
                break;
            case 4:
                printf("Modify the Bomb name: ");
                read(0, bomb, size - 1);
                break;
            default:
                break;
        }
    }

    return 0;
}