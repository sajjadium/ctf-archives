#include <stdio.h>
#include <string.h>

char flag[200];

int main() {
    if (!fopen("/flag.txt", "r")) {
        puts("Missing /flag.txt; please contact the admin.");
        return 0;
    }

    freopen("/flag.txt", "r", stdin);
    if (scanf("%s", flag) <= 0) {
        puts("Missing flag; please contact the admin.");
        return 0;
    }

    puts(flag);
    return 0;
}
