#include <stdlib.h>
#include <stdio.h>

int main(int argc, char** argv){
    FILE *a = fopen("flag.txt", "r");
    int n;
    while ((n = fgetc(a)) != EOF) {
      putchar(n); // who cares about speed anyway
    }
}