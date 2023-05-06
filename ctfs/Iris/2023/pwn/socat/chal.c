#include <stdlib.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    if(argc < 2) return -1;
    if(setenv("FLAG", "NO!", 1) != 0) return -1;
    execvp(argv[1], argv+1);
    return 0;
}
