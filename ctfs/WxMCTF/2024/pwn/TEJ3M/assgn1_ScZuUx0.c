#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void win(){
    system("cat flag.txt");
}

void func(){
    char buf[040];
    while(1) {
        puts("Enter your info: \n");
        gets(buf);
        if(strlen(buf) < 31) {
            puts("Thank you for valid data!!!\n");
            break;
        }
        puts("My teacher says that's unsafe!\n");
    }
}

void main() {
    setvbuf(stdin, NULL, 2, 0);
    setvbuf(stdout, NULL, 2, 0);
    func();
}
