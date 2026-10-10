#include <stdio.h>

const int M = 1000000;

int main() {
    int a = 1;
    int b = 1;
    for (int i=0; i<2<<26; i++) {
        b = (a+b) % M;
        a = (b-a+M) % M;
    }
    printf("%d\n", b);
    return 0;
}