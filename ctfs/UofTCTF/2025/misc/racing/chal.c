#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    if (setuid(0) != 0)
    {
        perror("Error setting UID");
        return EXIT_FAILURE;
    }

    char *fn = "/home/user/permitted";
    char buffer[128];
    char f[128];
    FILE *fp;

    if (!access(fn, R_OK))
    {
        printf("Enter file to read: ");
        fgets(f, sizeof(f), stdin);
        f[strcspn(f, "\n")] = 0;

        if (strstr(f, "flag") != NULL)
        {
            printf("Can't read the 'flag' file.\n");
            return 1;
        }

        if (strlen(f) == 0)
        {
            fp = fopen(fn, "r");
        }
        else
        {
            fp = fopen(f, "r");
        }

        fread(buffer, sizeof(char), sizeof(buffer) - 1, fp);
        fclose(fp);
        printf("%s\n", buffer);
        return 0;
    }
    else
    {
        printf("Cannot read file.\n");
        return 1;
    }
}
