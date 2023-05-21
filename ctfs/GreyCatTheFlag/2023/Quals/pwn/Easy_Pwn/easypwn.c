#include <stdio.h>
#include <stdlib.h>

void win() {
    system("cat flag.txt");
    exit(0);
}

int main() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
    char str[8];
    printf("Type your string: ");
    read(0, str, 1024);
    printf(str);
    puts("");
    return 0;
}
