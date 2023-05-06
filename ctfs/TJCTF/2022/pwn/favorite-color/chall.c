#include <stdio.h>
#include <stdlib.h>

struct Color
{
    char friendlyName[32];
    unsigned char r, g, b;
};

struct Color myFavoriteColor = {.friendlyName = "purple", .r = 0x32, .g = 0x54, .b = 0x34};

int main()
{
    unsigned char r, g, b;
    struct Color c;

    setbuf(stdout, NULL);

    puts("what's your favorite color's rgb value? (format: r, g, b)");
    scanf("%hu, %hu, %hu", &r, &g, &b);

    if (r == myFavoriteColor.r && g == myFavoriteColor.g && b == myFavoriteColor.b)
    {
        puts("no!!!");
        return 1;
    }

    puts("good... good... and its pretty name?");
    scanf("%s", &(c.friendlyName));

    c.r = r;
    c.g = g;
    c.b = b;

    printf("%s (%d, %d, %d) is a pretty cool color... but it's not as cool as %s (%d, %d, %d)...\n",
           c.friendlyName, c.r, c.g, c.b,
           myFavoriteColor.friendlyName, myFavoriteColor.r, myFavoriteColor.g, myFavoriteColor.b);

    if (c.r == myFavoriteColor.r && c.g == myFavoriteColor.g && c.b == myFavoriteColor.b)
    {
        puts("oh wait...");
        puts("it seems as if they're the same...");

        char buf[100] = {0};
        FILE *file = fopen("./flag.txt", "r");
        if (file == NULL)
        {
            puts("no flag!!! feels bad L");
            exit(1);
        }

        fgets(buf, 64, file);
        printf("here's a flag: %s", buf);
        fclose(file);
    }
}
