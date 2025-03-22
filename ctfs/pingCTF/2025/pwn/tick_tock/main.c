#include<stdlib.h>
#include<stdio.h>
#include<string.h>



char flag[] = "ping{NOT_A_REAL_FLAG}";


int main(int argc, char **argv) {

    if (argc != 2) {
        printf("Usage: %s <flag>\n", argv[0]);
        return 1;
    }
    if (!strcmp(argv[1], flag)) {
        printf("Correct!\n");
        return 0;
    } else {
        printf("Incorrect!\n");
        return 1;
    }


    return 0;
    
}