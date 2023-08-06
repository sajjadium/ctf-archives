#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main() {
    char *c = malloc(64);
    char *d = malloc(64);
    printf("%p\n", d);
    unsigned long a = 0;
    unsigned long b = 0;
    
    free(c);
    
    scanf("%lu", &a);
    scanf("%lu", &b);
    
    *((unsigned long *)a) = b;
    
    puts("Exiting...");
    
    free(c);
    
    int fd = open("flag.txt", O_RDONLY);
    d[read(fd, d, 64)-1] = 0;
    puts(d);
    free(d);
    return 0;
}