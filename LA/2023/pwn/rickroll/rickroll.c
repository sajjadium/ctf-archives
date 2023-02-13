#include <stdio.h>

int main_called = 0;

int main(void) {
    if (main_called) {
        puts("nice try");
        return 1;
    }
    main_called = 1;
    setbuf(stdout, NULL);
    printf("Lyrics: ");
    char buf[256];
    fgets(buf, 256, stdin);
    printf("Never gonna give you up, never gonna let you down\nNever gonna run around and ");
    printf(buf);
    printf("Never gonna make you cry, never gonna say goodbye\nNever gonna tell a lie and hurt you\n");
    return 0;
}
