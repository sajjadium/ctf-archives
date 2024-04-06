#include <stdio.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("An internal error occured\n");
        return 1;
    }

    FILE *file = fopen("minishell.log", "a");
    if (file == NULL) {
        printf("Error opening file\n");
        return 1;
    }
    for (size_t i = 1; i < argc; i++)
    {
        fprintf(file, "%s ", argv[i]);
    
    }
    fprintf(file, "\n");

    fclose(file);
    
    

    

    return 0;
}
