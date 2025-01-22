#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    char *fn = "/home/user/permitted";
    char buffer[128];
    FILE *fp;

    if (!access(fn, W_OK))
    {
        printf("Enter text to write: ");
        scanf("%100s", buffer);
        fp = fopen(fn, "w");
        fwrite("\n", sizeof(char), 1, fp);
        fwrite(buffer, sizeof(char), strlen(buffer), fp);
        fclose(fp);
        return 0;
    }
    else
    {
        printf("Cannot write to file.\n");
        return 1;
    }
}
