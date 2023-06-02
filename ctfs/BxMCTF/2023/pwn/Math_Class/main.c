#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    srand(time(NULL));
    int lim = rand() % 8192;
    for (int i = 0; i < lim; i++) {
        rand();
    }
    
    printf("Ok, it's time to do some math!\n");
    for (int i = 0, a, b, c; i < 5; i++) {
        a = rand(); b = rand();
        printf("%d + %d = ?\n", a, b);
        scanf("%d", &c);
        if (a + b != c) {
            printf("Wrong answer\n");
            return 0;
        }
    }
    printf("Ok, let's switch it up. This time you give me the first number, and I give the rest!\n");
    for (int i = 0, a, b, c; i < 5; i++) {
        b = rand(); c = rand();
        printf("? + # = %d\n", c);
        scanf("%d", &a);
        printf("The equation was ? + %d = %d\n", b, c);
        if (a + b != c) {
            printf("Wrong answer\n");
            return 0;
        }
    }
    printf("Ok, you get the flag now, I guess\n");
    printf("%s\n", getenv("FLAG"));
}
