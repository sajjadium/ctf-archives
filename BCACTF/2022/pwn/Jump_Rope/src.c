#include <stdio.h>
#include <stdlib.h>

void a() {
    FILE *fptr = fopen("flag.txt", "r");
    char flag[100];
    if(fptr == NULL){
        printf("\nLooks like we've run out of jump ropes...\n");
        printf("Challenge is misconfigured. Please contact admin if you see this.\n");
    }

    fgets(flag, sizeof(flag), fptr);
    puts(flag);
}

void jumprope(){
    char arr[500];
    printf("\nBetter start jumping!\n");
    gets(arr);
    printf("Woo, that was quite the workout wasn't it!\n");
}

int main() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    printf("Here at BCA, fitness is one of our biggest priorities!\n");
    printf("Today's workout is going to be jumproping. Enjoy!\n");
    jumprope();

    return 1;
}
