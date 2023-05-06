#include <stdio.h>

int main(void) {
    setbuf(stdout, NULL);
    puts("What would you like to post?");
    char buf[512];
    fgets(buf, 512, stdin);
    printf("Here's your latest post:\n");
    printf(buf);
    printf("\nWhat would you like to post?\n");
    fgets(buf, 512, stdin);
    printf(buf);
    printf("\nYour free trial has expired. Bye!\n");
    return 0;
}
