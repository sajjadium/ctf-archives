// gcc nullptr.c -o nullptr
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void get_me_out_of_this_mess() { execl("/bin/sh", "sh", NULL); }

int main(void) {
    unsigned long addr;
    int menuchoice;
    while (1) {
        printf("[1. view, 2. null, -1. exit]> \n"); fflush(stdout);
        scanf("%d", &menuchoice); getc(stdin);
        switch (menuchoice) {
        case 1:
            printf("view address> \n"); fflush(stdout);
            scanf("%lu", &addr); getc(stdin);
            printf("%p: %p\n", addr, *(void**)addr);
            break;
        case 2:
            printf("nuke address> \n"); fflush(stdout);
            scanf("%lu", &addr); getc(stdin);
            *(void**)addr = NULL;
            printf("ok!\n");
            break;
        case -1:
            printf("bye!\n");
            return 1;
        default:;
        }
    }
    return 0;
}
